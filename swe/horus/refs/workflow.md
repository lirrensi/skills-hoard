# Workflow

`.agents/WORKFLOW.md` — the project's pipeline profile. A few lines that tell Horus how this project operates when you're not steering.

## What it can do

Override defaults. Skip stages. Add specialist passes. Change behavior.

## Examples

A no-docs project:
```markdown
# Workflow
- no docs — scout code directly
- always engage
```

A project that always audits:
```markdown
# Workflow
- run Anubis after every plan
- run Osiris on all API changes
```

A project with a task system:
```markdown
# Workflow
- use tasks for goals, not files
- auto-engage after goal created
```

## Rules

- Keep it under 10 lines. If it's longer, it's too complex.
- Only write what differs from the default pipeline.
- Horus reads it at Step 0. Applies what's there. Ignores the rest.
