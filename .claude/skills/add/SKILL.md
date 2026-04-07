---
name: add
description: Fetch a source and save it to the appropriate raw/ subdirectory. Does NOT process or ingest into the wiki — use /ingest for that.
argument-hint: <path-or-url> [paper|note|experiment|ref]
allowed-tools: Read Write Bash WebFetch Glob Skill
---

# Add Source to Raw

Fetch and save a source to `raw/`. This is a pure download/copy operation — no wiki processing.

Input: $ARGUMENTS

## Steps

1. **Parse arguments**
   - First argument: path or URL
   - Second argument (optional): category — one of `paper`, `note`, `experiment`, `ref`
   - If category is omitted, infer from source type:
     - arXiv URL, PDF, `.pdf` → `paper`
     - `.md`, `.txt` personal notes → `note`
     - data files, `.csv`, `.xlsx`, experiment logs → `experiment`
     - everything else (slides, docs, web clips, misc) → `ref`

2. **Determine target directory**

   | Category | Directory |
   |----------|-----------|
   | paper | `raw/papers/` |
   | note | `raw/notes/` |
   | experiment | `raw/experiments/` |
   | ref | `raw/refs/` |

3. **Fetch the source**

   - **URL (web page, tweet, blog)**: Use WebFetch to retrieve content. Save as markdown: `raw/{category}/{slug}.md`
   - **arXiv URL** (`arxiv.org/abs/XXXX.XXXXX`): Use WebFetch to get the abstract page. Save as markdown: `raw/papers/{slug}.md`. Note: PDF download requires the user to download manually — inform them of the PDF URL.
   - **Google Doc URL**: Extract doc ID, use google_drive_fetch (if available), save as markdown to target directory.
   - **Local file path**: The file is already local. Do NOT copy or move it. Just confirm its location and category.
   - **PPTX/DOCX/XLSX**: Use the corresponding skill to read, save extracted text as markdown alongside the original.

4. **Generate filename**
   - Slug: lowercase, hyphens, max 60 chars
   - For papers: use short title or `{firstauthor}-{year}-{keyword}` if title is too long
   - Avoid overwriting existing files — check first

5. **Report to user**
   - File saved at: `raw/{category}/{filename}`
   - Remind: run `/ingest` to process new sources into the wiki

## Examples

```
/add https://arxiv.org/abs/1706.03762 paper
/add https://x.com/karpathy/status/123456 ref
/add https://docs.google.com/document/d/1abc.../edit ref
/add raw/experiments/results.csv experiment    # already local, just confirm
```
