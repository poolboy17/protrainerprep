# Pro Trainer Prep — SEO Quality Control Gates
# Last updated: 2026-02-10
# Source of truth for automated and manual QC validation

---

## Word Count Ranges (rendered, including component text)

| Page Type | Min | Max | Notes |
|-----------|-----|-----|-------|
| Pillar | 2,000 | 4,000 | Comprehensive top-of-funnel guide |
| Hub | 1,500 | 3,000 | Cluster overview with SpokeCards |
| Spoke | 700 | 2,500 | Focused reviews, comparisons, guides |

Word count includes all rendered text: prose, component content
(StatHighlight, RealMath, ProTip, KeyTakeaway, AffiliateCTA,
BottomLine), and headings. This matches what Google indexes.

---

## SEO Field Constraints

| Field | Max Length | Severity |
|-------|-----------|----------|
| Title tag | ≤60 chars | [BLOCK] |
| Excerpt / meta description | ≤155 chars | [WARN] |
| URL slug | ≤5 words | [WARN] |

---

## Required Frontmatter

| Field | Required | Notes |
|-------|----------|-------|
| publishDate | Yes | ISO 8601 format |
| title | Yes | ≤60 chars |
| excerpt | Yes | ≤155 chars |
| image | Yes | Unsplash CDN URL |
| category | Yes | guides, certifications, career-building, career-change |
| tags | Yes | 3–6, lowercase |
| metadata.canonical | Recommended | Full protrainerprep.com URL |

---

## Required Components

Every article must include:
- `<AffiliateCTA>` — at least one, using nationalcouncilonstrength.sjv.io domain
- `<BottomLine>` — closing summary component

---

## Banned Words (in prose)

Never use in article body text:
- journey, unlock your potential, game-changer, dive in
- landscape, delve, realm, furthermore, in conclusion
- it's important to note, in today's world

Note: "RealMath" component name contains "realm" — exclude
component tags and import lines from banned word scanning.

---

## Internal Linking

| Rule | Severity |
|------|----------|
| Spokes must link back to their hub | [WARN] |
| Hubs must link to all 10 spokes | [BLOCK] |
| Minimum 3 internal links per article | [WARN] |
| Zero broken internal links | [BLOCK] |

---

## Page Type Classification

| Slug | Type |
|------|------|
| how-to-become-personal-trainer | Pillar |
| career-building-guide | Hub |
| fitness-certification-guide | Hub |
| career-change-fitness-guide | Hub |
| All other .mdx files | Spoke |

---

## Architecture Limits

| Dimension | Current | Max |
|-----------|---------|-----|
| Spokes per hub | 10 | 12 (career-building, career-change) / 10 (certifications) |
| Total articles | 34 | Scale as needed |
| Hub count | 3 + 1 pillar | Add hubs for new topic clusters |

---

## Page Templates (source of truth for structure)

Every page MUST be built from its corresponding template.
Templates live in `docs/templates/` and define:
- Required H2 sections
- Required components per section
- Linking obligations
- Word count per section
- QC checklist

| Page Type | Template | Min H2s | Min Components |
|-----------|----------|---------|----------------|
| Pillar | PILLAR-TEMPLATE.md | 8 | 6 types |
| Hub | HUB-TEMPLATE.md | 6 | 4 types |
| Sub-Hub | HUB-TEMPLATE.md | 6 | 4 types |
| Spoke | SPOKE-TEMPLATE.md | 4 | 3 types |

---

## Scaffold Gate (BLOCK — runs before hydration)

No prose is written until the scaffold passes validation.
The scaffold defines H2 headings, component slots, link placements,
and section word targets. See `docs/templates/SCAFFOLD-GATE.md`.

```bash
python workflow_engine.py validate-scaffold --slug article-slug --tier spoke
```

**If scaffold fails → hydration is blocked.**

---

## Pipeline Enforcement Order

```
1. Template selected (based on seoTier)
2. Frontmatter populated
3. Scaffold created (H2s, components, links planned)
4. ── SCAFFOLD GATE ── (must pass)
5. Prose hydration (fill in the skeleton)
6. ── POST-HYDRATION GATE ── (must pass)
7. Publish
```

---

## Valid Categories (updated 2026-02-16)

- guides
- certifications
- career-change
- career-building
- career-growth
- ceu
