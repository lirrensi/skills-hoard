# Field Manual Principles

Use this reference when turning source material into a skill folder, or when a skill should
feel more like a field manual than a freeform prompt.

## Core Assumptions

- The reader may be rushed, tired, or unfamiliar.
- The writer must keep the path clear even when context is thin.
- Source material outranks intuition.
- The source corpus is canonical; the skill is a downstream compression.
- The final skill should be easy for another agent to resume.

## Writing Rules

- Put purpose first.
- Use short headings.
- Keep one action per step.
- Put prerequisites before procedures.
- Put checks right after the action they verify.
- Put failure handling near the step that can fail.
- Use stable nouns and stable file names.
- Avoid nested explanations in the core flow.
- Keep examples in references unless they define the pattern.
- Build around rule, example, checklist, and recovery path.

## Source Rules

- Separate raw notes, examples, constraints, and policy.
- Keep provenance when a claim came from a file, eval, or user note.
- If sources conflict, preserve the conflict instead of smoothing it away.
- If the source packet is thin, collect more before polishing the skill.

## Skill File Split

- `SKILL.md`: trigger, routing, mode selection, and pointers.
- `references/*.md`: mode playbooks, doctrine, examples, and eval criteria.
- `ideas.md`: raw notes and candidate material, not policy.
- `distill.md`: source-corpus-to-skill compression guidance.

## Creation Checklist

- clear trigger
- clear mode split
- source packet present
- corpus or source pack identified
- repeated patterns moved to references
- validation path available

## Improvement Checklist

- identify the failure surface
- compare against local skills
- trim bloat first
- add missing decision points
- add recovery paths
- validate with realistic prompts
