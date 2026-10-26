#!/usr/bin/env python3
"""Build the Writing section from content/writing/*.md.

Reads every Markdown file in content/writing/ except README.md and names that
start with an underscore. Writes writing/index.html, writing/<slug>.html,
writing/feed.xml, assets/css/pygments.css, and inserts or updates only the
/writing/ entries in sitemap.xml. Refreshes the homepage Writing block in
index.html and de.html, and the data-writing-nav href on every page that
carries the nav. A second run with the same sources writes identical bytes.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.sax.saxutils import escape as xml_escape

import markdown
import yaml
from markdown.extensions.codehilite import CodeHiliteExtension
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "writing"
OUT = ROOT / "writing"
SITEMAP = ROOT / "sitemap.xml"
PYGMENTS_CSS = ROOT / "assets" / "css" / "pygments.css"

SITE = "https://timursalakhetdinov.com"
DEFAULT_OG_IMAGE = f"{SITE}/images/og-cover-v5.jpg"
DEFAULT_OG_ALT = (
    "Social preview card with a portrait of Timur Salakhetdinov, "
    "Data Scientist & Data Analyst."
)
DEFAULT_OG_WIDTH = "2400"
DEFAULT_OG_HEIGHT = "1260"
# lastmod for /writing/ when no article has been published yet.
SECTION_INTRODUCED = "2026-10-26"
# Newest published articles rendered on the homepages.
HOME_LATEST_COUNT = 3
WRITING_BLURB = (
    "Public notes on LLM agent systems, applied machine learning, and "
    "time-series forecasting, from a data scientist and data analyst in Germany."
)
WORDS_PER_MINUTE = 220
AUTHOR = "Timur Salakhetdinov"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DRAFT_SLUG_RE = re.compile(r"^_[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_KEYS = ("title", "date", "description", "slug", "tags")
OPTIONAL_KEYS = ("og_image", "substack_url", "updated", "related_projects")
ALLOWED_KEYS = set(REQUIRED_KEYS) | set(OPTIONAL_KEYS)

FENCE_RE = re.compile(r"^(`{3,}|~{3,})[^\n]*\n.*?\n\1[ \t]*$", re.M | re.S)
INLINE_CODE_RE = re.compile(r"``[^`\n]+``|`[^`\n]+`")
DISPLAY_MATH_RE = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", re.S)
INLINE_MATH_RE = re.compile(
    r"(?<!\\)\$(?!\$|\s)((?:\\.|[^$\n\\])+?)(?<!\s)(?<!\\)\$(?!\$)"
)
URL_BLOCK_RE = re.compile(r"[ \t]*<url\b[^>]*>.*?</url>[ \t]*\n?", re.S)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.I)
SRC_ATTR_RE = re.compile(r"""\bsrc\s*=\s*(['"])(.*?)\1""", re.I)
CSS_URL_RE = re.compile(r"url\(\s*([^)]+?)\s*\)")

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
DE_MONTHS = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]
HOME_BLOCK_RE = re.compile(
    r"<!-- writing:latest:start -->.*?<!-- writing:latest:end -->",
    re.S,
)
NAV_ANCHOR_RE = re.compile(r"<a\b[^>]*\bdata-writing-nav\b[^>]*>")
HOME_PAGES = (
    (ROOT / "index.html", "en"),
    (ROOT / "de.html", "de"),
)
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
RSS_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

ORIGIN_TRIAL = (
    '<meta http-equiv="origin-trial" content="Amx40mtg9rixjk+HmaGAs5WOyScpWMKhqdbzpkt9TX93eQ3TwGCIV31nFpphHKJfmIZTin0Xoh80xBmrfHZMIw8AAABWeyJvcmlnaW4iOiJodHRwczovL3RpbXVyc2FsYWtoZXRkaW5vdi5jb206NDQzIiwiZmVhdHVyZSI6IldlYk1DUCIsImV4cGlyeSI6MTgwNjM2NDgwMH0=">'
    '<script src="/assets/js/webmcp.js" defer></script>'
)
RSS_LINK = (
    '<link rel="alternate" type="application/rss+xml" '
    'title="Timur Salakhetdinov — Writing" href="/writing/feed.xml">'
)


class WritingStyle(Style):
    """Muted palette aligned with the site ink and accent colours."""

    background_color = "#fbfbf9"
    default_style = "#202426"
    styles = {
        Comment: "italic #626b71",
        Keyword: "#075593",
        Name.Function: "#075593",
        Name.Class: "#075593",
        Name.Builtin: "#075593",
        String: "#3f5c45",
        Number: "#075593",
        Operator: "#485159",
        Operator.Word: "#075593",
        Punctuation: "#485159",
    }


@dataclass(frozen=True)
class Article:
    path: Path
    title: str
    date: date
    description: str
    slug: str
    tags: tuple[str, ...]
    og_image: str | None
    substack_url: str | None
    updated: date | None
    related_projects: tuple[str, ...]
    body: str
    html: str
    words: int
    minutes: int
    has_math: bool

    @property
    def url(self) -> str:
        return f"{SITE}/writing/{self.slug}.html"

    @property
    def iso_date(self) -> str:
        return self.date.isoformat()

    @property
    def modified(self) -> date:
        return self.updated or self.date

    @property
    def iso_modified(self) -> str:
        return self.modified.isoformat()


def main() -> None:
    if not CONTENT.is_dir():
        raise SystemExit(f"missing source directory: {CONTENT}")
    articles = load_articles()
    write_pygments_css()
    OUT.mkdir(parents=True, exist_ok=True)
    for article in articles:
        sync_images(article)
        page = render_article(article)
        write_if_changed(OUT / f"{article.slug}.html", page)
    write_if_changed(OUT / "index.html", render_index(articles))
    write_if_changed(OUT / "feed.xml", render_feed(articles))
    remove_stale(articles)
    update_sitemap(articles)
    update_home_latest(articles)
    update_nav_hrefs(bool(articles))
    check_outputs(articles)
    print(f"writing: {len(articles)} article(s)")


def load_articles() -> list[Article]:
    articles: list[Article] = []
    for path in sorted(CONTENT.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        draft = path.name.startswith("_")
        article = parse_article(path, draft=draft)
        if article is not None:
            articles.append(article)
    articles.sort(key=lambda article: (-article.date.toordinal(), article.slug))
    slugs = [article.slug for article in articles]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("duplicate article slugs")
    return articles


def parse_article(path: Path, *, draft: bool) -> Article | None:
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.startswith("---"):
        raise SystemExit(f"{path}: file must start with YAML front matter")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{path}: front matter is not closed")
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise SystemExit(f"{path}: invalid YAML front matter ({exc})") from exc
    if not isinstance(meta, dict):
        raise SystemExit(f"{path}: front matter must be a mapping")
    unknown = sorted(set(meta) - ALLOWED_KEYS)
    if unknown:
        raise SystemExit(f"{path}: unknown front matter keys: {', '.join(unknown)}")
    missing = [key for key in REQUIRED_KEYS if key not in meta]
    if missing:
        raise SystemExit(f"{path}: missing front matter keys: {', '.join(missing)}")

    title = require_text(path, "title", meta["title"])
    description = require_text(path, "description", meta["description"])
    slug = require_text(path, "slug", meta["slug"])
    if slug != path.stem:
        raise SystemExit(f"{path}: slug {slug!r} does not match filename {path.stem!r}")
    pattern = DRAFT_SLUG_RE if draft else SLUG_RE
    if not pattern.fullmatch(slug):
        raise SystemExit(f"{path}: slug {slug!r} is not a lowercase hyphenated name")
    try:
        published = as_date(meta["date"])
    except ValueError as exc:
        raise SystemExit(f"{path}: date must be YYYY-MM-DD") from exc
    tags = parse_tags(path, meta["tags"])
    og_image = optional_text(path, "og_image", meta.get("og_image"))
    substack = optional_text(path, "substack_url", meta.get("substack_url"))
    if "updated" in meta and meta.get("updated") is not None:
        try:
            updated = as_date(meta["updated"])
        except ValueError as exc:
            raise SystemExit(f"{path}: updated must be YYYY-MM-DD") from exc
    else:
        updated = None
    related = parse_related(path, meta.get("related_projects"))
    if substack and urlsplit(substack).scheme not in {"http", "https"}:
        raise SystemExit(f"{path}: substack_url must be an http(s) URL")
    if og_image:
        check_og_image(path, og_image)
    if draft:
        return None

    body = parts[2].lstrip("\n")
    rendered, has_math = render_markdown(body)
    rendered = rewrite_images(path, slug, rendered)
    words = count_words(body)
    minutes = max(1, -(-words // WORDS_PER_MINUTE)) if words else 1
    return Article(
        path=path,
        title=title,
        date=published,
        description=description,
        slug=slug,
        tags=tags,
        og_image=og_image,
        substack_url=substack,
        updated=updated,
        related_projects=related,
        body=body,
        html=rendered,
        words=words,
        minutes=minutes,
        has_math=has_math,
    )


def require_text(path: Path, key: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{path}: {key} must be a non-empty string")
    return value.strip()


def optional_text(path: Path, key: str, value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{path}: {key} must be a non-empty string when set")
    return value.strip()


def parse_related(path: Path, value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise SystemExit(f"{path}: related_projects must be a list of site paths")
    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise SystemExit(f"{path}: each related_projects entry must be a site path")
        raw = item.strip()
        if "://" in raw or raw.startswith("//"):
            raise SystemExit(f"{path}: related_projects entries must be site paths, not URLs")
        if not raw.startswith("/"):
            raw = "/" + raw
        target = map_site_path(urlsplit(raw).path)
        if not target.is_file():
            raise SystemExit(f"{path}: related project not found: {raw}")
        items.append(raw.split("#", 1)[0])
    return tuple(items)


def project_link_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.S | re.I)
    if not match:
        return path.stem.replace("-", " ")
    title = re.sub(r"<[^>]+>", "", match.group(1))
    return html.unescape(re.sub(r"\s+", " ", title)).strip()


def parse_tags(path: Path, value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise SystemExit(f"{path}: tags must be a list")
    tags: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise SystemExit(f"{path}: each tag must be a non-empty string")
        tags.append(item.strip())
    return tuple(tags)


def as_date(value: object) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return date.fromisoformat(value)
    raise ValueError(str(value))


def check_og_image(path: Path, og_image: str) -> None:
    local = local_site_path(og_image)
    if local is not None and not local.is_file():
        raise SystemExit(f"{path}: og_image does not exist: {og_image}")


def local_site_path(url: str) -> Path | None:
    if url.startswith(SITE + "/"):
        url = url[len(SITE):]
    elif url.startswith(SITE):
        url = "/"
    if not url.startswith("/"):
        return None
    path = unquote(urlsplit(url).path)
    return ROOT / path.lstrip("/")


def shield_code(text: str) -> tuple[str, list[str]]:
    chunks: list[str] = []

    def hold(match: re.Match[str]) -> str:
        chunks.append(match.group(0))
        return f"CODEHOLD{len(chunks) - 1}ENDHOLD"

    shielded = FENCE_RE.sub(hold, text)
    shielded = INLINE_CODE_RE.sub(hold, shielded)
    return shielded, chunks


def restore_code(text: str, chunks: list[str]) -> str:
    def restore(match: re.Match[str]) -> str:
        return chunks[int(match.group(1))]

    return re.sub(r"CODEHOLD(\d+)ENDHOLD", restore, text)


def render_markdown(body: str) -> tuple[str, bool]:
    shielded, chunks = shield_code(body)
    display: list[tuple[str, str]] = []
    inline: list[tuple[str, str]] = []

    def hold_display(match: re.Match[str]) -> str:
        latex = match.group(1)
        if latex.startswith("\n"):
            latex = latex[1:]
        if latex.endswith("\n"):
            latex = latex[:-1]
        token = f"MATHBLOCK{len(display)}PLACEHOLDER"
        display.append((token, latex))
        return token

    def hold_inline(match: re.Match[str]) -> str:
        token = f"MATHINLINE{len(inline)}PLACEHOLDER"
        inline.append((token, match.group(1)))
        return token

    shielded = DISPLAY_MATH_RE.sub(hold_display, shielded)
    shielded = INLINE_MATH_RE.sub(hold_inline, shielded)
    dollars: list[str] = []

    def hold_dollar(_match: re.Match[str]) -> str:
        token = f"DOLLAR{len(dollars)}PLACEHOLDER"
        dollars.append(token)
        return token

    shielded = re.sub(r"\\\$", hold_dollar, shielded)
    restored = restore_code(shielded, chunks)
    rendered = markdown.markdown(
        restored,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.sane_lists",
            CodeHiliteExtension(css_class="highlight", linenums=False, guess_lang=False),
        ],
        output_format="html",
    )
    for token, latex in display:
        block = f'<div class="math math-display">$${html.escape(latex)}$$</div>'
        inline_block = f'<span class="math math-display">$${html.escape(latex)}$$</span>'
        rendered, count = re.subn(
            rf"<p>\s*{re.escape(token)}\s*</p>",
            lambda _match, block=block: block,
            rendered,
            count=1,
        )
        if count == 0:
            rendered = rendered.replace(token, inline_block, 1)
        elif token in rendered:
            rendered = rendered.replace(token, inline_block)
    for token, latex in inline:
        span = f'<span class="math math-inline">${html.escape(latex)}$</span>'
        if token not in rendered:
            raise SystemExit("math placeholder was dropped while rendering Markdown")
        rendered = rendered.replace(token, span)
    for token in dollars:
        if token not in rendered:
            raise SystemExit("escaped dollar placeholder was dropped while rendering Markdown")
        rendered = rendered.replace(token, "$")
    if re.search(r"(?:MATHBLOCK|MATHINLINE|DOLLAR)\d+PLACEHOLDER|CODEHOLD\d+ENDHOLD", rendered):
        raise SystemExit("a build placeholder survived Markdown rendering")
    return rendered, bool(display or inline)


def count_words(body: str) -> int:
    shielded, _chunks = shield_code(body)
    text = re.sub(r"CODEHOLD\d+ENDHOLD", " ", shielded)
    text = DISPLAY_MATH_RE.sub(" ", text)
    text = INLINE_MATH_RE.sub(" ", text)
    return len(re.findall(r"[0-9A-Za-z]+(?:'[A-Za-z]+)?", text))


def rewrite_images(path: Path, slug: str, rendered: str) -> str:
    seen = 0

    def replace_tag(match: re.Match[str]) -> str:
        nonlocal seen
        tag = match.group(0)
        src_match = SRC_ATTR_RE.search(tag)
        if not src_match:
            return tag
        src = src_match.group(2)
        new_src, local = locate_image(path, slug, src)
        if new_src != src:
            start, end = src_match.span(2)
            tag = tag[:start] + new_src + tag[end:]
        attrs = ""
        if local is not None:
            width, height = image_size(local)
            attrs += f' width="{width}" height="{height}"'
        if seen > 0:
            attrs += ' loading="lazy" decoding="async"'
        seen += 1
        if not attrs:
            return tag
        if tag.endswith("/>"):
            return tag[:-2].rstrip() + attrs + " />"
        return tag[:-1].rstrip() + attrs + ">"

    return IMG_TAG_RE.sub(replace_tag, rendered)


def locate_image(path: Path, slug: str, src: str) -> tuple[str, Path | None]:
    split = urlsplit(src)
    if split.scheme or src.startswith("//"):
        return src, None
    if src.startswith("/") or src.startswith("#"):
        local = None
        if src.startswith("/"):
            candidate = map_site_path(split.path)
            if candidate.is_file() and candidate.suffix.lower() in IMAGE_EXTENSIONS:
                local = candidate
        return src, local
    published = resolve_image_src(path, slug, src)
    raw_path = unquote(urlsplit(published).path)
    rel = Path(raw_path)
    source_root = CONTENT / slug
    if rel.parts and rel.parts[0] == slug:
        local = source_root.joinpath(*rel.parts[1:])
    else:
        local = source_root / rel
    return published, local


def image_size(path: Path) -> tuple[int, int]:
    if path.suffix.lower() == ".svg":
        text = path.read_text(encoding="utf-8", errors="replace")
        width = re.search(r'\bwidth\s*=\s*["\'](\d+(?:\.\d+)?)', text)
        height = re.search(r'\bheight\s*=\s*["\'](\d+(?:\.\d+)?)', text)
        if width and height:
            return int(float(width.group(1))), int(float(height.group(1)))
        viewbox = re.search(
            r'\bviewBox\s*=\s*["\']\s*[-\d.]+\s+[-\d.]+\s+([-\d.]+)\s+([-\d.]+)',
            text,
        )
        if not viewbox:
            raise SystemExit(f"{path}: SVG has no width/height or viewBox")
        return int(float(viewbox.group(1))), int(float(viewbox.group(2)))
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Pillow is required to read article image sizes") from exc
    with Image.open(path) as image:
        width, height = image.size
    if width < 1 or height < 1:
        raise SystemExit(f"{path}: image dimensions are unusable")
    return width, height


def resolve_image_src(path: Path, slug: str, src: str) -> str:
    split = urlsplit(src)
    if split.scheme or src.startswith("//") or src.startswith("/") or src.startswith("#"):
        return src
    raw_path = unquote(split.path)
    rel = Path(raw_path)
    if not raw_path or rel.is_absolute() or ".." in rel.parts:
        raise SystemExit(f"{path}: invalid image path {src!r}")
    source_root = CONTENT / slug
    if rel.parts and rel.parts[0] == slug:
        filesystem_path = source_root.joinpath(*rel.parts[1:])
        published = rel.as_posix()
    else:
        filesystem_path = source_root / rel
        published = Path(slug, rel).as_posix()
    if not filesystem_path.is_file():
        raise SystemExit(f"{path}: image not found for {src!r} (looked in {filesystem_path})")
    suffix = ""
    if split.query:
        suffix += "?" + split.query
    if split.fragment:
        suffix += "#" + split.fragment
    return published + suffix


def sync_images(article: Article) -> None:
    source = CONTENT / article.slug
    dest = OUT / article.slug
    if not source.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        return
    dest.mkdir(parents=True, exist_ok=True)
    keep: set[Path] = set()
    for path in source.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if any(part.startswith(".") for part in path.relative_to(source).parts):
            continue
        relative = path.relative_to(source)
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        if not target.exists() or target.read_bytes() != data:
            target.write_bytes(data)
        keep.add(target.resolve())
    for path in list(dest.rglob("*")):
        if path.is_file() and path.resolve() not in keep:
            path.unlink()
    for path in sorted((p for p in dest.rglob("*") if p.is_dir()), key=lambda item: len(item.parts), reverse=True):
        if not any(path.iterdir()):
            path.rmdir()
    if dest.exists() and not any(dest.rglob("*")):
        dest.rmdir()


def remove_stale(articles: list[Article]) -> None:
    keep_files = {"index.html", "feed.xml", *(f"{article.slug}.html" for article in articles)}
    keep_dirs = {article.slug for article in articles}
    if not OUT.exists():
        return
    for child in OUT.iterdir():
        if child.name.startswith("."):
            continue
        if child.is_file() and child.name not in keep_files:
            child.unlink()
        elif child.is_dir() and child.name not in keep_dirs:
            shutil.rmtree(child)


def render_index(articles: list[Article]) -> str:
    if articles:
        items = ["  <ul class=\"archive-list\">"]
        for article in articles:
            tags = ""
            if article.tags:
                labels = "".join(f"<span>{escape(tag)}</span>" for tag in article.tags)
                tags = f"""
          <div class="archive-footer">
            <div class="archive-tags">{labels}</div>
          </div>"""
            items.append(
                f"""    <li>
      <a class="archive-item" href="/writing/{escape(article.slug)}.html">
        <div class="archive-meta">
          <time datetime="{article.iso_date}">{format_date(article.date)}</time>
          <span>{article.minutes} min read</span>
        </div>
        <h2 class="archive-title">{escape(article.title)}</h2>
        <p class="archive-desc">{escape(article.description)}</p>{tags}
      </a>
    </li>"""
            )
        items.append("  </ul>")
        body = "\n".join(items)
    else:
        body = f'  <p class="writing-empty">{escape(WRITING_BLURB)} First articles coming soon.</p>'

    description = WRITING_BLURB
    title = "Writing: LLM agents and forecasting | Timur Salakhetdinov"
    canonical = f"{SITE}/writing/"
    item_list = []
    for position, article in enumerate(articles, start=1):
        item_list.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": article.title,
                "url": article.url,
            }
        )
    collection: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": canonical,
        "inLanguage": "en",
        "isPartOf": {
            "@type": "WebSite",
            "name": AUTHOR,
            "url": f"{SITE}/",
        },
    }
    if item_list:
        collection["mainEntity"] = {"@type": "ItemList", "itemListElement": item_list}
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Writing", "item": canonical},
        ],
    }
    main = f"""<main>
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <a href="/">Home</a>
    <span aria-hidden="true">/</span>
    <span aria-current="page">Writing</span>
  </nav>

  <p class="eyebrow">§ 04 · Articles</p>
  <h1>Writing</h1>
  <p class="summary">{escape(description)}</p>
{body}

  <p class="source"><a href="/">← Back to portfolio home</a> · <a href="/writing/feed.xml">RSS</a></p>
</main>"""
    return render_page(
        title=title,
        description=description,
        canonical=canonical,
        og_type="website",
        og_title=title,
        og_description=description,
        og_image=DEFAULT_OG_IMAGE,
        writing_current=True,
        json_ld=[collection, breadcrumb],
        main=main,
        extra_head="",
        extra_scripts="",
        has_articles=bool(articles),
    )


def render_article(article: Article) -> str:
    og_image = absolute_url(article.og_image) if article.og_image else DEFAULT_OG_IMAGE
    using_default = og_image == DEFAULT_OG_IMAGE
    og_alt = DEFAULT_OG_ALT if using_default else article.title
    title = f"{article.title} | {AUTHOR}"
    tags = ""
    if article.tags:
        labels = "".join(f"<span>{escape(tag)}</span>" for tag in article.tags)
        tags = f'\n  <div class="tags">{labels}</div>'
    substack = ""
    if article.substack_url:
        substack = (
            '\n  <p class="substack"><a href="'
            + escape(article.substack_url)
            + '" target="_blank" rel="noopener noreferrer">Also on Substack</a></p>'
        )
    extra_head = '\n  <link rel="stylesheet" href="/assets/css/pygments.css">'
    if article.has_math:
        extra_head += '\n  <link rel="stylesheet" href="/assets/katex/katex.min.css">'
    extra_scripts = ""
    if article.has_math:
        extra_scripts = """
<script src="/assets/katex/katex.min.js"></script>
<script src="/assets/katex/auto-render.min.js"></script>
<script>
  (function () {
    var root = document.querySelector(".prose");
    if (!root || typeof renderMathInElement !== "function") return;
    renderMathInElement(root, {
      delimiters: [
        {left: "$$", right: "$$", display: true},
        {left: "$", right: "$", display: false}
      ],
      throwOnError: false
    });
  })();
</script>"""
    article_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": article.title,
        "description": article.description,
        "url": article.url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": article.url},
        "datePublished": article.iso_date,
        "dateModified": article.iso_modified,
        "inLanguage": "en",
        "image": og_image,
        "author": {
            "@type": "Person",
            "name": AUTHOR,
            "url": f"{SITE}/",
        },
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Writing", "item": f"{SITE}/writing/"},
            {"@type": "ListItem", "position": 3, "name": article.title, "item": article.url},
        ],
    }
    image_meta = ""
    if using_default:
        image_meta = f"""
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="{DEFAULT_OG_WIDTH}">
  <meta property="og:image:height" content="{DEFAULT_OG_HEIGHT}">"""
    main = f"""<main>
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <a href="/">Home</a>
    <span aria-hidden="true">/</span>
    <a href="/writing/">Writing</a>
    <span aria-hidden="true">/</span>
    <span aria-current="page">{escape(article.title)}</span>
  </nav>
  <p class="eyebrow"><time datetime="{article.iso_date}">{format_date(article.date)}</time> · {article.minutes} min read</p>
  <h1>{escape(article.title)}</h1>
  <p class="summary">{escape(article.description)}</p>{tags}{substack}
  <div class="prose">
{article.html}
  </div>{render_related(article)}
  <p class="source"><a href="/">Home</a> · <a href="/writing/">All writing</a></p>
</main>"""
    return render_page(
        title=title,
        description=article.description,
        canonical=article.url,
        og_type="article",
        og_title=article.title,
        og_description=article.description,
        og_image=og_image,
        og_alt=og_alt,
        image_meta=image_meta,
        published=article.iso_date,
        writing_current=False,
        has_articles=True,
        json_ld=[article_ld, breadcrumb],
        main=main,
        extra_head=extra_head,
        extra_scripts=extra_scripts,
    )


