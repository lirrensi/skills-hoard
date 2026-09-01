# Scripts Index

Complete catalog of all 35+ scripts organized by phase.

## Phase 01: Literature

### search_semantic_scholar.py
**Purpose**: Search Semantic Scholar API for academic papers

**Usage**:
```bash
python scripts/literature/search_semantic_scholar.py \
  --query "transformer attention" \
  --top-conferences --min-citations 5 -o results.jsonl
```

**Flags**:
- `--query`: Search query (required)
- `--top-conferences`: Filter to NeurIPS, ICML, ICLR, etc.
- `--peer-reviewed-only`: Exclude preprints
- `--min-citations N`: Minimum citation count
- `--venue VENUE`: Specific venue filter
- `--year-min Y`: Minimum year
- `-o`: Output file

### search_openalex.py
**Purpose**: Search OpenAlex API (broader coverage)

**Usage**:
```bash
python scripts/literature/search_openalex.py \
  --query "neural networks" --min-citations 10 -o results.jsonl
```

**Flags**: Same as search_semantic_scholar.py

### search_crossref.py
**Purpose**: Search Crossref API (journals focus)

**Usage**:
```bash
python scripts/literature/search_crossref.py \
  --query "machine learning" --types article-journal -o results.jsonl
```

### download_arxiv_source.py
**Purpose**: Download source/PDF from arXiv

**Usage**:
```bash
python scripts/literature/download_arxiv_source.py \
  --arxiv-id 2301.12345 --output-dir papers/
```

**Flags**:
- `--arxiv-id`: arXiv ID (required)
- `--output-dir`: Download directory
- `--format`: pdf or source

### download_papers.py
**Purpose**: Batch download PDFs from JSONL

**Usage**:
```bash
python scripts/literature/download_papers.py \
  --jsonl results.jsonl --output-dir papers/ \
  --sort-by-citations --max-downloads 15
```

**Flags**:
- `--jsonl`: Input JSONL file (required)
- `--output-dir`: Download directory (required)
- `--sort-by-citations`: Sort by citation count before downloading
- `--max-downloads N`: Limit downloads

---

## Phase 03: Experiments

### stat_summary.py
**Purpose**: Generate statistical analysis code

**Usage**:
```bash
python scripts/experiments/stat_summary.py \
  --input data.csv --group-by condition \
  --metrics accuracy,f1 --output analysis.py
```

**Flags**:
- `--input`: Input data file (required)
- `--group-by`: Column to group by
- `--metrics`: Comma-separated metric columns
- `--output`: Output Python script

### format_pvalue.py
**Purpose**: Format p-values for publication

**Usage**:
```bash
python scripts/experiments/format_pvalue.py --p-value 0.002345 --style apastyle
# Output: p = .002
```

**Flags**:
- `--p-value`: P-value to format (required)
- `--style`: apastyle or generic

### ref_numeric_values.py
**Purpose**: Add traceability hyperlinks between LaTeX and code

**Usage**:
```bash
python scripts/experiments/ref_numeric_values.py \
  --latex paper.tex --data results.csv --code analysis.py
```

**Flags**:
- `--latex`: LaTeX file
- `--data`: Data file
- `--code`: Python analysis script

---

## Phase 04: Visualization

### figure_template.py
**Purpose**: Generate Python code for figures

**Usage**:
```bash
python scripts/visualization/figure_template.py \
  --type bar --data results.csv --output figure_code.py
```

**Flags**:
- `--type`: bar, line, scatter, violin, heatmap
- `--data`: Input data file
- `--output`: Output Python script

### results_to_table.py
**Purpose**: Convert CSV/JSON to LaTeX table

**Usage**:
```bash
python scripts/visualization/results_to_table.py \
  --input results.csv --columns method,accuracy,f1 \
  --sort-by accuracy --style booktabs --output table.tex
```

**Flags**:
- `--input`: Input data file (required)
- `--columns`: Comma-separated column names
- `--sort-by`: Column to sort by
- `--style`: booktabs, siunitx, basic
- `--output`: Output .tex file

---

## Phase 06: Formatting

### latex_checker.py
**Purpose**: Check LaTeX for venue compliance

**Usage**:
```bash
python scripts/formatting/latex_checker.py \
  --latex paper.tex --venue neurips2024 --check double-blind
```

**Flags**:
- `--latex`: LaTeX file (required)
- `--venue`: Target venue (neurips2024, icml2024, etc.)
- `--check`: double-blind, page-limit, formatting
- `--strict`: Fail on warnings

