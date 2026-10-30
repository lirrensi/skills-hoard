# Performance: Migrations And Schema

> DDL and migration risk review. Locks, reversibility, and sequencing — not SQL authoring.
>
> Load this when the diff or repo contains migrations, DDL, or schema changes.

---

## Lock Class Per Operation

| Operation | PG lock | MySQL lock | Note |
|---|---|---|---|
| ADD COLUMN nullable, no default | Lightweight | Lightweight | Safe starting point. |
| ADD COLUMN with volatile default / NOT NULL | Rewrite / heavy | Rebuild | Backfill separately instead. |
| DROP COLUMN | Lightweight metadata, dependent views break | Rebuild on older versions | Irreversible — flag prominently. |
| ADD INDEX | Share lock unless CONCURRENTLY | Online DDL varies by version | Prefer concurrent / online builds. |
| DROP TABLE / DROP COLUMN | Exclusive | Exclusive | Irreversible means irreversible. |

---

## Duration By Table Size

| Size | Expectation |
|---|---|
| Small (<10k rows) | Most ops complete fast; still verify in CI. |
| Medium (10k–1M rows) | Index builds and rewrites need scheduling. |
| Large (>1M rows, or unknown) | Assume large. Require online/concurrent path plus backfill plan. |

---

## Reversibility

| Migration | Reversible | Action |
|---|---|---|
| Additive nullable column / new table / new index | Yes | Standard rollback applies. |
| Backfill + constraint added later | Yes, in stages | Roll back constraint before data. |
| DROP COLUMN / DROP TABLE / type narrowing | No | Flag prominently; require backup + explicit sign-off. |

---

## Safe Sequence

Add nullable → backfill in batches → validate → add NOT NULL / constraint. Never combine schema change and data rewrite in one deploy.

---

## Pre / Post Validation

| Phase | Check |
|---|---|
| Pre | Confirm table size, lock class, replica lag headroom, rollback story. |
| Post | Confirm row counts, constraint holds, index used by plan, app reads/writes succeed. |
