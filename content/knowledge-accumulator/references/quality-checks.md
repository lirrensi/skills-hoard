# Quality Checks

Use these checks to keep the knowledge base useful without turning it into bureaucracy.

## Core gates

### 1. Retrieval gate

Important material should have a clear home in `taxonomy.md` and a discoverable place in `corpus.md`.

Check:

- every major addition maps to at least one taxonomy area
- overloaded sections are visible rather than silently growing forever
- recurring user questions have a plausible retrieval path

### 2. Provenance gate

Important claims should be traceable.

Check:

- links have short why-this-matters annotations
- embedded material has clear attribution
- high-value or disputed notes record where they came from and when they were checked if known

### 3. Gap visibility gate

Unknowns should be explicit.

Check:

- contradictions are recorded instead of flattened away
- thin areas appear in `gaps.md`
- next harvest targets are named

### 4. Resumeability gate

Another agent should be able to continue the project without guessing too much.

Check:

- `charter.md` still matches the real project
- `session_log.md` explains what changed recently
- source handling assumptions are visible in `source_map.md`

### 5. Coverage gate

The corpus should not grow blindly.

Check:

- taxonomy areas with weak coverage are identified
- source-type skew is visible
- important use cases are not all supported by a single source class unless intentional

## Lightweight audit checklist

Run this after a meaningful harvest session or before distillation:

- [ ] New material was mapped into the taxonomy
- [ ] New sources were added or updated in `source_map.md`
- [ ] Search activity worth preserving was recorded in `search_log.md`
- [ ] New gaps or contradictions were added to `gaps.md`
- [ ] Coverage concerns were reflected in `coverage_report.md`
- [ ] `session_log.md` says what changed and what should happen next

## Distillation readiness check

Before compressing into a guide or skill, ask:

- are the core sections stable enough to compress
- are the key decisions backed by enough evidence
- are important contradictions either resolved or clearly marked
- do we know what is being omitted by compression

If not, keep accumulating.
