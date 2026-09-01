# Paper Writing Pipeline Overview

Complete end-to-end academic paper production workflow with phase dependencies, state management, and checkpointing.

## Phase Dependency Graph

```
01. Literature (search + review)
       ↓
02. Ideation (novelty check + math reasoning)
       ↓
03. Experiments (data analysis + traceability)
       ↓
04. Visualization (figures + tables)
       ↓
05. Writing (sections + related work)
       ↓
06. Formatting (LaTeX + citations)
       ↓
07. Assembly (compile + validate)
       ↓
08. Revision (reviewer responses + rebuttals)
```

**Advanced phases** (09) can be invoked at any point:
- Survey generation (complete survey paper)
- Paper-to-code (implement from paper)
- Algorithm design (pseudocode + UML)

## Phase Descriptions

### Phase 01: Literature
- **Skills**: `literature-search`, `literature-review`
- **Inputs**: Research topic, keywords
- **Outputs**: JSONL paper database, structured review notes
- **Scripts**: `search_openalex.py`, `search_crossref.py`, `download_arxiv_source.py`

### Phase 02: Ideation
- **Skills**: `novelty-assessment`, `math-reasoning`
- **Inputs**: Research idea, hypotheses
- **Outputs**: Novelty assessment report, formalized notation, proof templates
- **Scripts**: None (prompt-based)

### Phase 03: Experiments
- **Skills**: `data-analysis`, `backward-traceability`
- **Inputs**: Experimental data (CSV/JSON)
- **Outputs**: Statistical analysis code, traceable results with hyperlinks
- **Scripts**: `stat_summary.py`, `format_pvalue.py`, `ref_numeric_values.py`

### Phase 04: Visualization
- **Skills**: `figure-generation`, `table-generation`
- **Inputs**: Data files, figure specifications
- **Outputs**: Publication-quality figures (PNG/PDF), LaTeX tables
- **Scripts**: `figure_template.py`, `results_to_table.py`

### Phase 05: Writing
- **Skills**: `paper-writing-section`, `related-work-writing`
- **Inputs**: Section type, research content, paper database
- **Outputs**: LaTeX section files with citations
- **Scripts**: None (prompt-based)

### Phase 06: Formatting
- **Skills**: `latex-formatting`, `citation-management`
- **Inputs**: Draft LaTeX, .bib file
- **Outputs**: Venue-compliant LaTeX, validated bibliography
- **Scripts**: `latex_checker.py`, `clean_latex.py`, `validate_citations.py`, `harvest_citations.py`

### Phase 07: Assembly
- **Skills**: `paper-assembly`, `paper-compilation`
- **Inputs**: All section files, figures, tables, .bib
- **Outputs**: Final PDF, compilation report, validation checklist
- **Scripts**: `assembly_checker.py`, `compile_paper.py`, `fix_latex_errors.py`

### Phase 08: Revision
- **Skills**: `paper-revision`, `rebuttal-writing`
- **Inputs**: Reviewer comments, current draft
- **Outputs**: Revised paper, point-by-point rebuttal document
- **Scripts**: None (prompt-based)

### Phase 09: Advanced
- **Skills**: `survey-generation`, `paper-to-code`, `algorithm-design`
- **Inputs**: Varies by skill
- **Outputs**: Survey paper, code repository, algorithm pseudocode + diagrams
- **Scripts**: None (prompt-based)

## State Management

Each phase produces checkpoints that feed into the next:
- `phase01_output/`: paper_db.jsonl, review_notes.md
- `phase02_output/`: novelty_report.md, notation_guide.md
- `phase03_output/`: analysis_code.py, traceable_results.csv
- `phase04_output/`: figures/, tables/
- `phase05_output/`: sections/*.tex
- `phase06_output/`: formatted_paper.tex, references.bib
- `phase07_output/`: paper.pdf, compilation_report.md
- `phase08_output/`: revised_paper.tex, rebuttal.tex

## Validation Points

1. **After Phase 01**: Verify paper_db.jsonl has ≥15 relevant papers
2. **After Phase 03**: Run `validate_citations.py` to check all cite keys
3. **After Phase 06**: Run `latex_checker.py` for venue compliance
4. **After Phase 07**: Verify PDF compiles with 0 errors, 0 undefined refs

## Common Patterns

- **Two-pass refinement**: Write draft → Review → Refine (used in writing phases)
- **Multi-agent dialogue**: Generate diverse expert personas for reviews
- **Citation harvesting loop**: 20-round iterative citation discovery
- **Figure VLM feedback loop**: Generate → Validate → Fix (3 phases)
- **Compilation auto-fix loop**: Compile → Parse errors → Fix → Repeat