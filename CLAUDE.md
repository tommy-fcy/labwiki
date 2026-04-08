# LabWiki — Claude Code Schema

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
│   └── refs/              # Reference materials (slides, docs, web clips, misc)
├── code/                  # Project code (scripts, notebooks, implementations)
├── wiki/                  # Claude-maintained knowledge base
│   ├── index.md           # Master catalog of all wiki pages
│   ├── log.md             # Chronological operation log (append-only)
│   ├── synthesis.md       # Evolving project understanding and thesis
│   ├── papers/            # Paper summaries (one per ingested paper)
│   ├── concepts/          # Theoretical concepts, ideas, phenomena
│   ├── methods/           # Techniques, algorithms, tools, frameworks, benchmarks
│   ├── experiments/       # Experiment designs, results, analyses
│   ├── threads/           # Research threads — investigations, comparisons, open questions
│   └── checkpoints/       # Milestone snapshots and reports
```

### Rules

- `raw/` is **immutable**. Claude reads from it but never creates, modifies, or deletes files here.
- `code/` is a working directory. Claude may read and write code here when asked.
- `wiki/` is **Claude-maintained**. Every file here is created or updated by Claude following the workflows below. The user reads it; Claude writes it.
- `wiki/log.md` is **append-only**. Claude appends to the end; never edits earlier entries.

---

## 2. Page Types and Frontmatter

All wiki pages use YAML frontmatter enclosed in `---`. Every page has a base schema; each type extends it.

### 2.1 Base Schema (shared by all pages)

```yaml
---
title: "Human-Readable Title"
type: paper | concept | method | experiment | thread | checkpoint
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
---
```

- `title` — Required. Natural language display name.
- `type` — Required. One of the six enumerated values.
- `created` / `updated` — Required. ISO date. Update `updated` on every modification.
- `tags` — YAML list. Lowercase, hyphenated. Only in frontmatter, never inline `#tag`.
- `sources` — YAML list of source page slugs that informed this page (e.g., `[src-attention-is-all-you-need]`).
- `related` — YAML list of related wiki page slugs. Maintain bidirectionally.

### 2.2 Paper Page (`wiki/papers/src-{slug}.md`)

```yaml
---
title: "Paper Title"
type: paper
source_type: journal | conference | preprint | thesis | report | book-chapter | survey
authors: ["Last, First", "Last, First"]
year: 2024
venue: "NeurIPS 2024"
file: "raw/papers/filename.pdf"
url: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
---
```

Body sections:
- **Summary** — 3-5 sentence overview
- **Key Contributions** — Bullet list of main claims/results
- **Methodology** — How the work was done
- **Results** — Key quantitative/qualitative findings
- **Relevance** — Why this matters to the project
- **Extracted Entities** — Wikilinks to concept/method pages touched by this paper
- **Notes** — Anything else notable, limitations, open questions

### 2.3 Concept Page (`wiki/concepts/{slug}.md`)

```yaml
---
title: "Concept Name"
type: concept
aliases: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
---
```

- `aliases` — Alternative names for this concept (e.g., `["self-attention", "scaled dot-product attention"]`).

Body sections:
- **Definition** — Concise definition
- **Explanation** — Detailed explanation with context
- **Key Aspects** — Important properties or sub-topics
- **Connections** — How this relates to other concepts/methods (with wikilinks)
- **Open Questions** — Unresolved aspects

### 2.4 Method Page (`wiki/methods/{slug}.md`)

```yaml
---
title: "Method Name"
type: method
method_type: algorithm | framework | tool | library | benchmark | dataset | metric
aliases: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
---
```

Body sections:
- **Description** — What it is and what it does
- **How It Works** — Technical details
- **Strengths and Limitations** — Trade-offs
- **Usage** — Where and how it's applied
- **Connections** — Relationships to concepts, other methods, experiments

