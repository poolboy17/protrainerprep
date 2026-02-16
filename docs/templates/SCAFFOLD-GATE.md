# Scaffold Validation Gate
# This gate runs BETWEEN outline creation and prose hydration.
# If the scaffold fails, NO PROSE IS WRITTEN.

---

## Purpose

The scaffold is the skeleton of the article. It contains:
- Complete frontmatter
- All H2 headings with brief descriptions
- Component assignments (which component goes where)
- Link placements (which internal links go where)
- Word count targets per section

The scaffold is NOT prose. It is structure only.

---

## Gate Checks (automated by workflow_engine.py)

### Pillar Scaffold
- [ ] ≥8 H2 headings defined
- [ ] Links to all 3 hub pages assigned
- [ ] ≥2 StatHighlight slots
- [ ] ≥1 RealMath slot
- [ ] ≥1 ActionSteps slot
- [ ] AffiliateCTA + BottomLine slots at end
- [ ] Section word targets sum to 2,000–4,000

### Hub Scaffold
- [ ] ≥6 H2 headings defined
- [ ] Link UP to pillar assigned
- [ ] Links to ALL spokes in cluster assigned
- [ ] SpokeCards slot present
- [ ] ≥1 StatHighlight slot
- [ ] ≥1 RealMath slot
- [ ] AffiliateCTA + BottomLine slots at end
- [ ] Section word targets sum to 1,500–3,000

### Spoke Scaffold
- [ ] ≥4 H2 headings defined
- [ ] Link UP to parent hub assigned
- [ ] ≥2 sibling spoke links assigned
- [ ] ≥1 type-appropriate component slot (RealMath, ProsCons, etc.)
- [ ] KeyTakeaway slot present
- [ ] AffiliateCTA + BottomLine slots at end
- [ ] Section word targets sum to 700–2,500

---

## Scaffold Format

A scaffold file looks like this:

```markdown
---
[complete frontmatter]
---

## H2 Title Here
<!-- Target: 200 words -->
<!-- Components: StatHighlight -->
<!-- Links: /certifications/ncsf-cpt-review, /career-change/career-change-fitness-guide -->
[Brief description of what this section covers]

## Next H2 Title
<!-- Target: 300 words -->
<!-- Components: RealMath, KeyTakeaway -->
<!-- Links: /certifications/nasm-vs-ncsf -->
[Brief description]

...
```

---

## Enforcement

The workflow engine validates the scaffold BEFORE hydration begins:

```bash
python workflow_engine.py validate-scaffold --slug article-slug --tier spoke
```

If the scaffold fails, the engine outputs:
- Which checks failed
- What needs to be added
- Suggested H2 structures based on article type

No prose is written until the scaffold passes.

---

## Why This Exists

Without this gate, articles get written as prose blobs:
- No H2 structure → bad for SEO and scannability
- No component plan → thin content without data visualization
- No link plan → orphaned pages and broken pyramid
- No word targets → sections that are too thin or too bloated

The scaffold is the contract. Hydration fills it in.