### clean_latex.py
**Purpose**: Remove comments, TODOs, debug code

**Usage**:
```bash
python scripts/formatting/clean_latex.py \
  --input paper.tex --output paper_clean.tex \
  --remove-todos --remove-comments
```

**Flags**:
- `--input`: Input .tex file (required)
- `--output`: Output .tex file (required)
- `--remove-todos`: Remove \todo{} commands
- `--remove-comments`: Remove % comments
- `--remove-debug`: Remove \verb, draft markers

---

## Phase 06: Citations

### validate_citations.py
**Purpose**: Validate cite keys against .bib file

**Usage**:
```bash
python scripts/citations/validate_citations.py \
  --latex paper.tex --bib references.bib --strict
```

**Flags**:
- `--latex`: LaTeX file (required)
- `--bib`: BibTeX file (required)
- `--auto-fix`: Generate placeholder entries for missing keys
- `--strict`: Fail on warnings

**Reports**:
- Missing citations (cite key not in .bib)
- Unused bib entries (in .bib but not cited)
- Duplicate keys
- Missing required fields

### harvest_citations.py
**Purpose**: Auto-harvest missing citations from draft

**Usage**:
```bash
python scripts/citations/harvest_citations.py \
  --latex paper.tex --bib references.bib \
  --max-rounds 20 --output references_updated.bib
```

**Flags**:
- `--latex`: LaTeX file with placeholder citations
- `--bib`: Existing .bib file
- `--max-rounds`: Maximum iteration rounds (default 20)
- `--output`: Updated .bib file

**Process**:
1. Find `[@TODO: description]` placeholders
2. Search Semantic Scholar
3. Add BibTeX entry
4. Replace placeholder with cite key
5. Repeat

---

## Phase 07: Assembly

### assembly_checker.py
**Purpose**: Validate assembly state and dependencies

**Usage**:
```bash
python scripts/assembly/assembly_checker.py \
  --dir paper_draft/ --state assembly_state.json \
  --venue neurips2024 --strict --report validation.md
```

**Flags**:
- `--dir`: Paper directory (required)
- `--state`: State file
- `--check-all`: Run all checks
- `--venue`: Target venue
- `--strict`: Fail on warnings
- `--report`: Output report file

### compile_paper.py
**Purpose**: Compile LaTeX to PDF with error detection

**Usage**:
```bash
python scripts/assembly/compile_paper.py \
  --latex paper.tex --bib references.bib \
  --output-dir pdf/ --max-passes 3
```

**Flags**:
- `--latex`: Main .tex file (required)
- `--bib`: .bib file (required)
- `--output-dir`: Output directory
- `--max-passes`: Maximum pdflatex passes (default 3)

**Pipeline**: pdflatex → bibtex → pdflatex ×2

### fix_latex_errors.py
**Purpose**: Auto-fix common LaTeX compilation errors

**Usage**:
```bash
python scripts/assembly/fix_latex_errors.py \
  --latex paper.tex --log paper.log \
  --auto-fix --max-iterations 5
```

**Flags**:
- `--latex`: .tex file to fix (required)
- `--log`: Compilation log file (required)
- `--auto-fix`: Automatically apply fixes
- `--max-iterations`: Maximum fix attempts

**Common fixes**:
- Missing `\usepackage`
- Undefined control sequences
- Citation key mismatches
- File path errors

---

## Script Location Mapping

All scripts are located in `scripts/` subdirectories by phase:
```
scripts/
├── literature/       # search_*.py, download_*.py
├── experiments/      # stat_summary.py, format_pvalue.py, ref_numeric_values.py
├── visualization/    # figure_template.py, results_to_table.py
├── formatting/       # latex_checker.py, clean_latex.py
├── citations/        # validate_citations.py, harvest_citations.py
└── assembly/         # assembly_checker.py, compile_paper.py, fix_latex_errors.py
```

## Original Source Locations

Scripts consolidated from:
- `skill-library-candidates/literature-search/scripts/`
- `skill-library-candidates/data-analysis/scripts/`
- `skill-library-candidates/figure-generation/scripts/`
- `skill-library-candidates/table-generation/scripts/`
- `skill-library-candidates/latex-formatting/scripts/`
- `skill-library-candidates/citation-management/scripts/`
- `skill-library-candidates/paper-assembly/scripts/`
- `skill-library-candidates/paper-compilation/scripts/`
- `skill-library-candidates/backward-traceability/scripts/`