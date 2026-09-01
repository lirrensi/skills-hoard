# Mode: Inquire

**Trigger:** Asked to find, explain, compare, govern, or clarify how something works.

This is the **default mode**, especially for subagent use. You are a reader and interpreter. You do not write or change anything unless explicitly asked.

---

## Workflow

### 1. Orient via INDEX.md
Start with the root `docs/INDEX.md` to understand the landscape. Then drill into relevant folder INDEX.md files. Never open individual files at random — use the index map first.

### 2. Follow the stack downward
Read in order:
1. `docs/overview/` — for product identity and purpose
2. `docs/spec/` — for the canonical behavioral answer
3. `docs/architecture/` — for implementation context
4. `docs/verification/` — for how behavior and implementation are checked
5. `docs/stories/` — for how the system was learned, debugged, or surprised us

### 3. Cross-reference
If the spec references another spec, follow the link. Use `links: depends_on` in frontmatter to understand dependencies.

### 4. Inspect code only if necessary
Only read code when:
- Docs are silent on the question
- Docs appear stale or contradictory
- Asked specifically about implementation details

### 5. Report clearly
Structure your answer:
- **What overview says** — identity, purpose, scope
- **What spec says** — exact behavior, requirements, scenarios
- **What architecture says** — implementation structure
- **What verification says** — test/verification taxonomy, tools, suites, evidence, traceability, and gaps
- **What stories say** — historical context, prior debug sessions, how the system was learned
- **What code does** (if checked) — actual behavior
- **Whether they agree** — flag any discrepancies

---

## Search Strategy

1. **Start with INDEX.md** — scan the relevant folder's INDEX.md for document summaries and tags.
2. **Follow tags** — if you know the domain (e.g. "auth"), check the tags section of INDEX.md.
3. **Read frontmatter** — `title` and `tags` in frontmatter tell you if a doc is relevant before reading it.
4. **Use `links`** — `depends_on` tells you what to read first.
5. **Check `docs/stories/` for history** — when the question is "has anyone seen this before?", "why did we do it this way?", or involves weird behavior, search stories first.

---

## What NOT to do in Inquire mode

- ❌ Create, edit, move, or delete any documents
- ❌ Propose changes or write delta specs
- ❌ Make architectural decisions
- ❌ Write code or suggest code changes (unless explicitly asked)
- ❌ Guess when docs are silent — say "not documented" and flag it

---

## Reference Files to Load

Only if you need them for this inquiry:
- `../principles.md` — if you need to cite philosophy or conflict resolution rules
- `../spec-format.md` — if you're explaining how a spec is structured
- `../verification.md` — if you're explaining how correctness is checked
- `../ontology.md` — if you need to reference node types or link types
- `../folder-structure.md` — if the question involves doc organization
- `../stories.md` — if the inquiry involves historical context, debug sessions, or empirical lessons
