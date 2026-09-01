# Revision Phase (08)

Revise papers based on reviewer feedback and write rebuttals.

## Skills Consolidated

- **paper-revision**: Systematic revision based on reviewer comments
- **rebuttal-writing**: Point-by-point rebuttal generation

## Revision Workflow

### Step 1: Map Reviewer Comments to Sections

Create a mapping of each concern to the affected section(s):

| Reviewer | Comment ID | Concern | Affected Section | Action Required |
|----------|------------|---------|------------------|-----------------|
| R1 | 1.1 | Unclear methodology | Methods | Add pseudocode |
| R1 | 1.2 | Missing baseline X | Results | Run experiment |
| R2 | 2.1 | Related work incomplete | Related Work | Add 3 papers |
| R2 | 2.2 | Claims not supported | Results | Add statistical tests |

### Step 2: Prioritize Actions

**Must-do** (affects acceptance):
- Missing experiments requested
- Critical methodological clarifications
- Major related work gaps

**Should-do** (strengthens paper):
- Additional ablation studies
- Clarification of ambiguous claims
- Minor related work additions

**Nice-to-do** (if time permits):
- Stylistic improvements
- Additional visualizations
- Expanded discussion

### Step 3: Execute Revisions

For each action:
1. **Identify exact location** in paper
2. **Make targeted edit** (don't rewrite entire section)
3. **Track changes** (for rebuttal reference)
4. **Verify improvement** (addresses concern)

### Step 4: Verify Improvements

After revisions:
- [ ] All "must-do" items addressed
- [ ] Paper still compiles
- [ ] Changes don't introduce new issues
- [ ] Page count still within limits

## Revision Types

### Add Experiment
1. Run the requested experiment
2. Add results to appropriate table/figure
3. Update Results section with analysis
4. Update Abstract if key finding

### Clarify Method
1. Add pseudocode (if missing)
2. Add mathematical formulation (if vague)
3. Add complexity analysis (if requested)
4. Cross-reference to appendix if space-constrained

### Add Related Work
1. Search for requested papers
2. Add to .bib file
3. Integrate into thematic organization
4. Update compare/contrast analysis

### Strengthen Claims
1. Add statistical significance tests
2. Add effect sizes
3. Add confidence intervals
4. Qualify overconfident statements

## Rebuttal Writing

### Structure

```latex
\documentclass{letter}
\begin{document}

\textbf{Rebuttal to Reviews for Paper [ID]: [Title]}

\section*{Reviewer 1}

\textbf{Comment 1.1:} [Quote reviewer concern]

\textbf{Response:} [Direct answer, be thankful]

We thank the reviewer for this insightful comment. [Address concern directly]. 
As clarified in Section 3.2 (page 5), we [explain]. We have also added 
[description of change] to make this clearer.

\textit{Changes made:} Added pseudocode in Algorithm 1, clarified text in Section 3.2.

\textbf{Comment 1.2:} [Next concern]
...

\end{document}
```

### Response Principles

1. **Be thankful**: Always start with gratitude
2. **Be direct**: Answer the question asked
3. **Provide evidence**: Data, citations, or clear reasoning
4. **Point to changes**: "We have added..." or "As clarified in Section..."
5. **Stay calm**: Don't argue, explain and clarify

### Common Response Patterns

**Misunderstanding**:
> We apologize for the lack of clarity. What we meant is [clear explanation]. 
> We have rewritten Section X to make this clearer.

**Missing experiment**:
> This is an excellent suggestion. We have now run this experiment and 
> added the results to Table Y. The results show [finding], which 
> [supports/qualifies] our main claim.

**Disagreement** (tactful):
> We appreciate this perspective. While we acknowledge that [reviewer point], 
> our focus is on [your focus]. The results in Table X show that in this 
> setting, our approach [result]. We have added a discussion of this 
> trade-off in the Limitations section.

**Cannot address** (honest):
> We agree this would be valuable. However, due to [constraint], we were 
> unable to complete this experiment before the deadline. We have added 
> this to the Future Work section and will prioritize it in follow-up work.

## Rebuttal Best Practices

### Do's
- ✓ Address every concern (even briefly)
- ✓ Be specific about changes made
- ✓ Include page/section references
- ✓ Stay within page limits (typically 2 pages)
- ✓ Proofread for tone and clarity

### Don'ts
- ✗ Argue or be defensive
- ✗ Say "the reviewer should have known"
- ✗ Make changes that introduce new problems
- ✗ Promise experiments you can't complete
- ✗ Exceed page limits

## Validation Checklist

- [ ] Every reviewer comment addressed
- [ ] Responses are polite and professional
- [ ] All promised changes made to paper
- [ ] Rebuttal within page limits
- [ ] Paper still compiles after changes
- [ ] No new errors introduced

## Reference Files

- **Revision prompts**: See original `paper-revision/references/revision-prompts.md`
- **Rebuttal prompts**: See original `rebuttal-writing/references/rebuttal-prompts.md`

## Downstream

- **Final output**: Revised paper PDF + rebuttal PDF
- **Submission**: Upload both to CMT/OpenReview
- **If accepted**: Proceed to camera-ready
- **If rejected**: Consider resubmission to different venue