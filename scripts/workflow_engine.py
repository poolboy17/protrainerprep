"""
Pro Trainer Prep — Executable Workflow Engine
=============================================

This is THE system. It runs the full pipeline for any article or hub page.
It validates, flags, and blocks. Nothing publishes without passing.

Usage:
  # Validate a single article
  python workflow_engine.py validate --slug ncsf-cpt-review --type spoke
  
  # Validate a hub with full spoke wiring check  
  python workflow_engine.py validate --slug how-to-become-personal-trainer --type hub
  
  # Validate ALL articles
  python workflow_engine.py validate-all
  
  # Full hub audit (hub content + all spoke backlinks + cross-linking matrix)
  python workflow_engine.py hub-audit --slug how-to-become-personal-trainer
  
  # Pre-publish check (everything must pass before git push)
  python workflow_engine.py pre-publish --slug ncsf-cpt-review
"""

import re, yaml, os, sys, json
from collections import defaultdict
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

CONTENT_DIR = None  # Set dynamically
ALL_SPOKES = []
ALL_HUBS = []
ALL_SLUGS = []

VALID_CATEGORIES = ['guides', 'reviews', 'comparisons', 'career', 'deals', 'business', 'certifications']

FILLER_PHRASES = [
    'in today\'s world', 'it\'s important to note', 'it goes without saying',
    'at the end of the day', 'in conclusion', 'without further ado',
    'it should be noted', 'needless to say', 'as we all know',
    'the fact of the matter is', 'at this point in time'
]

# ============================================================
# CORE UTILITIES
# ============================================================

def load_article(slug, content_dir):
    """Load article content from MDX file"""
    path = os.path.join(content_dir, f"{slug}.mdx")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()

def extract_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except:
            return {}
    return {}

def extract_body(content):
    parts = content.split('---', 2)
    return parts[2] if len(parts) >= 3 else content

def count_words(body):
    clean = re.sub(r'<[^>]+/?>', '', body)
    clean = re.sub(r'import\s+.*?;', '', clean)
    clean = re.sub(r'\{[^}]+\}', '', clean)
    clean = re.sub(r'[#*|`\[\]()-]', ' ', clean)
    return len(clean.split())

def extract_internal_links(content):
    md = re.findall(r'\(/blog/([^)"\'\s]+)', content)
    href = re.findall(r'href="/blog/([^"]+)"', content)
    props = re.findall(r'href:\s*"/blog/([^"]+)"', content)
    all_links = md + href + props
    return list(set([l.rstrip('/').split('#')[0].split('?')[0] for l in all_links]))

def extract_affiliate_ids(content):
    return list(set(re.findall(r'sjv\.io/c/3162789/(\d+)/12472', content)))

def extract_h2s(body):
    return re.findall(r'^## (.+)', body, re.MULTILINE)

def section_word_counts(body):
    sections = re.split(r'^## ', body, flags=re.MULTILINE)
    result = []
    for sec in sections[1:]:
        title = sec.split('\n')[0]
        clean = re.sub(r'<[^>]+/?>', '', sec)
        clean = re.sub(r'\{[^}]+\}', '', clean)
        words = len(clean.split())
        result.append((title, words))
    return result

# ============================================================
# VALIDATION CHECKS
# ============================================================

class QCResult:
    def __init__(self, slug, article_type):
        self.slug = slug
        self.article_type = article_type
        self.blocks = []
        self.warns = []
        self.info = []
        self.scores = {}
        self.metrics = {}
    
    def block(self, msg):
        self.blocks.append(msg)
    
    def warn(self, msg):
        self.warns.append(msg)
    
    @property
    def passed(self):
        return len(self.blocks) == 0
    
    @property
    def verdict(self):
        if self.blocks:
            return "❌ FAIL"
        elif self.warns:
            return "⚠️  WARN"
        return "✅ PASS"
    
    def to_dict(self):
        return {
            "slug": self.slug,
            "type": self.article_type,
            "verdict": "PASS" if self.passed else "FAIL",
            "blocks": self.blocks,
            "warns": self.warns,
            "scores": self.scores,
            "metrics": self.metrics
        }