def render_related(article: Article) -> str:
    if not article.related_projects:
        return ""
    items = []
    for href in article.related_projects:
        title = project_link_title(map_site_path(urlsplit(href).path))
        items.append(f'    <li><a href="{escape(href)}">{escape(title)}</a></li>')
    body = "\n".join(items)
    return f"""
  <section class="related">
    <h2>Related projects</h2>
    <ul>
{body}
    </ul>
  </section>"""


def render_page(
    *,
    title: str,
    description: str,
    canonical: str,
    og_type: str,
    og_title: str,
    og_description: str,
    og_image: str,
    main: str,
    json_ld: list[dict[str, object]],
    extra_head: str,
    extra_scripts: str,
    writing_current: bool,
    has_articles: bool,
    og_alt: str = DEFAULT_OG_ALT,
    image_meta: str = "",
    published: str | None = None,
) -> str:
    # Writing pages use the English project-page form: /#writing once the
    # homepage block exists, /writing/ while it is hidden.
    writing_href = "/#writing" if has_articles else "/writing/"
    current = ' aria-current="page"' if writing_current and not has_articles else ""
    published_meta = ""
    if published:
        published_meta = f'\n  <meta property="article:published_time" content="{escape(published)}">'
    if not image_meta and og_image == DEFAULT_OG_IMAGE:
        image_meta = f"""
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="{DEFAULT_OG_WIDTH}">
  <meta property="og:image:height" content="{DEFAULT_OG_HEIGHT}">"""
    ld_blocks = "\n".join(
        f'  <script type="application/ld+json">\n{json_script(block)}\n  </script>'
        for block in json_ld
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{escape(canonical)}">
  {RSS_LINK}

  <meta property="og:type" content="{escape(og_type)}">
  <meta property="og:site_name" content="{escape(AUTHOR)}">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{escape(og_title)}">
  <meta property="og:description" content="{escape(og_description)}">
  <meta property="og:url" content="{escape(canonical)}">
  <meta property="og:image" content="{escape(og_image)}">
  <meta property="og:image:secure_url" content="{escape(og_image)}">
  <meta property="og:image:alt" content="{escape(og_alt)}">{image_meta}{published_meta}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(og_title)}">
  <meta name="twitter:description" content="{escape(og_description)}">
  <meta name="twitter:image" content="{escape(og_image)}">
  <meta name="twitter:image:alt" content="{escape(og_alt)}">
  <meta name="author" content="{escape(AUTHOR)}">

  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/assets/css/project.css">
  <link rel="stylesheet" href="/assets/css/writing.css">{extra_head}

