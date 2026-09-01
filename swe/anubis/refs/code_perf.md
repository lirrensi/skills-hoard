# Performance Review Router

> Split by bottleneck shape: fundamentals, services/data paths, and client/runtime behavior.
>
> Start with the smallest module set that matches where latency or throughput is actually spent.

## Modules

- `./perf/core.md` - Triage, tooling, algorithmic complexity, CPU/memory basics, observability, and general anti-patterns.
- `./perf/services_and_data.md` - Databases, caches, queues, networks, service topology, contention, and overload control.
- `./perf/frontend_and_runtime.md` - Frontend rendering, file/storage paths, startup time, runtime/GC tuning, and mobile constraints.

## Common Loadouts

| Repo Shape | Load |
|------------|------|
| Backend service / API / worker | `core` + `services_and_data` |
| Frontend / SPA / local-first UI | `core` + `frontend_and_runtime` |
| CLI / desktop app | `core` + `frontend_and_runtime` |
| Full-stack app | `core` + `services_and_data` + `frontend_and_runtime` |
| Performance bug with unknown source | `core` first, then add the module that matches the hotspot |

## Loading Rule

- Start with `./perf/core.md`.
- Add `services_and_data` for backend latency, throughput, queues, or database issues.
- Add `frontend_and_runtime` for page speed, startup time, local file paths, or device/runtime constraints.
- Load all three modules only when the product genuinely spans both service and client/runtime bottlenecks.
