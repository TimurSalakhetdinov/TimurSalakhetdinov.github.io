# Writing sources

Markdown articles for the site live in this directory. `scripts/build_writing.py` turns them into static pages under `writing/`.

## File layout

- One article: `content/writing/<slug>.md`
- Images for that article: `content/writing/<slug>/` (png, jpg, jpeg, gif, webp, svg, avif)
- Drafts and notes: any `.md` file whose name starts with `_` is ignored. `README.md` is ignored too.

`content/writing/_example.md` is a format sample. The leading underscore keeps it out of the build, so it is never published.

## Front matter

Every article starts with YAML front matter:

```yaml
---
title: Article title
date: 2026-10-26
description: One or two sentences for the list page, meta description, and RSS item.
slug: article-title
tags:
  - forecasting
  - agents
og_image: /images/og-cover-v5.jpg
substack_url: https://example.substack.com/p/article-title
---
```

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Plain text. |
| `date` | yes | `YYYY-MM-DD`. Newest articles are listed first. |
| `description` | yes | Plain text. |
| `slug` | yes | Must match the filename. Published slugs are lowercase letters, numbers, and hyphens. |
| `tags` | yes | YAML list. May be empty. |
| `og_image` | no | Absolute `https` URL or a site path such as `/images/og-cover-v5.jpg`. If omitted, the site preview image is used. |
| `substack_url` | no | `http` or `https` URL. Adds an “Also on Substack” link. |

Unknown keys are a build error, so a typo is not silently dropped.

## Markdown

- Fenced code blocks with a language tag, for example `` ```python ``. Highlighting uses Pygments.
- Inline math: `$...$`. No space immediately after the opening `$` or immediately before the closing `$`.
- Display math: `$$...$$`, on its own or inside a paragraph.
- A dollar sign that is not math can be escaped as `\$`.
- Images are referenced relative to this directory: `![Chart](my-note/chart.png)`. A bare filename that exists in `content/writing/<slug>/`, such as `chart.png`, is rewritten to `my-note/chart.png`. The build copies those files to `writing/<slug>/`.

## Build

From the repository root:

```bash
python3 -m pip install -r scripts/requirements-writing.txt
python3 scripts/build_writing.py
```

The script writes `writing/index.html`, one `writing/<slug>.html` per article, `writing/feed.xml`, and the Pygments stylesheet `assets/css/pygments.css`. It inserts or updates only the `/writing/` entries in `sitemap.xml`. It also fills the homepage Writing block in `index.html` and `de.html`. That block stays hidden until an article is published, then shows the newest three (`HOME_LATEST_COUNT`) as cards and points the nav link at `#writing`. Running it again with the same sources changes nothing.

`writing/` is generated. Edit the Markdown sources, then run the script again.
