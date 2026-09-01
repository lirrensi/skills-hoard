# Completion Standards

## What "Done" Means

A task is only done when:

1. The code changes are complete and correct
2. Tests are updated, added, and passing
3. Documentation reflects the changes
4. The project builds cleanly (if applicable)
5. The change has been run, tested, or deployed and verified to work
6. A clear proof of work is provided
7. The user can inspect the result without additional work from the agent

**Not done:**
- Code edited but tests not run
- Tests passing but build not attempted
- Build succeeding but artifact never executed or checked
- Docs not updated
- "It should work" without verification

## Catastrophic Failure — When to Stop

Only stop early if a hard blocker makes further progress impossible despite reasonable workarounds:

- Required compiler or toolchain cannot be installed in the environment
- Permanent network failure blocking required dependencies
- Missing permissions that cannot be resolved
- External service is down and the task is fundamentally impossible without it
- The plan contains a real contradiction that makes correct execution impossible
- Continuing would clearly cause destructive or unsafe behavior outside the approved scope

In such cases:
1. Document the blocker precisely
2. State what was attempted to resolve it
3. Report what *was* completed before the blocker
4. Mark the task as failed/blocked with full context

Do **not** stop for:
- A test failing (fix it)
- A build error (fix it)
- A linter complaint (fix it)
- Uncertainty about whether something is needed (assume project conventions require it)
- Wanting to ask the user a preference (decide based on project norms and move forward)

## Example Deliverable

> **Engage complete.**
>
> **Done:** Implemented JWT refresh token rotation in the auth module.
>
> **Files:**
> - `src/auth/login.ts` — refresh logic
> - `tests/auth/login.test.ts` — 4 new tests for rotation
> - `docs/auth.md` — updated flow diagram and endpoint docs
> - `CHANGELOG.md` — v2.4.0 entry
>
> **Validation:**
> - `pnpm test` — 47/47 passing (was 43/43)
> - `pnpm build` — clean, no errors
> - `pnpm lint` — clean
> - Ran dev server, hit `/auth/refresh` with expired token — returned 200 with new token
>
> **Proof:**
> - Build artifact: `dist/app-v2.4.0.zip`
> - Preview URL live and verified: `https://preview-123.app`
> - End-to-end login flow tested and working
>
> **Decisions:** Used 15-minute sliding window for refresh expiration to match existing session timeout convention.
>
> **Assumptions:** The `REFRESH_SECRET` env var is already set in staging; if missing, the endpoint will 500.
>
> **Deviations:** None — followed the plan exactly.
>
> **Blockers:** None.
>
> **Next steps:** Ready for production deploy when approved.
