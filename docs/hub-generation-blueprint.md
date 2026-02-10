# Pro Trainer Prep — Hub Generation Blueprint

## Overview

Hub pages are the most important pages on the site. They sit at the top of the SEO architecture, carry the most link equity, target the highest-volume keywords, and every spoke's ranking performance depends on the hub being rock solid. They require their own layered generation system because their QC gates, content requirements, and structural obligations are fundamentally different from spoke articles.

This blueprint runs parallel to the Article Generation Blueprint (which governs spokes) and should be executed **before** any spokes in a new cluster are written — the hub defines the spoke map.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  LAYER 0 — CLUSTER PLANNING                                      │
│  Define the topic cluster, spoke map, and hub positioning         │
│  Output: cluster_plan.yaml                                        │
├─────────────────────── QC GATE 0 ────────────────────────────────┤
│  LAYER 1 — HUB STRATEGY                                          │
│  SERP analysis, keyword targeting, competitive gap, hub type      │
│  Output: hub_strategy_brief.yaml                                  │
├─────────────────────── QC GATE 1 ────────────────────────────────┤
│  LAYER 2 — STRUCTURAL SCAFFOLD                                    │
│  Complete outline, spoke link map, component plan, schema plan    │
│  Output: hub_outline.md                                           │
├─────────────────────── QC GATE 2 ────────────────────────────────┤
│  LAYER 3 — CONTENT HYDRATION                                      │
│  Prose, data tables, comparison matrices, spoke integration       │
│  Output: hub_draft.mdx                                            │
├─────────────────────── QC GATE 3 ────────────────────────────────┤
│  LAYER 4 — POLISH & CONVERSION                                    │
│  Scannability, CTA placement, featured snippet formatting         │
│  Output: hub_polished.mdx                                         │
├─────────────────────── QC GATE 4 ────────────────────────────────┤
│  LAYER 5 — QC VALIDATE                                            │
│  Full technical, SEO, linking, and compliance audit                │
│  Output: hub_qc_report.md (READ-ONLY — flags issues, fixes none) │
├─────────────────────── QC GATE 5 ────────────────────────────────┤
│  LAYER 6 — EDITOR                                                 │
│  Fix all BLOCKs flagged by QC, address WARNs                     │
│  Output: hub_final.mdx                                            │
├──────────────── RE-VALIDATE (back to Layer 5) ───────────────────┤
│  LAYER 7 — PUBLISH & WIRE                                         │
│  Deploy, verify live rendering, connect spokes, ping sitemap      │
│  Output: live URL + deployment verification                       │
└──────────────────────────────────────────────────────────────────┘
```

### QC Gate Severity Key

| Tag       | Meaning                                                     |
|-----------|-------------------------------------------------------------|
| `[BLOCK]` | Hard stop. Hub cannot proceed until resolved.               |
| `[WARN]`  | Flagged for review. Document the deviation and proceed.     |
| `[AUTO]`  | Validated by script. No human judgment required.             |

### Failure Path Rules

1. **Fail-forward** (cosmetic, additive): Fix in place, re-run gate.
2. **Fail-back** (structural): Return to specified earlier layer.
3. **Maximum rework**: 2 attempts per gate.

---

## Layer 0 — Cluster Planning

**Purpose:** Define the entire topic cluster before writing anything. The hub doesn't exist in isolation — it's the center of a spoke wheel, and the spoke map must be complete before the hub is written.

### 0.1 — Topic Cluster Definition

| Field | Description | Example |
|-------|-------------|---------|
| Cluster name | Human-readable cluster label | "NCSF Certification" |
| Hub keyword | Primary keyword the hub targets | "how to become a personal trainer" |
| Hub search intent | Informational / Commercial / Navigational | Informational |
| Hub type | Guide / Comparison Matrix / Resource Center | Guide |
| Estimated spoke count | Number of spokes in this cluster | 10 |

### 0.2 — Spoke Map

Define every spoke before writing the hub. Each spoke entry:

| Field | Description |
|-------|-------------|
| Slug | URL slug (e.g., `ncsf-cpt-review`) |
| Title (working) | Draft title |
| Type | Review / Comparison / Career / Guide / Deals |
| Primary keyword | Target keyword for the spoke |
| Hub link context | Where in the hub this spoke should be linked FROM |
| Priority | P1 (launch with hub) / P2 (within 30 days) / P3 (within 90 days) |

### 0.3 — Cluster Positioning

- How does this hub differentiate from competing hubs already ranking?
- What unique data, angle, or framework does this hub offer?
- Which persona(s) does this hub primarily serve?
- What is the affiliate monetization path through this hub?

**⛳ QC Gate 0 — Cluster Plan Review**

| Check | Severity | Criteria |
|-------|----------|----------|
| Hub keyword defined | [BLOCK] | Non-empty, specific, matches search intent |
| Spoke map has ≥5 spokes | [BLOCK] | Cluster must have enough depth to justify a hub |
| Every spoke has a slug and type | [BLOCK] | No TBD entries |
| Hub type selected | [BLOCK] | One of: Guide, Comparison Matrix, Resource Center |
| Positioning statement complete | [WARN] | Answers "why would someone read THIS instead of what already ranks?" |
| Affiliate path identified | [WARN] | At least one monetization touchpoint mapped |

---

## Layer 1 — Hub Strategy

**Purpose:** Research the competitive landscape and define the strategic approach for this specific hub.

### 1.1 — SERP Gap Analysis

For the hub's primary keyword, analyze the top 5 ranking pages:

| Competitor | URL | Word Count | H2 Count | Tables | Videos | Unique Angle |
|-----------|-----|-----------|----------|--------|--------|-------------|
| | | | | | | |

**Extract:**
- What topics do all top 5 cover? (table stakes — hub must include these)
- What topics do only 1-2 cover? (differentiation opportunities)
- What topics do none cover? (gap opportunities — highest value)
- What structural formats do they use? (tables, calculators, comparison charts)
- What's missing from all of them? (this becomes the hub's USP)

### 1.2 — Keyword Mapping

| Field | Value |
|-------|-------|
| Primary keyword | |
| Secondary keywords (3-5) | |
| Long-tail variations (5-10) | |
| Featured snippet opportunity? | Yes/No + format (paragraph/list/table) |
| People Also Ask targets (3-5) | |

### 1.3 — Persona Targeting

Which personas does this hub serve? Rank by priority:

| Persona | Priority | Key question they're asking | Where in hub it's answered |
|---------|----------|---------------------------|---------------------------|
| | | | |

### 1.4 — Affiliate Integration Map

| Placement | Product/Offer | Affiliate ID | CTA copy (draft) | Position in hub |
|-----------|--------------|--------------|-------------------|-----------------|
| | | | | |

**⛳ QC Gate 1 — Strategy Review**

| Check | Severity | Criteria |
|-------|----------|----------|
| SERP analysis has ≥3 competitors | [BLOCK] | Must understand competitive landscape |
| Gap opportunity identified | [BLOCK] | At least one topic/angle competitors miss |
| Primary + secondary keywords listed | [BLOCK] | Hub must target specific terms |
| Featured snippet format identified | [WARN] | If opportunity exists, format must be planned |
| PAA targets defined | [WARN] | ≥3 PAA questions mapped |
| Affiliate placements mapped | [WARN] | At least 1 CTA planned |

---

## Layer 2 — Structural Scaffold

**Purpose:** Build the complete outline. The hub outline is more detailed than a spoke outline because the hub must serve as a comprehensive navigation center.

### 2.1 — Title & Meta

| Field | Constraint | Value |
|-------|-----------|-------|
| H1 / Title tag | ≤60 characters, primary keyword in first 30 chars | |
| Meta description | 120-155 characters, includes primary keyword | |
| URL slug | ≤5 words, matches primary keyword | |

### 2.2 — H2 Structure

Hubs require a specific content architecture:

**Required sections (every hub must have):**

| Section | Purpose | Min words |
|---------|---------|-----------|
| Opening hook + StatHighlight | Immediate value, key data points | 100 |
| "What/Why" foundational section | Establishes authority and context | 200 |
| Core content (3-5 H2s) | The meat — varies by hub type | 200 each |
| Comparison/decision framework | Helps reader choose/decide | 200 |
| FAQ section | Targets PAA, adds topical depth | 150 |
| Bottom Line / Summary | Wraps with clear recommendation | 100 |

**Hub-specific requirements by type:**

**Guide Hub:**
- Step-by-step or sequential structure
- Each step is an H2
- Each step links to relevant spokes
- RealMath component for cost/time calculations
- ActionSteps component for takeaways

**Comparison Matrix Hub:**
- Master comparison table early (above the fold)
- Individual breakdowns as H2s
- ChooseIf components for decision support
- Links to individual review spokes from each breakdown

**Resource Center Hub:**
- Categorized sections (by topic, not alphabet)
- SpokeCards for navigation to spokes
- Curated recommendations, not just a link dump
- KeyTakeaway for each category

### 2.3 — Spoke Link Map

**Every spoke in the cluster must be linked from the hub.** Map each spoke to its link location:

| Spoke slug | Link context in hub | Anchor text (draft) | Link type |
|-----------|-------------------|--------------------|-----------| 
| | Which H2 section | | Inline / SpokeCard / Table cell |

**Link rules for hubs:**
- Every spoke linked at least once (100% spoke coverage)
- Primary link should be contextual (within prose), not just in a nav section
- SpokeCards component for grouped navigation
- No spoke should be linked more than 3 times (dilutes equity)

### 2.4 — Component Plan

| Component | Count | Placement |
|-----------|-------|-----------|
| StatHighlight | 1 | After opening paragraph |
| AffiliateCTA | 1-2 | After core content, before FAQ |
| KeyTakeaway | 2-3 | After major decision points |
| RealMath | 1-2 | Cost/time calculations |
| SpokeCards | 1-2 | After relevant sections |
| BottomLine | 1 | End of article |
| FAQ (native H3s) | 1 | Dedicated section, targets PAA |

**⛳ QC Gate 2 — Scaffold Review**

| Check | Severity | Criteria |
|-------|----------|----------|
| Title ≤60 chars | [BLOCK][AUTO] | Character count check |
| Primary keyword in first 30 chars of title | [BLOCK][AUTO] | Position check |
| Meta 120-155 chars | [BLOCK][AUTO] | Character count check |
| URL slug ≤5 words | [BLOCK][AUTO] | Word count check |
| ≥6 H2 sections planned | [BLOCK] | Hub needs depth |
| Every spoke mapped to a link location | [BLOCK] | 100% spoke coverage in link map |
| StatHighlight planned | [BLOCK] | Hub must open with data |
| AffiliateCTA planned | [BLOCK] | Hub must monetize |
| BottomLine planned | [BLOCK] | Hub must conclude with recommendation |
| FAQ section with ≥3 questions | [WARN] | PAA targeting |
| SpokeCards component planned | [WARN] | Navigation aid |
| Comparison table planned (if applicable) | [WARN] | Decision support |

---

## Layer 3 — Content Hydration

**Purpose:** Write the actual content. Hub content standards are higher than spoke standards because hubs carry more SEO weight.

### 3.1 — Content Standards (Hub-Specific)

| Metric | Hub Minimum | Hub Target |
|--------|-------------|------------|
| Total word count | 1,500–3,000 (hub) / 2,000–4,000 (pillar) | 2,000+ recommended |
| H2 sections | 6+ | 8+ |
| Data points (numbers, $, %) | 15+ | 25+ |
| Internal links (total) | 10+ | All spokes + 2-3 cross-hub |
| Spoke coverage | 100% | 100% |
| Tables | 1+ | 2+ |
| Component diversity | 4+ unique types | 6+ |
| Paragraphs >4 sentences | 0 | 0 |

### 3.2 — Prose Rules for Hubs

- **First 50 words** must include the primary keyword
- **Opening paragraph** must establish what the reader will get from this page and why it's different from other resources
- **Every H2 section** must contain at least one of: data point, internal link, or component
- **No section** should exceed 400 words without a visual break (table, component, list)
- **Spoke links** must use descriptive anchor text, not "click here" or "this article"
- **Comparison data** must use tables, not prose paragraphs listing features

### 3.3 — Hub-to-Spoke Integration

For each spoke link in the hub:
- The link must be contextually relevant (placed where a reader would naturally want more depth)
- The anchor text must describe what the spoke covers
- The surrounding sentence must give the reader a reason to click

**Good:** "We break down every dollar in our [cheapest certifications guide](/blog/cheapest-personal-trainer-certifications)."
**Bad:** "See our [article](/blog/cheapest-personal-trainer-certifications) for more info."

### 3.4 — Affiliate Integration

- AffiliateCTA must appear after the reader has received genuine value (never before the first H2)
- CTA copy must be specific to the content context, not generic
- The CTA must reference a specific savings amount or value proposition
- Maximum 2 AffiliateCTA components per hub (more feels salesy)
- Contextual text links to affiliate offers are fine in addition to CTAs

**⛳ QC Gate 3 — Hydration Review**

| Check | Severity | Criteria |
|-------|----------|----------|
| Word count 1,500–3,000 (hub) or 2,000–4,000 (pillar) | [BLOCK] | Content depth gate |
| Primary keyword in first 50 words | [BLOCK] | SEO requirement |
| Every spoke linked at least once | [BLOCK] | 100% spoke coverage |
| ≥1 table present | [BLOCK] | Data presentation |
| ≥15 data points | [BLOCK] | Data density |
| No paragraph >4 sentences | [WARN] | Readability |
| No section >400 words without visual break | [WARN] | Scannability |
| Anchor text descriptive (not generic) | [WARN] | Link quality |
| AffiliateCTA present | [WARN] | Monetization |

---

## Layer 4 — Polish & Conversion

**Purpose:** Optimize for scannability, conversion, and SERP features.

### 4.1 — Scannability Audit

- [ ] Bold key phrases in each paragraph (1-2 per paragraph max)
- [ ] H2 headings are scannable and descriptive (reader can get the gist by reading only H2s)
- [ ] Tables have clear headers and consistent formatting
- [ ] Components break up long prose sections
- [ ] No wall-of-text sections

### 4.2 — Featured Snippet Optimization

If a featured snippet opportunity was identified in Layer 1:

**Paragraph snippet:** Write a 40-60 word definition/answer directly after the relevant H2, with the target question as the H2 text.

**List snippet:** Use a numbered or bulleted list with 5-8 items directly after the H2.

**Table snippet:** Place a comparison table with clear headers directly after the H2.

### 4.3 — CTA Optimization

- CTA button text is action-oriented and specific
- CTA description references a concrete value proposition
- CTA placement follows the reader's decision journey (not random)

### 4.4 — Brand Voice Check

| Rule | Check |
|------|-------|
| "NCSF" not "ncsf" | Always uppercase for organization acronyms |
| "NCCA-accredited" | Hyphenated compound modifier |
| Price formatting | "$399" not "$399.00" unless comparing decimals |
| Cert names | Full name on first mention, acronym thereafter |
| Competitor mentions | Factual and respectful — never dismissive |
| Site name | "Pro Trainer Prep" — always full name |

**⛳ QC Gate 4 — Polish Review**

| Check | Severity | Criteria |
|-------|----------|----------|
| Hook in first sentence | [BLOCK] | Reader must be engaged immediately |
| Primary keyword in first 50 words | [BLOCK][AUTO] | SEO requirement |
| H2s are scannable standalone | [WARN] | Reader can skim H2s and understand the page |
| No paragraph >4 sentences | [WARN][AUTO] | Readability |
| CTA text is specific and action-oriented | [WARN] | Conversion quality |
| Brand terminology consistent | [WARN] | Professional presentation |
| ≥1 visual break per 400 words | [WARN] | Scannability |
| No filler phrases | [WARN][AUTO] | Content quality |

---

## Layer 5 — QC Validate (READ-ONLY)

**Purpose:** Full audit. This layer FLAGS issues but FIXES NOTHING. All fixes happen in Layer 6 (Editor).

### 5.1 — Technical Validation

| Check | Severity | Method |
|-------|----------|--------|
| Frontmatter parses cleanly | [BLOCK][AUTO] | `astro build` completes |
| All internal links resolve | [BLOCK][AUTO] | No 404s |
| Affiliate links use correct tracking URLs | [BLOCK][AUTO] | Match Impact Radius link map |
| Images load | [BLOCK][AUTO] | URL resolves with 200 |
| MDX renders without artifacts | [BLOCK][AUTO] | No broken tables, unclosed tags |
| Category exists in taxonomy | [WARN][AUTO] | Valid category value |
| `type: hub` in frontmatter | [BLOCK] | Hub must be typed |

### 5.2 — SEO Validation

| Check | Severity | Target |
|-------|----------|--------|
| Title tag ≤60 chars | [BLOCK][AUTO] | Character count |
| Meta description 120-155 chars | [BLOCK][AUTO] | Character count |
| Primary keyword in H1 | [BLOCK][AUTO] | Present and natural |
| Primary keyword in first 50 words | [BLOCK][AUTO] | Position check |
| Keyword density 0.5%-2.0% | [WARN][AUTO] | Word frequency |
| URL slug ≤5 words | [WARN][AUTO] | Word count |
| Image alt text present | [WARN][AUTO] | Every image has alt |
| Canonical URL correct | [WARN][AUTO] | Matches expected URL |

### 5.3 — Hub-Specific Link Validation

| Check | Severity | Target |
|-------|----------|--------|
| Hub links to ALL spokes | [BLOCK] | 100% outbound spoke coverage |
| Every spoke links BACK to hub | [BLOCK] | 100% inbound backlink coverage |
| Bidirectional link rate | [BLOCK] | Must be 100% for hub pages |
| No orphaned spokes | [BLOCK] | Every spoke reachable from hub |
| Cross-hub links (if multiple hubs exist) | [WARN] | Hub should link to other hubs |
| Spoke link anchor text is descriptive | [WARN] | Not generic "click here" |

### 5.4 — Content Quality Scoring

Rate the hub 1-5 on each dimension:

| Dimension | 1 (Fail) | 3 (Acceptable) | 5 (Excellent) |
|-----------|----------|----------------|---------------|
| Comprehensiveness | Missing major subtopics | Covers basics | Best answer on SERP |
| Data density | Few numbers | Some data tables | Comprehensive sourced data |
| Navigation value | Reader must scroll to find spokes | Spokes linked inline | SpokeCards + inline + table links |
| Conversion readiness | No CTA | CTA present | Strategic CTAs with specific value props |
| Spoke integration | Spokes linked but disconnected | Links with context | Links with reasons to click |
| Scannability | Wall of text | H2s and some breaks | Can understand page from H2s alone |

**Hub publishing threshold: Average ≥ 4.0 (higher than spoke threshold of 3.5)**

### 5.5 — Legal/Compliance

| Check | Severity | Standard |
|-------|----------|----------|
| Affiliate disclosure present | [BLOCK] | AffiliateDisclosure component or text |
| No unsubstantiated income claims | [BLOCK] | No specific earnings promises |
| No medical/dietary advice | [WARN] | Refer to professionals |
| Competitor comparisons factual | [WARN] | Every claim verifiable |

**⛳ QC Gate 5 — Validation Report**

Output: A QC report listing every check with PASS/FAIL/WARN status. This report is the input to Layer 6.

---

## Layer 6 — Editor

**Purpose:** Fix every BLOCK flagged by Layer 5. Address WARNs where practical. Touch nothing that passed.

### Editor Rules

1. **Fix BLOCKs first, WARNs second.** Don't polish what's already passing.
2. **Minimal edits.** Change only what the QC report flagged. Don't rewrite passing sections.
3. **Preserve structure.** If the scaffold is sound, the editor fixes content within the existing structure.
4. **Backlink injection.** If spokes are missing backlinks to this hub, the Editor adds them to the spokes (not just the hub).
5. **After all fixes: re-run Layer 5.** The Editor's output goes back through QC. If BLOCKs remain, repeat.

### Editor Checklist

- [ ] All BLOCKs from QC report addressed
- [ ] WARNs reviewed and addressed where practical
- [ ] No new issues introduced by edits
- [ ] Spokes updated with backlinks if QC flagged missing backlinks
- [ ] Re-validation requested

**⛳ QC Gate 6 — Editor Verification**

Re-run Layer 5 QC Validate. If zero BLOCKs → proceed to Layer 7. If BLOCKs remain → back to Editor (max 2 cycles).

---

## Layer 7 — Publish & Wire

**Purpose:** Deploy the hub and verify it works in production. This is the final layer — nothing ships without this.

### 7.1 — Pre-Publish Checklist

- [ ] `astro build` passes locally
- [ ] Git commit message references hub name and QC pass
- [ ] All spoke backlinks committed in same push (or preceding push)

### 7.2 — Post-Deploy Verification

| Check | Method |
|-------|--------|
| Page loads at expected URL | `curl -s -o /dev/null -w "%{http_code}" https://protrainerprep.com/blog/{slug}` |
| Title tag renders correctly | Parse `<title>` from HTML |
| Meta description renders correctly | Parse `<meta name="description">` |
| All spoke links resolve (no 404s) | Crawl all internal links from rendered HTML |
| AffiliateCTA renders and links work | Verify `sjv.io` link present |
| Canonical URL correct | Parse `<link rel="canonical">` |
| Open Graph tags present | Parse `og:title`, `og:description`, `og:image` |
| Sitemap updated | Check sitemap.xml includes new hub URL |
| Google Search Console | Submit URL for indexing (manual step) |

