# Scan Guide — What Counts as a Part

## The filter: feature-flow, not file

A part is a **feature flow or subsystem the user can name** — “the ingestion pipeline,” “the auth flow,” “the report renderer.” It is not a file by accident; it is a flow by purpose.

**Counts:**
- A flow: `Kafka → Flink → Postgres` (3 files + infra, one user outcome)
- A section: `report rendering (HTML → PDF)` (templates + engine + QC)
- A subsystem: `on-call handover bot` (6 teams depend on it)

**Never counts:**
- 20-line README, `utils/foo.ts`, a single helper, a config tweak, a typo fix. If you need “and” to describe what the part *does* for a user (“it formats *and* validates *and* logs”), it’s probably too small. Commonsense: would a user notice the before/after? If no, ghost it.

## How to surface 5–8 candidates

1. **Map:** `glob` + `grep` + `read` top-level, but filter with taste. Look for flows with fan-out, long files, TODOs, `any`, `FIXME`, slow paths, or “this is gross” comments.
2. **Rank by noticeable need:** Which flow has the biggest gap between current and *insane*? Not “most bugs” — most *upside* if made extreme.
3. **List 5–8:** Each as `name — path(s) — one-line why it noticeably needs it`. No trivia.

## Example candidates

- `ingestion pipeline — src/ingest/*, infra/flink/* — p95 6h, cost +22%, batch not streaming`
- `auth flow — src/auth/*, src/session/* — 3 systems, 1.8m search per handle`

If you surface a 20-line util, you failed the gate — re-filter.
