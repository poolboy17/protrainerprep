"""
ProTrainer Pipe — Multi-threaded SEO Optimizer for ProTrainerPrep
=================================================================
Reads all MDX articles, validates against SEO-QC-GATES, auto-fixes
what it can, and writes back. Multi-threaded for speed.

Usage:
  python protrainer-pipe.py                 # optimize all
  python protrainer-pipe.py --slug NAME     # optimize one article
  python protrainer-pipe.py --dry-run       # show changes without writing
  python protrainer-pipe.py --diff          # show before/after diffs
  python protrainer-pipe.py --validate-only # just run validation, no writes
"""

import os, re, sys, json, yaml, copy, argparse, io
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Force UTF-8 on Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, 'src', 'data', 'post')
SPEC_VERSION = '1.0.0'

SITE_URL = 'https://protrainerprep.com'

VALID_CATEGORIES = ['guides', 'certifications', 'career-change',
                    'career-building', 'career-growth', 'ceu']

# Category → URL prefix mapping
CATEGORY_ROUTES = {
    'guides': 'guides',
    'certifications': 'certifications',
    'career-change': 'career-change',
    'career-building': 'career-building',
    'career-growth': 'career-growth',
    'ceu': 'ceu',
}

HUBS = {
    'career-building-guide': 'career-building',
    'fitness-certification-guide': 'certifications',
    'career-change-fitness-guide': 'career-change',
}
PILLAR = 'how-to-become-personal-trainer'

BANNED_WORDS = [
    'journey', 'unlock your potential', 'game-changer', 'dive in',
    'landscape', 'delve', 'realm', 'furthermore', 'in conclusion',
    "it's important to note", "in today's world",
]

FILLER_PHRASES = [
    "in today's world", "it's important to note", "it goes without saying",
    "at the end of the day", "in conclusion", "without further ado",
    "it should be noted", "needless to say", "as we all know",
    "the fact of the matter is", "at this point in time",
]

# Replacement map for banned words (context-aware)
BANNED_REPLACEMENTS = {
    'journey': 'path',
    'unlock your potential': 'build your skills',
    'game-changer': 'significant advantage',
    'dive in': 'get started',
    'landscape': 'market',
    'delve': 'look',
    'realm': 'area',
    'furthermore': '',  # just remove
    'in conclusion': '',
    "it's important to note": '',
    "in today's world": '',
}

# Thread-safe print lock
print_lock = Lock()

# ============================================================
# UTILITIES
# ============================================================

def safe_print(*args, **kwargs):
    with print_lock:
        try:
            print(*args, **kwargs)
        except UnicodeEncodeError:
            # Fallback for Windows console encoding
            text = ' '.join(str(a) for a in args)
            print(text.encode('ascii', 'replace').decode('ascii'), **kwargs)

def load_mdx(slug):
    """Load an MDX file and return (fm_dict, fm_raw, body, raw)."""
    path = os.path.join(CONTENT_DIR, f"{slug}.mdx")
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    m = re.match(r'^---\s*\n(.*?)\n---', raw, re.DOTALL)
    if not m:
        return {}, '', raw, raw
    fm_dict = yaml.safe_load(m.group(1)) or {}
    fm_raw = m.group(1)
    body = raw[m.end():]
    return fm_dict, fm_raw, body, raw

def save_mdx(slug, fm_raw, body):
    """Write raw frontmatter string + body back to MDX file (no YAML re-dump)."""
    path = os.path.join(CONTENT_DIR, f"{slug}.mdx")
    out = f"---\n{fm_raw}\n---{body}"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out)

def extract_prose(body):
    """Strip import lines and component tags to get prose only."""
    text = re.sub(r'import\s+[^\n]+\n', '', body)
    text = re.sub(r'<[^>]+/?>', '', text)
    return text

def count_words(body):
    """Count words in article body (prose + component text)."""
    clean = re.sub(r'import\s+[^\n]+', '', body)
    clean = re.sub(r'<[^>]+/?>', '', clean)
    clean = re.sub(r'\{[^}]+\}', '', clean)
    clean = re.sub(r'[#*|`\[\]()-]', ' ', clean)
    return len(clean.split())

