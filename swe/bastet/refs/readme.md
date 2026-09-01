# README Writing Guide
> Load when Bastet is asked to write, review, refresh, or improve `README.md`.
>
> Goal: make the repo front door clear, trustworthy, fast to scan, and easy to act on.

---

## Core idea

A strong README helps a reader answer, in order:

1. What is this?
2. Why should I care?
3. How do I get it working?
4. How do I use it correctly?
5. Where do I go for deeper detail?

The README is not a dumping ground for every fact in the repo. It is the front door.

Optimize for orientation first, action second, depth third.

If forced to choose, missing critical context is worse than a slightly long README.

---

## The principles

### 1. Reader first

Always infer the primary audience before drafting:

| Repo type | Primary reader | README emphasis |
|---|---|---|
| Public open source | Evaluators, users, contributors | Fit, install, usage, contribution, license |
| Internal app/service | Teammates, new hires, on-call engineers | Setup, run commands, env, architecture links, runbooks |
| Library/package | Developers comparing options | One-liner, install, minimal usage, API shape, caveats |
| CLI tool | Terminal users | Install, commands, flags, examples, output |
| Personal/portfolio | Future you, reviewers | What it is, why it exists, stack, demo, lessons |
| Config/dotfiles | Future you, maintainers | What lives here, how to apply it, gotchas, extension points |

Do not assume open-source defaults if the repo is clearly private or internal.

### 2. Cognitive funneling

Order information from broad and high-value to narrow and detailed.

Use this funnel:

1. Hook
2. Orient
3. Get in
4. Go deeper
5. Close

Or, more concretely:

| Zone | What it should do |
|---|---|
| Hook | Name the project and show immediate signals of trust |
| Orient | Explain what it does, for whom, and why it exists |
| Get in | Give the fastest path to a working install or run |
| Depth | Cover usage, configuration, API, architecture links, caveats |
| Close | Explain contribution, support, status, and license as needed |

The best README lets a slightly familiar reader refresh their memory without scrolling much.

### 3. Progressive disclosure

The reader should get value quickly, then more depth only if they keep going.

- Put the one-liner and quickstart near the top.
- Put the minimal working example before advanced options.
- Link to deeper docs instead of forcing the whole manual into `README.md`.
- Use a table of contents only when the document is long enough to need one.

Use this rule of thumb: too long is better than too short when the alternative is leaving the reader confused. If the README grows heavy, split depth into `docs/` and keep the front door strong instead of deleting essential guidance.

### 4. Structure should feel predictable

People scan READMEs. Reuse familiar section order unless the repo has a strong reason not to.

The reader should not have to hunt for install steps, usage, or contribution notes.

### 5. Show, do not merely describe

Good README sections are concrete:

- real commands, not pseudocode
- real file paths, env var names, and entrypoints
- real sample output when it helps
- real screenshots or GIFs when the interface matters

If code appears in the README, it should be runnable or very close to runnable.

### 6. Respect the reader's time

The README is not sales copy.

- Say what the project does plainly.
- State limits and caveats early when they matter.
- Let the reader decide quickly whether the repo fits their needs.
- Prefer concise explanation over grand claims.

### 7. Specific beats hype

Prefer:

- exact commands over vague setup guidance
- named dependencies over "standard prerequisites"
- concrete examples over abstract promises
- specific constraints over hand-wavy reassurance

Replace vague claims like "powerful" or "seamless" with evidence, features, behavior, or output.

### 8. Visual hierarchy matters

Use headings, spacing, tables, badges, and code blocks to guide scanning.

- Keep the first screen useful.
- Use badges contextually, not automatically.
- Avoid giant unbroken paragraphs.
- Avoid burying setup steps inside prose.

### 9. Truth beats polish

An accurate plain README is better than a beautiful stale one.

Before calling the README good, verify it against the repo:

- package manifests and scripts
- lockfiles and toolchain pins
- `Makefile` / `justfile` / task runner commands
- `.env.example`
- actual entrypoints
- CI and release state

### 10. The README is a living index

The README should point to deeper documents when the repo has them:

