---
title: Example article (not published)
date: 2026-01-15
description: A draft that shows the writing format. The leading underscore keeps it out of the build.
slug: _example
tags:
  - example
  - drafting
og_image: /images/og-cover-v5.jpg
substack_url: https://example.substack.com/p/example
---

This file is a draft. `scripts/build_writing.py` ignores every Markdown file in `content/writing/` whose name starts with an underscore, so this page is never written to `writing/`.

Inline math sits in a sentence, $E = mc^2$, and display math is its own block:

$$
\mathrm{MASE} = \frac{\mathrm{MAE}}{\mathrm{MAE}_{\text{naive}}}
$$

A fenced block names its language so Pygments can highlight it:

```python
def reading_time(words: int) -> int:
    return max(1, round(words / 220))
```

Images for a published article `my-note.md` live in `content/writing/my-note/` and are referenced as `my-note/figure.png`.
