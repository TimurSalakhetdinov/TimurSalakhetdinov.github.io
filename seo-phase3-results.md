# SEO Phase 3 Results — On-page SEO
**Site:** timursalakhetdinov.com  
**Date:** 2026-05-20  
**Branch:** `claude/seo-portfolio-optimization-PnypN`  
**Commit:** `a7d6c45`

---

## 3.1 Semantic H2 Headings — Projects and Writing

### CSS rule added to both pages

```css
.sec-h2 {
  font-family: var(--serif); font-size: inherit; font-weight: 400;
  color: var(--ink-soft); margin: 0; letter-spacing: 0.01em;
}
```

Placed inside the existing `<style>` block, directly after the `.sec-right` rule. Uses `font-size: inherit` so it sits inline within the `.sec-head-l` flex row at body scale, complementing (not competing with) the 28px `.sec-title` span. Uses `var(--ink-soft)` for visual hierarchy without introducing a new colour.

### H2 text added

| Section | Page | H2 text |
|---|---|---|
| § 03 Projects | `index.html` | `Selected Projects: Bayesian inference, knowledge graphs, agentic AI` |
| § 03 Projects | `de.html` | `Ausgewählte Projekte: Bayesianische Inferenz, Wissensgraphen, agentische KI` |
| § 04 Writing | `index.html` | `Writing on probabilistic ML and agentic systems` |
| § 04 Writing | `de.html` | `Beiträge zu probabilistischem ML und agentischen Systemen` |

---

## 3.2 Image Alt Text

All project thumbnails now have descriptive, non-keyword-stuffed alt text. The avatar and SVG diagram are unchanged.

### index.html

| Image | Alt text |
|---|---|
| `images/avatar.jpg` | `Timur Salakhetdinov` (unchanged) |
| `images/thumbs/06.jpg` | `Project thumbnail for a knowledge graph question answering system with SPARQL retrieval.` |
| `images/thumbs/05.png` | `Project thumbnail for a machine learning route modelling project using KVG public transport data.` |
| `images/thumbs/03.jpg` | `Project thumbnail for a Neo4j graph analysis of artist influence networks.` |
| `images/thumbs/01.jpg` | `Project thumbnail for a hierarchical Bayesian Pareto/NBD replication of Abe (2009).` |
| `images/thumbs/02.jpeg` | `Project thumbnail for the ChefTreff AI Hackathon product detection challenge.` |

### de.html

| Image | Alt text |
|---|---|
| `images/avatar.jpg` | `Timur Salakhetdinov` (unchanged) |
| `images/thumbs/06.jpg` | `Projektvorschau zu einem System für Frage-Antwort-Verarbeitung über Wissensgraphen mit SPARQL.` |
| `images/thumbs/05.png` | `Projektvorschau zur Routenmodellierung mit Machine Learning anhand von KVG-Verkehrsdaten.` |
| `images/thumbs/03.jpg` | `Projektvorschau zur Neo4j-Graphanalyse von Künstler-Einflussnetzwerken.` |
| `images/thumbs/01.jpg` | `Projektvorschau zur Replikation des hierarchischen Bayesianischen Pareto/NBD-Modells nach Abe (2009).` |
| `images/thumbs/02.jpeg` | `Projektvorschau zur Produkterkennungs-Challenge beim ChefTreff AI Hackathon.` |

**Confirmed: zero non-decorative empty `alt=""` attributes remain on either page.**  
The SVG agent topology diagram retains `aria-label="Agent topology diagram"` — no change needed.  
`images/thumbs/04.png` is not referenced in either HTML file — left untouched.

---

## 3.3 Descriptive Anchor Text

All five project link labels updated on both pages. Zero `↗ repo` occurrences remain.

| Project | EN anchor | DE anchor |
|---|---|---|
| Knowledge Graph Question Answering | `↗ KGQA repo` | `↗ KGQA-Repo` |
| KVG ML Route Modelling | `↗ KVG model repo` | `↗ KVG-Modell-Repo` |
| Neo4j Graph Analysis of Artist Influence Networks | `↗ Artist graph repo` | `↗ Künstlergraph-Repo` |
| Hierarchical Bayesian Pareto/NBD: Replication of Abe (2009) | `↗ Pareto/NBD repo` | `↗ Pareto/NBD-Repo` |
| ChefTreff AI Hackathon: Product Detection | `↗ ChefTreff repo` | `↗ ChefTreff-Repo` |

