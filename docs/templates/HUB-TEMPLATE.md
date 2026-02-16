# Hub Page Template
# seoTier: hub | sub-hub
# Source of truth for cluster overview pages
# Word count: 1,500–3,000
# This page links DOWN to every spoke in its cluster and UP to the pillar.

---

## Frontmatter (required fields)

```yaml
publishDate: YYYY-MM-DDTHH:MM:SSZ
title: >
  # ≤60 chars. "[Topic]: [Value prop or scope]"
excerpt: >
  # ≤155 chars. Summarize what the reader will learn.
image: # Unsplash CDN URL
category: # certifications | career-change | career-building | ceu
tags:
  - # 3–6 lowercase tags
author: Pro Trainer Prep
type: hub
seoTier: "hub"       # or "sub-hub"
seoParent: "[pillar-or-parent-hub-slug]"
```

---

## Required Imports

```mdx
import StatHighlight from '~/components/blog/StatHighlight.astro';
import KeyTakeaway from '~/components/blog/KeyTakeaway.astro';
import ProTip from '~/components/blog/ProTip.astro';
import RealMath from '~/components/blog/RealMath.astro';
import SpokeCards from '~/components/blog/SpokeCards.astro';
import ActionSteps from '~/components/blog/ActionSteps.astro';
import AffiliateCTA from '~/components/blog/AffiliateCTA.astro';
import BottomLine from '~/components/blog/BottomLine.astro';
```

---

## Required H2 Structure (minimum 6 H2s)

```
## [Overview — answer "what is this cluster about" in first 100 words]
   - StatHighlight: 1 anchor stat
   - Set context for the entire cluster
   - 200–300 words

## [Comparison/overview matrix of options in this cluster]
   - Table or ComparisonMatrix if applicable
   - Link to each spoke being compared
   - 300–500 words

## [Decision framework — how to choose]
   - KeyTakeaway component
   - Logic for which spoke path to take
   - 200–400 words

## [Cost/data breakdown]
   - RealMath component with real numbers
   - 200–400 words

## [Common questions / FAQ for this cluster]
   - 3–5 questions, paragraph answers
   - Each answer links to the relevant spoke
   - 200–400 words

## [SpokeCards — visual links to all spokes]
   - SpokeCards component listing ALL spokes in this hub
   - EVERY spoke must be linked here. No exceptions.
   - 50–100 words intro

## [Next steps / CTA]
   - AffiliateCTA component
   - Link UP to pillar
   - BottomLine component
   - 100–200 words
```

---

## Linking Requirements

| Rule | Required |
|------|----------|
| Link UP to pillar page | BLOCK if missing |
| Link to EVERY spoke in this cluster | BLOCK if missing |
| Link to sibling hubs (at least 1) | WARN if missing |
| Minimum 10 unique internal links | BLOCK if under |
| SpokeCards component present | BLOCK if missing |
| AffiliateCTA present | BLOCK if missing |
| BottomLine present | BLOCK if missing |

---

## QC Gate (must pass before publish)

- [ ] Title ≤60 chars
- [ ] Excerpt ≤155 chars
- [ ] Word count 1,500–3,000
- [ ] ≥6 H2 headings
- [ ] Links UP to pillar
- [ ] Links to ALL spokes in cluster
- [ ] ≥10 unique internal links
- [ ] ≥1 StatHighlight
- [ ] ≥1 RealMath or data component
- [ ] SpokeCards component present
- [ ] ≥1 AffiliateCTA
- [ ] ≥1 BottomLine
- [ ] ≥4 component types used
- [ ] No banned phrases
- [ ] Primary keyword in first 100 words
- [ ] seoTier: "hub" or "sub-hub" in frontmatter
- [ ] seoParent set to correct parent slug
