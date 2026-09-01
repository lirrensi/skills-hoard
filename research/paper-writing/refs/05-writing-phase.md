# Writing Phase (05)

Write paper sections with structured guidance and citation management.

## Skills Consolidated

- **paper-writing-section**: Write specific sections (Abstract, Intro, Methods, Results, etc.)
- **related-work-writing**: Generate Related Work sections with thematic organization

## Section Writing Workflow

### Two-Pass Refinement Process

**Pass 1: Draft**
- Get content down quickly
- Focus on ideas, not polish
- Include placeholder citations `[TODO: cite relevant work]`

**Pass 2: Refine**
- Improve clarity and flow
- Replace placeholders with real citations
- Strengthen topic sentences
- Add transitions

### Section-Specific Guidance

#### Abstract (150-250 words)
```
1. Problem statement (1-2 sentences)
2. Limitations of existing work (1 sentence)
3. Our approach (1-2 sentences)
4. Key results (1-2 sentences with numbers)
5. Impact/implications (1 sentence)
```

#### Introduction (1-2 pages)
```
1. Broad context and motivation
2. Specific problem being addressed
3. Limitations of current approaches
4. Our contributions (numbered list)
5. Paper organization (optional)
```

**Contributions format**:
> Our contributions are:
> 1. We propose [method] that [does what].
> 2. We prove [theoretical result].
> 3. We demonstrate [empirical result] on [datasets].

#### Methods
```
1. Problem formulation (mathematical)
2. Overall approach (high-level)
3. Detailed algorithm (pseudocode)
4. Complexity analysis
5. Implementation details
```

#### Results
```
1. Experimental setup (datasets, baselines, metrics)
2. Main results (with figures/tables)
3. Ablation studies
4. Analysis of failures/limitations
```

#### Discussion/Conclusion
```
1. Summary of key findings
2. Broader implications
3. Limitations (be honest)
4. Future work
```

## Related Work Writing

### Thematic Organization (NOT chronological)

**Bad**: "Smith et al. (2020) did X. Then Johnson et al. (2021) did Y..."

**Good**: 
> **Approach Category 1: Method X**
> Smith et al. [1] propose... Johnson et al. [2] extend this by...
> 
> **Approach Category 2: Method Y**
> Lee et al. [3] take a different approach...

### Compare/Contrast Pattern

For each related work:
1. **What they do**: Clear description
2. **How it's similar**: Acknowledge overlap
3. **How it's different**: Differentiate your work
4. **Why yours is better** (if applicable): Quantified advantage

### Related Work Template

```latex
\section{Related Work}

\subsection{Category 1: [Name]}
Opening sentence defining the category...

Smith et al.~\cite{smith2020} propose [method]. Their approach [key idea], 
achieving [result] on [benchmark]. \textit{Limitation:} [issue].

Johnson et al.~\cite{johnson2021} address this by [improvement]. 
However, they still [remaining issue].

\subsection{Category 2: [Name]}
...

\paragraph{Our Work.} Unlike prior work, we [key differentiator]. 
Specifically, we [specific contribution].
```

## Citation Best Practices

### Inline Citation Format

```latex
% First mention (narrative)
Smith et al.~\cite{smith2020} propose...

% Subsequent or parenthetical
This approach has been studied~\cite{smith2020,johnson2021}.

% Multiple citations (chronological or alphabetical)
Prior work~\cite{smith2020,johnson2021,lee2022} shows...
```

### Citation Density

- **Introduction**: 1-2 citations per paragraph
- **Related Work**: 2-4 citations per paragraph
- **Methods**: 1 citation per novel technique borrowed
- **Results**: Minimal (mostly for baseline comparisons)

### Harvesting Missing Citations

```bash
# Auto-harvest missing citations from draft
python scripts/writing/harvest_citations.py \
  --latex paper.tex \
  --bib references.bib \
  --output references_updated.bib
```

**20-round iterative process**:
1. Identify placeholder citations (`[TODO: ...]`)
2. Search for most relevant paper
3. Add to .bib file
4. Repeat until all placeholders resolved

## Validation Checklist

- [ ] All sections have clear topic sentences
- [ ] Transitions between paragraphs are smooth
- [ ] All placeholder citations replaced
- [ ] All \cite keys resolve (run `validate_citations.py`)
- [ ] No citation is used without explanation
- [ ] Related work organized thematically, not chronologically
- [ ] Contributions are numbered and specific

## Reference Files

- **Section tips**: See original `paper-writing-section/references/section-tips.md`
- **Refinement prompts**: See original `paper-writing-section/references/refinement-prompts.md`
- **Related work prompts**: See original `related-work-writing/references/related-work-prompts.md`

## Downstream

- **Feeds into**: Phase 06 (formatting), Phase 07 (assembly)
- **Requires from**: Phase 01 (citations), Phase 04 (figures/tables)
- **Reference files**: `refs/06-formatting-phase.md`, `refs/07-assembly-phase.md`