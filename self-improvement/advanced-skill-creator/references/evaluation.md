# Evaluation Reference

Load this reference when the user wants to evaluate the revised skill, when you need to compare before versus after behavior, or when a change is risky enough that "looks better" is not good enough.

## Evaluation Stance

Evaluate improvements aggressively. The goal is to measure whether the skill got better, not whether the new wording merely sounds nicer.

## Build the Eval Set

Create a compact but varied test set. Prefer 6-10 prompts when the skill matters, and only go smaller when the task is truly lightweight.

Cover multiple categories:

- `core-success` - straightforward requests the skill should handle well
- `edge-case` - unusual but realistic situations the skill should still guide correctly
- `near-miss` - prompts that look related but should trigger different behavior, a different mode, or a refusal to overreach
- `failure-regression` - known bad cases from user complaints, logs, or prior evals
- `research-staleness` - prompts that expose whether outdated assumptions are still present

Good eval prompts are realistic, detailed, and slightly messy. They should sound like what a user would actually say, not abstract toy prompts.

## Compare Against a Baseline

Whenever possible, compare the revised skill against one of these:

- the previous version of the skill
- the current installed version
- no skill at all

The goal is to measure improvement, not just produce another output.

## Evaluate the Right Dimensions

For each prompt, judge the revised skill on several dimensions:

1. `triggering` - did the skill activate when it should, and stay out when it should not
2. `routing` - did it choose the right mode, branch, or level of effort
3. `factuality` - did it avoid stale or contradicted advice
4. `source_anchoring` - did it stay grounded in local source material instead of inventing policy
5. `corpus_fit` - did it preserve the distinction between upstream source corpus and downstream skill
6. `decision quality` - did it make better tradeoffs, not just longer outputs
7. `efficiency` - did it reduce wasted motion, repetition, and unnecessary setup
8. `generality` - does the fix seem portable beyond the exact prompt

## Use Both Qualitative and Concrete Checks

Mix human judgment with crisp checks.

Useful concrete checks include:

- whether the skill selected the correct mode
- whether the revision relied on source material instead of making things up
- whether it cited or incorporated newly researched constraints
- whether it avoided previously observed bad behavior
- whether a required warning, branch, or prerequisite appeared
- whether low-value boilerplate was removed
- whether long guidance moved into references instead of staying in `SKILL.md`
- whether the source corpus stayed canonical and the skill stayed compressed

Useful qualitative checks include:

- whether the revised skill feels more trustworthy
- whether the workflow is easier to follow under pressure
- whether the output reflects understanding instead of template filling
- whether the skill now teaches better judgment to a non-expert model

## Read the Transcript, Not Just the Final Output

If execution traces or reasoning artifacts are available, inspect them.

Look for:

- repeated searches caused by unclear guidance
- unnecessary setup work
- hesitation at decision points
- brittle dependence on one example
- evidence that the new text changed behavior for the better

## Decide What to Do Next

After the eval pass, classify each issue:

- `fixed` - clear improvement over baseline
- `partial` - improved but still weak
- `regressed` - new version got worse
- `uncertain` - needs more targeted testing

Then revise again with restraint. If a fix helps only one prompt but hurts generality or clarity, back it out.

## Minimal Eval Template

For each eval, capture:

```text
Prompt:
Why this eval exists:
Baseline used:
Observed behavior:
What improved:
What still failed:
Next edit, if any:
```
