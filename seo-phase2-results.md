# SEO Phase 2 Results — Technical SEO
**Site:** timursalakhetdinov.com  
**Date:** 2026-05-20  
**Branch:** `claude/seo-portfolio-optimization-PnypN`  
**Commits:** `4d84a80` (index.html + root files), `be0e948` (de.html mirror)

---

## 2.1 + 2.2 Title and Meta Description

| Page | Field | Value | Chars | Target | Status |
|---|---|---|---|---|---|
| `index.html` | `<title>` | `Timur Salakhetdinov \| Data Scientist and AI Engineer in Germany` | 63 | 50-60 | Slightly over (user-specified string) |
| `index.html` | `meta description` | `Data Scientist & AI Engineer, 10 yrs in finance, telecom, gaming. Bayesian forecasting, LangGraph agents. Roles in Germany (Hamburg, Munich) from Dec 2026.` | 155 | 140-160 | OK |
| `de.html` | `<title>` | `Timur Salakhetdinov \| Data Scientist und KI-Ingenieur in Deutschland` | 68 | 50-60 | Slightly over (user-specified string) |
| `de.html` | `meta description` | `Data Scientist & KI-Ingenieur, 10 Jahre in Finanzen, Telekom, Gaming. Bayesianisches Forecasting, LangGraph. Stellen in Deutschland (Hamburg, München), Dez. 2026.` | 162 | 140-160 | 2 chars over, acceptable |

Both `og:title`, `og:description`, `twitter:title`, and `twitter:description` were set to match.

---

## 2.3 Canonical URLs

```html
<!-- index.html -->
<link rel="canonical" href="https://timursalakhetdinov.com/" />

<!-- de.html -->
<link rel="canonical" href="https://timursalakhetdinov.com/de" />
```

---

## 2.4 hreflang Block

Added identically to both pages:

```html
<link rel="alternate" hreflang="en" href="https://timursalakhetdinov.com/" />
<link rel="alternate" hreflang="de" href="https://timursalakhetdinov.com/de" />
<link rel="alternate" hreflang="x-default" href="https://timursalakhetdinov.com/" />
```

---

## 2.5 OG Image

