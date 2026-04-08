---
name: add
description: Fetch a source and save it to the appropriate raw/ subdirectory. Uses tools/fetch.py for zero-token downloads. NO summarization, NO wiki processing.
argument-hint: <url> [paper|note|experiment|ref]
allowed-tools: Bash Read Glob
---

# Add Source to Raw

Input: $ARGUMENTS

**This skill calls `tools/fetch.py` via Bash. Zero LLM tokens for the actual download.**

## Steps

1. **Parse arguments**
   - First argument: URL
   - Second argument (optional): category — `paper`, `note`, `experiment`, `ref`

2. **Run fetch.py**

   If category is provided:
   ```bash
   python tools/fetch.py "<url>" --category <category>
   ```

   If no category (auto-detect):
   ```bash
   python tools/fetch.py "<url>"
   ```

3. **If fetch.py is not available** (e.g., no Python), fall back to:
   - PDF/image URLs: `curl -L -o raw/<category>/<filename> "<url>"`
   - Other URLs: use WebFetch and save raw content AS-IS

4. **Report the output** from fetch.py to the user. Remind: run `/ingest` to process into the wiki.

## What fetch.py handles automatically

| URL Type | Action | Output |
|----------|--------|--------|
| arXiv | Extracts title, authors, abstract | `raw/papers/arxiv_XXXX_XXXXX.md` |
| PDF | Downloads binary file | `raw/papers/<filename>.pdf` |
| Image | Downloads binary file | `raw/refs/<filename>.<ext>` |
| Tweet/X | Fetches via oEmbed API | `raw/refs/<filename>.md` |
| Webpage | Converts HTML to markdown | `raw/refs/<filename>.md` |

All saved files include YAML frontmatter (source_url, type, title, captured_at).

## Examples

```
/add https://arxiv.org/abs/2403.07378
/add https://arxiv.org/pdf/2403.07378 paper
/add https://x.com/karpathy/status/123456
/add https://example.com/blog-post ref
```
