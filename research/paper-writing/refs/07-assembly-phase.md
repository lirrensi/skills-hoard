# Assembly Phase (07)

Orchestrate full paper compilation with error detection and auto-fix.

## Skills Consolidated

- **paper-assembly**: Full pipeline orchestration with state management and checkpointing
- **paper-compilation**: LaTeX compilation with error detection, chktex, and citation validation

## Assembly Workflow

### State Management

The assembly process maintains state across phases:
```
assembly_state.json:
{
  "phase": "compilation",
  "checkpoint": "section_integration",
  "sections_complete": ["abstract", "intro", "methods", "results", "discussion"],
  "figures_complete": ["fig1", "fig2", "fig3"],
  "tables_complete": ["tab1", "tab2"],
  "errors": [],
  "warnings": []
}
```

### Dependency Tracking

Each section has dependencies:
- **Abstract**: No dependencies (can be written last)
- **Introduction**: Requires literature review
- **Methods**: Requires algorithm design, math formalization
- **Results**: Requires experiments, figures, tables
- **Discussion**: Requires all other sections

### Assembly Command

```bash
python scripts/assembly/assembly_checker.py \
  --dir paper_draft/ \
  --state assembly_state.json \
  --check-all
```

**Checks**:
- All sections present
- All figures/tables referenced
- All citations valid
- No missing dependencies
- State file up to date

## Compilation Pipeline

### Basic Compilation

```bash
python scripts/assembly/compile_paper.py \
  --latex paper.tex \
  --bib references.bib \
  --output-dir pdf/ \
  --max-passes 3
```

**Pipeline**:
1. `pdflatex paper.tex`
2. `bibtex paper`
3. `pdflatex paper.tex` (×2 for reference resolution)
4. Validate output

### Error Detection and Auto-Fix

```bash
python scripts/assembly/fix_latex_errors.py \
  --latex paper.tex \
  --log paper.log \
  --auto-fix \
  --max-iterations 5
```

**Common fixes**:
- Missing `\usepackage` → Add package
- Undefined control sequence → Check spelling or add package
- Citation undefined → Add to .bib or fix cite key
- File not found → Check figure/table paths
- Package conflicts → Reorder package loading

### Compilation Reports

After compilation, you get:
- **Status**: Success/Failure
- **Page count**: Total pages
- **Warnings**: Non-fatal issues
- **Citation stats**: Total citations, unused bib entries
- **Reference stats**: Total refs, undefined refs
- **Figure stats**: Total figures, missing figures

## Chktex Style Checking

```bash
# Run chktex (requires chktex installed)
chktex -q paper.tex

# Common chktex warnings to suppress
% chktex '-W2'  # Suppress warning 2 (line length)
% chktex '-W45' # Suppress warning 45 (paragraph indentation)
```

## Pre-Submission Validation

### Full Validation Command

```bash
python scripts/assembly/assembly_checker.py \
  --dir paper_final/ \
  --venue neurips2024 \
  --strict \
  --report validation_report.md
```

### Validation Checklist

- [ ] Compiles with 0 errors
- [ ] Compiles with ≤5 warnings
- [ ] All \cite keys resolve
- [ ] All \ref keys resolve
- [ ] All figures included and referenced
- [ ] All tables included and referenced
- [ ] Page count within limits
- [ ] Double-blind compliance (if required)
- [ ] No TODOs or draft markers
- [ ] PDF/A compliant (if required)

### Error Priority

| Priority | Issue | Action |
|----------|-------|--------|
| **Critical** | Compilation fails | Fix immediately |
| **Critical** | Undefined citations/references | Add or fix |
| **High** | Missing figures/tables | Add or remove references |
| **Medium** | Chktex warnings | Fix or suppress with comment |
| **Low** | Style inconsistencies | Fix if time permits |

## PDF Validation

### Post-Compilation Checks

1. **Open PDF and verify**:
   - All pages render correctly
   - All figures display
   - All tables formatted properly
   - Hyperlinks work (if enabled)

2. **Check metadata**:
   - Title, authors (if not double-blind)
   - Keywords

3. **File size**:
   - Should be <50 MB for most venues
   - Compress figures if needed

## Scripts

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `assembly_checker.py` | Validate assembly state | `--dir`, `--state`, `--check-all`, `--venue`, `--strict`, `--report` |
| `compile_paper.py` | Compile LaTeX to PDF | `--latex`, `--bib`, `--output-dir`, `--max-passes` |
| `fix_latex_errors.py` | Auto-fix compilation errors | `--latex`, `--log`, `--auto-fix`, `--max-iterations` |

## Reference Files

- **Orchestration patterns**: See original `paper-assembly/references/orchestration-patterns.md`

## Downstream

- **Feeds into**: Phase 08 (revision if reviewer feedback received)
- **Requires from**: All previous phases (01-06)
- **Reference files**: `refs/08-revision-phase.md`