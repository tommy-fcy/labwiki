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

This is a personal research library maintained by Claude Code. Unlike the project mode (focused on one topic), library mode is for **broad knowledge accumulation** — reading papers, blogs, and notes across many areas to build macro-level understanding and research taste.

The wiki is a persistent, compounding artifact. Claude owns all wiki content; the user owns sources, direction, and judgment.

### First Run

If the `name` field above is empty, this is a fresh copy of LabWiki (library mode). Before doing anything else:
1. Ask the user what this library is for (e.g., "AI research", "Machine Learning", "CS broadly").
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
│   ├── papers/            # Paper/source summaries (one per ingested source)
│   ├── concepts/          # Theoretical concepts, ideas, phenomena
│   ├── methods/           # Techniques, algorithms, tools, frameworks
│   ├── threads/           # Cross-area investigations, comparisons, insights
│   └── checkpoints/       # Periodic review snapshots
```

### Rules

- `raw/` is **immutable**. Claude reads from it but never creates, modifies, or deletes files here.
- `wiki/` is **Claude-maintained**. Every file here is created or updated by Claude following the workflows below. The user reads it; Claude writes it.
- `wiki/log.md` is **append-only**. Claude appends to the end; never edits earlier entries.

---

## 2. Page Types and Frontmatter

All wiki pages use YAML frontmatter enclosed in `---`. Every page has a base schema; each type extends it.

### 2.1 Base Schema (shared by all pages)

```yaml
---
title: "Human-Readable Title"
type: paper | concept | method | area | thread | checkpoint
area: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
---
```

- `title` — Required. Natural language display name.
- `type` — Required. One of the six enumerated values.
- `area` — Required for papers, concepts, and methods. The primary area this page belongs to. Must match an existing area slug. A page can only belong to one primary area; use `tags` for secondary associations.
- `created` / `updated` — Required. ISO date. Update `updated` on every modification.
- `tags` — YAML list. Lowercase, hyphenated. Only in frontmatter, never inline `#tag`.
- `sources` — YAML list of source page slugs that informed this page.
- `related` — YAML list of related wiki page slugs. Maintain bidirectionally.

### 2.2 Area Page (`wiki/areas/{slug}.md`)

```yaml
---
title: "Area Name"
type: area
aliases: []
paper_count: 0
concept_count: 0
method_count: 0
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
related: []
---
```

Area pages are **mini-syntheses** for each research domain. They are the primary organizing unit.

Body sections:
- **Overview** — What this area is about (2-3 sentences)
- **State of the Art** — Current best understanding, key results
- **Key Themes** — Major sub-topics and directions
- **Open Problems** — Unresolved questions and active research fronts
- **Key Papers** — Wikilinks to the most important papers in this area
- **Key Concepts** — Wikilinks to core concepts
- **Connections** — How this area relates to other areas

### 2.3 Paper Page (`wiki/papers/src-{slug}.md`)

```yaml
---
title: "Paper Title"
type: paper
area: "compression"
source_type: journal | conference | preprint | thesis | report | book-chapter | survey | blog | tweet | note | repo
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
- **Takeaways** — Personal relevance, what to remember, how it shapes understanding
- **Extracted Entities** — Wikilinks to concept/method pages touched by this paper
- **Notes** — Anything else notable, limitations, open questions

### 2.4 Concept Page (`wiki/concepts/{slug}.md`)

```yaml
---
title: "Concept Name"
type: concept
area: "compression"
aliases: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
---
```

Body sections:
- **Definition** — Concise definition
- **Explanation** — Detailed explanation with context
- **Key Aspects** — Important properties or sub-topics
- **Connections** — How this relates to other concepts/methods (with wikilinks)
- **Open Questions** — Unresolved aspects

### 2.5 Method Page (`wiki/methods/{slug}.md`)

```yaml
---
title: "Method Name"
type: method
area: "compression"
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
- **Connections** — Relationships to concepts, other methods

### 2.6 Thread Page (`wiki/threads/{slug}.md`)

```yaml
---
title: "Thread Title"
type: thread
thread_type: investigation | comparison | question | cross-area | trend
status: open | resolved | parked
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
related: []
---
```

