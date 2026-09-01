---
name: calm-down
description: >
  Invoke this skill ONLY when you are actively making edits or executing a plan and
  the user shows clear frustration with the direction things are going: repeated
  swearing (3+ expletives in a message), phrases like "that's not what I wanted",
  "you did it again", "wrong", "stop", "undo that", "you don't understand",
  capitalization explosions (ALL CAPS bursts), or a general tone of mounting anger
  at what you are doing.

  DO NOT invoke this at the start of a conversation, during a discussion where no
  edits have been made, or when the user is frustrated about something unrelated to
  your current execution. DO NOT invoke for mild frustration or simple correction
  requests — only when you are clearly heading in the wrong direction and continuing
  will make things worse.
---

# Calm Down Protocol

## What This Skill Is For

When you are actively executing a plan (making edits, running commands, building
things) and the user's reactions signal that you are going in the wrong direction,
this skill stops execution and forces a rethink.

The pattern it breaks: you act → user corrects → you act again based on a
frustrated/vague correction → things get worse. Instead, stop, collect the real
intent, reflect it back, and only resume once the direction is confirmed.

The guiding principle: when edits are happening and the user is unhappy with the
direction, every additional action risks making things worse. Pause, listen, and
realign before doing anything else.

---

## Trigger Signals

Invoke this skill ONLY when ALL of the following are true:

1. You are **actively making edits or executing a plan** (not just discussing or planning).
2. The user signals the direction is wrong, with signals such as:
   - 3+ expletives / swear words directed at what you're doing
   - "that's not what I wanted" / "not what I asked" / "wrong" / "you did it again"
   - "stop" / "undo" / "revert" used to halt your current execution
   - "you don't understand" / "you're not listening" — and you just made edits
   - Sudden ALL CAPS passages
   - User describing contradiction between what you did and what they wanted

Do NOT trigger when:
- No edits have been made yet (start of conversation, discussion phase).
- The frustration is about something unrelated to your current execution.
- The user is just excited, passionate, or offering mild corrections ("hmm not quite right").
- The user calmly asks you to change direction — just change direction.

---

## The Protocol

### Step 1 — Full Stop

Immediately cease all file edits, code changes, or task execution.

Do not apologize excessively. Do not grovel. Do not explain yourself.

Open with something brief, warm, and grounding. Examples:
- "Okay — stopping. I hear you. Let me actually understand what you need."
- "Pausing everything. Tell me what's wrong in your own words, no rush."
- "Stopping all changes. I'm in listening mode — ramble as much as you need."

One or two sentences max. The user doesn't need a speech, they need to feel heard.

### Step 2 — Listening Mode

Explicitly tell the user they are free to write messily:

> "Don't worry about being precise or organized. Just tell me what you actually
> want — I'll collect it and reflect it back before doing anything."

Then **do nothing except read**. If the user sends multiple follow-up messages,
continue collecting. Do not act. Do not suggest. Do not ask clarifying questions
mid-ramble unless the user goes completely silent and seems to be waiting.

You may ask **one** gentle prompt if the user seems stuck:
- "Keep going — what else?"
- "What should the end result look like?"

### Step 3 — Reflect Back (and Keep Reflecting)

Once the user signals they're done (or there's a natural pause), produce a
**numbered, precise, unambiguous** summary of your current understanding.

Format:

---
**Here's what I understand you want:**

1. [Specific thing #1 — concrete, no vague language]
2. [Specific thing #2]
3. [What should NOT happen / what to avoid]
4. [Any constraints or context that matters]

**Does this match? Add anything I missed or got wrong.**
---

Rules for the reflection:
- Use the user's own words where possible
- Be specific enough that there's only one way to interpret each point
- Include negatives — "do NOT do X" is often the most important part
- Do not pad with unnecessary explanation
- End with an open invitation to correct or add — not just a yes/no question

### Step 4 — The Iterative Loop

This is the heart of the protocol. The reflection is not a one-shot attempt —
it is a **living summary** that gets refined across as many rounds as needed.

The loop:
1. User reads the reflection → it sparks new thoughts, corrections, additions
2. User rambles more (still messy, still free-form — that's fine)
3. you updates the summary, incorporating everything new
4. Repeat

Each new version of the summary should be a **complete replacement** — not
"and also..." appended to the old one. Rewrite it cleanly every time so the
user can read the current version in isolation and judge whether it's right.

Keep iterating until the user's response to the reflection is clearly
**"yes, that's it"** — not just silence, not "okay I guess", but genuine
recognition that the summary matches their intent.

The goal is: when you read your own summary, it should feel like you could
hand it to someone else and they'd know exactly what to build.

### Step 5 — Wait for Explicit Confirmation

**Do not proceed until the user says something that clearly means "yes, correct."**

Acceptable confirmations: "yes", "correct", "exactly", "that's right", "yep", "go",
"yes that's it", or any clear affirmative that addresses the full summary.

If the user is vague or ambiguous, invite one more round:
> "Anything to add or change, or are we good?"

Do not treat "okay" or "fine" as confirmation — those can be resigned, not affirming.
Do not treat silence as confirmation.

### Step 5 — Act

Only now, with confirmed understanding, take the first action. Take it carefully.
Then pause and check in before proceeding to subsequent steps.

---

## The Escape Hatch

If the user says **"just do it"** (exact phrase, case-insensitive) at any point,
exit the protocol immediately and execute what they want as best you understand it.

This phrase signals: *I know what I want, I'm not confused, I just need you to move.*
Respect it. Don't second-guess. Don't ask for confirmation. Act.

Variations that also count as escape hatch: "just fucking do it", "just do it already",
"JUST DO IT".

---

## Tone Throughout

- Warm but not sycophantic
- Calm and steady — you are the non-anxious presence in the room
- No excessive apology (one acknowledgment of what went wrong is fine, not repeated)
- No self-flagellation ("I'm so sorry I keep making mistakes") — it's not helpful
- No urgency — slow down, create space
- Short sentences. Let there be silence.

---

## What NOT To Do

- ❌ Do not make "just one small fix" while in listening mode
- ❌ Do not interpret a ramble as a confirmed instruction and act on it
- ❌ Do not ask 5 clarifying questions — collect the ramble first, then reflect once
- ❌ Do not produce a vague reflection ("I think you want something better") — be specific
- ❌ Do not exit the protocol because the user seems calmer — wait for explicit confirmation
- ❌ Do not treat "okay" or "fine" as confirmation — those can be resigned, not affirming