{ld_blocks}
  {ORIGIN_TRIAL}
</head>
<body>
<header class="nav">
  <a class="nav-brand" href="/" aria-label="Timur Salakhetdinov, homepage">
    <div class="nav-mark">ts</div>
    <span class="nav-name">Timur Salakhetdinov</span>
    <span class="nav-role">/ data scientist · data analyst</span>
  </a>
  <nav aria-label="Sections">
    <ul class="nav-links" id="navLinks">
      <li><a href="/#about"><span class="nav-num">§01</span><span>About</span></a></li>
      <li><a href="/#skills"><span class="nav-num">§02</span><span>Skills</span></a></li>
      <li><a href="/projects/"><span class="nav-num">§03</span><span>Projects</span></a></li>
      <li><a href="{writing_href}" data-writing-nav{current}><span class="nav-num">§04</span><span>Writing</span></a></li>
      <li><a href="/#contact"><span class="nav-num">§05</span><span>Contact</span></a></li>
    </ul>
  </nav>
  <div class="nav-right">
    <div class="lang-toggle">
      <span class="lang-active">EN</span>
      <span class="lang-sep">·</span>
      <a href="/de" hreflang="de">DE</a>
    </div>
    <div class="nav-status">
      <span class="nav-dot"></span>
      <span>available from Apr 2027 · Germany</span>
    </div>
    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks" aria-label="Toggle navigation menu" data-menu-text="Menu" data-close-text="Close">
      <span class="nav-toggle-icon" aria-hidden="true">
        <span></span><span></span>
      </span>
      <span class="nav-toggle-label">Menu</span>
    </button>
  </div>
