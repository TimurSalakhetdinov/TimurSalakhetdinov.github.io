# SEO Audit — Phase 1
**Site:** timursalakhetdinov.com  
**Date:** 2026-05-20  
**Scope:** All public-facing HTML pages

---

## 1. Files Inventoried

| Path | Type |
|---|---|
| `index.html` | Public page (EN, `/`) |
| `de.html` | Public page (DE, `/de`) |

No other public-facing HTML files exist in the repository.

---

## 2. Title and Meta Description

| Page | Title | Chars | Status | Meta Description | Chars | Status |
|---|---|---|---|---|---|---|
| `index.html` | `Timur Salakhetdinov — Data Scientist · AI Engineer` | 53 | OK (target 50-60) | `Data scientist with ten years of analytical experience across finance, telecom, and gaming. Currently at InnoGames building production ML forecasting systems, M.Sc. candidate at Leuphana University.` | 198 | Too long (target 140-160) |
| `de.html` | `Timur Salakhetdinov — Data Scientist · KI-Ingenieur` | 54 | OK | `Data Scientist mit zehn Jahren Analyseerfahrung in Finanzen, Telekommunikation und Gaming. Derzeit bei InnoGames im Bereich produktives ML-Forecasting, M.Sc.-Kandidat an der Leuphana Universität.` | 196 | Too long |

---

## 3. Heading Hierarchy

### `index.html` (English)

| Level | Text | Issue |
|---|---|---|
| H1 | `Probabilistic forecasting, agentic systems, and ten years of analytics turned into production ML.` | OK — single H1 |
| H2 | `An agentic forecasting architecture for game revenue.` | OK (Featured project) |
| *(no H2)* | Projects section § 03 uses `<span class="sec-title">` not a heading | Missing H2 |
| H3 | `Knowledge Graph Question Answering` | OK |
| H3 | `KVG ML Route Modelling` | OK |
| H3 | `Neo4j Graph Analysis of Artist Influence Networks` | OK |
| H3 | `Hierarchical Bayesian Pareto/NBD: Replication of Abe (2009)` | OK |
| H3 | `ChefTreff AI Hackathon: Product Detection` | OK |
| *(no H2)* | Writing section § 04 uses `<span class="sec-title">` not a heading | Missing H2 |
| H2 | `Looking for a data scientist or AI engineer in Germany from December 2026?` | OK (Contact) |
| H3 | `${post.title}` (JS-injected Medium posts) | OK |

### `de.html` (German)

Identical structure with translated text. Same two missing H2s.

---

## 4. Images

| Page | `src` | `alt` value | Status |
|---|---|---|---|
| Both | `images/avatar.jpg` | `"Timur Salakhetdinov"` | OK |
| Both | `images/thumbs/06.jpg` | `""` | Needs descriptive alt (SPARQL/KGQA project) |
| Both | `images/thumbs/05.png` | `""` | Needs descriptive alt (KVG route modelling) |
| Both | `images/thumbs/03.jpg` | `""` | Needs descriptive alt (Neo4j artist networks) |
| Both | `images/thumbs/01.jpg` | `""` | Needs descriptive alt (Bayesian Pareto/NBD) |
| Both | `images/thumbs/02.jpeg` | `""` | Needs descriptive alt (ChefTreff AI hackathon) |

Note: the inline SVG agent topology diagram uses `aria-label="Agent topology diagram"` — acceptable as-is.

---

## 5. Technical SEO Checklist

| Signal | `index.html` | `de.html` | Action |
|---|---|---|---|
| `<title>` length (target 50-60 chars) | 53 chars — OK | 54 chars — OK | None |
| `<meta description>` length (target 140-160 chars) | 198 — too long | 196 — too long | Trim both |
| Exactly one `<h1>` per page | Yes | Yes | None |
| `<link rel="canonical">` | Missing | Missing | Add |
| `hreflang` pair + `x-default` | Missing | Missing | Add |
| `og:title` | Present | Present | None |
| `og:description` | Present | Present | None |
| `og:type` | Present | Present | None |
| `og:image` | **Missing** | **Missing** | Add (critical) |
| `og:image:width`, `og:image:height`, `og:image:alt` | **Missing** | **Missing** | Add |
| `twitter:card` | **Missing** | **Missing** | Add |
| JSON-LD structured data | **Missing** | **Missing** | Add |
| `robots.txt` at repo root | **Missing** | n/a | Create |
| `sitemap.xml` at repo root | **Missing** | n/a | Create |
| `favicon.ico` | Present | n/a | None |
| `apple-touch-icon.png` (180x180) | Present | n/a | None |
| `site.webmanifest` | Present | n/a | None |
| Google Fonts `<link rel="preconnect">` | Present | Present | None |
| `font-display: swap` | Via `display=swap` URL param | Same | None |
| Email as indexable plain text | Yes (`timsalakhetdinov@gmail.com`) | Yes | None |

