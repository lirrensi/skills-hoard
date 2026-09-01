# Visualization Phase (04)

Generate publication-quality figures and tables.

## Skills Consolidated

- **figure-generation**: 3-phase pipeline with VLM visual feedback
- **table-generation**: Convert results to LaTeX tables with booktabs

## Figure Generation Pipeline

### Phase 1: Query Expansion
Expand vague figure requests into detailed specifications:
- **Input**: "Plot accuracy comparison"
- **Output**: "Bar chart comparing accuracy of 4 methods on 3 datasets, error bars showing 95% CI, x-axis = datasets, y-axis = accuracy %, grouped bars per dataset"

### Phase 2: Code Generation
Generate Python/MATLAB code for figure creation:
```bash
python scripts/visualization/figure_template.py \
  --type bar \
  --data results.csv \
  --output figure_code.py
```

### Phase 3: VLM Visual Feedback Loop
1. Generate initial figure
2. Run VLM (vision-language model) to critique
3. Fix issues identified
4. Repeat until VLM scores ≥4/5

## Figure Quality Checklist

- [ ] Resolution: ≥300 DPI for raster, vector (PDF/SVG) preferred
- [ ] Font size: ≥8pt when printed at final size
- [ ] Color: Colorblind-safe palette (use viridis, plasma, or similar)
- [ ] Labels: All axes labeled with units
- [ ] Legends: Clear, outside plot if possible
- [ ] Error bars: Specify what they represent (SD, SE, or CI)
- [ ] Caption: Self-contained, explains what's shown

## Table Generation

### Basic Usage
```bash
python scripts/visualization/results_to_table.py \
  --input results.csv \
  --columns method,accuracy,f1,latency \
  --sort-by accuracy \
  --style booktabs \
  --output table.tex
```

### Output Format (booktabs)
```latex
\begin{table}[t]
\centering
\caption{Comparison of methods on Dataset X}
\label{tab:methods_comparison}
\begin{tabular}{lrrr}
\toprule
Method & Accuracy & F1 Score & Latency (ms) \\
\midrule
Method A & 95.2 & 94.8 & 120 \\
Method B & 93.1 & 92.5 & 95 \\
Method C & 91.5 & 90.8 & 110 \\
\bottomrule
\end{tabular}
\end{table}
```

### Table Styling Options

| Style | Description |
|-------|-------------|
| `booktabs` | Professional (toprule, midrule, bottomrule) |
| `siunitx` | Number alignment with decimal points |
| `multicolumn` | Multi-column headers for grouped data |
| `resize` | Scale to fit text width |

### Multi-Column Headers

```latex
\begin{tabular}{lcccc}
\toprule
& \multicolumn{2}{c}{Dataset A} & \multicolumn{2}{c}{Dataset B} \\
\cmidrule(lr){2-3} \cmidrule(lr){4-5}
Method & Acc & F1 & Acc & F1 \\
\midrule
...
```

## Figure Types

### Common Plot Types

| Data Type | Plot Type | Library |
|-----------|-----------|---------|
| Categorical comparison | Bar chart | matplotlib/seaborn |
| Distribution | Violin/box plot | seaborn |
| Time series | Line plot | matplotlib |
| Correlation | Scatter/heatmap | seaborn |
| Hierarchy | Tree/dendrogram | scipy/matplotlib |
| Network | Graph visualization | networkx |

### Colorblind-Safe Palettes

```python
# Sequential
cmap = 'viridis'  # or 'plasma', 'inferno', 'magma'

# Diverging
cmap = 'coolwarm'  # or 'seismic', 'RdBu'

# Categorical
colors = ['#0173B2', '#DE8F05', '#023690', '#D1329E']  # Colorblind-safe
```

## Output Formats

| Format | Use Case |
|--------|----------|
| PDF/SVG | Preferred (vector, scalable) |
| PNG | When vector not supported (≥300 DPI) |
| TIFF | Some journals require (≥600 DPI) |

## Validation

- [ ] Figures render without warnings
- [ ] All text legible at final size
- [ ] Colors distinguishable for colorblind viewers
- [ ] File size reasonable (<10 MB for raster)
- [ ] Tables compile without errors
- [ ] All references (\label/\ref) defined

## Scripts

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `figure_template.py` | Generate figure code | `--type`, `--data`, `--output` |
| `results_to_table.py` | Convert CSV/JSON to LaTeX table | `--input`, `--columns`, `--sort-by`, `--style` |

## Reference Files

- **Figure prompts**: See original `figure-generation/references/figure-prompts.md`
- **Table templates**: See original `table-generation/references/table-templates.md`

## Downstream

- **Feeds into**: Phase 05 (results section writing), Phase 07 (assembly)
- **Reference files**: `refs/05-writing-phase.md`, `refs/07-assembly-phase.md`