"""Quick diagnostic scan of all 57 MDX articles."""
import os, re, yaml

DIR = r"D:\dev\projects\protrainerprep\src\data\post"

BANNED = [
    'journey', 'unlock your potential', 'game-changer', 'dive in',
    'landscape', 'delve', 'realm', 'furthermore', 'in conclusion',
    "it's important to note", "in today's world"
]

FILLER = [
    "in today's world", "it's important to note", "it goes without saying",
    "at the end of the day", "in conclusion", "without further ado",
    "it should be noted", "needless to say", "as we all know",
    "the fact of the matter is", "at this point in time"
]

HUBS = ['career-building-guide', 'fitness-certification-guide', 'career-change-fitness-guide']
PILLAR = 'how-to-become-personal-trainer'

stats = {
    'total': 0, 'no_canonical': 0, 'no_seoTier': 0, 'no_seoParent': 0,
    'title_over_60': 0, 'excerpt_over_155': 0, 'banned_hits': 0,
    'filler_hits': 0, 'no_affiliate_cta': 0, 'no_bottomline': 0,
    'no_disclosure': 0, 'few_links': 0, 'no_hub_backlink': 0,
    'mojibake': 0, 'missing_tags': 0
}
issues = []

for fname in sorted(os.listdir(DIR)):
    if not fname.endswith('.mdx'):
        continue
    slug = fname.replace('.mdx', '')
    stats['total'] += 1
    
    with open(os.path.join(DIR, fname), encoding='utf-8') as f:
        raw = f.read()
    
    # Extract frontmatter
    m = re.match(r'^---\s*\n(.*?)\n---', raw, re.DOTALL)
    fm = yaml.safe_load(m.group(1)) if m else {}
    body = raw.split('---', 2)[2] if raw.count('---') >= 2 else raw
    
    # Strip imports and component tags for prose analysis
    prose = re.sub(r'import\s+.*?;', '', body)
    prose = re.sub(r'<[^>]+/?>', '', prose)
    prose_lower = prose.lower()
    
    slug_issues = []
    
    # Frontmatter checks
    meta = fm.get('metadata', {})
    if not meta.get('canonical'):
        stats['no_canonical'] += 1
        slug_issues.append('no-canonical')
    if not fm.get('seoTier'):
        stats['no_seoTier'] += 1
        slug_issues.append('no-seoTier')
    if not fm.get('seoParent'):
        stats['no_seoParent'] += 1
        slug_issues.append('no-seoParent')
    if not fm.get('tags') or len(fm.get('tags', [])) < 3:
        stats['missing_tags'] += 1
        slug_issues.append(f"tags={len(fm.get('tags', []))}")
    
    title = fm.get('title', '').strip()
    excerpt = fm.get('excerpt', '').strip()
    if len(title) > 60:
        stats['title_over_60'] += 1
        slug_issues.append(f'title={len(title)}c')
    if len(excerpt) > 155:
        stats['excerpt_over_155'] += 1
        slug_issues.append(f'excerpt={len(excerpt)}c')
    
    # Banned words (in prose only, not component tags)
    for b in BANNED:
        if b == 'realm':
            # Skip if only in RealMath component name
            test = re.sub(r'RealMath', '', prose_lower)
            if b in test:
                stats['banned_hits'] += 1
                slug_issues.append(f'banned:{b}')
        elif b in prose_lower:
            stats['banned_hits'] += 1
            slug_issues.append(f'banned:{b}')
    
    # Filler
    for f_phrase in FILLER:
        if f_phrase in prose_lower:
            stats['filler_hits'] += 1
            slug_issues.append(f'filler:{f_phrase[:20]}')
    
    # Components
    if 'AffiliateCTA' not in raw:
        stats['no_affiliate_cta'] += 1
        slug_issues.append('no-AffiliateCTA')
    if 'BottomLine' not in raw:
        stats['no_bottomline'] += 1
        slug_issues.append('no-BottomLine')
    if 'AffiliateDisclosure' not in raw:
        stats['no_disclosure'] += 1
        slug_issues.append('no-Disclosure')
    
    # Internal links
    link_slugs = set(re.findall(r'\(/([^)]+?)(?:/?)(?:\))', raw))
    # Also href patterns
    link_slugs.update(re.findall(r'href="(/[^"]+)"', raw))
    if len(link_slugs) < 3:
        stats['few_links'] += 1
        slug_issues.append(f'links={len(link_slugs)}')
    
    # Hub backlink (spokes should link to their hub)
    if slug not in HUBS and slug != PILLAR:
        parent = fm.get('seoParent', '')
        if parent and parent not in raw:
            stats['no_hub_backlink'] += 1
            slug_issues.append(f'no-backlink-to:{parent}')
    
    # Mojibake detection
    mojibake_patterns = ['â€™', 'â€"', 'â€œ', 'â€\x9d', 'Ã©', 'Ã¨', 'Ã¼']
    for mp in mojibake_patterns:
        if mp in raw:
            stats['mojibake'] += 1
            slug_issues.append('mojibake')
            break
    
    if slug_issues:
        issues.append((slug, slug_issues))

print("=" * 70)
print(f"  PROTRAINERPREP DIAGNOSTIC SCAN — {stats['total']} articles")
print("=" * 70)
print()
for key, val in stats.items():
    if key != 'total' and val > 0:
        print(f"  {key:25s}: {val}")
print()
print(f"  Articles with issues: {len(issues)}/{stats['total']}")
print()
for slug, iss in issues:
    print(f"  {slug:50s} {', '.join(iss)}")