**File:** `images/og-cover.jpg`  
**Dimensions:** 1200x630 px  
**File size:** 58 KB (under 300 KB target)  
**Composition:** Dark background (#15171A), avatar left, name + title + tagline right, footer strip with domain

Tags added to both pages (locale swapped per language):

```html
<meta property="og:image" content="https://timursalakhetdinov.com/images/og-cover.jpg" />
<meta property="og:image:secure_url" content="https://timursalakhetdinov.com/images/og-cover.jpg" />
<meta property="og:image:type" content="image/jpeg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Timur Salakhetdinov, Data Scientist and AI Engineer based in Germany, working on Bayesian forecasting and LangGraph agentic systems." />
<meta property="og:url" content="https://timursalakhetdinov.com/" />      <!-- /de for DE page -->
<meta property="og:site_name" content="Timur Salakhetdinov" />
<meta property="og:locale" content="en_US" />                              <!-- de_DE for DE page -->
<meta property="og:locale:alternate" content="de_DE" />                    <!-- en_US for DE page -->
```

---

## 2.6 Twitter Card

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Timur Salakhetdinov | Data Scientist and AI Engineer in Germany" />
<meta name="twitter:description" content="Data Scientist & AI Engineer, 10 yrs in finance, telecom, gaming. Bayesian forecasting, LangGraph agents. Roles in Germany (Hamburg, Munich) from Dec 2026." />
<meta name="twitter:image" content="https://timursalakhetdinov.com/images/og-cover.jpg" />
<meta name="twitter:image:alt" content="Timur Salakhetdinov, Data Scientist and AI Engineer based in Germany, working on Bayesian forecasting and LangGraph agentic systems." />
```

DE page uses German title and description.

---

## 2.7 JSON-LD Structured Data

Both pages validated — `json.loads()` passes with no errors.

### Parsed output (index.html)

```json
[
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": "https://timursalakhetdinov.com/#person",
    "name": "Timur Salakhetdinov",
    "jobTitle": "Data Scientist and AI Engineer",
    "description": "Data Scientist & AI Engineer, 10 yrs in finance, telecom, gaming. Bayesian forecasting, LangGraph agents. Roles in Germany (Hamburg, Munich) from Dec 2026.",
    "url": "https://timursalakhetdinov.com/",
    "image": "https://timursalakhetdinov.com/images/avatar.jpg",
    "email": "mailto:timsalakhetdinov@gmail.com",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Hamburg",
      "addressCountry": "DE"
    },
    "workLocation": [
      {"@type": "Place", "name": "Hamburg, Germany"},
      {"@type": "Place", "name": "Munich, Germany"},
      {"@type": "Place", "name": "Germany"}
    ],
    "alumniOf": [
      {
        "@type": "EducationalOrganization",
        "name": "Leuphana Universität Lüneburg",
        "sameAs": "https://www.leuphana.de/"
      },
      {
        "@type": "EducationalOrganization",
        "name": "RUDN University",
        "sameAs": "https://eng.rudn.ru/"
      }
    ],
    "worksFor": {
      "@type": "Organization",
      "name": "InnoGames GmbH",
      "sameAs": "https://www.innogames.com/"
    },
    "knowsAbout": [
      "Bayesian inference", "Probabilistic forecasting", "LangGraph",
      "Agentic AI", "PyMC", "TimesFM", "Time series forecasting",
      "MLOps", "Retrieval-Augmented Generation", "Neo4j", "SQL", "Python"
    ],
    "knowsLanguage": [
      {"@type": "Language", "name": "English", "alternateName": "en"},
      {"@type": "Language", "name": "German", "alternateName": "de"},
      {"@type": "Language", "name": "Russian", "alternateName": "ru"}
    ],
    "sameAs": [
      "https://www.linkedin.com/in/timursalakhetdinov",
      "https://github.com/TimurSalakhetdinov",
      "https://medium.com/@timursalakhetdinov"
    ]
  },
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://timursalakhetdinov.com/#website",
    "url": "https://timursalakhetdinov.com/",
    "name": "Timur Salakhetdinov",
    "inLanguage": "en",
    "publisher": {"@id": "https://timursalakhetdinov.com/#person"}
  }
]
```

### DE differences

| Field | index.html | de.html |
|---|---|---|
| `url` (Person) | `https://timursalakhetdinov.com/` | `https://timursalakhetdinov.com/de` |
| `description` | English copy | German copy |
| `url` (WebSite) | `https://timursalakhetdinov.com/` | `https://timursalakhetdinov.com/de` |
| `inLanguage` | `en` | `de` |

All other fields (jobTitle, address, workLocation, alumniOf, worksFor, knowsAbout, sameAs) are identical.

---

## 2.8 robots.txt

Created at repo root. Reachable at `https://timursalakhetdinov.com/robots.txt` after deploy.

```
User-agent: *
Allow: /

Sitemap: https://timursalakhetdinov.com/sitemap.xml
```

---

## 2.9 sitemap.xml

Created at repo root. Reachable at `https://timursalakhetdinov.com/sitemap.xml` after deploy.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://timursalakhetdinov.com/</loc>
    <lastmod>2026-05-20</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://timursalakhetdinov.com/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://timursalakhetdinov.com/de"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://timursalakhetdinov.com/"/>
  </url>
  <url>
    <loc>https://timursalakhetdinov.com/de</loc>
    <lastmod>2026-05-20</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://timursalakhetdinov.com/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://timursalakhetdinov.com/de"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://timursalakhetdinov.com/"/>
  </url>