def extract_internal_links(content):
    """Extract internal link targets from markdown and HTML link patterns."""
    patterns = [
        r'\]\(/([^)"\'\s]+)',       # [text](/path)
        r'href="/([^"]+)"',         # href="/path"
        r"href='/([^']+)'",         # href='/path'
    ]
    links = []
    for p in patterns:
        links.extend(re.findall(p, content))
    slugs = set()
    for link in links:
        link = link.rstrip('/').split('#')[0].split('?')[0]
        parts = link.split('/')
        if len(parts) >= 2:
            slug = parts[-1]
            if slug and not slug.startswith('.') and not any(
                slug.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.svg', '.xml']
            ):
                slugs.add(slug)
    return slugs

def get_article_type(fm, slug):
    """Determine article type from frontmatter or slug."""
    if slug == PILLAR:
        return 'pillar'
    if fm.get('type') == 'hub' or slug in HUBS:
        return 'hub'
    return 'spoke'

def build_canonical(slug, category):
    """Build canonical URL from slug and category."""
    cat_prefix = CATEGORY_ROUTES.get(category, category)
    return f"{SITE_URL}/{cat_prefix}/{slug}"

# ============================================================
# OPTIMIZATION PASSES
# ============================================================

def fix_frontmatter(fm, fm_raw, slug, changes):
    """Fix frontmatter issues via surgical text edits on fm_raw string."""
    category = fm.get('category', '')
    atype = get_article_type(fm, slug)

    # Ensure metadata.canonical exists
    meta = fm.get('metadata', {})
    if not meta.get('canonical'):
        canonical = build_canonical(slug, category)
        if 'metadata:' in fm_raw:
            # Append canonical under existing metadata block
            fm_raw = fm_raw.replace('metadata:', f'metadata:\n  canonical: {canonical}', 1)
        else:
            # Add metadata block at end of frontmatter
            fm_raw = fm_raw.rstrip() + f'\nmetadata:\n  canonical: {canonical}'
        changes.append(f'+ canonical: {canonical}')

    # Ensure seoTier
    if not fm.get('seoTier'):
        fm_raw = fm_raw.rstrip() + f'\nseoTier: "{atype}"'
        changes.append(f'+ seoTier: {atype}')

    # Ensure seoParent (spokes → their hub, hubs → pillar)
    if not fm.get('seoParent') and slug != PILLAR:
        if atype == 'hub':
            fm_raw = fm_raw.rstrip() + f'\nseoParent: "{PILLAR}"'
            changes.append(f'+ seoParent: {PILLAR}')
        elif atype == 'spoke':
            for hub_slug, hub_cat in HUBS.items():
                if hub_cat == category:
                    fm_raw = fm_raw.rstrip() + f'\nseoParent: "{hub_slug}"'
                    changes.append(f'+ seoParent: {hub_slug}')
                    break

    # Ensure seoHub
    if not fm.get('seoHub') and category:
        fm_raw = fm_raw.rstrip() + f'\nseoHub: "{category}"'
        changes.append(f'+ seoHub: {category}')

    return fm_raw


def fix_title(fm, fm_raw, slug, changes):
    """Truncate title to 60 chars if over limit via raw text surgery."""
    title = fm.get('title', '').strip()
    if len(title) > 60:
        truncated = title[:57]
        last_space = truncated.rfind(' ')
        if last_space > 40:
            truncated = truncated[:last_space]
        new_title = truncated.rstrip() + '...'
        # Replace in raw frontmatter — handle both > block and inline styles
        # Try block scalar first: "title: >\n  actual title"
        block_pattern = r'(title:\s*>\s*\n\s*)' + re.escape(title)
        if re.search(block_pattern, fm_raw):
            fm_raw = re.sub(block_pattern, r'\g<1>' + new_title, fm_raw, count=1)
        else:
            # Inline: "title: Some Title" or "title: 'Some Title'"
            fm_raw = fm_raw.replace(title, new_title, 1)
        changes.append(f'~ title: {len(title)}c -> {len(new_title)}c')
    return fm_raw

def fix_banned_words(body, changes):
    """Remove/replace banned words from prose (not imports or component tags)."""
    # Split body into segments: imports, component blocks, and prose
    lines = body.split('\n')
    fixed_lines = []
    fixes = 0

    for line in lines:
        # Skip import lines and component tags
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('<') or stripped.startswith('{'):
            fixed_lines.append(line)
            continue

        modified = line
        line_lower = modified.lower()

        for banned in BANNED_WORDS:
            if banned == 'realm':
                # Don't match 'RealMath' — only standalone 'realm'
                if re.search(r'\brealm\b', line_lower) and 'RealMath' not in modified:
                    replacement = BANNED_REPLACEMENTS.get(banned, '')
                    modified = re.sub(r'\brealm\b', replacement, modified, flags=re.IGNORECASE)
                    fixes += 1
            elif banned in line_lower:
                replacement = BANNED_REPLACEMENTS.get(banned, '')
                # Case-insensitive replace
                pattern = re.escape(banned)
                modified = re.sub(pattern, replacement, modified, flags=re.IGNORECASE)
                fixes += 1

        # Clean up double spaces from removals
        modified = re.sub(r'  +', ' ', modified)
        # Clean up orphaned sentence starts
        modified = re.sub(r'^\s*,\s*', '', modified)
        fixed_lines.append(modified)

    if fixes:
        changes.append(f'~ removed {fixes} banned word(s)')
    return '\n'.join(fixed_lines)

