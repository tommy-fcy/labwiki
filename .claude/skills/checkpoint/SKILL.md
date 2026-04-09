---
name: checkpoint
description: Create a checkpoint of the wiki's current state. Produces either a lightweight snapshot or a detailed report.
argument-hint: [snapshot|report] [phase-name]
allowed-tools: Read Write Edit Glob Grep Bash
---

# Checkpoint

Create a wiki checkpoint. Arguments: $ARGUMENTS

Follow the **Workflow: Checkpoint** defined in CLAUDE.md.

## Level Determination

Parse arguments:
- If first argument is `snapshot` or `report`, use that level
- If first argument is neither, treat entire argument as the phase name and ask user for level
- If no arguments, ask user: "Snapshot (quick status, ~1 page) or Report (detailed analysis, ~3-5 pages)?"
- The remaining argument (or second argument) is the phase name for the slug

## Steps

1. **Gather metrics** — count all wiki pages by type:
   - Count files in `wiki/sources/`, `wiki/concepts/`, `wiki/methods/`, `wiki/experiments/`, `wiki/threads/`
   - Read the last checkpoint (if any) to compute deltas

2. **Determine checkpoint ID** — scan `wiki/checkpoints/`, new ID = max(existing) + 1, first = 1

3. **Write checkpoint page** at `wiki/checkpoints/cp-{NNN}-{slug}.md`
   - Use the snapshot or report body template from CLAUDE.md Section 6
   - Fill frontmatter with all counts
   - For **report**: read `wiki/synthesis.md` and key wiki pages to produce the detailed analysis

4. **Update `wiki/index.md`** — add checkpoint entry with detail_level, date, and counts

5. **Append to `wiki/log.md`**

## Examples

```
/checkpoint snapshot initial-survey
/checkpoint report literature-review-complete
/checkpoint                              # will ask for level and name
```