- `docs/product.md`
- `docs/spec.md`
- `docs/arch.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- runbooks, API docs, or examples

Do not duplicate a full manual when a stable deeper doc already exists.

If a `docs/` folder exists, add a short "Where to read next" or "More documentation" section near the end of the README. It should work as a quick map, not a second table of contents.

---

## Bastet modes for README work

### Create from scratch

When no README exists or the current one is unusable:

1. Identify repo type and audience.
2. Inspect actual commands and prerequisites from the repo.
3. Draft the skeleton in cognitive-funnel order.
4. Fill only what can be verified.
5. Mark gaps explicitly rather than inventing details.

### Improve an existing README

When structure exists but quality is weak:

1. Preserve useful existing content.
2. Reorder into a clearer scan path.
3. Tighten the opening.
4. Replace vague prose with concrete commands and examples.
5. Move deep detail into linked docs when the README is overloaded.

### Refresh a stale README

When the README exists but no longer matches the repo:

1. Compare claims to the current project state.
2. Fix stale commands, dependencies, flags, paths, screenshots, and badges.
3. Remove sections that no longer reflect reality.
4. Add missing setup or usage details that the current repo now requires.

### Review only

When asked for critique rather than edits:

Report in this order:

1. what the README does well
2. what blocks onboarding or evaluation
3. what is stale or misleading
4. what Bastet would change first

---

## Recommended section order

Use this default order unless the repo type suggests a better variant.

### 1. Title

- Project name as H1
- Clear, searchable, self-explanatory when possible

### 2. Badges

- Treat badges as optional, not required.
- Skip them for private repos unless they add real value.
- For public repos, prefer a coherent set of meaningful signals rather than one or two lonely badges.
- If there are not enough trustworthy, useful badges yet, omit them instead of forcing sparse decoration.

### 3. One-line description

One sentence that says what it does, for whom, and what makes it distinct.

### 4. Visual or quick proof

Optional, but often helpful:

- screenshot
- GIF
- tiny CLI session
- small output sample

### 5. Table of contents

Only for longer READMEs.

### 6. Overview or features

Use short bullets or a short paragraph to answer:

- what problem this solves
- why it exists
- what makes it useful

### 7. Quickstart / installation

This is the highest-value section after the opening.

Requirements:

- list prerequisites first
- show exact copy-pasteable commands
- assume zero context
- keep the shortest path to "it works" visible

### 8. Usage

- minimal working example first
- common cases next
- advanced cases later or in linked docs
- show output when it clarifies behavior

### 9. Configuration / API / environment

Use tables when it improves scanning.

Good fits here:

- env vars
- CLI flags
- config keys
- API entrypoints
- important defaults and optional values

### 10. Project structure / deeper docs

If the repo has meaningful supporting docs, show where to go next.

If `docs/` exists, this section usually belongs near the end and should answer: "What should I read next?"

Good examples:

- `docs/product.md` for the human overview
- `docs/spec.md` for exact behavior
- `docs/arch.md` for implementation shape
- `docs/troubleshooting.md` for common failures
- `examples/` for runnable examples

### 11. Contributing / support

- how to open issues or PRs
- where contribution instructions live
- how to get help

### 12. Status / roadmap / caveats

Optional, but useful when it affects expectations.

### 13. License

Mandatory for public open-source repos. Surface it early if the license is restrictive.

### 14. Optional closing flourish

If it fits the project's personality, end with one small cute, human, or memorable touch.

Good fits:

- a tiny sign-off line
- a friendly invitation to try or contribute
- a short project motto
- one tasteful emoji or playful sentence

Keep it brief. The ending should leave charm, not clutter.

---

## README by repo type

### Library or package

Emphasize:

- what it does
- install command
- minimal usage example
- API shape
- caveats or compatibility notes

The reader is often evaluating whether to adopt it in minutes.

### App or service

Emphasize:

- what the system does
- local setup
- env requirements
- how to run dev / test / build
- where architecture and operations docs live

### CLI

Emphasize:

- install method
- command syntax
- common examples
- important flags and output
- shell/platform assumptions

### Internal repo

Emphasize:

- how teammates get running fast
- operational links and runbooks
- required secrets and setup sources
- ownership and support path

### Personal or portfolio project

Emphasize:

- what it is
- demo or screenshot
- tech stack
- why it was built
- notable constraints or lessons

---

## Writing rules Bastet should enforce

### Opening-screen test

Before scrolling, the reader should be able to see most of these:

- project name
- one-line description
- trust signals or status
- quickest path to trying it

### Command quality

- Commands must be copy-pasteable.
- Use fenced code blocks.
- Include prerequisites before the commands that require them.
- Do not hide required env vars or services.

### Example quality

- Start with the smallest useful example.
- Use real syntax.
- Include expected output when it reduces ambiguity.
- Keep examples in sync with actual behavior.

### Honesty about constraints

Surface important caveats instead of hiding them deep in the doc.

Examples:

- supported platforms
- required external services
- experimental status
- breaking compatibility constraints

### Link discipline

- Link specialized terms the reader may not know.
- Link deeper docs instead of duplicating them.
- Avoid dead-end "see docs" text without a path.

### Badge discipline

Each badge should answer a real reader question. If it does not, cut it.

Default posture:

- no badges is better than weak badges
- a coherent badge cluster is better than one or two token badges
- social badges like stars or downloads should appear only when they add believable signal
- trust badges usually beat vanity badges

### Visual discipline

- Prefer short paragraphs.
- Prefer bullets when scanning matters.
- Prefer tables for options, env vars, or flags.
- Keep heading levels consistent.

---

## Common README failures

### Weak openings

- title only, no one-liner
- one-liner too vague to be useful
- opening paragraph full of hype instead of substance

### Setup friction

- prerequisites missing
- commands not runnable as written
- hidden dependency on Docker, Redis, Postgres, cloud creds, or a specific OS

### Usage gaps

- no example
- only advanced examples, no minimal case
- pseudocode instead of real commands or code

### Structural problems

- wall of text
- no clear section order
- table of contents for a tiny README
- key setup details buried far below the fold

### Trust problems

- stale screenshots
- broken badges
- commands that no longer exist
- README describes an older product shape than the repo actually contains

### Tone problems

- sales language instead of explanation
- vague claims like "robust", "powerful", "intuitive", or "enterprise-grade"
- filler phrases that hide the actual instruction

### Clarity failures

- the reader still cannot answer what this is, why it exists, and how to start within the first screen or two
- the opening assumes prior context the newcomer does not have
- the README is technically accurate but not friendly to scan or act on

---

## README audit workflow

When Bastet is asked to improve an existing README, verify these against the repo before editing:

1. install commands
2. dev/test/build commands
3. package manager choice
4. runtime or toolchain version
5. env vars and config files
6. screenshots or example output
7. badge links and branches
8. links to docs, examples, contribution guides, and license

If the repo and README disagree, fix the README or flag the discrepancy explicitly.

---

## Starter skeleton

Use this when creating a README from scratch:

````markdown
# <Project Name>

<optional badges>

<one-line description>

<optional screenshot, GIF, or short output sample>

## Overview

<what it does, who it is for, why it exists>

## Quickstart

### Prerequisites

- <runtime or tool>
- <service or dependency>

### Install

```bash
<exact commands>
```

### Run

```bash
<exact commands>
```

## Usage

```bash
<minimal example>
```

<expected output or short explanation>

## Configuration

| Name | Required | Default | Description |
|---|---|---|---|
| `<ENV_VAR>` | yes/no | `<value>` | <what it controls> |

## Project structure

- `docs/...` - <deeper docs>
- `examples/...` - <runnable examples>

## Contributing

<how to contribute or where CONTRIBUTING.md lives>

## License

<license>
````

Adapt the skeleton to the repo. Do not force sections that are irrelevant.

---

## Final checklist

Before Bastet declares the README polished, confirm:

- The top of the file explains what the project is in one pass.
- The top of the file makes "what, why, and how to start" easy to grasp fast.
- The fastest path to trying the project is obvious.
- Commands, flags, paths, and env vars match the repo.
- The doc uses concrete examples, not vague promises.
- The structure is easy to scan.
- Deeper docs are linked where needed.
- The README helps a new reader avoid opening source code immediately.
- If the project voice allows it, the ending leaves a small memorable touch.