def fix_affiliate_disclosure(body, changes):
    """Add AffiliateDisclosure import + component if missing."""
    if 'AffiliateDisclosure' in body:
        return body

    lines = body.split('\n')
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('import '):
            last_import_idx = i

    if last_import_idx == -1:
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.strip() == '':
                last_import_idx = i
                break

    # Add import after last import line
    import_line = "import AffiliateDisclosure from '~/components/blog/AffiliateDisclosure.astro';"
    lines.insert(last_import_idx + 1, import_line)

    # Find first real prose paragraph — must skip:
    # - empty lines
    # - import lines
    # - component blocks (everything between < and />  or < and >...</tag>)
    # Key: track whether we're inside a multi-line component tag
    in_component = False
    disclosure_inserted = False
    for i in range(last_import_idx + 2, len(lines)):
        stripped = lines[i].strip()

        # Track multi-line component tags
        if in_component:
            if stripped.endswith('/>') or stripped.endswith('>'):
                in_component = False
            continue

        # Skip empty lines and imports
        if not stripped or stripped.startswith('import '):
            continue

        # Self-closing component on one line: <Foo ... />
        if stripped.startswith('<') and stripped.endswith('/>'):
            continue

        # Opening of multi-line component: <Foo  (no closing > on same line)
        if stripped.startswith('<') and not stripped.endswith('>'):
            in_component = True
            continue

        # Single-line component with closing: <Foo ...> or </Foo>
        if stripped.startswith('<'):
            continue

        # Component prop lines (start with lowercase or special chars like {)
        # These are continuation lines of a multi-line JSX component
        if stripped.startswith('{') or (stripped and stripped[0].islower()
                and '=' in stripped and not stripped.startswith('#')):
            continue

        # Found first real prose line — insert before it
        lines.insert(i, '<AffiliateDisclosure />')
        lines.insert(i, '')
        disclosure_inserted = True
        break

    if not disclosure_inserted:
        lines.insert(last_import_idx + 2, '')
        lines.insert(last_import_idx + 3, '<AffiliateDisclosure />')

    changes.append('+ AffiliateDisclosure component')
    return '\n'.join(lines)

def fix_heading_whitespace(body, changes):
    """Normalize ' ## Heading' to '## Heading' (strip leading whitespace on headings)."""
    fixed, count = re.subn(r'^[ \t]+(#{1,6} )', r'\1', body, flags=re.MULTILINE)
    if count:
        changes.append(f'~ fixed {count} heading(s) with leading whitespace')
    return fixed


def fix_filler_phrases(body, changes):
    """Remove filler phrases from prose."""
    lines = body.split('\n')
    fixed_lines = []
    fixes = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('<') or stripped.startswith('{'):
            fixed_lines.append(line)
            continue

        modified = line
        for filler in FILLER_PHRASES:
            if filler in modified.lower():
                pattern = re.escape(filler)
                # Remove filler, handling ", filler," and "filler, " patterns
                modified = re.sub(r',?\s*' + pattern + r'\s*,?\s*', ' ',
                                  modified, flags=re.IGNORECASE)
                fixes += 1

        modified = re.sub(r'  +', ' ', modified)
        fixed_lines.append(modified)

    if fixes:
        changes.append(f'~ removed {fixes} filler phrase(s)')
    return '\n'.join(fixed_lines)


# ============================================================
# VALIDATION (read-only checks)
# ============================================================