</header>
{main}
<footer>
  <span>© Timur Salakhetdinov</span>
  <a href="/#contact">Contact</a>
  <a href="/imprint.html">Imprint</a>
  <a href="/privacy.html">Privacy</a>
</footer>
<script src="/assets/js/site-nav.js" defer></script>{extra_scripts}
<script data-goatcounter="https://timursalakhetdinov.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""


def render_feed(articles: list[Article]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        "  <channel>",
        "    <title>Timur Salakhetdinov — Writing</title>",
        f"    <link>{SITE}/writing/</link>",
        "    <description>Articles by Timur Salakhetdinov.</description>",
        "    <language>en</language>",
    ]
    if articles:
        lines.append(f"    <lastBuildDate>{rfc822(articles[0].date)}</lastBuildDate>")
    for article in articles:
        lines.extend(
            [
                "    <item>",
                f"      <title>{xml_text(article.title)}</title>",
                f"      <link>{article.url}</link>",
                f'      <guid isPermaLink="true">{article.url}</guid>',
                f"      <pubDate>{rfc822(article.date)}</pubDate>",
                f"      <description>{xml_text(article.description)}</description>",
            ]
        )
        for tag in article.tags:
            lines.append(f"      <category>{xml_text(tag)}</category>")
        lines.append("    </item>")
    lines.extend(["  </channel>", "</rss>", ""])
    return "\n".join(lines)