### 7.3 — Spoke Wiring Verification

After hub deploys, verify the full link circuit:

```
For each spoke in cluster:
  ✅ Hub links TO spoke (in rendered HTML)
  ✅ Spoke links BACK to hub (in rendered HTML)
  ✅ Spoke links to ≥2 sibling spokes
  = Full bidirectional circuit confirmed
```

### 7.4 — Performance Baseline

Within 48 hours of deployment:
- Run PageSpeed Insights on hub URL
- Record baseline scores (Performance, Accessibility, Best Practices, SEO)
- Flag any hub-specific performance issues (large images, slow components)

---

## Differences from Spoke Blueprint

| Dimension | Spoke | Hub |
|-----------|-------|-----|
| Word count range | 700–2,500 | 1,500–3,000 |
| Pillar word count range | N/A | 2,000–4,000 |
| Internal links minimum | 3 | 10+ (all spokes) |
| Spoke coverage required | Link to hub + 2 siblings | Link to ALL spokes |
| Backlink requirement | Link back to hub | All spokes link back |
| Quality score threshold | ≥3.5 avg | ≥4.0 avg |
| QC layers | 5 (QC) + 6 (Editor) | 5 (QC) + 6 (Editor) + 7 (Publish & Wire) |
| Post-deploy verification | Optional | Required |
| Featured snippet targeting | Optional | Required (if opportunity exists) |
| Comparison tables | Optional | Required (if hub type warrants) |
| FAQ section | Recommended | Required |
| Cross-hub linking | N/A | Required (when multiple hubs exist) |