def validate_article(slug, fm, body, all_slugs):
    """Run validation checks, return (blocks, warns)."""
    blocks = []
    warns = []
    atype = get_article_type(fm, slug)
    word_count = count_words(body)
    h2s = re.findall(r'^## (.+)', body, re.MULTILINE)
    internal_links = extract_internal_links(body)

    # Title length
    title = fm.get('title', '').strip()
    if len(title) > 60:
        blocks.append(f'Title too long: {len(title)}c (max 60)')
    elif len(title) < 30:
        blocks.append(f'Title too short: {len(title)}c (min 30)')

    # Excerpt length
    excerpt = fm.get('excerpt', '').strip()
    if len(excerpt) > 155:
        blocks.append(f'Excerpt too long: {len(excerpt)}c (max 155)')

    # Word count
    min_words = {'pillar': 2000, 'hub': 1500, 'spoke': 700}
    if word_count < min_words.get(atype, 700):
        blocks.append(f'Thin content: {word_count}w (min {min_words.get(atype, 700)})')

    # H2 count (allow leading whitespace — some MDX has " ## ")
    h2s = re.findall(r'^\s*## (.+)', body, re.MULTILINE)
    min_h2 = {'pillar': 8, 'hub': 6, 'spoke': 3}
    if len(h2s) < min_h2.get(atype, 3):
        blocks.append(f'Too few H2s: {len(h2s)} (min {min_h2.get(atype, 3)})')

    # Required fields
    for field in ['title', 'excerpt', 'image', 'category', 'publishDate']:
        if field not in fm:
            blocks.append(f'Missing frontmatter: {field}')

    # Category valid
    cat = fm.get('category', '').lower()
    if cat and cat not in VALID_CATEGORIES:
        warns.append(f"Category '{cat}' not in taxonomy")

    # Internal links
    min_links = {'pillar': 10, 'hub': 10, 'spoke': 3}
    if len(internal_links) < min_links.get(atype, 3):
        warns.append(f'Few internal links: {len(internal_links)} (target {min_links.get(atype, 3)}+)')

    # Affiliate disclosure
    if 'AffiliateDisclosure' not in body:
        blocks.append('Missing AffiliateDisclosure')

    # BottomLine component
    if 'BottomLine' not in body:
        warns.append('Missing BottomLine component')

    # AffiliateCTA
    if 'AffiliateCTA' not in body:
        warns.append('Missing AffiliateCTA component')

    # Banned words
    prose = extract_prose(body)
    prose_lower = prose.lower()
    for banned in BANNED_WORDS:
        if banned == 'realm':
            if re.search(r'\brealm\b', prose_lower):
                warns.append(f"Banned word: '{banned}'")
        elif banned in prose_lower:
            warns.append(f"Banned word: '{banned}'")

    # Hub backlink (spokes should link to parent)
    if atype == 'spoke':
        parent = fm.get('seoParent', '')
        if parent and parent not in body:
            warns.append(f'No backlink to parent hub: {parent}')

    return blocks, warns

# ============================================================
# CORE: OPTIMIZE ONE ARTICLE
# ============================================================

def optimize_article(slug, dry_run=False, show_diff=False):
    """
    Load, optimize, validate, and save one article.
    Returns dict with slug, changes, blocks, warns, word_count.
    """
    fm, fm_raw, body, raw = load_mdx(slug)
    changes = []

    if show_diff:
        snapshot_fm_raw = fm_raw
        snapshot_body = body

    # === FIX PASSES (fm_raw = surgical text edits, body = content fixes) ===
    fm_raw = fix_frontmatter(fm, fm_raw, slug, changes)
    fm_raw = fix_title(fm, fm_raw, slug, changes)
    body = fix_banned_words(body, changes)
    body = fix_filler_phrases(body, changes)
    body = fix_affiliate_disclosure(body, changes)
    body = fix_heading_whitespace(body, changes)

    # Re-parse frontmatter for validation
    fm_updated = yaml.safe_load(fm_raw) or {}

    # === VALIDATE ===
    all_slugs = set()
    blocks, warns = validate_article(slug, fm_updated, body, all_slugs)

    # === SAVE (raw frontmatter preserved — no yaml.dump) ===
    if changes and not dry_run:
        save_mdx(slug, fm_raw, body)

    # === DIFF ===
    diff_lines = []
    if show_diff and changes:
        old_lines = set(snapshot_fm_raw.splitlines())
        new_lines = set(fm_raw.splitlines())
        for line in sorted(new_lines - old_lines):
            diff_lines.append(f"  + {line.strip()}")

    return {
        'slug': slug,
        'type': get_article_type(fm_updated, slug),
        'changes': changes,
        'blocks': blocks,
        'warns': warns,
        'word_count': count_words(body),
        'diff': diff_lines,
    }


# ============================================================
# PIPELINE: MULTI-THREADED RUNNER
# ============================================================