### 2.5 Experiment Page (`wiki/experiments/{slug}.md`)

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
sources: []
related: []
---
```

Body sections:
- **Objective** — What this experiment tests
- **Setup** — Configuration, parameters, data
- **Results** — What happened (include figures/tables if available)
- **Analysis** — Interpretation of results
- **Implications** — What this means for the project
- **Next Steps** — Follow-up experiments or questions

### 2.6 Thread Page (`wiki/threads/{slug}.md`)

```yaml
---
title: "Thread Title"
type: thread
thread_type: investigation | comparison | question | gap-analysis | literature-review
status: open | resolved | parked
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
---
```

Threads are research investigations — questions being pursued, comparisons being made, gaps being analyzed. They are the filed results of queries and explorations.

Body sections:
- **Question / Objective** — What this thread investigates
- **Context** — Background and motivation
- **Findings** — What has been discovered so far
- **Evidence** — Supporting data with citations
- **Conclusions** — Current best understanding
- **Open Issues** — What remains unresolved

### 2.7 Checkpoint Page (`wiki/checkpoints/cp-{NNN}-{slug}.md`)

```yaml
---
title: "Checkpoint: Phase Name"
type: checkpoint
checkpoint_id: 1
detail_level: snapshot | report
paper_count: 0
concept_count: 0
method_count: 0
experiment_count: 0
thread_count: 0
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
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
| Paper | `src-{slug}.md` | `wiki/papers/` | `src-attention-is-all-you-need.md` |
| Concept | `{slug}.md` | `wiki/concepts/` | `self-attention.md` |
| Method | `{slug}.md` | `wiki/methods/` | `transformer.md` |
| Experiment | `{slug}.md` | `wiki/experiments/` | `baseline-accuracy-test.md` |
| Thread | `{slug}.md` | `wiki/threads/` | `scaling-vs-architecture.md` |
| Checkpoint | `cp-{NNN}-{slug}.md` | `wiki/checkpoints/` | `cp-001-initial-survey.md` |

### Deduplication

Before creating any concept, method, or experiment page, search the wiki for pages with matching slugs or overlapping aliases. If a match exists, **update that page** rather than creating a duplicate.

---

## 4. Linking Conventions

### Wikilinks

- Always use `[[slug]]` or `[[slug|Display Text]]` for internal references.
- Never use markdown-style `[text](path)` for wiki cross-references.
- Obsidian resolves `[[slug]]` by shortest unique path, so bare slugs work across subdirectories.

### Citation Style

Reference papers in running text using display-text form:

```
[[src-attention-is-all-you-need|Vaswani et al. (2017)]]
```

### Cross-Reference Targets

- Paper pages: link to every concept and method they touch
- Concept/method pages: link to related concepts, methods, and citing papers
- Experiment pages: link to methods used and concepts tested
- Thread pages: link to all evidence sources

### Bidirectional Maintenance

When creating or updating page A with a link to page B:
1. Check if page B's `related` frontmatter includes A's slug.
2. If not, add it. This ensures bidirectional discoverability.

---

## 5. Workflow: Ingest

**Trigger:** User provides a source and asks to ingest it (e.g., "ingest this", "read this paper", "add this to the wiki"), or runs `/ingest` with no arguments for batch mode.

### Batch Mode (no arguments)

When `/ingest` is called with no arguments:

1. **Scan** all files in `raw/` recursively (skip `.gitkeep`).
2. **Read `wiki/.hashlog`** to get already-ingested file hashes.
3. **Compute SHA256** for each file in `raw/`. Compare against hashlog.
4. **List unprocessed sources** — files whose hash is not in hashlog.
5. **Ingest all unprocessed sources automatically.** No need to ask — the user invoked `/ingest` to process everything new.
6. **For multiple sources**, dispatch parallel Agent subprocesses (one per source) for Steps 1-6 below. Collect results, then do Steps 7-9 once at the end. This is significantly faster than serial processing.

### Pre-Checks (single source)

