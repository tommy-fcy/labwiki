# LabWiki — Claude Code Schema (Project Mode)

> **This file is the brain of the wiki. Claude Code reads it on every session.**

## 0. Project Identity

Fill these fields on first use. Leave blank for template copies.

```yaml
topic: ""
description: ""
started: ""
```

This is a personal research knowledge base maintained by Claude Code. The wiki is a persistent, compounding artifact — knowledge is compiled once and kept current, not re-derived on every query. Claude owns all wiki content; the user owns sources, direction, and judgment.

### First Run

If the `topic` field above is empty, this is a fresh copy of LabWiki. Before doing anything else:
1. Ask the user what research topic this wiki is for.
2. Fill in `topic`, `description`, and `started` (today's date).
3. Confirm with the user, then proceed normally.

---

## 1. Directory Structure

```
project-root/
├── CLAUDE.md              # This file — schema and instructions
├── .gitignore
├── tools/                 # Utility scripts (fetch.py, etc.)
├── raw/                   # Immutable source materials (user-managed, Claude reads only)
│   ├── papers/            # Academic papers (PDF, markdown)
│   ├── notes/             # Personal notes, meeting notes, journal entries
│   ├── experiments/       # Experiment data, results, logs
│   ├── repos/             # Interesting repositories and codebases
│   └── refs/              # Reference materials (slides, docs, web clips, misc)
├── code/                  # Project code (scripts, notebooks, implementations)
├── wiki/                  # Claude-maintained knowledge base
│   ├── index.md           # Master catalog of all wiki pages
│   ├── log.md             # Chronological operation log (append-only)
│   ├── synthesis.md       # Evolving project understanding and thesis
│   ├── sources/           # Source summaries (papers, blogs, notes, repos — one per ingested source)
│   ├── experiments/       # Experiment designs, results, analyses
│   ├── threads/           # Research threads — investigations, comparisons, accumulated topic knowledge
│   └── checkpoints/       # Milestone snapshots and reports
```

### Rules

- `raw/` is **immutable**. Claude reads from it but never creates, modifies, or deletes files here.
- `code/` is a working directory. Claude may read and write code here when asked.
- `wiki/` is **Claude-maintained**. Every file here is created or updated by Claude following the workflows below. The user reads it; Claude writes it.
- `wiki/log.md` is **append-only**. Claude appends to the end; never edits earlier entries.

---

## 2. Page Types and Frontmatter

All wiki pages use YAML frontmatter enclosed in `---`.

### 2.1 Source Page (`wiki/sources/src-{slug}.md`)

```yaml
---
title: "Source Title"
type: source
source_type: paper | blog | repo | note | slides | tweet | webpage
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
- Use `[[wikilinks]]` to link to other sources or threads
- Use `tags` in frontmatter to capture key concepts and methods (e.g., `[svd, compression, low-rank]`)

**What NOT to do:**
- Don't force sections like "Methodology" or "Results" on a blog post
- Don't repeat the abstract verbatim — distill it
- Don't write more than ~15 bullets. If it's that complex, the source itself is the reference

### 2.2 Experiment Page (`wiki/experiments/{slug}.md`)

```yaml
---
title: "Experiment Title"
type: experiment
status: planned | running | completed | abandoned
date: YYYY-MM-DD
file: "raw/experiments/..."
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
related: []
---
```

Body: objective, setup, results, analysis, next steps — written freely, include what's relevant.

### 2.3 Thread Page (`wiki/threads/{slug}.md`)

```yaml
---
title: "Thread Title"
type: thread
thread_type: investigation | comparison | question | topic-synthesis | literature-review
status: open | resolved | parked
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
related: []
---
```

Threads are for **cross-source knowledge accumulation**. When multiple sources touch the same topic and you want a unified view, create a thread. They replace the need for separate concept/method pages.

Body: question or topic, findings from multiple sources with citations, current understanding, open issues.

### 2.4 Checkpoint Page (`wiki/checkpoints/cp-{NNN}-{slug}.md`)

```yaml
---
title: "Checkpoint: Phase Name"
type: checkpoint
checkpoint_id: 1
detail_level: snapshot | report
source_count: 0
experiment_count: 0
thread_count: 0
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
| Source | `src-{slug}.md` | `wiki/sources/` | `src-svd-llm.md` |
| Experiment | `{slug}.md` | `wiki/experiments/` | `baseline-accuracy.md` |
| Thread | `{slug}.md` | `wiki/threads/` | `svd-compression.md` |
| Checkpoint | `cp-{NNN}-{slug}.md` | `wiki/checkpoints/` | `cp-001-initial-survey.md` |

---

## 4. Linking Conventions

- Always use `[[slug]]` or `[[slug|Display Text]]` for internal references. Never markdown-style links for wiki cross-references.
- Citation style: `[[src-svd-llm|Wang et al. (2024)]]`
- Link source pages to related sources and threads. Link threads to all relevant sources.
- Maintain `related` frontmatter bidirectionally.

---

## 5. Workflow: Ingest

**Trigger:** User provides a source or runs `/ingest`.

### Batch Mode (no arguments)

1. **Scan** all files in `raw/` recursively (skip `.gitkeep`).
2. **Read `wiki/.hashlog`** to get already-ingested file hashes.
3. **Compute SHA256** for each file in `raw/`. Compare against hashlog.
4. **Ingest all unprocessed sources automatically.**
5. **For multiple sources**, dispatch parallel Agent subprocesses. Collect results, then update synthesis/index/log once at the end.

### Single Source

1. **Identify source type** from file extension or user description.
2. **Check hashlog** for duplicates.
3. **Read the source** thoroughly.
4. **Discuss with user (MANDATORY):** present title, 3-5 key takeaways, proposed tags, connections to existing wiki content. Wait for confirmation.
5. **Create source page** in `wiki/sources/src-{slug}.md`.
6. **Update synthesis.md** incrementally if the source adds significant understanding.
7. **Update index.md** and **append to log.md**.
8. **Update hashlog.**

---

## 6. Workflow: Checkpoint

**Trigger:** User says "checkpoint", "snapshot", or "progress report".

Ask user: **Snapshot** (~1 page) or **Report** (~3-5 pages)? Default to snapshot.

#### Snapshot Template

```markdown
## Current Phase
[1-2 sentences]

## Key Findings
- [3-7 bullets]

## Open Questions
- [3-5 bullets]

## Next Steps
- [3-5 bullets]

## Wiki Status
- Sources: N (+M since last checkpoint)
- Experiments: N (+M)
- Threads: N (+M)
```

#### Report Template

```markdown
## Executive Summary
[2-3 paragraphs]

## Key Findings by Theme
### [Theme 1]
[Findings with citations]

## Contradictions and Open Questions
## Gap Analysis
## Recommendations
```

---

## 7. Workflow: Query

**Trigger:** User asks a question about wiki content.

### Tiered Search (minimize token usage)

**Tier 1: Index scan.** Read `wiki/index.md` only. Answer if sufficient.

**Tier 2: Targeted read.** Read 3-5 most relevant pages from the index.

**Tier 3: Broad search.** Grep across `wiki/`, read up to 10-15 pages. Read `wiki/synthesis.md` for cross-cutting themes.

### After answering

If the answer is a significant synthesis worth preserving, ask: "File this as a thread?" If yes: create in `wiki/threads/`, update index and log.

---

## 8. Workflow: Lint

**Trigger:** User says "lint" or "health check".

Checks: orphan pages, broken wikilinks, missing frontmatter, stale pages, index accuracy, synthesis freshness.

Output: structured report, then ask "Shall I fix what I can?"

---

## 9. Index Format

```markdown
## Sources (N)
- [[src-svd-llm]] — paper — SVD-based LLM compression
- [[src-karpathy-blog]] — blog — LLM training tips

## Experiments (N)
- [[baseline-accuracy]] — completed — Initial benchmark

## Threads (N)
- [[svd-compression]] — open — Accumulated understanding of SVD-based compression

## Checkpoints (N)
- [[cp-001-initial-survey]] — snapshot — 2026-04-08
```

---

## 10. Log Format

Append-only. `## [YYYY-MM-DD] operation | Title` with bullet body.

Operations: `ingest`, `query`, `checkpoint`, `lint`, `thread`

---

## 11. Obsidian Compatibility

1. Wikilinks only for internal references.
2. Frontmatter in ISO date format for Dataview.
3. Tags only in frontmatter, never inline `#tag`.

### Example Dataview Queries

```dataview
TABLE source_type, authors, year
FROM "wiki/sources"
SORT year DESC
```

```dataview
TABLE status, date
FROM "wiki/experiments"
SORT date DESC
```

```dataview
LIST
FROM "wiki/sources"
WHERE contains(tags, "compression")
```

---

## 12. Rules and Guardrails

1. **Never delete wiki pages.** Mark obsolete pages with `deprecated: true`.
2. **Never modify files in `raw/`.** Read only.
3. **Never edit earlier log entries.** Log is append-only.
4. **Always update `updated` date** on any page modification.
5. **Always confirm with user** before proceeding with ingest.
6. **Keep source pages concise.** Distill, don't transcribe.
7. **Use threads for accumulated knowledge.** If a topic spans 3+ sources, it deserves a thread.
8. **Consistent citation style**: `[[src-slug|Author et al. (Year)]]`.
9. **When in doubt, ask.** The user is the architect; Claude is the builder.