def validate_article(slug, content, article_type, all_slugs_map):
    """
    Full Layer 5 QC validation.
    article_type: 'spoke' or 'hub'
    all_slugs_map: dict of slug -> content for cross-link checking
    """
    r = QCResult(slug, article_type)
    fm = extract_frontmatter(content)
    body = extract_body(content)
    word_count = count_words(body)
    h2s = extract_h2s(body)
    internal_links = extract_internal_links(content)
    aff_ids = extract_affiliate_ids(content)
    sections = section_word_counts(body)
    
    r.metrics = {
        "word_count": word_count,
        "h2_count": len(h2s),
        "internal_links": len(set(internal_links)),
        "affiliate_ids": aff_ids,
        "sections": sections,
    }
    
    # --- TECHNICAL ---
    
    # Frontmatter fields
    for field in ['title', 'excerpt', 'image', 'category', 'publishDate']:
        if field not in fm:
            r.block(f"Missing frontmatter: {field}")
    
    # Hub must have type: hub
    if article_type == 'hub':
        if fm.get('type') != 'hub':
            r.warn("Hub page missing type: hub in frontmatter")
    
    # Category
    cat = fm.get('category', '').lower()
    if cat and cat not in VALID_CATEGORIES:
        r.warn(f"Category '{cat}' not in taxonomy")
    
    # --- SEO ---
    
    title = fm.get('title', '').strip()
    excerpt = fm.get('excerpt', '').strip()
    
    # Title
    if len(title) > 60:
        r.block(f"Title too long: {len(title)}c (max 60)")
    elif len(title) < 30:
        r.block(f"Title too short: {len(title)}c (min 30)")
    
    # Meta description
    if len(excerpt) > 155:
        r.block(f"Meta too long: {len(excerpt)}c (max 155)")
    elif len(excerpt) < 80:
        r.block(f"Meta too short: {len(excerpt)}c (min 80)")
    
    # Word count
    min_words = 1500 if article_type == 'hub' else 800
    target_words = 2000 if article_type == 'hub' else 1200
    if word_count < min_words:
        r.block(f"Thin content: {word_count}w (min {min_words})")
    elif word_count < target_words:
        r.warn(f"Below target: {word_count}w (target {target_words}+)")
    
    # H2 count
    min_h2 = 6 if article_type == 'hub' else 3
    if len(h2s) < min_h2:
        r.block(f"Too few H2s: {len(h2s)} (min {min_h2})")
    
    # Keyword in first 50 words
    clean_body = re.sub(r'<[^>]+/?>', '', body)
    clean_body = re.sub(r'import\s+.*?;', '', clean_body)
    first_50 = ' '.join(clean_body.split()[:50]).lower()
    # Use slug words as proxy for primary keyword
    slug_words = slug.replace('-', ' ')
    key_terms = [w for w in slug.split('-') if len(w) > 3]
    kw_in_intro = any(t in first_50 for t in key_terms)
    if not kw_in_intro:
        r.warn(f"Key terms not in first 50 words: {key_terms}")
    
    # --- INTERNAL LINKS ---
    
    unique_links = list(set(internal_links))
    min_links = 10 if article_type == 'hub' else 3
    if len(unique_links) < min_links:
        r.block(f"Too few internal links: {len(unique_links)} (min {min_links})")
    
    # Hub-specific: must link to ALL spokes
    if article_type == 'hub':
        spoke_slugs = [s for s in all_slugs_map.keys() if s != slug and extract_frontmatter(all_slugs_map[s]).get('type') != 'hub']
        missing_outbound = [s for s in spoke_slugs if s not in unique_links]
        if missing_outbound:
            r.block(f"Hub missing links to {len(missing_outbound)} spokes: {', '.join(missing_outbound)}")
        
        # Check all spokes link BACK to this hub
        missing_backlinks = []
        for spoke_slug in spoke_slugs:
            spoke_links = extract_internal_links(all_slugs_map[spoke_slug])
            if slug not in spoke_links:
                missing_backlinks.append(spoke_slug)
        if missing_backlinks:
            r.block(f"{len(missing_backlinks)} spokes missing backlink to hub: {', '.join(missing_backlinks)}")
    
    # Spoke: must link to at least one hub
    if article_type == 'spoke':
        hub_slugs = [s for s in all_slugs_map.keys() if extract_frontmatter(all_slugs_map[s]).get('type') == 'hub']
        has_hub_link = any(h in unique_links for h in hub_slugs)
        if not has_hub_link:
            r.block("Spoke has no link to any hub page")
    
    # --- AFFILIATE/COMPLIANCE ---
    
    has_disclosure = 'AffiliateDisclosure' in content or 'affiliate' in body.lower()[:500]
    if not has_disclosure:
        r.block("No affiliate disclosure")
    
    has_cta = 'AffiliateCTA' in content
    if not has_cta:
        r.warn("No AffiliateCTA component")
    
    if not aff_ids:
        r.warn("No tracked affiliate links")
    
    if '933875' in content:
        r.block("Old generic AdID 933875 still present")
    
    # --- CONTENT QUALITY ---
    
    # Data density
    data_points = re.findall(r'\$[\d,]+|\d+%|\d{2,}', body)
    min_data = 15 if article_type == 'hub' else 5
    if len(data_points) < min_data:
        r.warn(f"Low data density: {len(data_points)} points (min {min_data})")
    
    # Filler phrases
    for filler in FILLER_PHRASES:
        if filler in body.lower():
            r.warn(f"Filler phrase: '{filler}'")
    
    # Components
    components_used = set()
    for comp in ['StatHighlight', 'RealMath', 'AffiliateCTA', 'BottomLine', 
                  'KeyTakeaway', 'ProTip', 'ActionSteps', 'Checklist', 'SpokeCards',
                  'ChooseIf', 'QuickAnswer']:
        if comp in content:
            components_used.add(comp)
    
    if article_type == 'hub':
        if 'StatHighlight' not in components_used:
            r.warn("Hub missing StatHighlight component")
        if 'BottomLine' not in components_used:
            r.warn("Hub missing BottomLine component")
        if len(components_used) < 4:
            r.warn(f"Low component diversity: {len(components_used)} types (hub target: 4+)")
    
    # --- SCORING ---
    
    r.scores['intent'] = 5 if word_count > 2000 else 4 if word_count > 1500 else 3 if word_count > 1000 else 2
    r.scores['data'] = 5 if len(data_points) > 20 else 4 if len(data_points) > 10 else 3 if len(data_points) > 5 else 2
    r.scores['conversion'] = 5 if has_cta and len(aff_ids) > 1 else 4 if has_cta else 3
    r.scores['linking'] = 5 if len(unique_links) > 8 else 4 if len(unique_links) > 5 else 3 if len(unique_links) > 2 else 2
    r.scores['readability'] = 4 if len(h2s) > 5 else 3
    r.scores['avg'] = round(sum(v for k,v in r.scores.items() if k != 'avg') / 5, 1)
    
    threshold = 4.0 if article_type == 'hub' else 3.5
    if r.scores['avg'] < threshold:
        r.warn(f"Quality score {r.scores['avg']} below {article_type} threshold ({threshold})")
    
    return r


