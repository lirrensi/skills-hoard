# Action items

This essence captures decisions that require follow-through. Use it when the source contains tasks, owners, due dates, or operational commitments.

## Use when

- The source contains concrete next steps, owners, deadlines, blockers, or follow-through commitments.
- The reader needs operational accountability, not just meeting notes or intentions.

## Do not use when

- The main value is why a decision was made rather than what must happen next.
- The material is still exploratory and should stay as gaps, questions, or broader notes.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve owner, due date, dependency, and proof of done, but do not add task board layout, reminder cadence, or final reporting format here.

## Best editable shape

Prefer YAML.

```yaml
essence: action-items
actions:
  - task: <what needs doing>
    owner: <person or team>
    status: todo|in-progress|blocked|done
    due: <date or none>
    depends_on:
      - <dependency>
    source:
      - <where this came from>
```

## What good action-item content does

- Turns intentions into trackable commitments.
- Makes accountability, timing, and done-ness visible.
- Keeps each item small enough to execute and verify.

## Common failure modes

- Vague verbs like "handle" or "look into."
- Tasks with no owner, no success condition, or multiple hidden owners.
- Mixing decisions, discussion notes, and actions together.

## Preserve from the source

- Intent, owner, deadline, dependencies, and blockers.
- Any required review, approval, or proof of completion.
- The context that explains why the task exists.

## Pre-save checks

- A stranger could execute the task without guessing.
- There is one accountable owner.
- Success is observable enough to verify.
