# Step: Brief

Before extracting a brief:

1. Check the project root for `EDITING.md` and use it if present.
2. If root `EDITING.md` is missing, offer to create it from the bundled template/reference or temporarily fall back to the bundled `EDITING.md`.
3. Check the project root for `VOICE.md` and use it if present.
4. If root `VOICE.md` is missing, infer voice from the material for this pass and ask whether the user wants to create `VOICE.md` if the task involves substantial rewriting or ongoing work.

## Goal

Extract the essay's core intent from existing material when the spine is still unclear.

## Focus

Produce a lightweight working brief that identifies:
- situation versus story
- one big idea
- audience
- tone / register
- main sections or threads
- must-keep constraints
- must-avoid constraints

Ask only for what is missing.

## Output format

```markdown
# Essay Brief

## One Big Idea
- [...]

## Situation vs. Story
- **Situation:** [...]
- **Story:** [...]

## Audience
- [...]

## Voice
- [...]

## Main Threads
- [...]

## Must Keep
- [...]

## Must Avoid
- [...]
```