Threads in library mode often span areas — comparing approaches across domains, noting trends, or connecting ideas from different subfields.

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
title: "Checkpoint: Review Name"
type: checkpoint
checkpoint_id: 1
detail_level: snapshot | report
paper_count: 0
concept_count: 0
method_count: 0
area_count: 0
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
| Area | `{slug}.md` | `wiki/areas/` | `compression.md` |
| Paper | `src-{slug}.md` | `wiki/papers/` | `src-svd-llm.md` |
| Concept | `{slug}.md` | `wiki/concepts/` | `singular-value-decomposition.md` |
| Method | `{slug}.md` | `wiki/methods/` | `svd-llm.md` |
| Thread | `{slug}.md` | `wiki/threads/` | `pruning-vs-quantization.md` |
| Checkpoint | `cp-{NNN}-{slug}.md` | `wiki/checkpoints/` | `cp-001-april-review.md` |

### Deduplication

Before creating any concept, method, or area page, search the wiki for pages with matching slugs or overlapping aliases. If a match exists, **update that page** rather than creating a duplicate.

---

## 4. Linking Conventions

### Wikilinks

- Always use `[[slug]]` or `[[slug|Display Text]]` for internal references.
- Never use markdown-style `[text](path)` for wiki cross-references.
- Obsidian resolves `[[slug]]` by shortest unique path, so bare slugs work across subdirectories.

### Citation Style

Reference papers in running text using display-text form:

```
[[src-svd-llm|Wang et al. (2024)]]
```

### Cross-Reference Targets

- Paper pages: link to area, concepts, and methods they touch
- Concept/method pages: link to area, related concepts, methods, and citing papers
- Area pages: link to key papers, concepts, methods, and related areas
- Thread pages: link to all evidence sources and relevant areas

### Bidirectional Maintenance

When creating or updating page A with a link to page B:
1. Check if page B's `related` frontmatter includes A's slug.
2. If not, add it. This ensures bidirectional discoverability.

---

## 5. Workflow: Ingest

**Trigger:** User provides a source and asks to ingest it, or runs `/ingest` with no arguments for batch mode.

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
   - GitHub repo URL → repo (clone or read README via WebFetch)
   - Google Doc URL → extract document ID, use google_drive_fetch MCP tool (if available)
   - Directory in `raw/repos/` → repo (read README, key source files)

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
2. **Proposed area** — which area this source belongs to (or propose a new area)
3. **3-5 key takeaways** from the source
4. **Proposed entities** — concepts and methods to create or update, with brief rationale
5. **Connections** — how this source relates to existing wiki content (if any)

**Wait for user confirmation before proceeding.** The user may reassign the area, redirect emphasis, or skip certain entities.

### Step 3: Create Paper/Source Summary Page

Create `wiki/papers/src-{slug}.md` with full frontmatter and body sections per the schema. Set the `area` field. Include wikilinks to all concept/method pages.

### Step 4: Update or Create Concept Pages

For each concept identified in Step 2:
- If the page **exists**: read it, add new information from this source, add source slug to `sources` list, update `updated` date.
- If **new**: create `wiki/concepts/{slug}.md` with full frontmatter and body. Set `area` field.

### Step 5: Update or Create Method Pages

Same logic as Step 4, applied to `wiki/methods/`.

### Step 6: Cross-Link

Ensure all pages created/updated in Steps 3-5 have:
- Wikilinks in body text pointing to related pages
- `sources` frontmatter listing relevant source page slugs
- `related` frontmatter maintained bidirectionally

### Step 7: Update Area Page

Read the relevant `wiki/areas/{area}.md`. Update incrementally:
- Add new themes or refine existing understanding
- Update Key Papers / Key Concepts sections with new wikilinks
- Increment `paper_count` / `concept_count` / `method_count`
- If this is a **new area**, create the area page first, then add it to `areas` list in Section 0.

### Step 8: Update landscape.md

Read current `wiki/landscape.md`. If this source adds significant cross-area understanding:
- Update incrementally. **Never rewrite from scratch.**
- Note new trends, connections between areas, or paradigm shifts.
- If the source is minor or within a single area, skip and note "landscape unchanged" in log.

