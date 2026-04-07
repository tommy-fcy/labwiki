---
name: lint
description: Health-check the wiki. Finds orphan pages, broken links, missing frontmatter, stale content, duplicates, and other issues.
allowed-tools: Read Write Edit Glob Grep Bash
---

# Lint Wiki

Run a health check on the LabWiki. Follow the **Workflow: Lint** defined in CLAUDE.md.

## Checks

Run all 8 checks:

1. **Orphan pages** — files in `wiki/` subdirectories not listed in `wiki/index.md`
2. **Broken wikilinks** — `[[...]]` targets in wiki pages with no matching file
3. **Missing frontmatter** — required fields absent or empty for the page's type (check against schemas in CLAUDE.md)
4. **Stale pages** — pages not updated after newer related sources were ingested
5. **Duplicate entities** — overlapping aliases or very similar slugs across concept/method pages
6. **Index accuracy** — every wiki file has an index entry; every index entry has a file
7. **Source backlinks** — `sources` list entries in concept/method pages match actual source pages in `wiki/papers/`
8. **Synthesis freshness** — `wiki/synthesis.md` references recent sources

## Process

1. Use Glob to list all `.md` files in `wiki/` subdirectories
2. Read `wiki/index.md` to get the catalog
3. For each check, scan relevant files and collect issues
4. Present a structured report:

```
## Wiki Health Check

**Summary**: X issues found across Y checks

### 1. Orphan Pages — [N issues | Clean]
- ...

### 2. Broken Wikilinks — [N issues | Clean]
- ...

(etc.)

### Recommendations
1. [Prioritized fix suggestions]
```

5. Ask: "Shall I fix the issues I can fix automatically?"
6. If user agrees, fix and log the changes
