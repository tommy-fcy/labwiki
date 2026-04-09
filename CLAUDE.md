# LabWiki

This is the LabWiki template repository. It is not an active wiki — it contains templates and tools for creating new wikis.

## To create a new wiki

1. Copy this repository
2. Choose a mode and copy the template to `CLAUDE.md`:
   - `cp templates/project.md CLAUDE.md` — focused on one research topic
   - `cp templates/library.md CLAUDE.md` — broad knowledge accumulation across areas
3. Run `claude` — Claude will read `CLAUDE.md` and guide you through setup

## Repository contents

- `templates/project.md` — Project mode schema (single topic, deep dive)
- `templates/library.md` — Library mode schema (multi-area, broad reading)
- `templates/wiki-library/` — Scaffold files for library mode (landscape.md, index.md, log.md)
- `tools/fetch.py` — Zero-token URL fetcher for `/add` skill
- `.claude/skills/` — Slash commands: `/add`, `/ingest`, `/query`, `/checkpoint`, `/lint`
- `wiki/` — Wiki scaffold files (index.md, synthesis.md, log.md) for project mode
- `raw/` — Empty source directories (`papers/`, `notes/`, `experiments/`, `refs/`, `repos/`)
