# Paper Writing Meta-Skill

Consolidated academic paper writing skill combining 19 specialized capabilities into a single, organized reference system.

## Structure

```
paper-writing/
├── SKILL.md                    # Main entry point (~30 lines)
├── refs/                       # Phase-specific reference files
│   ├── 00-pipeline-overview.md # Full pipeline with dependencies
│   ├── 01-literature-phase.md  # Literature search & review
│   ├── 02-ideation-phase.md    # Novelty & math reasoning
│   ├── 03-experiments-phase.md # Data analysis & traceability
│   ├── 04-visualization-phase.md # Figures & tables
│   ├── 05-writing-phase.md     # Section writing
│   ├── 06-formatting-phase.md  # LaTeX & citations
│   ├── 07-assembly-phase.md    # Compilation & validation
│   ├── 08-revision-phase.md    # Reviewer responses
│   ├── 09-advanced-phase.md    # Survey, paper-to-code, algorithms
│   └── scripts-index.md        # Complete script catalog (35+ scripts)
├── scripts/                    # All scripts organized by phase
│   ├── literature/             # search_*.py, download_*.py (5 scripts)
│   ├── experiments/            # stat_summary.py, format_pvalue.py (3 scripts)
│   ├── visualization/          # figure_template.py, results_to_table.py (2 scripts)
│   ├── formatting/             # latex_checker.py, clean_latex.py (2 scripts)
│   ├── citations/              # validate_citations.py, harvest_citations.py (2 scripts)
│   └── assembly/               # assembly_checker.py, compile_paper.py, fix_latex_errors.py (3 scripts)
└── templates/                  # Venue templates
    └── venues/                 # LaTeX templates for NeurIPS, ICML, etc.
```

## Usage

1. **Start at `SKILL.md`** - Quick access table routes you to the right phase
2. **Read phase reference** - Each `refs/XX-phase.md` has full workflows and examples
3. **Use scripts** - All 15 scripts in `scripts/` are ready to run
4. **Follow the pipeline** - Phases 01-08 are sequential; phase 09 is optional/parallel

## Consolidated Skills

This meta-skill replaces these 19 skills from `skill-library-candidates/`:

**Core (13)**:
- literature-search, literature-review, latex-formatting, paper-assembly
- paper-compilation, paper-revision, paper-writing-section, paper-to-code
- rebuttal-writing, data-analysis, figure-generation, novelty-assessment, math-reasoning

**Meta (6)**:
- citation-management, table-generation, algorithm-design
- related-work-writing, backward-traceability, survey-generation

## Benefits

- **Single entry point** - No need to search through 19 separate skills
- **Phase-based organization** - Mirrors actual research workflow
- **Complete script catalog** - All 15 scripts in one place with usage examples
- **Cross-references** - Each phase links to upstream/downstream phases
- **Maintainable** - Add new phases or scripts without bloating SKILL.md

## Original Locations

All content preserved from original skills in `skill-library-candidates/`. That directory can be archived or removed after verifying this meta-skill works as expected.