# ============================================================
# REPORT FORMATTING
# ============================================================

def print_result(r):
    print(f"\n{'─' * 70}")
    print(f"  {r.verdict}  {r.slug} ({r.article_type})")
    print(f"  Words: {r.metrics['word_count']} | H2s: {r.metrics['h2_count']} | Links: {r.metrics['internal_links']} | Score: {r.scores.get('avg', '?')}/5.0")
    
    if r.blocks:
        for b in r.blocks:
            print(f"    🔴 BLOCK: {b}")
    if r.warns:
        for w in r.warns:
            print(f"    🟡 WARN:  {w}")
    if not r.blocks and not r.warns:
        print(f"    ✅ Clean — zero issues")


def print_summary(results):
    total = len(results)
    passes = sum(1 for r in results if r.passed)
    fails = total - passes
    total_blocks = sum(len(r.blocks) for r in results)
    total_warns = sum(len(r.warns) for r in results)
    avg_score = round(sum(r.scores.get('avg', 0) for r in results) / max(total, 1), 1)
    
    print(f"\n{'=' * 70}")
    print(f"  SUMMARY — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Articles: {total} | PASS: {passes} | FAIL: {fails}")
    print(f"  BLOCKs: {total_blocks} | WARNs: {total_warns}")
    print(f"  Avg Score: {avg_score}/5.0")
    
    if fails > 0:
        print(f"\n  ❌ PUBLISH BLOCKED — {fails} article(s) have unresolved BLOCKs")
    else:
        print(f"\n  ✅ ALL CLEAR — safe to publish")
    print(f"{'=' * 70}")


# ============================================================
# WORKFLOW COMMANDS
# ============================================================

def load_all_articles(content_dir):
    """Load all MDX articles from a directory"""
    articles = {}
    for fname in os.listdir(content_dir):
        if fname.endswith('.mdx'):
            slug = fname.replace('.mdx', '')
            with open(os.path.join(content_dir, fname)) as f:
                articles[slug] = f.read()
    return articles


def cmd_validate(slug, article_type, content_dir):
    """Validate a single article"""
    articles = load_all_articles(content_dir)
    if slug not in articles:
        print(f"❌ Article not found: {slug}")
        return None
    
    r = validate_article(slug, articles[slug], article_type, articles)
    print_result(r)
    return r


