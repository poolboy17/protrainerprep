# Spoke Page Template
# seoTier: spoke
# Source of truth for bottom-layer content pages
# Word count: 700–2,500
# This page links UP to its hub and ACROSS to 2+ siblings.

---

## Frontmatter (required fields)

```yaml
publishDate: YYYY-MM-DDTHH:MM:SSZ
title: >
  # ≤60 chars. Specific keyword targeting long-tail query.
excerpt: >
  # ≤155 chars. Direct answer to the search query.
image: # Unsplash CDN URL
category: # certifications | career-change | career-building | career-growth | ceu
tags:
  - # 3–6 lowercase tags
author: Pro Trainer Prep
type: # review | comparison | career | data | guide
seoTier: "spoke"
seoHub: "[hub-cluster-name]"
seoParent: "[parent-hub-slug]"
```

---

## Required Imports (minimum)

```mdx
import KeyTakeaway from '~/components/blog/KeyTakeaway.astro';
import AffiliateCTA from '~/components/blog/AffiliateCTA.astro';
import BottomLine from '~/components/blog/BottomLine.astro';
```

### Additional imports based on article type:

- **Review**: + VerdictBox, ProsCons, AffiliateDisclosure, StatHighlight, ProTip
- **Comparison**: + StatHighlight, RealMath, QuickAnswer, ProTip
- **Career transition**: + ActionSteps, ProTip, RealMath
- **Cost/data**: + RealMath, StatHighlight
- **Specialty cert**: + ProTip, StatHighlight

---

## Required H2 Structure (minimum 4 H2s)

```
## [Direct answer — first 100 words address the search intent]
   - No preamble. Answer the question immediately.
   - If review: QuickAnswer component
   - If data: StatHighlight with anchor number
   - 100–250 words

## [Core content section 1 — the meat]
   - Deepest section. This is where the value lives.
   - Data, analysis, comparison, or step-by-step
   - Component: type-appropriate (RealMath for costs, ProsCons for reviews)
   - 200–500 words

## [Core content section 2 — secondary angle]
   - Different facet of the topic
   - KeyTakeaway component
   - Internal link to 1-2 sibling spokes
   - 200–400 words

## [Practical application / what to do next]
   - ActionSteps or ProTip component
   - AffiliateCTA positioned at natural decision point
   - Internal link to parent hub
   - 150–300 words

## [Optional: FAQ or edge cases]
   - Only if the topic warrants it
   - 2-3 questions max
   - Links to sibling spokes
   - 100–200 words

## [Closing]
   - BottomLine component — firm recommendation, not wishy-washy
   - Final sibling link
   - 50–100 words
```

---

## Linking Requirements

| Rule | Required |
|------|----------|
| Link UP to parent hub | BLOCK if missing |
| Link to ≥2 sibling spokes | BLOCK if missing |
| Minimum 3 unique internal links | BLOCK if under |
| AffiliateCTA present | BLOCK if missing |
| BottomLine present | BLOCK if missing |

---

## QC Gate (must pass before publish)

### Pre-Hydration Gate (scaffold must pass BEFORE writing prose):
- [ ] Frontmatter complete with all required fields
- [ ] seoTier, seoHub, seoParent set correctly
- [ ] ≥4 H2 headings defined in outline
- [ ] Parent hub link placement identified
- [ ] ≥2 sibling links placement identified
- [ ] Component slots assigned (which component in which section)
- [ ] AffiliateCTA position chosen
- [ ] BottomLine at end confirmed

### Post-Hydration Gate (after prose is written):
- [ ] Title ≤60 chars
- [ ] Excerpt ≤155 chars
- [ ] Word count 700–2,500
- [ ] ≥4 H2 headings present in rendered content
- [ ] Links UP to parent hub present
- [ ] ≥2 sibling spoke links present
- [ ] ≥3 unique internal links total
- [ ] ≥1 AffiliateCTA rendered
- [ ] ≥1 BottomLine rendered
- [ ] Primary keyword in first 100 words
- [ ] No banned phrases in body text
- [ ] Data density: ≥5 numeric data points
- [ ] No sections under 50 words (filler check)
