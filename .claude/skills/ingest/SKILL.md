---
name: ingest
description: Ingest sources into the wiki. With no arguments, scans raw/ for unprocessed sources (via hashlog) and ingests them. With a path argument, ingests that specific source.
argument-hint: [path]
allowed-tools: Read Write Edit Glob Grep Bash WebFetch Skill Agent
---

# Ingest Sources

Arguments: $ARGUMENTS

Follow the **Workflow: Ingest** defined in CLAUDE.md exactly.

## Mode Detection

- **No arguments** → **Batch mode**: scan `raw/` for unprocessed sources via hashlog, ingest each.
- **With path argument** → **Single mode**: ingest that specific source.

## Batch Mode (no arguments)

1. **Scan** all files in `raw/papers/`, `raw/notes/`, `raw/experiments/`, `raw/refs/` (recursively, skip `.gitkeep`)
2. **Read `wiki/.hashlog`** to get SHA256 hashes of already-ingested sources
3. **Compute SHA256** for each file. Use Bash: `sha256sum <file>` or `certutil -hashfile <file> SHA256`
4. **List unprocessed sources** — files whose hash is not in hashlog
5. **Ingest all automatically** — no need to ask. The user invoked `/ingest` to process everything new.
6. **For multiple sources**: dispatch parallel Agent subprocesses (one per source) for reading + entity extraction. This is 3-5x faster than serial. Collect results, then present all proposed entities to user at once.
7. After user confirmation on proposed entities, create all pages, then do synthesis/index/log/hashlog updates once at the end.

## Single Mode (with path)

### Source Detection

Determine the source type from the input:

- **Local file** (path to PDF, markdown, code, image, pptx, docx, xlsx): Read it directly
- **arXiv URL** (`arxiv.org/abs/...`): Use WebFetch to get the abstract page
- **Web URL** (article, blog, tweet): Use WebFetch to fetch content
- **Google Doc URL** (`docs.google.com/document/d/...`): Extract the document ID and use the google_drive_fetch tool
- **Google Doc ID** (raw ID string): Use google_drive_fetch directly

### Steps

1. **Check hashlog** — compute SHA256 of source file, check `wiki/.hashlog`. If already ingested, ask user: re-ingest or skip?
2. **Read the source** thoroughly using the appropriate tool
3. **Present key takeaways** to the user:
   - Source title and type
   - 3-5 key takeaways
   - Proposed concepts and methods to create/update
   - Connections to existing wiki content
4. **WAIT for user confirmation** before proceeding
5. **Create source summary page** in `wiki/sources/src-{slug}.md`
6. **Update or create concept pages** in `wiki/concepts/`
7. **Update or create method pages** in `wiki/methods/`
8. **Cross-link** all created/updated pages bidirectionally
9. **Update `wiki/synthesis.md`** if the source adds significant understanding
10. **Update `wiki/index.md`** with new/changed entries
11. **Append to `wiki/log.md`**
12. **Update `wiki/.hashlog`** — append SHA256 hash, file path, and date

## Rules

- Check CLAUDE.md for frontmatter schemas and naming conventions
- Always check hashlog + index for duplicates before creating new pages
- Use `[[wikilink]]` format for all internal references
- Citation style: `[[src-slug|Author et al. (Year)]]`
- Never skip the user confirmation gate

## Examples

```
/ingest                              # batch: scan raw/, ingest all new sources
/ingest raw/papers/attention.pdf     # single: ingest one specific file
```