1. **Identify source type** from file extension or user description:
   - `.pdf` → paper or document
   - `.py`, `.js`, `.ts`, `.rs`, `.go`, `.java`, `.cpp`, `.ipynb` → code
   - `.md`, `.txt` → note or document
   - `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg` → image
   - `.pptx` → slides (use pptx skill)
   - `.docx` → document (use docx skill)
   - `.csv`, `.xlsx` → data (use xlsx skill)
   - URL → website (use WebFetch)
   - Google Doc URL → extract document ID, use google_drive_fetch MCP tool (if available)

2. **Check hashlog.** Compute SHA256 of the source file. If the hash exists in `wiki/.hashlog`, this file was already ingested. Inform user and ask whether to re-ingest (update) or skip.

3. **Check for duplicates.** Also search `wiki/index.md` by title, filename, and URL as a secondary check.

4. **Verify source location.** If the file is not already in `raw/`, note its actual path. Do NOT move files into `raw/` — that is the user's responsibility.

### Step 1: Read the Source

Read the source material thoroughly. Per-type guidance:
- **PDF papers**: Use Read tool with `pages` parameter for large PDFs. Read in chunks if needed.
- **Code**: Read files, understand purpose, architecture, key functions.
- **Images**: View with Read tool. Describe contents.
- **PPTX/DOCX/XLSX**: Use the corresponding skill (pptx, docx, xlsx).
- **URLs**: Use WebFetch to retrieve and process content.
- **Multiple files**: Read each, identify connections between them.

### Step 2: Discuss with User (MANDATORY)

Present to the user:
1. **Source title and type**
2. **3-5 key takeaways** from the source
3. **Proposed entities** — concepts and methods to create or update, with brief rationale
4. **Connections** — how this source relates to existing wiki content (if any)

**Wait for user confirmation before proceeding.** The user may redirect, add emphasis, or skip certain entities. Do not proceed to Step 3 without user input.

### Step 3: Create Paper/Source Summary Page

Create `wiki/papers/src-{slug}.md` with full frontmatter and body sections per the schema. Include wikilinks to all entity/concept/method pages.

### Step 4: Update or Create Concept Pages

For each concept identified in Step 2:
- If the page **exists**: read it, add new information from this source, add source slug to `sources` list, update `updated` date.
- If **new**: create `wiki/concepts/{slug}.md` with full frontmatter and body.

### Step 5: Update or Create Method Pages

Same logic as Step 4, applied to `wiki/methods/`.

### Step 6: Cross-Link

Ensure all pages created/updated in Steps 3-5 have:
- Wikilinks in body text pointing to related pages
- `sources` frontmatter listing relevant source page slugs
- `related` frontmatter maintained bidirectionally

### Step 7: Update synthesis.md

Read current `wiki/synthesis.md`. If this source adds significant new understanding:
- Update incrementally. **Never rewrite from scratch.**
- Add new themes, refine existing understanding, note contradictions.
- If the source is minor or confirmatory, skip and note "synthesis unchanged" in log.
- If this is the **first source**, create the initial synthesis structure.

### Step 8: Update index.md

Add entries for every new page. Update descriptions for materially changed pages. Follow the index format (Section 9).

### Step 9: Append to log.md

Append a new entry following the log format (Section 8). Include counts of new and updated pages.

### Step 10: Update hashlog

Append the source file's SHA256 hash to `wiki/.hashlog`. Format: one line per ingested source.

```
# wiki/.hashlog — SHA256 hashes of ingested sources. Do not edit manually.
a1b2c3d4...  raw/papers/attention-is-all-you-need.pdf  2026-04-07
e5f6a7b8...  raw/refs/karpathy-tweet.md  2026-04-07
```

For URL sources (no local file), record `URL:<url>` in place of the file path.

### Completion

Report to user: list of created/updated pages with wikilinks, synthesis status.

---

## 6. Workflow: Checkpoint

**Trigger:** User says "checkpoint", "snapshot", "take stock", "milestone", or "progress report".

### Level Determination

Ask user: **Snapshot** (quick status, ~1 page) or **Report** (detailed analysis, ~3-5 pages)? Default to snapshot if unspecified.

