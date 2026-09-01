# Experiments Phase (03)

Statistical analysis and backward traceability for experimental results.

## Skills Consolidated

- **data-analysis**: Generate statistical analysis code with 4-round review
- **backward-traceability**: Make every number in PDF traceable to exact code lines

## Statistical Analysis Workflow

### Step 1: Define Analysis Plan
- Hypotheses to test
- Variables and measurements
- Statistical tests to use
- Significance level (α = 0.05 typical)

### Step 2: Generate Analysis Code
```bash
python scripts/experiments/stat_summary.py \
  --input data/experiment_results.csv \
  --group-by condition \
  --metrics accuracy,f1_score,latency \
  --output analysis_code.py
```

### Step 3: Four-Round Review Loop
Each round refines:
1. **Round 1**: Basic analysis structure
2. **Round 2**: Add effect sizes and confidence intervals
3. **Round 3**: Check assumptions, add non-parametric alternatives
4. **Round 4**: Format for publication, add visualizations

### Step 4: Output Requirements
Every analysis produces:
- **p-values**: With exact values (not just p < 0.05)
- **Effect sizes**: Cohen's d, η², or appropriate measure
- **Confidence intervals**: 95% CI for all estimates
- **Sample sizes**: N for each group

## Analysis Code Template

```python
import pandas as pd
import scipy.stats as stats
from statsmodels.stats.effect_size import cohens_d

# Load data
df = pd.read_csv("experiment_results.csv")

# Descriptive statistics
print(f"Mean ± SD: {df['metric'].mean():.3f} ± {df['metric'].std():.3f}")

# Statistical test (example: paired t-test)
t_stat, p_value = stats.ttest_rel(group1, group2)
print(f"t(df) = {t_stat:.3f}, p = {p_value:.4f}")

# Effect size
d = cohens_d(group1, group2)
print(f"Cohen's d = {d:.3f}")

# Confidence interval
ci = stats.t.interval(0.95, len(group1)-1, 
                      loc=np.mean(group1-group2), 
                      scale=stats.sem(group1-group2))
print(f"95% CI: [{ci[0]:.3f}, {ci[1]:.3f}]")
```

## P-Value Formatting

```bash
python scripts/experiments/format_pvalue.py \
  --p-value 0.002345 \
  --style apastyle
# Output: p = .002
```

**Format rules**:
- p < .001: Report as "p < .001"
- p ≥ .001: Report exact value to 3 decimals
- No leading zero for p-values (".05" not "0.05")

## Backward Traceability

### Goal
Every number in the final PDF links to the exact code line that produced it.

### Implementation

```bash
python scripts/experiments/ref_numeric_values.py \
  --latex paper.tex \
  --data results.csv \
  --code analysis.py
```

### LaTeX Output Pattern

```latex
Our method achieved accuracy of 
\hyperlink{code:line:42}{\hypertarget{num:acc:95.2}{95.2\%}} 
(on Dataset X).
```

Corresponding code annotation:
```python
# Line 42: accuracy = 95.2%
accuracy = (correct / total) * 100  # num:acc:95.2
```

### Traceability Checklist

- [ ] All reported numbers have `\hyperlink` references
- [ ] All code lines producing numbers have `# num:` comments
- [ ] IDs match between LaTeX and code
- [ ] Cross-references verified in compiled PDF

## Common Statistical Tests

| Comparison | Test | Python Function |
|------------|------|-----------------|
| 2 paired means | Paired t-test | `stats.ttest_rel()` |
| 2 independent means | Independent t-test | `stats.ttest_ind()` |
| >2 means (one-way) | ANOVA | `stats.f_oneway()` |
| >2 means (repeated) | Repeated measures ANOVA | `statsmodels` |
| Non-parametric 2-group | Mann-Whitney U | `stats.mannwhitneyu()` |
| Correlation | Pearson/Spearman | `stats.pearsonr()` / `stats.spearmanr()` |
| Categorical | Chi-square | `stats.chi2_contingency()` |

## Validation

- [ ] All p-values formatted correctly (no leading zero)
- [ ] Effect sizes reported for all significant results
- [ ] 95% CIs provided for all estimates
- [ ] Sample sizes (N) reported for all tests
- [ ] Traceability links verified in compiled PDF

## Scripts

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `stat_summary.py` | Generate analysis code | `--input`, `--group-by`, `--metrics`, `--output` |
| `format_pvalue.py` | Format p-values for publication | `--p-value`, `--style` |
| `ref_numeric_values.py` | Add traceability hyperlinks | `--latex`, `--data`, `--code` |

## Downstream

- **Feeds into**: Phase 04 (visualization), Phase 05 (results section)
- **Reference files**: `refs/04-visualization-phase.md`, `refs/05-writing-phase.md`