### Step 9: Update index.md

Add entries for every new page. Update descriptions for materially changed pages. Follow the index format (Section 9).

### Step 10: Append to log.md

Append a new entry following the log format (Section 10). Include counts of new and updated pages.

### Step 11: Update hashlog

Append the source file's SHA256 hash to `wiki/.hashlog`. Format: one line per ingested source.

```
# wiki/.hashlog — SHA256 hashes of ingested sources. Do not edit manually.
a1b2c3d4...  raw/papers/svd-llm.md  2026-04-08
e5f6a7b8...  raw/refs/karpathy-tweet.md  2026-04-08
```

### Completion

Report to user: list of created/updated pages with wikilinks, area assignment, landscape status.

---

## 6. Workflow: Checkpoint

**Trigger:** User says "checkpoint", "review", "take stock", or "what have I learned".

### Level Determination

Ask user: **Snapshot** (quick status, ~1 page) or **Report** (detailed review, ~3-5 pages)? Default to snapshot if unspecified.

### Step 1: Gather Metrics

Count all pages by type and by area. Read the last checkpoint to compute deltas.

### Step 2: Determine Checkpoint ID

Read existing checkpoints in `wiki/checkpoints/`. New ID = max(existing) + 1. First checkpoint = 1.

### Step 3: Write Checkpoint

#### Snapshot Body Template

```markdown
## Reading Status
[1-2 sentences on what areas have been active recently]

## Key Takeaways Since Last Review
- [3-7 bullets of most important things learned]

## Areas by Coverage

| Area | Papers | Concepts | Methods | Trend |
|------|--------|----------|---------|-------|
| ...  | ...    | ...      | ...     | ...   |

## Emerging Themes
- [Cross-area patterns or insights]

## Reading Queue / Gaps
- [Areas that need more sources, specific papers to look for]
```

#### Report Body Template

```markdown
## Overview
[2-3 paragraphs on the current state of the library and what has been learned]

## Area Deep Dives

### [Area 1]
- Coverage: N papers, M concepts
- State of understanding: [summary]
- Key open questions: [list]

### [Area 2]
...

## Cross-Area Insights
- [Connections, patterns, and trends that span multiple areas]

## Knowledge Gaps
- **Under-explored areas**: [areas with few sources]
- **Missing perspectives**: [viewpoints or approaches not yet represented]
- **Recommended reading**: [specific papers/blogs to look for]

## Research Taste Evolution
- [How the user's interests and understanding have shifted over time]

## Recommendations
- [Where to focus reading next]
```

### Step 4: Update index.md and log.md

---

## 7. Workflow: Query

**Trigger:** User asks a question about the library content.

### Tiered Search Strategy (minimize token usage)

Use a layered approach — stop as soon as you have enough information:

**Tier 1: Index scan (cheap).** Read `wiki/index.md` only. If the question can be answered from page titles and descriptions alone, answer immediately. Stop here.

**Tier 2: Targeted read (moderate).** If Tier 1 is insufficient, identify the 3-5 most relevant pages from the index. Read only those pages. For most queries this is enough. Stop here.

**Tier 3: Area-scoped search (moderate+).** If the question is about a specific area, read the area page first, then follow its key paper/concept links. This avoids reading unrelated areas.

**Tier 4: Broad search (expensive).** If Tier 2-3 are insufficient, use Grep across `wiki/` for query terms. Read up to 10-15 pages total. Also read `wiki/landscape.md` for cross-area themes.

Always prefer reading fewer pages. **Do not read all pages by default.** The index and area pages exist to avoid this.

### Synthesize

Compose an answer based on wiki content. Cite with wikilinks. If wiki content is insufficient, say so and identify what sources or pages would fill the gap.

### Optionally File

If the answer is a significant cross-area insight or comparison worth preserving, ask: "This seems worth filing as a thread. Shall I create a thread page?" If yes: create in `wiki/threads/`, update index and log.

---

## 8. Workflow: Lint

**Trigger:** User says "lint", "health check", "check the wiki", "validate".

### Checks

