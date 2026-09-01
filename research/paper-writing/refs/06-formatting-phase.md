# Formatting Phase (06)

LaTeX formatting and citation management for venue compliance.

## Skills Consolidated

- **latex-formatting**: Venue-specific templates, formatting checks, pre-submission validation
- **citation-management**: BibTeX lifecycle management, citation harvesting, validation

## LaTeX Formatting

### Venue Templates

Supported venues (check `templates/venues/` for latest):
- NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, ICCV, ECCV
- Nature, Science, PNAS
- IEEE, ACM transaction formats

### Basic Formatting Workflow

```bash
# Check LaTeX for venue compliance
python scripts/formatting/latex_checker.py \
  --latex paper.tex \
  --venue neurips2024 \
  --check double-blind

# Clean LaTeX (remove comments, TODOs, debug code)
python scripts/formatting/clean_latex.py \
  --input paper.tex \
  --output paper_clean.tex \
  --remove-todos --remove-comments
```

### Pre-Submission Checklist

- [ ] Correct venue template used
- [ ] Page limits respected (excluding references if allowed)
- [ ] Double-blind compliance (no self-citations that reveal identity)
- [ ] All figures/tables referenced in text
- [ ] All citations defined in .bib
- [ ] No compilation warnings
- [ ] PDF/A compliance (if required)

### Common Formatting Issues

| Issue | Fix |
|-------|-----|
| Margin violations | Use `\setlength{\marginparwidth}{0pt}` |
| Floating tables | Use `\begin{table*}` for wide tables |
| Citation overflow | Split long citation lists across lines |
| Figure too large | Use `\resizebox{\columnwidth}{!}{...}` |
| Missing bibliography | Ensure `\bibliography{file}` not `\bibliographystyle` only |

## Citation Management

### Validate Citations

```bash
python scripts/citations/validate_citations.py \
  --latex paper.tex \
  --bib references.bib
```

**Reports**:
- Missing citations (cite key not in .bib)
- Unused bib entries (in .bib but not cited)
- Duplicate keys
- Missing required fields (year, author, title)

### Harvest Missing Citations

```bash
python scripts/citations/harvest_citations.py \
  --latex paper.tex \
  --bib references.bib \
  --max-rounds 20 \
  --output references_updated.bib
```

**Process**:
1. Find placeholder citations: `[@TODO: transformer basics]`
2. Search Semantic Scholar for relevant papers
3. Add BibTeX entry to .bib
4. Replace placeholder with actual cite key
5. Repeat until all placeholders resolved or max rounds reached

### Auto-Fix Missing Citations

```bash
python scripts/citations/validate_citations.py \
  --latex paper.tex \
  --bib references.bib \
  --auto-fix
```

Generates `references_fixed.bib` with placeholder entries for missing keys.

### BibTeX Entry Format

```bibtex
@inproceedings{vaswani2017attention,
  title={Attention Is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and 
          Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and 
          Kaiser, \L ukasz and Polosukhin, Illia},
  booktitle={Advances in Neural Information Processing Systems},
  volume={30},
  year={2017},
  publisher={Curran Associates, Inc.}
}
```

**Required fields**: author, title, year, venue/booktitle/journal

### Citation Key Naming

**Format**: `firstAuthorYearKeyword`
- `vaswani2017attention` ✓
- `Vaswani2017Attention` ✗ (no capitalization)
- `vaswani_attention_2017` ✗ (no underscores, year in middle)

## Deduplication

**Check for duplicates**:
- Same paper, different keys
- Same key, different entries
- Conference vs. journal version of same paper

**Resolution**:
- Keep the peer-reviewed version
- Use the most complete BibTeX entry
- Consolidate citations to single key

## Validation

```bash
# Full validation before compilation
python scripts/citations/validate_citations.py \
  --latex paper.tex \
  --bib references.bib \
  --strict

# Check LaTeX syntax
python scripts/formatting/latex_checker.py \
  --latex paper.tex \
  --venue neurips2024 \
  --strict
```

## Scripts

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `latex_checker.py` | Check venue compliance | `--latex`, `--venue`, `--check`, `--strict` |
| `clean_latex.py` | Remove comments, TODOs | `--input`, `--output`, `--remove-todos`, `--remove-comments` |
| `validate_citations.py` | Validate cite keys | `--latex`, `--bib`, `--auto-fix`, `--strict` |
| `harvest_citations.py` | Auto-harvest missing citations | `--latex`, `--bib`, `--max-rounds`, `--output` |

## Reference Files

- **Venue templates**: See `templates/venues/`
- **Original venue-templates.md**: See original `latex-formatting/references/venue-templates.md`

## Downstream

- **Feeds into**: Phase 07 (assembly and compilation)
- **Requires from**: Phase 05 (written sections)
- **Reference files**: `refs/07-assembly-phase.md`