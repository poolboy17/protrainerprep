# Pillar Page Template
# seoTier: pillar
# Source of truth for the top of the SEO pyramid
# Word count: 2,000–4,000
# This page links DOWN to every hub. It is the entry point.

---

## Frontmatter (required fields)

```yaml
publishDate: YYYY-MM-DDTHH:MM:SSZ
title: >
  # ≤60 chars. Primary keyword first. Format: "[Keyword]: The Complete Guide"
excerpt: >
  # ≤155 chars. Answer the search intent in one sentence.
image: # Unsplash CDN URL
category: guides
tags:
  - # 3–6 lowercase tags
author: Pro Trainer Prep
seoTier: "pillar"
```

---

## Required Imports

```mdx
import StatHighlight from '~/components/blog/StatHighlight.astro';
import KeyTakeaway from '~/components/blog/KeyTakeaway.astro';
import ProTip from '~/components/blog/ProTip.astro';
import RealMath from '~/components/blog/RealMath.astro';
import ActionSteps from '~/components/blog/ActionSteps.astro';
import AffiliateCTA from '~/components/blog/AffiliateCTA.astro';
import BottomLine from '~/components/blog/BottomLine.astro';
```

---

## Required H2 Structure (minimum 8 H2s)

```
## [Primary keyword answer — first 100 words must address search intent]
   - StatHighlight: 1 anchor stat that hooks the reader
   - 150–300 words. No fluff. Answer the question immediately.

## [Step/Phase 1 of the journey]
   - Map to Hub 1 (Career Change). Link to hub page.
   - ProTip or KeyTakeaway component
   - 200–400 words

## [Step/Phase 2 of the journey]
   - Map to Hub 2 (Certifications). Link to hub page.
   - RealMath component with cost/time data
   - 200–400 words

## [Step/Phase 3 of the journey]
   - Map to Hub 3 (Career Building). Link to hub page.
   - ActionSteps component
   - 200–400 words

## [Data section — salary, timeline, costs]
   - StatHighlight or RealMath
   - Hard numbers only. No vague claims.
   - 200–400 words

## [Common mistakes / what most guides miss]
   - KeyTakeaway component
   - 150–300 words

## [FAQ — 3-5 questions]
   - Short paragraph answers, not lists
   - Internal links to relevant spokes
   - 200–400 words

## [Next steps / CTA]
   - AffiliateCTA component
   - Link to all 3 hubs explicitly
   - BottomLine component to close
   - 100–200 words
```

---

## Linking Requirements

| Rule | Required |
|------|----------|
| Link to EVERY hub page | BLOCK if missing |
| Minimum 8 unique internal links | BLOCK if under |
| AffiliateCTA present | BLOCK if missing |
| BottomLine present | BLOCK if missing |

---

## QC Gate (must pass before publish)

- [ ] Title ≤60 chars
- [ ] Excerpt ≤155 chars
- [ ] Word count 2,000–4,000
- [ ] ≥8 H2 headings
- [ ] Links to all hub pages
- [ ] ≥8 unique internal links
- [ ] ≥1 StatHighlight
- [ ] ≥1 RealMath or data component
- [ ] ≥1 AffiliateCTA
- [ ] ≥1 BottomLine
- [ ] No banned phrases
- [ ] Primary keyword in first 100 words
- [ ] seoTier: "pillar" in frontmatter