1. **Orphan pages** — files in `wiki/` subdirectories not listed in `index.md`
2. **Broken wikilinks** — `[[...]]` targets with no matching file
3. **Missing frontmatter** — required fields absent or empty for the page's type
4. **Missing area** — papers/concepts/methods without an `area` field
5. **Stale area pages** — area pages not updated after newer sources were ingested for that area
6. **Duplicate entities** — overlapping aliases or very similar slugs
7. **Index accuracy** — every wiki file has an index entry; every index entry has a file
8. **Source backlinks** — `sources` list entries match actual source pages
9. **Landscape freshness** — `landscape.md` references recent sources

### Output

Structured report with a Summary line, then each category (listing issues found or "Clean"), ending with prioritized Recommendations. Then ask: "Shall I fix the issues I can fix automatically?"

---

## 9. Index Format (`wiki/index.md`)

Organized into sections by page type with counts in headings. Each entry is one line: wikilink + description.

```markdown
## Areas (N)
- [[compression]] — Model compression: quantization, pruning, SVD, distillation
- [[reasoning]] — LLM reasoning capabilities and methods

## Papers (N)
- [[src-svd-llm]] — [compression] SVD-based LLM compression with truncation-aware whitening
- [[src-chain-of-thought]] — [reasoning] Chain-of-thought prompting for reasoning

## Concepts (N)
- [[singular-value-decomposition]] — [compression] Matrix factorization for dimensionality reduction
- [[chain-of-thought]] — [reasoning] Step-by-step reasoning in LLM outputs

## Methods (N)
- [[svd-llm]] — [compression] algorithm — Truncation-aware SVD compression

## Threads (N)
- [[pruning-vs-quantization]] — cross-area — Comparing two compression paradigms

## Checkpoints (N)
- [[cp-001-april-review]] — snapshot — 2026-04-08 — 5 papers, 3 areas
```

Entries include `[area]` tag for quick visual grouping. Sorted chronologically within each section (newest last). Counts updated on every change.

---

## 10. Log Format (`wiki/log.md`)

Append-only. Each entry is an H2 heading with ISO date, operation type, and brief title. Body is bullet list.

### Operation types

`ingest`, `query`, `checkpoint`, `lint`, `update`, `thread`

### Format

```markdown
## [YYYY-MM-DD] ingest | Paper Title
- Source: raw/papers/filename.md
- Area: compression
- Created: src-paper-slug, concept-name, method-name
- Updated: existing-concept (added new findings)
- New pages: 3, Updated pages: 1
- Area page: updated
- Landscape: unchanged

## [YYYY-MM-DD] checkpoint | Review Name
- Type: snapshot
- ID: cp-001
- Papers: 15, Concepts: 20, Methods: 10, Areas: 4, Threads: 3

## [YYYY-MM-DD] query | User Question Summary
- Searched: 4 pages
- Filed as thread: no
```

---

## 11. Obsidian Compatibility

1. **Wikilinks only** for internal references — `[[slug]]` or `[[slug|Display Text]]`.
2. **Frontmatter** is displayed in Obsidian's Properties panel. All dates in ISO format for native recognition.
3. **Tags** only in frontmatter `tags` field, never inline `#tag` in body text.
4. **Aliases** in frontmatter are recognized by Obsidian for search and link resolution.
5. **Images** from `raw/` referenced with relative paths.

### Example Dataview Queries

```dataview
TABLE paper_count, concept_count, method_count
FROM "wiki/areas"
WHERE type = "area"
SORT paper_count DESC
```

```dataview
TABLE area, authors, year, venue
FROM "wiki/papers"
WHERE type = "paper"
SORT year DESC
```

```dataview
TABLE area
FROM "wiki/concepts"
WHERE area = "compression"
SORT title ASC
```

```dataview
TABLE detail_level, paper_count, area_count
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
7. **Always assign an area** to every paper, concept, and method page.
8. **Preserve existing content** when updating pages — add, refine, or annotate. Never silently drop information.
9. **Consistent citation style**: `[[src-slug|Author et al. (Year)]]` in running text.
10. **Clean frontmatter**: no trailing spaces, `[]` for empty lists, omit optional fields that are empty.
11. **When in doubt, ask.** The user is the architect; Claude is the builder.
