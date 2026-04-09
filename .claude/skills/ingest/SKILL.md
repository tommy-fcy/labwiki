---
name: ingest
description: Ingest sources into the wiki. With no arguments, scans raw/ for unprocessed sources (via hashlog) and ingests them. With a path argument, ingests that specific source.
argument-hint: [path]
allowed-tools: Read Write Edit Glob Grep Bash WebFetch Agent
---

# Ingest Sources

Arguments: $ARGUMENTS

Follow the **Workflow: Ingest** defined in CLAUDE.md exactly.

## Mode Detection

- **No arguments** → **Batch mode**: scan `raw/` for unprocessed sources via hashlog, ingest each.
- **With path argument** → **Single mode**: ingest that specific source.

## Batch Mode (no arguments)

1. Scan all files in `raw/` recursively (skip `.gitkeep`)
2. Read `wiki/.hashlog` to get SHA256 hashes of already-ingested sources
3. Compute SHA256 for each file (`sha256sum` or `certutil -hashfile`)
4. Ingest all unprocessed sources automatically — no need to ask
5. For multiple sources: dispatch parallel Agent subprocesses. Collect results, then update synthesis/landscape/index/log/hashlog once at the end.

## Single Mode (with path)

1. **Check hashlog** — if already ingested, ask user: re-ingest or skip?
2. **Read the source** thoroughly
3. **Present key takeaways** to user: title, type, 3-5 key points, proposed tags, connections to existing content
4. **WAIT for user confirmation**
5. **Create source page** in `wiki/sources/src-{slug}.md` — concise, use tags for concepts/methods
6. **Update synthesis.md** (project) or **area page + landscape.md** (library) if significant
7. **Update index.md** and **append to log.md**
8. **Update hashlog**

## Rules

- Check CLAUDE.md for frontmatter schemas and naming conventions
- Source pages should be concise — distill, don't transcribe
- Use `[[wikilink]]` format for all internal references
- Citation style: `[[src-slug|Author et al. (Year)]]`
- Never skip the user confirmation gate