---

## 6. Root-Level Files

| File | Status |
|---|---|
| `favicon.ico` | Present (15 KB) |
| `apple-touch-icon.png` | Present (180x180, 10 KB) |
| `android-chrome-192x192.png` | Present |
| `android-chrome-512x512.png` | Present |
| `favicon-16x16.png` | Present |
| `favicon-32x32.png` | Present |
| `site.webmanifest` | Present |
| `robots.txt` | **Missing** |
| `sitemap.xml` | **Missing** |

---

## 7. Images Directory

```
images/
  avatar.jpg        (963 KB — large, candidate for WebP conversion)
  bg.jpg            (35 KB)
  fulls/
    01.jpg, 02.jpg, 03.jpg, 04.jpg, 05.jpg, 06.jpg
  thumbs/
    01.jpg, 02.jpeg, 03.jpg, 04.png, 05.png, 06.jpg
```

No OG cover image exists yet. One must be created at `images/og-cover.jpg` (1200x630).

---

## 8. Assets and Scripts

| File | Minified | Notes |
|---|---|---|
| `assets/css/fontawesome-all.min.css` | Yes | Third-party |
| `assets/css/main.css` | No | Custom styles |
| `assets/js/jquery.min.js` | Yes | Third-party |
| `assets/js/breakpoints.min.js` | Yes | Third-party |
| `assets/js/browser.min.js` | Yes | Third-party |
| `assets/js/jquery.poptrox.min.js` | Yes | Third-party |
| `assets/js/main.js` | No | Custom (117 lines) |
| `assets/js/util.js` | No | Custom |

The main CSS is embedded in `<style>` blocks inside each HTML file (454 lines), not loaded from `main.css`. The `main.css` file appears unused or legacy.

---

## 9. Medium Writing Feed

Both pages fetch posts at runtime via `rss2json.com`:

```javascript
const url = `https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@timursalakhetdinov&api_key=...`;
```

- If the account has no posts, or the API call fails, the Writing section renders as a blank horizontal rule.
- No fallback or empty-state handling exists.
- The API key is a free-tier rss2json key embedded in client-side JS (low risk, but visible).

---

## 10. Other Observations

- **Projects section (§ 03)**: the section label is a `<span>`, not a heading. H3 project titles therefore have no H2 parent in the document outline. Needs a visually hidden or styled H2.
- **Writing section (§ 04)**: same issue — `<span class="sec-title">Writing</span>`, no H2 wrapper.
- **Project link anchor text**: most row links end with `↗ repo`, which is non-descriptive for search engines. Should reference the project name.
- **OG image gap**: the most impactful missing element. Without `og:image`, social shares on LinkedIn, Slack, and Twitter render with no preview card.
- **No "What I work on" paragraph**: the projects section jumps straight into the table. A short prose paragraph with natural keyword coverage is missing.

---

## 11. Priority Action List for Phase 2+

Ranked by SEO impact:

1. Create `images/og-cover.jpg` (1200x630) and add all OG image tags
2. Add `<link rel="canonical">` to both pages
3. Add `hreflang` pair (`en`, `de`, `x-default`) to both pages
4. Add Twitter Card meta tags to both pages
5. Add JSON-LD `Person` + `WebSite` schemas to both pages
6. Create `robots.txt`
7. Create `sitemap.xml` with hreflang alternates
8. Trim meta descriptions to 140-160 chars
9. Add H2 headings to Projects and Writing sections (Phase 3)
10. Add descriptive `alt` text to project thumbnail images (Phase 3)
11. Add "What I work on" paragraph above projects (Phase 5)
12. Fix Writing section empty-state (Phase 5)
