# Steps and procedures

This essence captures how to do something in a reliable order. Use it when the source contains instructions, workflows, or operating procedures.

## Use when

- The reader needs an executable path from preconditions to verification.
- Order, branching, checks, and failure handling matter more than description alone.

## Do not use when

- The source is mainly about use cases, scenarios, or history rather than repeatable execution.
- The main value is policy guardrails, not the operational sequence itself.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve prerequisites, decision points, and verification, but do not add lesson pacing, UI choreography, or final training format cues here.

## Best editable shape

Prefer Markdown.

```markdown
# <procedure>

## Goal
<what this accomplishes>

## Preconditions
- <needed before starting>

## Steps
1. <action>
2. <action>
3. <action>

## Failure points
- <what can go wrong>

## Verification
- <how to know it worked>
```

## What good procedure content does

- Gives a new reader an executable path from start to finish.
- Keeps each step action-oriented and easy to verify.
- Exposes decision points instead of pretending the path is linear.

## Common failure modes

- Steps that contain multiple actions or hidden assumptions.
- Missing prerequisites, handoffs, or safety details.
- Describing the ideal process instead of the real one.

## Preserve from the source

- Sequence, dependencies, exceptions, and practical cues.
- Failure points and what they look like in reality.
- Success criteria for knowing a step worked.

## Pre-save checks

- A capable stranger could follow the procedure without guessing.
- Each step has one clear job.
- Branches, validations, and recovery points are explicit.
