# Quality Review Router

> Split by review intent: correctness first, then structure, then proof/tooling.
>
> Report findings by issue name + location. Do not rely on checklist numbers.

## Modules

- `./quality/core.md` - Day-to-day correctness, readability, state, defensive coding, and logic traps.
- `./quality/architecture_and_maintainability.md` - Structure, coupling, async/API design, duplication, over-engineering, and long-term maintainability.
- `./quality/verification_and_tooling.md` - Tests, refactor safety, docs drift, build hygiene, and tool-wrapper contract integrity.

## Common Loadouts

| Review Type | Load |
|-------------|------|
| General code review | `core` + `architecture_and_maintainability` |
| Bug hunt / correctness audit | `core` + `verification_and_tooling` |
| Refactor / simplification review | `architecture_and_maintainability` + `verification_and_tooling` |
| Scanner / wrapper / action / plugin review | `verification_and_tooling` + `architecture_and_maintainability` |
| Small feature diff | Start with `core`, add one more module only if the change expands in scope |

## Loading Rule

- Start with this router.
- Load `./quality/core.md` unless the review is explicitly narrow and non-core.
- Add one secondary module based on whether the risk is structural or verification/tooling related.
- Load all three modules only for full-codebase audits.
