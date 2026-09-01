# Security Review Router

> Split by trust boundary and attack surface.
>
> Report findings by issue name + location. Add CWE/CVE tags when relevant. Do not rely on checklist numbers.

## Modules

- `./security/core.md` - Input handling, secrets, logging, failure modes, and privacy controls that apply almost everywhere.
- `./security/identity.md` - Authentication, authorization, sessions, tenancy, and privilege boundaries.
- `./security/remote_surfaces.md` - Headers, APIs, browser/mobile surfaces, network edges, and abuse-prone exposed flows.
- `./security/execution_and_supply_chain.md` - Runtime, file/tool execution, CI/CD, agent/tool trust boundaries, and supply-chain risks.

## Common Loadouts

| Repo Shape | Load |
|------------|------|
| Web service / SaaS API | `core` + `identity` + `remote_surfaces` |
| Browser frontend | `core` + `remote_surfaces` |
| Local-first app / desktop / mobile | `core` + `remote_surfaces` + `execution_and_supply_chain` |
| CLI / scanner / extension / plugin | `core` + `execution_and_supply_chain` |
| AI or tool-using system | `core` + `execution_and_supply_chain` (+ `identity` if it acts on user/org data) |
| Broad platform / full-stack audit | Start with `core`, then add only the modules that match the repo's real surfaces |

## ML-Heavy Review Stance

- For LLM/ML/agentic systems, Anubis is a code-first reviewer: inspect code paths, configs, and existing automated tests.
- Do not pretend this is interactive red-teaming, heavy end-to-end validation, or runtime behavioral proof.
- If the repo is ML-heavy or relies on non-deterministic systems, review more deeply, then state the coverage limit explicitly: code + existing tests only.
- When important runtime behavior cannot be proven from code or existing tests, report that gap as a finding or coverage limitation, not as a silent assumption.

## Loading Rule

- Start with this router.
- Load `./security/core.md` for nearly every security review.
- Add only the extra modules that match the codebase's actual trust boundaries.
- Load all four modules only for genuinely broad platform reviews.
- If the repo uses LLMs, RAG, tools, agents, embeddings, notebooks, evals, or model-serving paths, always add `./security/execution_and_supply_chain.md` and apply the ML-heavy stance above.