All five link to GitHub repositories — no non-GitHub destinations to flag.

---

## 3.4 rel and target Attributes

### Project rows (§ 03)

All five `<a class="proj-row">` elements updated from `rel="noopener"` to `rel="noopener external"`. `target="_blank"` was already present on all five.

### Social and profile links (contact section, header)

Links to LinkedIn, GitHub, and Medium already carry `rel="noopener" target="_blank"`. No change needed per spec (no `nofollow`, these are vouched-for profiles).

### "All repositories on GitHub" footer link

Already had `rel="noopener" target="_blank"`. Left unchanged (not a project content link).

---

## 3.5 Featured Project Anchor (§ Thesis)

**No link exists.** The featured section contains the note:  
> "Work in progress through September 2026. Further details once the thesis is submitted."

No anchor was added. When the thesis or a writeup is published, add:
```html
<a href="[URL]" rel="noopener external" target="_blank">↗ Thesis writeup</a>
```

---

## Heading Outline Verification

### index.html (EN) — confirmed matches expected outline

```
H1: Probabilistic forecasting, agentic systems, and ten years of analytics turned into production ML.
  H2: An agentic forecasting architecture for game revenue.
  H2: Selected Projects: Bayesian inference, knowledge graphs, agentic AI
    H3: Knowledge Graph Question Answering
    H3: KVG ML Route Modelling
    H3: Neo4j Graph Analysis of Artist Influence Networks
    H3: Hierarchical Bayesian Pareto/NBD: Replication of Abe (2009)
    H3: ChefTreff AI Hackathon: Product Detection
  H2: Writing on probabilistic ML and agentic systems
  H2: Looking for a data scientist or AI engineer in Germany, Hamburg or Munich, from December 2026?
    H3: ${post.title}   (JS-injected at runtime)
```

### de.html (DE)

```
H1: Probabilistische Prognosen, agentische Systeme und zehn Jahre Analytics im produktiven ML-Einsatz.
  H2: Eine agentische Prognosearchitektur für Spielumsätze.
  H2: Ausgewählte Projekte: Bayesianische Inferenz, Wissensgraphen, agentische KI
    H3: Knowledge Graph Question Answering
    H3: KVG ML Route Modelling
    H3: Neo4j Graph Analysis of Artist Influence Networks
    H3: Hierarchical Bayesian Pareto/NBD: Replication of Abe (2009)
    H3: ChefTreff AI Hackathon: Product Detection
  H2: Beiträge zu probabilistischem ML und agentischen Systemen
  H2: Suchen Sie einen Data Scientist oder KI-Ingenieur in Deutschland, Hamburg oder München, ab Dezember 2026?
    H3: ${post.title}   (JS-injected at runtime)
```

Both pages: exactly one H1, all H3s have a parent H2, no skipped levels.

---

## Diff Summary

**Files changed:** `index.html`, `de.html`

| Change | index.html | de.html |
|---|---|---|
| `.sec-h2` CSS rule | Added | Added |
| H2 in § 03 | Added | Added (German) |
| H2 in § 04 | Added | Added (German) |
| 5 thumbnail alt attributes | Filled with EN descriptions | Filled with DE descriptions |
| 5 `↗ repo` anchors | Replaced with project-specific EN labels | Replaced with project-specific DE labels |
| 5 project row `rel` attributes | `noopener` → `noopener external` | `noopener` → `noopener external` |
| KGQA blurb | No change | Em dash removed: "Abfragen in natürlicher Sprache" (comma replacing dash) |

---

## What comes next (Phase 4)

- Convert `images/avatar.jpg` (963 KB) to WebP with JPEG fallback via `<picture>`
- Add `width` and `height` attributes to all `<img>` tags to prevent layout shift
- Add `<link rel="preload" as="image">` for the avatar (LCP element)
- Add `loading="lazy"` to all below-the-fold project thumbnails (NOT the avatar)
- Defer non-critical scripts