def run_pipeline(slugs=None, dry_run=False, show_diff=False,
                 validate_only=False, max_workers=8):
    """Run optimizer across all articles with thread pool."""
    # Discover all articles
    all_files = sorted(f.replace('.mdx', '')
                       for f in os.listdir(CONTENT_DIR)
                       if f.endswith('.mdx'))

    if slugs:
        targets = [s for s in all_files if s in slugs]
    else:
        targets = all_files

    total = len(targets)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    print('=' * 70)
    print(f'  PROTRAINER PIPE v{SPEC_VERSION} — {now}')
    print(f'  Articles: {total} | Workers: {max_workers}')
    print(f'  Mode: {"VALIDATE-ONLY" if validate_only else "DRY-RUN" if dry_run else "OPTIMIZE"}')
    print('=' * 70)

    results = []

    if validate_only:
        # Validate-only: still multi-threaded but no writes
        def validate_one(slug):
            fm, fm_raw, body, raw = load_mdx(slug)
            blocks, warns = validate_article(slug, fm, body, set(all_files))
            return {
                'slug': slug,
                'type': get_article_type(fm, slug),
                'changes': [],
                'blocks': blocks,
                'warns': warns,
                'word_count': count_words(body),
                'diff': [],
            }

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(validate_one, s): s for s in targets}
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                icon = '🔴' if r['blocks'] else '🟡' if r['warns'] else '✅'
                safe_print(f"  {icon} {r['slug']:50s} B={len(r['blocks'])} W={len(r['warns'])}")
    else:
        # Optimize: multi-threaded
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(optimize_article, s, dry_run, show_diff): s
                       for s in targets}
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                icon = '🔴' if r['blocks'] else '✏️' if r['changes'] else '✅'
                safe_print(f"  {icon} {r['slug']:50s} "
                           f"Δ={len(r['changes'])} B={len(r['blocks'])} W={len(r['warns'])}")
                if show_diff and r['diff']:
                    for d in r['diff']:
                        safe_print(f"      {d}")

    # === SUMMARY ===
    results.sort(key=lambda r: r['slug'])
    total_changes = sum(len(r['changes']) for r in results)
    total_blocks = sum(len(r['blocks']) for r in results)
    total_warns = sum(len(r['warns']) for r in results)
    passed = sum(1 for r in results if not r['blocks'])
    failed = total - passed
    changed = sum(1 for r in results if r['changes'])

    print()
    print('=' * 70)
    print(f'  SUMMARY')
    print(f'  Articles: {total} | PASS: {passed} | FAIL: {failed}')
    print(f'  Changes: {total_changes} across {changed} articles')
    print(f'  BLOCKs: {total_blocks} | WARNs: {total_warns}')

    if failed:
        print()
        print(f'  ❌ {failed} article(s) have unresolved BLOCKs:')
        for r in results:
            if r['blocks']:
                for b in r['blocks']:
                    print(f'     {r["slug"]}: {b}')
    else:
        print(f'  ✅ ALL CLEAR — zero BLOCKs')

    if dry_run:
        print()
        print(f'  ℹ️  DRY RUN — no files were modified')
        print(f'     Re-run without --dry-run to apply changes')

    print('=' * 70)

    # === AUDIT LOG ===
    log_path = os.path.join(BASE_DIR, 'protrainer-audit.jsonl')
    with open(log_path, 'a', encoding='utf-8') as f:
        for r in results:
            entry = {
                'timestamp': now,
                'slug': r['slug'],
                'type': r['type'],
                'changes': r['changes'],
                'block_count': len(r['blocks']),
                'warn_count': len(r['warns']),
                'word_count': r['word_count'],
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    return results

# ============================================================
# CLI
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='ProTrainer Pipe — Multi-threaded SEO Optimizer')
    parser.add_argument('--slug', nargs='*',
                        help='Optimize specific article(s) by slug')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show changes without writing files')
    parser.add_argument('--diff', action='store_true',
                        help='Show before/after diffs')
    parser.add_argument('--validate-only', action='store_true',
                        help='Run validation only, no optimization')
    parser.add_argument('--workers', type=int, default=8,
                        help='Number of threads (default: 8)')

    args = parser.parse_args()

    results = run_pipeline(
        slugs=args.slug,
        dry_run=args.dry_run,
        show_diff=args.diff,
        validate_only=args.validate_only,
        max_workers=args.workers,
    )

    # Exit code: 1 if any BLOCKs remain
    has_blocks = any(r['blocks'] for r in results)
    sys.exit(1 if has_blocks else 0)