def update_sitemap(articles: list[Article]) -> None:
    if not SITEMAP.is_file():
        raise SystemExit(f"missing sitemap: {SITEMAP}")
    text = SITEMAP.read_text(encoding="utf-8")
    index_lastmod = (
        max(article.modified for article in articles).isoformat()
        if articles
        else SECTION_INTRODUCED
    )
    entries = [(f"{SITE}/writing/", index_lastmod)]
    entries.extend((article.url, article.iso_modified) for article in articles)
    wanted = {loc: url_block(loc, lastmod) for loc, lastmod in entries}
    seen: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        block = match.group(0)
        loc_match = re.search(r"<loc>\s*([^<]+?)\s*</loc>", block)
        if not loc_match:
            return block
        loc = loc_match.group(1).strip()
        if loc in wanted:
            seen.add(loc)
            return wanted[loc]
        if is_writing_loc(loc):
            return ""
        return block

    updated = URL_BLOCK_RE.sub(replace, text)
    missing = [loc for loc, _lastmod in entries if loc not in seen]
    if missing:
        if "</urlset>" not in updated:
            raise SystemExit("sitemap.xml has no </urlset>")
        addition = "".join(wanted[loc] for loc in missing)
        updated = updated.replace("</urlset>", addition + "</urlset>", 1)
    write_if_changed(SITEMAP, updated)
    ET.parse(SITEMAP)


