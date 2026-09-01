# Session Ledger

Use this when the brainstorm will unfold over multiple exchanges or when the user is thinking out loud in fragments.

The goal is to make the session cumulative.

## Core Rule

Do not treat each message as a fresh brainstorm.

Instead:

1. capture the new thought
2. relate it to what already exists
3. mark whether it strengthens, mutates, contradicts, or replaces something earlier
4. preserve the history of why ideas stayed, changed, or died

## When To Use A Ledger

Use a running ledger when:

- the brainstorm lasts more than a quick one-off reply
- the user is sending many partial thoughts over time
- ideas are being refined, merged, or discarded
- the user wants to look back at what was explored
- repeated loops or rediscovered dead ends are likely

## Idea Record Shape

Each idea should keep:

- `id`: stable handle such as `I1`, `I2`, `I3`
- `idea`: short plain-language statement
- `source`: user, assistant, or hybrid
- `relation`: `seed`, `variant`, `combination`, `orthogonal`, `wildcard`, `contradiction`
- `cluster`: current bucket or theme
- `status`: `active`, `parked`, `selected`, `discarded`
- `notes`: why it matters, what changed, or why it was dropped

## Useful Lightweight Categories

When talking to the user, prefer simple categories over formal jargon:

- `same direction`
- `sharper version`
- `new direction`
- `very different bet`
- `probably weak`
- `discarded for now`

These are often easier to use in conversation than abstract framework labels.

## Discard Discipline

Discarded ideas are not garbage; they are part of the map.

When dropping an idea, note why:

- violates a real constraint
- duplicates a stronger idea
- too vague to act on
- interesting later, wrong now
- based on a bad assumption

This prevents circular conversations.

## Look-Back Moves

Periodically summarize the ledger for the user:

- what themes are emerging
- which ideas keep surviving refinement
- which ideas are genuinely novel
- what was discarded and why
- what remains underexplored

## File Guidance

If the session deserves a durable artifact, write or update `templates/brainstorm-record.md` shape.

If the brainstorm is short, keep the same structure inline without making a file.

## Anti-Patterns

- restarting from zero every turn
- deleting discarded ideas with no explanation
- treating small wording changes as new ideas
- losing track of which ideas are user-originated versus generated extensions
- keeping everything active forever and never pruning
