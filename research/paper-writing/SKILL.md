---
name: paper-writing
description: End-to-end academic paper production pipeline from literature search to final submission. Use for ANY research paper task: searching papers, writing sections, generating figures/tables, LaTeX formatting, citation management, compilation, or peer review responses.
---

# Paper Writing Meta-Skill

Complete academic paper production system consolidating 19 specialized capabilities.

## Quick Access by Phase

| Phase | Command | Reference File |
|-------|---------|----------------|
| **00. Pipeline Overview** | — | `refs/00-pipeline-overview.md` |
| **01. Literature** | `paper-writing search [topic]` | `refs/01-literature-phase.md` |
| **02. Ideation** | `paper-writing novelty [idea]` | `refs/02-ideation-phase.md` |
| **03. Experiments** | `paper-writing analyze [data]` | `refs/03-experiments-phase.md` |
| **04. Visualization** | `paper-writing viz [data]` | `refs/04-visualization-phase.md` |
| **05. Writing** | `paper-writing write [section]` | `refs/05-writing-phase.md` |
| **06. Formatting** | `paper-writing format [venue]` | `refs/06-formatting-phase.md` |
| **07. Assembly** | `paper-writing assemble [dir]` | `refs/07-assembly-phase.md` |
| **08. Revision** | `paper-writing revise [reviews]` | `refs/08-revision-phase.md` |
| **09. Advanced** | `paper-writing survey [topic]` | `refs/09-advanced-phase.md` |

## Available Scripts (35+)

See `refs/scripts-index.md` for complete script catalog organized by phase.

## Common Workflows

- **New Paper**: Start at `refs/01-literature-phase.md`
- **Add Section**: Go to `refs/05-writing-phase.md`
- **Fix Compilation**: Use `refs/07-assembly-phase.md`
- **Respond to Reviewers**: See `refs/08-revision-phase.md`

---

**Structure**: This meta-skill delegates to phase-specific reference files. Each reference contains full workflows, prompts, and script usage. The `scripts/` folder contains all 35+ bundled scripts organized by phase.