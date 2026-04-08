#!/usr/bin/env python3
"""
fetch.py — Download sources into raw/ subdirectories.
Zero LLM tokens. Pure Python with no external dependencies.

Usage:
    python tools/fetch.py <url> [--category paper|note|experiment|ref]
    python tools/fetch.py <url>                  # auto-detect category
    python tools/fetch.py <url> --category paper  # explicit category
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# URL type detection
# ---------------------------------------------------------------------------

def detect_url_type(url: str) -> str:
    lower = url.lower()
    if "twitter.com" in lower or "x.com" in lower:
        return "tweet"
    if "arxiv.org" in lower:
        return "arxiv"
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    if path.endswith(".pdf"):
        return "pdf"
    if any(path.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")):
        return "image"
    return "webpage"


def infer_category(url_type: str) -> str:
    if url_type in ("arxiv", "pdf"):
        return "paper"
    return "ref"


CATEGORY_DIR = {
    "paper": "raw/papers",
    "note": "raw/notes",
    "experiment": "raw/experiments",
    "ref": "raw/refs",
}

# ---------------------------------------------------------------------------
# Filename generation
# ---------------------------------------------------------------------------

def safe_filename(url: str, suffix: str) -> str:
    parsed = urllib.parse.urlparse(url)
    name = parsed.netloc + parsed.path
    name = re.sub(r"[^\w\-]", "_", name).strip("_")
    name = re.sub(r"_+", "_", name)[:80]
    return name + suffix


def unique_path(target_dir: Path, filename: str) -> Path:
    out = target_dir / filename
    if not out.exists():
        return out
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while out.exists():
        out = target_dir / f"{stem}_{counter}{suffix}"
        counter += 1
    return out

# ---------------------------------------------------------------------------
# SSL context (some sites need this)
# ---------------------------------------------------------------------------

def _ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    return ctx


def _urlopen(url: str, timeout: int = 15):
    headers = {"User-Agent": "labwiki-fetch/1.0"}
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=timeout, context=_ssl_context())

# ---------------------------------------------------------------------------
# Fetchers
# ---------------------------------------------------------------------------

def fetch_binary(url: str, suffix: str, target_dir: Path) -> Path:
    data = _urlopen(url).read()
    filename = safe_filename(url, suffix)
    out = unique_path(target_dir, filename)
    out.write_bytes(data)
    return out


def html_to_markdown(html: str) -> str:
    try:
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0
        return h.handle(html)
    except ImportError:
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:12000]


def fetch_tweet(url: str) -> tuple[str, str]:
    oembed_url = url.replace("x.com", "twitter.com")
    api = f"https://publish.twitter.com/oembed?url={urllib.parse.quote(oembed_url)}&omit_script=true"
    try:
        resp = _urlopen(api)
        data = json.loads(resp.read())
        tweet_text = re.sub(r"<[^>]+>", "", data.get("html", "")).strip()
        tweet_author = data.get("author_name", "unknown")
    except Exception:
        tweet_text = f"Tweet at {url} (could not fetch content)"
        tweet_author = "unknown"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = f"""---
source_url: "{url}"
type: tweet
author: "{tweet_author}"
captured_at: "{now}"
---

# Tweet by @{tweet_author}

{tweet_text}

Source: {url}
"""
    return content, safe_filename(url, ".md")


def fetch_arxiv(url: str) -> tuple[str, str]:
    arxiv_id_match = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", url)
    if not arxiv_id_match:
        return fetch_webpage(url)

    arxiv_id = arxiv_id_match.group(1)
    abs_url = f"https://export.arxiv.org/abs/{arxiv_id}"

    title, abstract, authors = arxiv_id, "", ""
    try:
        html = _urlopen(abs_url).read().decode("utf-8", errors="replace")

        m = re.search(r'class="title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
        if m:
            title = re.sub(r"<[^>]+>", " ", m.group(1)).strip()
            title = re.sub(r"^Title:\s*", "", title).strip()

        m = re.search(r'class="abstract[^"]*"[^>]*>(.*?)</blockquote>', html, re.DOTALL | re.IGNORECASE)
        if m:
            abstract = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            abstract = re.sub(r"^Abstract:\s*", "", abstract).strip()

        m = re.search(r'class="authors"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
        if m:
            authors = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            authors = re.sub(r"^Authors?:\s*", "", authors).strip()
    except Exception:
        pass

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = f"""---
source_url: "{url}"
arxiv_id: "{arxiv_id}"
type: paper
title: "{title}"
authors: "{authors}"
captured_at: "{now}"
---

# {title}

**Authors:** {authors}
**arXiv:** [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})
**PDF:** [Download](https://arxiv.org/pdf/{arxiv_id}.pdf)

## Abstract

{abstract}

Source: {url}
"""
    filename = f"arxiv_{arxiv_id.replace('.', '_')}.md"
    return content, filename


def fetch_webpage(url: str) -> tuple[str, str]:
    html = _urlopen(url).read().decode("utf-8", errors="replace")

    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    title = re.sub(r"\s+", " ", m.group(1)).strip() if m else url

    markdown = html_to_markdown(html)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = f"""---
source_url: "{url}"
type: webpage
title: "{title}"
captured_at: "{now}"
---

# {title}

Source: {url}

---

{markdown}
"""
    return content, safe_filename(url, ".md")

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def fetch(url: str, category: str | None = None, root: Path = Path(".")) -> Path:
    url_type = detect_url_type(url)
    if category is None:
        category = infer_category(url_type)

    target_dir = root / CATEGORY_DIR[category]
    target_dir.mkdir(parents=True, exist_ok=True)

    if url_type == "pdf":
        out = fetch_binary(url, ".pdf", target_dir)
        print(f"[fetch] PDF saved: {out.relative_to(root)}")
        return out

    if url_type == "image":
        suffix = Path(urllib.parse.urlparse(url).path).suffix or ".jpg"
        out = fetch_binary(url, suffix, target_dir)
        print(f"[fetch] Image saved: {out.relative_to(root)}")
        return out

    if url_type == "tweet":
        content, filename = fetch_tweet(url)
    elif url_type == "arxiv":
        content, filename = fetch_arxiv(url)
    else:
        content, filename = fetch_webpage(url)

    out = unique_path(target_dir, filename)
    out.write_text(content, encoding="utf-8")
    print(f"[fetch] {url_type} saved: {out.relative_to(root)}")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch a URL into raw/ subdirectory. Zero LLM tokens.",
        usage="python tools/fetch.py <url> [--category paper|note|experiment|ref]",
    )
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument(
        "--category", "-c",
        choices=["paper", "note", "experiment", "ref"],
        default=None,
        help="Target category (default: auto-detect from URL type)",
    )
    args = parser.parse_args()

    try:
        out = fetch(args.url, args.category)
        print(f"[fetch] Done. Run /ingest to process into wiki.")
    except (ValueError, RuntimeError) as e:
        print(f"[fetch] Error: {e}", file=sys.stderr)
        sys.exit(1)