def url_block(loc: str, lastmod: str) -> str:
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        "  </url>\n"
    )


def is_writing_loc(loc: str) -> bool:
    base = SITE + "/writing"
    return loc == base or loc.startswith(base + "/")


def write_pygments_css() -> None:
    css = HtmlFormatter(style=WritingStyle, cssclass="highlight").get_style_defs(".highlight")
    scoped: list[str] = []
    for line in css.splitlines():
        stripped = line.lstrip()
        if stripped and not stripped.startswith(".highlight") and not stripped.startswith("/*"):
            line = ".highlight " + stripped
        scoped.append(line)
    text = (
        "/* Generated by scripts/build_writing.py. Highlighting for writing pages. */\n"
        + "\n".join(scoped)
        + "\n"
    )
    write_if_changed(PYGMENTS_CSS, text)


def update_home_latest(articles: list[Article]) -> None:
    latest = articles[:HOME_LATEST_COUNT]
    for path, lang in HOME_PAGES:
        text = path.read_text(encoding="utf-8")
        if len(HOME_BLOCK_RE.findall(text)) != 1:
            raise SystemExit(f"{path}: expected one writing:latest block")
        block = render_home_block(latest, lang)
        updated = HOME_BLOCK_RE.sub(lambda _match: block, text, count=1)
        write_if_changed(path, updated)


def render_home_block(articles: list[Article], lang: str) -> str:
    if not articles:
        inner = '<section class="writing" id="writing" hidden></section>'
    else:
        cards = "\n".join(render_home_card(article, lang) for article in articles)
        more = "Alle Artikel" if lang == "de" else "All articles"
        inner = f"""<section class="writing" id="writing">
  <div class="sec-head">
    <div class="sec-head-l">
      <span class="sec-num">§ 04</span>
      <span class="sec-title">Writing</span>
    </div>
  </div>
  <div class="writing-grid" data-count="{len(articles)}">
{cards}
  </div>
  <div class="writing-more">
    <a href="/writing/" class="btn-repos">{more}</a>
  </div>
</section>"""
    return f"<!-- writing:latest:start -->\n{inner}\n<!-- writing:latest:end -->"


