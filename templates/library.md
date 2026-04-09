# LabWiki — Claude Code Schema (Library Mode)

> **This file is the brain of the wiki. Claude Code reads it on every session.**

## 0. Library Identity

Fill these fields on first use. Leave blank for template copies.

```yaml
name: ""
scope: ""
started: ""
areas: []
```

This is a personal research library maintained by Claude Code. Unlike project mode (focused on one topic), library mode is for **broad knowledge accumulation** — reading papers, blogs, and notes across many areas to build macro-level understanding and research taste.

The wiki is a persistent, compounding artifact. Claude owns all wiki content; the user owns sources, direction, and judgment.

### First Run

If the `name` field above is empty, this is a fresh copy of LabWiki (library mode). Before doing anything else:
1. Ask the user what this library is for (e.g., "AI research", "Machine Learning").
2. Ask for initial areas of interest (e.g., `[compression, reasoning, agents, training, architecture]`).
3. Fill in `name`, `scope`, `started` (today's date), and `areas`.
4. Create initial area pages in `wiki/areas/`.
5. Confirm with the user, then proceed normally.

---

## 1. Directory Structure

```
library-root/
├── CLAUDE.md              # This file — schema and instructions
├── .gitignore
├── tools/                 # Utility scripts (fetch.py, etc.)
├── raw/                   # Immutable source materials (user-managed, Claude reads only)
│   ├── papers/            # Academic papers (PDF, metadata markdown)
│   ├── notes/             # Personal notes, meeting notes, journal entries
│   ├── repos/             # Interesting repositories and codebases
│   └── refs/              # Blog posts, tweets, web clips, slides, misc
├── wiki/                  # Claude-maintained knowledge base
│   ├── index.md           # Master catalog of all wiki pages
│   ├── log.md             # Chronological operation log (append-only)
│   ├── landscape.md       # High-level overview across all areas
│   ├── areas/             # Area overviews (one per research domain)
│   ├── sources/           # Source summaries (papers, blogs, notes, repos — one per ingested source)
│   └── checkpoints/       # Periodic review snapshots
```

### Rules

- `raw/` is **immutable**. Claude reads from it but never creates, modifies, or deletes files here.
- `wiki/` is **Claude-maintained**. Every file here is created or updated by Claude following the workflows below. The user reads it; Claude writes it.
- `wiki/log.md` is **append-only**. Claude appends to the end; never edits earlier entries.

---

## 2. Page Types and Frontmatter

All wiki pages use YAML frontmatter enclosed in `---`.

### 2.1 Area Page (`wiki/areas/{slug}.md`)

```yaml
---
title: "Area Name"
type: area
aliases: []
source_count: 0
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
related: []
---
```

Area pages are **mini-syntheses** for each research domain. They are the primary organizing unit.

Body guidelines:
- Overview (2-3 sentences)
- State of the art and key themes
- Open problems
- Key sources (`[[wikilinks]]`)
- Connections to other areas

### 2.2 Source Page (`wiki/sources/src-{slug}.md`)

```yaml
---
title: "Source Title"
type: source
source_type: paper | blog | repo | note | slides | tweet | webpage
area: ""
authors: []
year: 2024
url: ""
file: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
related: []
---
```

Source pages are **concise reading records**. They capture what you read and why it matters. Concepts and methods are described inline — no separate pages needed.

**Body guidelines** (use what fits, skip what doesn't):
- Start with a **2-3 sentence summary**
- Then **key points** — the most important things to remember (bullets)
- Use `[[wikilinks]]` to link to other sources or area pages
- Use `tags` in frontmatter to capture key concepts and methods (e.g., `[svd, compression, low-rank]`)

**What NOT to do:**
- Don't force sections like "Methodology" or "Results" on a blog post
- Don't repeat the abstract verbatim — distill it
- Don't write more than ~15 bullets. If it's that complex, the source itself is the reference

### 2.3 Checkpoint Page (`wiki/checkpoints/cp-{NNN}-{slug}.md`)

```yaml
---
title: "Checkpoint: Review Name"
type: checkpoint
checkpoint_id: 1
detail_level: snapshot | report
source_count: 0
area_count: 0
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
---
```

Body structure depends on `detail_level` — see Section 6.

---

## 3. Naming Conventions

### Slugs

- Lowercase, hyphens for spaces, no underscores/dots/special characters
- Max 60 characters
- Prefer short recognizable names over verbose descriptions

### File Names by Type

| Type | Pattern | Directory | Example |
|------|---------|-----------|---------|
| Area | `{slug}.md` | `wiki/areas/` | `compression.md` |
| Source | `src-{slug}.md` | `wiki/sources/` | `src-svd-llm.md` |
| Checkpoint | `cp-{NNN}-{slug}.md` | `wiki/checkpoints/` | `cp-001-april-review.md` |

---

## 4. Linking Conventions

- Always use `[[slug]]` or `[[slug|Display Text]]` for internal references. Never markdown-style links for wiki cross-references.
- Citation style: `[[src-svd-llm|Wang et al. (2024)]]`
- Link source pages to their area and to related sources. Link area pages to key sources.
- Maintain `related` frontmatter bidirectionally.

---

## 5. Workflow: Ingest

**Trigger:** User provides a source or runs `/ingest`.

### Batch Mode (no arguments)

1. **Scan** all files in `raw/` recursively (skip `.gitkeep`).
2. **Read `wiki/.hashlog`** to get already-ingested file hashes.
3. **Compute SHA256** for each file in `raw/`. Compare against hashlog.
4. **Ingest all unprocessed sources automatically.**
5. **For multiple sources**, dispatch parallel Agent subprocesses. Collect results, then update area pages/landscape/index/log once at the end.

### Single Source

1. **Identify source type** from file extension or user description.
2. **Check hashlog** for duplicates.
3. **Read the source** thoroughly.
   - **PDF papers**: Use Read tool with `pages` parameter for large PDFs.
   - **Repos**: Read the README first, then scan key source files.
   - **URLs**: Use WebFetch to retrieve and process content.
4. **Discuss with user (MANDATORY):** present title, proposed area, 3-5 key takeaways, proposed tags, connections to existing wiki content. Wait for confirmation.
5. **Create source page** in `wiki/sources/src-{slug}.md`. Set `area` field.
6. **Update area page** — add new findings, update source count, add wikilink to source.
7. **Update landscape.md** incrementally if the source adds significant cross-area understanding.
8. **Update index.md** and **append to log.md**.
9. **Update hashlog.**

---

## 6. Workflow: Checkpoint

**Trigger:** User says "checkpoint", "review", or "what have I learned".

Ask user: **Snapshot** (~1 page) or **Report** (~3-5 pages)? Default to snapshot.

#### Snapshot Template

```markdown
## Reading Status
[1-2 sentences on recent reading activity]

## Key Takeaways Since Last Review
- [3-7 bullets]

## Areas by Coverage

| Area | Sources | Trend |
|------|---------|-------|
| ...  | ...     | ...   |

## Emerging Themes
- [Cross-area patterns or insights]

## Reading Queue / Gaps
- [Areas that need more sources]
```

#### Report Template

```markdown
## Overview
[2-3 paragraphs]

## Area Deep Dives
### [Area 1]
- Coverage, key findings, open questions

## Cross-Area Insights
## Knowledge Gaps
## Research Taste Evolution
## Recommendations
```

---

## 7. Workflow: Query

**Trigger:** User asks a question about library content.

### Tiered Search (minimize token usage)

**Tier 1: Index scan.** Read `wiki/index.md` only. Answer if sufficient.

**Tier 2: Targeted read.** Read 3-5 most relevant pages from the index.

**Tier 3: Area-scoped search.** Read the relevant area page, then follow its source links.

**Tier 4: Broad search.** Grep across `wiki/`, read up to 10-15 pages. Read `wiki/landscape.md`.

---

## 8. Workflow: Lint

**Trigger:** User says "lint" or "health check".

Checks: orphan pages, broken wikilinks, missing frontmatter, missing area field, stale area pages, index accuracy, landscape freshness.

Output: structured report, then ask "Shall I fix what I can?"

---

## 9. Index Format

```markdown
## Areas (N)
- [[compression]] — Model compression: quantization, pruning, SVD
- [[reasoning]] — LLM reasoning capabilities and methods

## Sources (N)
- [[src-svd-llm]] — paper — [compression] SVD-based LLM compression
- [[src-karpathy-blog]] — blog — [reasoning] LLM training insights

## Checkpoints (N)
- [[cp-001-april-review]] — snapshot — 2026-04-08
```

---

## 10. Log Format

Append-only. `## [YYYY-MM-DD] operation | Title` with bullet body.

Operations: `ingest`, `query`, `checkpoint`, `lint`

---

## 11. Obsidian Compatibility

1. Wikilinks only for internal references.
2. Frontmatter in ISO date format for Dataview.
3. Tags only in frontmatter, never inline `#tag`.

### Example Dataview Queries

```dataview
TABLE source_count
FROM "wiki/areas"
SORT source_count DESC
```

```dataview
TABLE source_type, area, year
FROM "wiki/sources"
SORT year DESC
```

```dataview
LIST
FROM "wiki/sources"
WHERE area = "compression"
SORT year DESC
```

---

## 12. Rules and Guardrails

1. **Never delete wiki pages.** Mark obsolete pages with `deprecated: true`.
2. **Never modify files in `raw/`.** Read only.
3. **Never edit earlier log entries.** Log is append-only.
4. **Always update `updated` date** on any page modification.
5. **Always assign an area** to every source page.
6. **Always confirm with user** before proceeding with ingest.
7. **Keep source pages concise.** Distill, don't transcribe.
8. **Consistent citation style**: `[[src-slug|Author et al. (Year)]]`.
9. **When in doubt, ask.** The user is the architect; Claude is the builder.