def cmd_validate_all(content_dir):
    """Validate all articles"""
    articles = load_all_articles(content_dir)
    
    print("=" * 70)
    print(f"  PRO TRAINER PREP — FULL SITE QC VALIDATION")
    print(f"  {len(articles)} articles × {20}+ checks")
    print("=" * 70)
    
    results = []
    for slug, content in sorted(articles.items()):
        fm = extract_frontmatter(content)
        atype = 'hub' if fm.get('type') == 'hub' else 'spoke'
        r = validate_article(slug, content, atype, articles)
        print_result(r)
        results.append(r)
    
    print_summary(results)
    return results


def cmd_hub_audit(hub_slug, content_dir):
    """Full hub audit: content + spoke wiring + cross-linking matrix"""
    articles = load_all_articles(content_dir)
    
    if hub_slug not in articles:
        print(f"❌ Hub not found: {hub_slug}")
        return
    
    print("=" * 70)
    print(f"  HUB AUDIT: {hub_slug}")
    print("=" * 70)
    
    # 1. Validate hub content
    r = validate_article(hub_slug, articles[hub_slug], 'hub', articles)
    print_result(r)
    
    # 2. Spoke wiring
    hub_links = set(extract_internal_links(articles[hub_slug]))
    spoke_slugs = [s for s in articles if s != hub_slug and extract_frontmatter(articles[s]).get('type') != 'hub']
    
    print(f"\n{'─' * 70}")
    print(f"  SPOKE WIRING")
    print(f"{'─' * 70}")
    
    for spoke in sorted(spoke_slugs):
        spoke_links = set(extract_internal_links(articles[spoke]))
        out = "✅" if spoke in hub_links else "❌"
        back = "✅" if hub_slug in spoke_links else "❌"
        bidir = "✅" if (spoke in hub_links and hub_slug in spoke_links) else "❌"
        print(f"  {bidir} {spoke:45s} hub→spoke:{out}  spoke→hub:{back}")
    
    # 3. Cross-spoke matrix
    print(f"\n{'─' * 70}")
    print(f"  SPOKE CROSS-LINKS")
    print(f"{'─' * 70}")
    
    for spoke in sorted(spoke_slugs):
        spoke_links = set(extract_internal_links(articles[spoke]))
        siblings = [s for s in spoke_slugs if s != spoke and s in spoke_links]
        hubs = [s for s in articles if extract_frontmatter(articles[s]).get('type') == 'hub' and s in spoke_links]
        ok = "✅" if len(siblings) >= 2 and len(hubs) >= 1 else "⚠️"
        print(f"  {ok} {spoke:45s} {len(siblings)} siblings, {len(hubs)} hubs")
    
    return r


def cmd_pre_publish(slug, content_dir):
    """Pre-publish gate — everything must pass"""
    articles = load_all_articles(content_dir)
    fm = extract_frontmatter(articles[slug])
    atype = 'hub' if fm.get('type') == 'hub' else 'spoke'
    
    print("=" * 70)
    print(f"  PRE-PUBLISH CHECK: {slug}")
    print("=" * 70)
    
    r = validate_article(slug, articles[slug], atype, articles)
    print_result(r)
    
    if r.passed:
        print(f"\n  ✅ CLEAR TO PUBLISH")
    else:
        print(f"\n  ❌ PUBLISH BLOCKED — {len(r.blocks)} BLOCK(s) must be resolved")
        print(f"     Run Editor layer, then re-validate.")
    
    return r


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Pro Trainer Prep QC Workflow Engine")
    parser.add_argument('command', choices=['validate', 'validate-all', 'hub-audit', 'pre-publish'])
    parser.add_argument('--slug', help='Article slug')
    parser.add_argument('--type', choices=['spoke', 'hub'], default='spoke')
    parser.add_argument('--dir', default='.', help='Content directory with .mdx files')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        if not args.slug:
            print("--slug required for validate")
            sys.exit(1)
        r = cmd_validate(args.slug, args.type, args.dir)
        sys.exit(0 if r and r.passed else 1)
    
    elif args.command == 'validate-all':
        results = cmd_validate_all(args.dir)
        sys.exit(0 if all(r.passed for r in results) else 1)
    
    elif args.command == 'hub-audit':
        if not args.slug:
            print("--slug required for hub-audit")
            sys.exit(1)
        cmd_hub_audit(args.slug, args.dir)
    
    elif args.command == 'pre-publish':
        if not args.slug:
            print("--slug required for pre-publish")
            sys.exit(1)
        r = cmd_pre_publish(args.slug, args.dir)
        sys.exit(0 if r and r.passed else 1)

