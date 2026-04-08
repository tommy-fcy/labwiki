# LabWiki

A lightweight, LLM-maintained knowledge base for research, inspired by [Andrej Karpathy's idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Drop in sources, ask questions, and let Claude Code build and maintain a structured wiki that compounds over time.

## What is this?

Most people's experience with LLMs and documents is **retrieval**: upload files, the LLM finds relevant chunks, generates an answer, and forgets everything. Nothing accumulates.

LabWiki is different. Instead of retrieving from raw documents on every query, the LLM **incrementally builds a persistent wiki** — summaries, concept pages, method pages, cross-references, and an evolving synthesis. Knowledge is compiled once and kept current. The cross-references are already there. The contradictions have been flagged. Each new source makes the whole wiki richer.

You never write the wiki yourself. You curate sources, ask questions, and direct the analysis. The LLM does all the summarizing, cross-referencing, filing, and bookkeeping.

## How it works

```
You add sources ──→ Claude reads & discusses ──→ Wiki pages get created/updated
You ask questions ──→ Claude searches the wiki ──→ Synthesized answer with citations
You say "checkpoint" ──→ Claude takes stock ──→ Milestone snapshot saved
```

Three layers:

- **`raw/`** — Your source materials (papers, notes, data). Immutable. Claude reads but never modifies.
- **`wiki/`** — Claude-maintained knowledge base. Summaries, concepts, methods, experiments, threads, checkpoints.
- **`CLAUDE.md`** — The schema that tells Claude how to operate. This is what makes it work.

## Quick start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- [GitHub CLI](https://cli.github.com/) (`gh`) installed
- [Obsidian](https://obsidian.md/) (recommended for browsing, not required)

### Setup

1. **Clone** this repository:
   ```bash
   git clone https://github.com/tommy-fcy/labwiki.git my-research-topic
   cd my-research-topic
   ```

2. **Install [Claudian](https://github.com/YishenTu/claudian)** (optional — Claude Code inside Obsidian):

   macOS / Linux:
   ```bash
   mkdir -p .obsidian/plugins/claudian && gh release download --repo YishenTu/claudian --pattern "main.js" --pattern "manifest.json" --pattern "styles.css" --dir .obsidian/plugins/claudian
   ```

   Windows (PowerShell):
   ```powershell
   mkdir -Force .obsidian\plugins\claudian | Out-Null; gh release download --repo YishenTu/claudian --pattern "main.js" --pattern "manifest.json" --pattern "styles.css" --dir .obsidian\plugins\claudian
   ```

   Then in Obsidian: Settings → Community Plugins → disable Restricted Mode → enable **Claudian**.

3. **Open in Claude Code**:
   ```bash
   claude
   ```
   Claude reads `CLAUDE.md` and asks you to fill in the project identity (topic, description).

4. **Open in Obsidian** (optional): Open the project folder as an Obsidian vault. Browse the wiki with graph view, Dataview queries, and wikilink navigation.

### Usage

**Add sources:**
```
/add https://arxiv.org/abs/1706.03762 paper
/add https://x.com/karpathy/status/123456 ref
```

**Ingest into wiki:**
```
/ingest                              # process all new sources in raw/
/ingest raw/papers/attention.pdf     # process one specific source
```

**Ask questions:**
```
/query What methods exist for improving transformer efficiency?
/query Compare self-attention and cross-attention mechanisms
```

**Checkpoint:**
```
/checkpoint snapshot initial-survey
/checkpoint report literature-review-complete
```

**Health check:**
```
/lint
```

## Directory structure

```
labwiki/
├── CLAUDE.md              # Schema — the brain of the system
├── raw/                   # Your source materials (immutable)
│   ├── papers/            # Academic papers
│   ├── notes/             # Personal notes, meeting notes
│   ├── experiments/       # Experiment data, results
│   └── refs/              # Slides, docs, web clips, misc
├── code/                  # Project code, scripts, notebooks
└── wiki/                  # Claude-maintained knowledge base
    ├── index.md           # Master catalog
    ├── log.md             # Operation log (append-only)
    ├── synthesis.md       # Evolving project thesis
    ├── papers/            # Paper summaries
    ├── concepts/          # Theoretical concepts
    ├── methods/           # Techniques, tools, algorithms
    ├── experiments/       # Experiment tracking
    ├── threads/           # Research investigations
    └── checkpoints/       # Milestone snapshots
```

## Slash commands

| Command | What it does |
|---------|-------------|
| `/add <url-or-path> [type]` | Fetch a source and save to `raw/` (no wiki processing) |
| `/ingest` | Scan `raw/` for new sources and ingest them all into the wiki |
| `/ingest <path>` | Ingest a specific source into the wiki |
| `/query <question>` | Search the wiki, synthesize an answer, optionally file as a thread |
| `/checkpoint [snapshot\|report] [name]` | Create a milestone snapshot or detailed report |
| `/lint` | Health-check the wiki (orphan pages, broken links, stale content) |

## Workflows

### Ingest

When you ingest a source, Claude:
1. Reads the source material
2. Presents key takeaways and proposed entities (**waits for your confirmation**)
3. Creates a paper summary page
4. Creates or updates concept and method pages
5. Cross-links everything
6. Updates the synthesis, index, and log

### Checkpoint

Two levels:
- **Snapshot** (~1 page): Current phase, key findings, open questions, next steps
- **Report** (~3-5 pages): Executive summary, coverage map, findings by theme, gap analysis, recommendations

### Query

Claude searches the wiki, synthesizes an answer with citations, and optionally files significant analyses as thread pages.

## Obsidian compatibility

- All internal links use `[[wikilink]]` format
- YAML frontmatter on every page (works with Obsidian Properties and Dataview)
- Tags only in frontmatter — clean for Dataview queries
- Graph view shows the knowledge structure

## Design philosophy

- **No code, no scripts, no dependencies.** Just markdown files and a schema. Copy the directory and it works anywhere with Claude Code.
- **Human directs, LLM executes.** You choose what to ingest and what to emphasize. Claude does the bookkeeping.
- **Knowledge compounds.** Every source makes the wiki richer. Every question can become a permanent thread.
- **Same initialization.** Copy the template for any new research topic. The structure is domain-agnostic.

## References

- [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the original idea of LLM-maintained personal knowledge bases
- [Graphify](https://github.com/safishamsi/graphify) — token-efficient knowledge graph framework; LabWiki borrows its hashlog caching, tiered search, and parallel agent patterns

## License

MIT