---

## Appendix: Hub Type Templates

### Guide Hub Template

```
Opening hook + StatHighlight
H2: Step 1 (or foundational concept)
  → Links to relevant spokes
H2: Step 2
  → Links to relevant spokes
  → KeyTakeaway
H2: Step 3
  → AffiliateCTA (after value delivered)
...
H2: Cost/Investment section
  → RealMath component
  → Link to cheapest-certs spoke
H2: FAQ
  → H3 per question (PAA targets)
H2: Summary
  → ActionSteps
  → BottomLine
```

### Comparison Matrix Hub Template

```
Opening hook + StatHighlight
H2: Quick comparison table
  → Master table with all options
  → KeyTakeaway
H2: Option A breakdown
  → Link to Option A review spoke
H2: Option B breakdown
  → Link to Option B review spoke
  → AffiliateCTA
...
H2: How to choose
  → ChooseIf components
  → Decision framework
H2: FAQ
H2: Bottom Line
  → BottomLine
```

### Resource Center Hub Template

```
Opening hook + StatHighlight
H2: Category 1
  → SpokeCards for category spokes
  → KeyTakeaway
H2: Category 2
  → SpokeCards
H2: Category 3
  → AffiliateCTA
...
H2: Getting Started
  → ActionSteps
H2: FAQ
H2: Bottom Line
```
