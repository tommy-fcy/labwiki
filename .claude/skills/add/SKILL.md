---
name: add
description: Fetch a source and save it to the appropriate raw/ subdirectory. Pure download — NO summarization, NO analysis, NO wiki processing. Use /ingest for that.
argument-hint: <path-or-url> [paper|note|experiment|ref]
allowed-tools: Read Write Bash WebFetch Glob
---

# Add Source to Raw

Input: $ARGUMENTS

**CRITICAL: This skill is a pure fetch/save operation. Do NOT summarize, analyze, or extract key points. Just download and save the raw content. All analysis happens later via `/ingest`.**

## Steps

1. **Parse arguments**
   - First argument: path or URL
   - Second argument (optional): category — `paper`, `note`, `experiment`, `ref`
   - If category is omitted, infer:
     - arXiv URL, `.pdf` → `paper`
     - `.md`, `.txt` → `note`
     - `.csv`, `.xlsx`, data files → `experiment`
     - everything else → `ref`

2. **Determine target directory**

   | Category | Directory |
   |----------|-----------|
   | paper | `raw/papers/` |
   | note | `raw/notes/` |
   | experiment | `raw/experiments/` |
   | ref | `raw/refs/` |

3. **Fetch and save** (per source type)

   **arXiv PDF URL** (`arxiv.org/pdf/...`):
   - WebFetch CANNOT download binary PDFs.
   - Convert to abstract URL: replace `/pdf/` with `/abs/`
   - Use WebFetch on the abstract URL
   - Save the fetched content AS-IS to `raw/papers/{slug}.md` — do NOT rewrite or summarize
   - Tell user: "PDF must be downloaded manually: https://arxiv.org/pdf/XXXX.XXXXX — save it to `raw/papers/`"

   **arXiv abstract URL** (`arxiv.org/abs/...`):
   - Use WebFetch to get the page
   - Save the fetched content AS-IS to `raw/papers/{slug}.md`
   - Tell user the PDF URL for manual download

   **Web URL** (article, blog, tweet):
   - Use WebFetch to retrieve content
   - Save the fetched markdown AS-IS to `raw/{category}/{slug}.md` — do NOT rewrite or summarize

   **Google Doc URL**:
   - Extract doc ID, use google_drive_fetch (if available)
   - Save raw content to target directory

   **Local file path**:
   - The file is already on disk. Do NOT copy or move it.
   - Just confirm: "File already at `{path}`, categorized as `{category}`. Run `/ingest` to process."

4. **Generate filename**
   - Slug: lowercase, hyphens, max 60 chars
   - Check for existing files — do not overwrite

5. **Report**
   - "Saved to: `raw/{category}/{filename}`"
   - "Run `/ingest` to process into the wiki."
   - Nothing else. No summary. No analysis.
