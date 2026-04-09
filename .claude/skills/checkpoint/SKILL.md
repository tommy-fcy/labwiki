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

- If first argument is `snapshot` or `report`, use that level
- Otherwise, ask user. Default to snapshot.

## Steps

1. **Gather metrics** — count files in `wiki/sources/`, `wiki/experiments/`, `wiki/threads/`, `wiki/areas/` (as applicable)
2. **Determine checkpoint ID** — scan `wiki/checkpoints/`, new ID = max + 1
3. **Write checkpoint page** using the template from CLAUDE.md
4. **Update index.md and log.md**

## Examples

```
/checkpoint snapshot initial-survey
/checkpoint report literature-review-complete
/checkpoint
```
