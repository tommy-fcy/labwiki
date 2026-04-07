---
name: query
description: Query the wiki for information. Uses a tiered search strategy to minimize token usage. Synthesizes an answer with citations, and optionally files the result as a thread.
argument-hint: <question>
allowed-tools: Read Write Edit Glob Grep Bash
---

# Query Wiki

Answer the following question using the wiki: $ARGUMENTS

Follow the **Workflow: Query** defined in CLAUDE.md. Use the tiered search strategy.

## Tiered Search (stop as soon as you have enough)

### Tier 1: Index scan (cheap)

Read `wiki/index.md` only. Check if the question can be answered from page titles and one-line descriptions alone.

Examples that Tier 1 can handle:
- "Do we have a page on X?" → check index
- "How many papers have we ingested?" → count entries
- "List all methods" → read Methods section

**If sufficient, answer immediately and stop. Do not read any other pages.**

### Tier 2: Targeted read (moderate)

If Tier 1 is insufficient, identify the **3-5 most relevant pages** from the index. Read only those pages. This handles most queries:
- "What does paper X say about Y?"
- "Explain concept Z"
- "What method did experiment W use?"

**If sufficient, answer and stop.**

### Tier 3: Broad search (expensive)

Only if Tier 2 is insufficient:
- Use Grep across `wiki/` for query terms to find additional pages
- Read `wiki/synthesis.md` for cross-cutting themes
- Read up to **10-15 pages total** (hard cap)

This is for complex synthesis questions:
- "Compare all methods for X"
- "What contradictions exist in the literature?"
- "Summarize everything we know about Y"

## Synthesize

Compose an answer based on wiki content:
- Cite sources with wikilinks: `[[src-slug|Author et al. (Year)]]`
- Reference concept/method pages: `[[slug]]`
- If wiki content is insufficient, explicitly state what's missing

## Optionally File

If the answer is a significant synthesis or comparison worth preserving, ask:
> "This analysis seems worth filing as a thread. Shall I create a thread page?"

If yes: create `wiki/threads/{slug}.md`, update index and log.