### Step 1: Gather Metrics

Count all pages by type (scan filesystem). Read the last checkpoint to compute deltas.

### Step 2: Determine Checkpoint ID

Read existing checkpoints in `wiki/checkpoints/`. New ID = max(existing) + 1. First checkpoint = 1.

### Step 3: Write Checkpoint

#### Snapshot Body Template

```markdown
## Current Phase
[1-2 sentences describing where the project stands]

## Key Findings
- [3-7 bullets of most important discoveries so far]

## Open Questions
- [3-5 bullets of unresolved questions]

## Next Steps
- [3-5 bullets of planned actions]

## Wiki Status
- Papers: N (+M since last checkpoint)
- Concepts: N (+M)
- Methods: N (+M)
- Experiments: N (+M)
- Threads: N (+M)
```

#### Report Body Template

```markdown
## Executive Summary
[2-3 paragraphs summarizing overall project status]

## Knowledge Coverage Map

| Theme | Coverage | Key Sources | Gaps |
|-------|----------|-------------|------|
| ...   | ...      | ...         | ...  |

## Key Findings by Theme

### [Theme 1]
[Findings with citations]

### [Theme 2]
[Findings with citations]

## Contradictions and Unresolved Questions
- [List with evidence from both sides]

## Gap Analysis
- **Missing topics**: [concepts/methods not yet covered]
- **Thin areas**: [topics with only 1-2 sources]
- **Needed sources**: [specific papers/data to look for]

## Evolution Since Last Checkpoint
[Quantitative deltas and qualitative changes]

## Recommendations
- [Specific prioritized next steps]
```

### Step 4: Update index.md and log.md

---

## 7. Workflow: Query

**Trigger:** User asks a question about wiki content ("what does the wiki say about...", "compare X and Y", "summarize...").

### Tiered Search Strategy (minimize token usage)

Use a layered approach — stop as soon as you have enough information:

**Tier 1: Index scan (cheap).** Read `wiki/index.md` only. If the question can be answered from page titles and descriptions alone (e.g., "do we have a page on X?", "how many papers?"), answer immediately. Stop here.

**Tier 2: Targeted read (moderate).** If Tier 1 is insufficient, identify the 3-5 most relevant pages from the index. Read only those pages. For most queries this is enough. Stop here.

**Tier 3: Broad search (expensive).** If Tier 2 is insufficient, use Grep across `wiki/` for query terms to find additional relevant pages. Read up to 10-15 pages total. Also read `wiki/synthesis.md` for cross-cutting themes.

Always prefer reading fewer pages. **Do not read all pages by default.** The index exists to avoid this.

### Synthesize

Compose an answer based on wiki content. Cite with wikilinks. If wiki content is insufficient, say so and identify what sources or pages would fill the gap.

### Optionally File

If the answer is a significant synthesis, comparison, or investigation worth preserving, ask: "This seems worth filing as a thread. Shall I create a thread page?" If yes: create in `wiki/threads/`, update index and log.

---

## 8. Workflow: Lint

**Trigger:** User says "lint", "health check", "check the wiki", "validate".

### Checks

1. **Orphan pages** — files in `wiki/` subdirectories not listed in `index.md`
2. **Broken wikilinks** — `[[...]]` targets with no matching file
3. **Missing frontmatter** — required fields absent or empty for the page's type
4. **Stale pages** — pages not updated after newer related sources were ingested
5. **Duplicate entities** — overlapping aliases or very similar slugs across concept/method pages
6. **Index accuracy** — every wiki file has an index entry; every index entry has a file
7. **Source backlinks** — `sources` list entries match actual source pages
8. **Synthesis freshness** — `synthesis.md` references recent sources

### Output

Structured report with a Summary line, then each category (listing issues found or "Clean"), ending with prioritized Recommendations. Then ask: "Shall I fix the issues I can fix automatically?"

---

## 9. Index Format (`wiki/index.md`)

