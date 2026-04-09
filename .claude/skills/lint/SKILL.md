---
name: lint
description: Health-check the wiki. Finds orphan pages, broken links, missing frontmatter, stale content, and other issues.
allowed-tools: Read Write Edit Glob Grep Bash
---

# Lint Wiki

Follow the **Workflow: Lint** defined in CLAUDE.md.

## Checks

1. **Orphan pages** — files in `wiki/` subdirectories not listed in `wiki/index.md`
2. **Broken wikilinks** — `[[...]]` targets with no matching file
3. **Missing frontmatter** — required fields absent or empty for the page's type
4. **Stale pages** — pages not updated after newer related sources were ingested
5. **Index accuracy** — every wiki file has an index entry; every index entry has a file
6. **Synthesis/landscape freshness** — references recent sources

## Output

Structured report, then ask: "Shall I fix what I can?"