def render_home_card(article: Article, lang: str) -> str:
    shown = format_date_de(article.date) if lang == "de" else format_date(article.date)
    tags = ""
    if article.tags:
        labels = "".join(
            f'<span class="method-tag">{escape(tag)}</span>' for tag in article.tags[:2]
        )
        tags = f'\n      <div class="writing-card-tags">{labels}</div>'
    return f"""    <a class="writing-card" href="/writing/{escape(article.slug)}.html">
      <time datetime="{article.iso_date}">{escape(shown)}</time>
      <h3>{escape(article.title)}</h3>
      <p>{escape(article.description)}</p>{tags}
    </a>"""


def update_nav_hrefs(has_articles: bool) -> None:
    for path in nav_pages():
        text = path.read_text(encoding="utf-8")
        found = NAV_ANCHOR_RE.findall(text)
        if len(found) != 1:
            raise SystemExit(f"{path}: expected one data-writing-nav link, found {len(found)}")
        href = writing_nav_href(path, has_articles)
        current = ' aria-current="page"' if href == "/writing/" and path == OUT / "index.html" else ""
        replacement = f'<a href="{href}" data-writing-nav{current}>'
        updated = NAV_ANCHOR_RE.sub(replacement, text, count=1)
        write_if_changed(path, updated)


def writing_nav_href(path: Path, has_articles: bool) -> str:
    if not has_articles:
        return "/writing/"
    rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
    if rel in {"index.html", "de.html"}:
        return "#writing"
    if rel == "projects/de.html" or (rel.startswith("projects/") and rel.endswith("-de.html")):
        return "/de#writing"
    return "/#writing"


def nav_pages() -> list[Path]:
    pages = [ROOT / "index.html", ROOT / "de.html"]
    pages.extend(sorted((ROOT / "projects").glob("*.html")))
    pages.extend(sorted(OUT.glob("*.html")))
    return pages


def check_outputs(articles: list[Article]) -> None:
    if (OUT / "_example.html").exists():
        raise SystemExit("draft _example.md was published")
    index = (OUT / "index.html").read_text(encoding="utf-8")
    if articles:
        if "First articles coming soon." in index:
            raise SystemExit("index still shows the empty state")
    elif "First articles coming soon." not in index or "time-series forecasting" not in index:
        raise SystemExit("empty index is missing its description")
    if "noindex" in index.lower() or 'rel="alternate" hreflang' in index:
        raise SystemExit("writing index must stay indexable and English-only")
    if '"@type": "CollectionPage"' not in index:
        raise SystemExit("writing index is missing CollectionPage JSON-LD")
    feed = (OUT / "feed.xml").read_text(encoding="utf-8")
    ET.fromstring(feed.encode("utf-8"))
    ET.parse(SITEMAP)
    for html_path in sorted(OUT.glob("*.html")):
        check_html_links(html_path)
    check_css_urls(ROOT / "assets" / "katex" / "katex.min.css")
    check_css_urls(PYGMENTS_CSS)
    for article in articles:
        page = (OUT / f"{article.slug}.html").read_text(encoding="utf-8")
        if article.url not in page:
            raise SystemExit(f"{article.slug}: canonical URL missing")
        if '"@type": "BlogPosting"' not in page:
            raise SystemExit(f"{article.slug}: BlogPosting JSON-LD missing")
        if f'"dateModified": "{article.iso_modified}"' not in page:
            raise SystemExit(f"{article.slug}: dateModified missing")
        if 'rel="alternate" hreflang' in page:
            raise SystemExit(f"{article.slug}: writing pages stay English-only, without hreflang")
        if 'href="/"' not in page or 'href="/writing/"' not in page:
            raise SystemExit(f"{article.slug}: missing a link home or back to /writing/")
    check_home_and_nav(articles)
    check_robots()
    if RSS_LINK not in (ROOT / "index.html").read_text(encoding="utf-8"):
        raise SystemExit("index.html is missing the writing RSS link")
    if RSS_LINK not in (ROOT / "de.html").read_text(encoding="utf-8"):
        raise SystemExit("de.html is missing the writing RSS link")
    check_site_links()


def check_home_and_nav(articles: list[Article]) -> None:
    latest = articles[:HOME_LATEST_COUNT]
    for path, lang in HOME_PAGES:
        text = path.read_text(encoding="utf-8")
        match = HOME_BLOCK_RE.search(text)
        if match is None:
            raise SystemExit(f"{path}: writing:latest block missing")
        block = match.group(0)
        if "medium-posts" in block or "medium.com" in block:
            raise SystemExit(f"{path}: Medium feed markup is still in the Writing block")
        if latest:
            if 'id="writing" hidden' in block:
                raise SystemExit(f"{path}: Writing block is hidden while articles exist")
            if f'data-count="{len(latest)}"' not in block:
                raise SystemExit(f"{path}: Writing block card count is not {len(latest)}")
            more = "Alle Artikel" if lang == "de" else "All articles"
            if f'<a href="/writing/" class="btn-repos">{more}</a>' not in block:
                raise SystemExit(f"{path}: missing the {more} link")
            if block.count('class="writing-card"') != len(latest):
                raise SystemExit(f"{path}: expected {len(latest)} homepage cards")
            for article in latest:
                shown = format_date_de(article.date) if lang == "de" else format_date(article.date)
                if f'/writing/{article.slug}.html' not in block or shown not in block:
                    raise SystemExit(f"{path}: missing homepage card for {article.slug}")
                expected_tags = min(2, len(article.tags))
                card = block.split(f'/writing/{article.slug}.html', 1)[1].split("</a>", 1)[0]
                if card.count('class="method-tag"') != expected_tags:
                    raise SystemExit(f"{path}: {article.slug} should show {expected_tags} tags")
            for article in articles[HOME_LATEST_COUNT:]:
                if f'/writing/{article.slug}.html' in block:
                    raise SystemExit(f"{path}: homepage shows more than {HOME_LATEST_COUNT} articles")
        else:
            if 'id="writing" hidden' not in block:
                raise SystemExit(f"{path}: empty Writing block must stay hidden")
            if "writing-card" in block or "All articles" in block or "Alle Artikel" in block:
                raise SystemExit(f"{path}: empty Writing block should not list articles")
    has_articles = bool(articles)
    for path in nav_pages():
        href = writing_nav_href(path, has_articles)
        text = path.read_text(encoding="utf-8")
        current = ' aria-current="page"' if href == "/writing/" and path == OUT / "index.html" else ""
        expected = f'<a href="{href}" data-writing-nav{current}>'
        if expected not in text:
            raise SystemExit(f"{path}: nav href is not {href}")
        if text.count("data-writing-nav") != 1:
            raise SystemExit(f"{path}: expected one data-writing-nav marker")