Organized into sections by page type with counts in headings. Each entry is one line: wikilink + description.

```markdown
## Papers (N)
- [[src-attention-is-all-you-need]] — Introduces transformer architecture with self-attention mechanism
- [[src-bert]] — Pre-trained bidirectional representations for NLP

## Concepts (N)
- [[self-attention]] — Mechanism for computing token-to-token relevance
- [[transfer-learning]] — Leveraging pre-trained representations for downstream tasks

## Methods (N)
- [[transformer]] — algorithm — Encoder-decoder architecture based on self-attention
- [[adam-optimizer]] — algorithm — Adaptive learning rate optimizer

## Experiments (N)
- [[baseline-accuracy-test]] — completed — Initial accuracy benchmark on test set

## Threads (N)
- [[scaling-vs-architecture]] — open — Investigating whether scale or architecture matters more

## Checkpoints (N)
- [[cp-001-initial-survey]] — snapshot — 2026-04-07 — 5 papers, 12 concepts, 8 methods
```

Entries sorted chronologically within each section (newest last). Counts updated on every change.

---

## 10. Log Format (`wiki/log.md`)

Append-only. Each entry is an H2 heading with ISO date, operation type, and brief title. Body is bullet list.

### Operation types

`ingest`, `query`, `checkpoint`, `lint`, `update`, `thread`

### Format

```markdown
## [YYYY-MM-DD] ingest | Paper Title
- Source: raw/papers/filename.pdf
- Created: src-paper-slug, concept-name, method-name
- Updated: existing-concept (added new findings)
- New pages: 3, Updated pages: 1
- Synthesis: updated (added new theme)

## [YYYY-MM-DD] checkpoint | Phase Name
- Type: snapshot
- ID: cp-001
- Papers: 5, Concepts: 12, Methods: 8, Experiments: 2, Threads: 3

## [YYYY-MM-DD] query | User Question Summary
- Searched: 4 pages
- Filed as thread: no

## [YYYY-MM-DD] lint | Health Check
- Issues found: 2 orphan pages, 1 broken link
- Auto-fixed: 2, Remaining: 1
```

---

## 11. Obsidian Compatibility

1. **Wikilinks only** for internal references — `[[slug]]` or `[[slug|Display Text]]`.
2. **Frontmatter** is displayed in Obsidian's Properties panel. All dates in ISO format for native recognition.
3. **Tags** only in frontmatter `tags` field, never inline `#tag` in body text.
4. **Aliases** in frontmatter are recognized by Obsidian for search and link resolution.
5. **Images** from `raw/` referenced with relative paths: `![[../raw/papers/figure.png]]` or `![](../raw/papers/figure.png)`.

### Example Dataview Queries

```dataview
TABLE authors, year, venue
FROM "wiki/papers"
WHERE type = "paper"
SORT year DESC
```

```dataview
LIST
FROM "wiki/concepts"
WHERE contains(sources, "src-attention-is-all-you-need")
```

```dataview
TABLE status, date
FROM "wiki/experiments"
SORT date DESC
```

```dataview
TABLE detail_level, paper_count, concept_count
FROM "wiki/checkpoints"
SORT checkpoint_id DESC
```

---

## 12. Rules and Guardrails

1. **Never delete wiki pages.** If a page becomes obsolete, add `deprecated: true` to frontmatter and note the reason.
2. **Never modify files in `raw/`.** Read only.
3. **Never edit earlier log entries.** Log is append-only.
4. **Always update the `updated` date** on any page modification.
5. **Always check for duplicates** before creating concept/method pages (search index + aliases).
6. **Always confirm with user** before proceeding with ingest (Step 2 gate).
7. **Preserve existing content** when updating pages — add, refine, or annotate. Never silently drop information.
8. **Consistent citation style**: `[[src-slug|Author et al. (Year)]]` in running text.
9. **Clean frontmatter**: no trailing spaces, `[]` for empty lists, omit optional fields that are empty.
10. **When in doubt, ask.** The user is the architect; Claude is the builder.