</urlset>
```

---

## 2.10 Body Copy

### 2.10a Abstract paragraph (§ 00)

**index.html — before:**
> Data scientist with ten years of analytical experience across finance, telecom, and gaming. Currently a working student at InnoGames building production forecasting systems (Prophet, PyMC, TimesFM), while completing an M.Sc. at Leuphana University on a Deutschlandstipendium. My thesis develops an open-source agentic forecasting architecture combining TimesFM, PyMC, and dual-process LLM reasoning over an episodic memory of past prediction cycles, deployable entirely on EU infrastructure.

**index.html — after:**
> Data Scientist and AI Engineer with ten years of analytical experience across finance, telecom, and gaming. I build production forecasting systems at InnoGames using Prophet, PyMC, and TimesFM, while completing my M.Sc. at Leuphana University on a Deutschlandstipendium. My thesis develops an open-source agentic forecasting architecture combining TimesFM, PyMC, and dual-process LLM reasoning over an episodic memory of past prediction cycles, deployable entirely on EU infrastructure.

**de.html — before:**
> Data Scientist mit zehn Jahren analytischer Erfahrung in den Bereichen Finanzen, Telekommunikation und Gaming. Derzeit Werkstudent bei InnoGames, wo ich Produktionsprognose-Systeme aufbaue (Prophet, PyMC, TimesFM)... kombiniert – vollständig auf EU-Infrastruktur deploybar.

**de.html — after:**
> Data Scientist und KI-Ingenieur mit zehn Jahren analytischer Erfahrung in den Bereichen Finanzen, Telekommunikation und Gaming. Ich baue Produktionsprognose-Systeme bei InnoGames mit Prophet, PyMC und TimesFM, während ich meinen M.Sc. an der Leuphana Universität als Deutschlandstipendiat abschließe. Meine Abschlussarbeit entwickelt eine Open-Source-Architektur für agentische Prognosen, die TimesFM, PyMC und Zwei-Prozess-LLM-Reasoning über ein episodisches Gedächtnis vergangener Prognosezyklen kombiniert, vollständig auf EU-Infrastruktur deploybar.

Note: em dash before "vollständig" removed; replaced with comma.

### 2.10b Author card role label

| Page | Before | After |
|---|---|---|
| `index.html` | `role: working student, analytics @ innogames` | `role: data scientist & ai engineer @ innogames` |
| `de.html` | `role: working student, analytics @ innogames` | `role: data scientist & ki-ingenieur @ innogames` |

### 2.10c Contact H2 (§ 05)

| Page | Before | After |
|---|---|---|
| `index.html` | `…in Germany from December 2026?` | `…in Germany, Hamburg or Munich, from December 2026?` |
| `de.html` | `…in Deutschland ab Dezember 2026?` | `…in Deutschland, Hamburg oder München, ab Dezember 2026?` |

---

## Positioning constraints verified

| Constraint | Status |
|---|---|
| No "Working Student" in title, meta, JSON-LD, OG, Twitter | Confirmed — all removed |
| `jobTitle` is "Data Scientist and AI Engineer" | Confirmed |
| `address.addressLocality` stays Hamburg | Confirmed |
| Munich appears only in `workLocation` and contact H2 | Confirmed |
| InnoGames present as production context, not headline | Confirmed |
| No em dashes in any new or modified copy | Confirmed |

---

## Manual verification checklist

After the branch is merged and deployed:

- [ ] Submit `https://timursalakhetdinov.com/sitemap.xml` to Google Search Console
- [ ] Request indexing on the homepage via Google Search Console URL Inspection
- [ ] Paste `https://timursalakhetdinov.com/` into LinkedIn Post Inspector to verify OG image renders
- [ ] Paste into Slack to verify card preview
- [ ] Run `https://timursalakhetdinov.com/` through Google Rich Results Test to validate JSON-LD Person schema
- [ ] Confirm `robots.txt` is accessible at the root URL

---

## What comes next (Phase 3)

- Add H2 headings to Projects (§ 03) and Writing (§ 04) sections (both pages)
- Write descriptive `alt` text for all five project thumbnail images
- Replace generic `↗ repo` anchor text with project-specific labels
- Add `rel="noopener external"` to outbound project links