def check_robots() -> None:
    text = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://timursalakhetdinov.com/sitemap.xml" not in text:
        raise SystemExit("robots.txt is missing the sitemap line")
    for line in text.splitlines():
        stripped = line.split("#", 1)[0].strip().lower()
        if stripped.startswith("disallow:") and "/writing" in stripped:
            raise SystemExit("robots.txt blocks /writing/")


def check_site_links() -> None:
    pages = [
        path
        for path in ROOT.rglob("*.html")
        if ".git" not in path.parts and "assets" not in path.parts
    ]
    for path in pages:
        check_page_links(path)


def check_page_links(path: Path) -> None:
    parser = _LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    for url in parser.urls:
        split = urlsplit(url)
        if split.scheme in {"mailto", "javascript", "data", "tel"}:
            continue
        if not url or url.startswith(("mailto:", "javascript:", "data:", "tel:")):
            continue
        if split.scheme in {"http", "https"} and not url.startswith(SITE):
            continue
        target = resolve_local_url(path, url) if split.path or not split.fragment else path
        if split.scheme in {"http", "https"} and url.startswith(SITE):
            target = map_site_path(unquote(split.path))
        elif url.startswith("/"):
            target = map_site_path(unquote(split.path))
        elif split.path:
            target = (path.parent / unquote(split.path)).resolve()
        else:
            target = path
        if target is None:
            continue
        if not target.exists():
            raise SystemExit(f"{path}: broken link {url} -> {target}")
        if not split.fragment or target.suffix.lower() not in {".html", ".htm"}:
            continue
        text = target.read_text(encoding="utf-8")
        if split.fragment == "writing":
            if not writing_section_visible(text):
                raise SystemExit(f"{path}: {url} points at #writing while that block is hidden")
            continue
        if f'id="{split.fragment}"' not in text and f"id='{split.fragment}'" not in text:
            raise SystemExit(f"{path}: {url} has no matching id on {target}")


def writing_section_visible(text: str) -> bool:
    for match in re.finditer(r"<section\b[^>]*>", text, re.I):
        tag = match.group(0)
        if not re.search(r'\bid\s*=\s*["\']writing["\']', tag):
            continue
        return not re.search(r"\bhidden\b", tag)
    return False


def check_html_links(path: Path) -> None:
    parser = _LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    for url in parser.urls:
        target = resolve_local_url(path, url)
        if target is None:
            continue
        if not target.exists():
            raise SystemExit(f"{path}: broken link {url} -> {target}")


def check_css_urls(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"missing stylesheet: {path}")
    for match in CSS_URL_RE.finditer(path.read_text(encoding="utf-8")):
        raw = match.group(1).strip().strip("\"'")
        if raw.startswith("data:"):
            continue
        target = resolve_local_url(path, raw)
        if target is not None and not target.exists():
            raise SystemExit(f"{path}: broken CSS url {raw} -> {target}")


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value for key, value in attrs if value is not None}
        if tag in {"a", "link"} and "href" in values:
            self.urls.append(values["href"])
        if tag in {"img", "script", "source"} and "src" in values:
            self.urls.append(values["src"])


def resolve_local_url(source: Path, url: str) -> Path | None:
    if not url or url.startswith(("#", "mailto:", "javascript:", "data:")):
        return None
    split = urlsplit(url)
    if split.scheme in {"http", "https"}:
        if not url.startswith(SITE):
            return None
        path = split.path
    elif split.scheme or url.startswith("//"):
        return None
    elif url.startswith("/"):
        path = split.path
    else:
        relative = unquote(split.path)
        return (source.parent / relative).resolve()
    return map_site_path(unquote(path))


def map_site_path(path: str) -> Path:
    trimmed = path.strip("/")
    if trimmed == "":
        return ROOT / "index.html"
    direct = ROOT / trimmed
    if direct.is_file():
        return direct
    if (ROOT / (trimmed + ".html")).is_file():
        return ROOT / (trimmed + ".html")
    index = ROOT / trimmed / "index.html"
    if index.is_file():
        return index
    return direct


def write_if_changed(path: Path, text: str) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def absolute_url(url: str) -> str:
    if url.startswith(("http://", "https://")):
        return url
    if url.startswith("/"):
        return SITE + url
    return f"{SITE}/{url.lstrip('./')}"


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def xml_text(value: str) -> str:
    return xml_escape(value, {'"': "&quot;", "'": "&apos;"})


def json_script(data: dict[str, object]) -> str:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    return "\n".join("  " + line if line else line for line in text.replace("<", "\\u003c").splitlines())


def format_date(value: date) -> str:
    return f"{value.day} {MONTHS[value.month - 1]} {value.year}"


def format_date_de(value: date) -> str:
    return f"{value.day}. {DE_MONTHS[value.month - 1]} {value.year}"


def rfc822(value: date) -> str:
    return (
        f"{WEEKDAYS[value.weekday()]}, {value.day:02d} {RSS_MONTHS[value.month - 1]} "
        f"{value.year} 00:00:00 +0000"
    )


if __name__ == "__main__":
    main()
