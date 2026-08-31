---
name: next-best-improvement
description: >
  Picks one feature-flow-level fragment of the whole project that noticeably needs extreme improvement and makes it insane — can do anything (refactor, redesign, perf, UX, deps, tests) to make it extremely better. Uses a whole-project scan then one of 3 picking modes: ask user for a specific part, yolo (AI picks the most needy part), or random (AI surfaces candidates then randomly picks one). This is THE extreme skill for ANY “improve a part”, “make this insane”, “extreme polish”, “yolo improve”, “random improvement”, “next improvement”, “pick a section to improve”, “take this feature and make it extreme”, “out-of-the-box improvement”, or “brainstorm an insane improvement” — even if the user doesn’t say “next-best-improvement”. Also trigger for “improve this feature flow”, “extreme refactor this part”, “take the worst part and make it best”. Do NOT trigger for small high-leverage “next-best-thing” (smallest move) or whole-project architecture (use nextreme-architect) — this is one picked fragment, extreme.
license: MIT
compatibility: git>=2.20
---

# Nextreme Next-Best-Improvement — The Extreme Fragment Engine

This skill produces **one insane, taste-driven, proof-backed improvement** to a single feature-flow-level fragment that survives review: every change is on a **new branch**, every before/after is shown, every win is benchmarked. The output is not a vague suggestion — it is a **merged-ready branch + proof pack** with disciplined diff, measured gains, and zero AI slop. You get three deliverables: the **branch**, the **before/after + diff**, and the **proof/benchmarks**.

You are **extreme and unbound inside the picked part** — you can do anything that leads to improvement — but you are **disciplined about how you pick**. You scan the whole project with commonsense (never a 20-line README or a trivial util), surface feature-flow-level candidates that noticeably need it, then you **must** create a new branch before you touch a file, and **must** pick exactly one fragment via the 3-mode menu. Inside that part, you have full creative freedom to brainstorm extreme, out-of-the-box solutions.

---

## Why This Is Not Generic

Most “improve” skills are bounded: they polish the file you pointed at, or they pick the easiest line to lint. They never ask what *deserves* to be improved, they never create a branch, and they never prove the win — so the diff is noise and the improvement is invisible.

This fuses the core of `next-best-thing` (smallest high-leverage move) and `nextreme-decision` (commit to one insane pick) but refuses their bounds.

| Generic | This skill |
|---|---|
| Picks the file you named, or the easiest fix | Scans the whole project, surfaces feature-flow-level candidates that noticeably need it, uses commonsense (never trivia) |
| Works on `main`, no proof | **Hard gate: creates a new branch first** — cannot proceed without it; proves with before/after + benchmarks |
| One safe tweak | **Anything** inside the picked part — refactor, redesign, perf 10x, UX, deps, tests — extreme brainstorming, out-of-the-box |
| Silent pick | **3-mode menu you must present:** user-picked → `yolo` (AI picks most needy) → `random` (candidates then random) — one fragment per run |

> If the picked part wants a better improvement that no pattern names, invent it — but keep it branch-isolated, validated, and proven.

---

## Golden Code Quality Rules — ENFORCED

These are non-negotiable. Every branch and every script this skill ships must pass them. Violation = task fails.

Keep code human-readable, small, and obvious. No AI slop.

* **Names tell the truth** — variables/functions reveal intent. No `data`, `info`, `result`, `handler`, `manager`, `helper`, `utils`, `foo`.
* **One job per unit** — if you need "and" to describe what a function does, split it. Files own one domain.
* **Guard clauses over nesting** — early returns, fail fast. No pyramids, no `else` after `return`. Nesting past 2–3 levels is a signal to restructure.
* **No duplication** — never copy-paste. Third occurrence of the same logic = must abstract. Two is coincidence, not a pattern.
* **No dead weight** — zero dead code, commented-out code, `console.log`, unused imports. Delete, don't comment out.
* **Types are contracts** — no `any`, no silent `as` casts, narrow `unknown` explicitly. At an untyped boundary (`JSON.parse`, third-party API), a cast is allowed only alongside visible runtime validation.
* **Errors never silent** — every failure path is handled, returned, or logged with context. Never an empty catch, never a swallowed promise.
* **No magic** — no unexplained numbers or strings. Name every constant. No cryptic one-liners.
* **Explicit dependencies** — no hidden globals, no surprise side effects. Inputs in, outputs out. Pure where possible.
* **Readability > cleverness** — code reads like prose: linear flow, consistent style, self-documenting. Comments explain why, not what.
* **No premature abstraction** — no wrappers, layers, or helpers you don't need today. YAGNI. Abstract on the real second pattern.
* **Leave it cleaner, not bigger** — boy-scout only on touched code.
* **State assumptions, don't guess silently** — if the spec is ambiguous, say what you assumed and why, in a comment or PR note.

**Auto-rejected AI slop:** placeholder `TODO` without a ticket, generic scaffolding, empty `try/catch`, `lorem`-ish names, duplicated boilerplate, over-engineered factories/managers, unvalidated `as` casts at boundaries, silent assumptions about ambiguous specs, inconsistent style within one file, **and fragment-level slop:** improving a trivia file, working on `main`, no before/after, no proof, `Click to add` residue, overlapping UX.

---

## Improvement Axes — You Can Do Anything Inside the Picked Part

| Axis | You Might | Example insane win |
|---|---|---|
| **Architecture** | Split a god-file, introduce a deep module, flip data flow | 600-line handler → 3 deep modules, testable in isolation |
| **Performance** | Index, cache, stream, parallelize, cut N+1 | p95 6h → 4m with incremental materialization |
| **UX / Visual** | Bento grid, editorial taste, motion, empty states | Zinc backbone + tracking iron law, no AI vertical rhythm |
| **Correctness** | Harden types, eliminate `any`, add invariant checks | 11 `any` → 0, plus `validate` at boundaries |
| **DX** | CLI polish, error messages, docs, `validate` QC | Every failure path logs with context, not silent |
| **Product** | Rethink the feature flow itself | Replace 3-step wizard with one-shot graph query |

All ship: `scripts/branch_guard.py` (branch gate) + `scripts/proof_builder.py` (before/after + benchmarks). You choose the axis per fragment — state the one-line justification.

---

## Core Workflow — Extreme but Gated

Each step ends on a **completion criterion**. Do not proceed until it passes.

### 1. Scan — Understand the Whole Project with Commonsense

Map the repo as `nextreme-architect` would: `glob` + `grep` + `read` key files, but filter with taste. Surface **feature-flow-level** candidates that noticeably need extreme improvement — a whole feature, a major section, a subsystem, a critical flow — never a 20-line README, never a single trivial helper. Use commonsense: if you need “and” to describe what the part *does* for a user, it’s probably too small.

Reference: `references/scan-guide.md` — what counts as a part, how to surface 5–8 candidates.

Completion criterion: 5–8 candidates listed, each is a feature-flow (file group or flow) with one-line *why it noticeably needs it*; no trivia.

### 2. Branch — Hard Gate (Cannot Proceed Without It)

Create a new branch **before** you read the picked part for edit. This is not optional.

```bash
git checkout -b next-best-improvement/<slug>
# slug = kebab of the fragment (e.g. event-graph-ingest)
```

If branch creation fails, stop and fix git — do not touch a file on `main`.

Reference: `scripts/branch_guard.py` — idempotent branch creation, dirty-tree check.

Completion criterion: `git branch --show-current` is `next-best-improvement/<slug>` and `git status` is clean (or stashed) — proven by command output.

### 3. Ask — Present the 3 Choices (You Must Ask)

Present exactly this menu and wait — the pick is the unique bit:

```
Pick one fragment to extremely improve:

1. Specific — you tell me the part (e.g. “the ingestion pipeline”)
2. Yolo — I pick the single fragment that most needs extreme improvement
3. Random — I surface candidates then randomly pick one

Reply with 1, 2, or 3 (or the part name for 1).
```

Do not auto-pick, do not collapse choices. If the user pre-answered in their prompt (`yolo`, `random`, `improve X`), honor it and skip the wait — but still log which mode was used.

Completion criterion: one mode is chosen and one fragment is locked (name + path + why it was picked); logged as `mode: user|yolo|random`.

### 4. Extreme Brainstorm — Out-of-the-Box Before You Code

For the locked fragment, propose **3 insane alternatives** before you commit to one. Each is a different axis (e.g., architecture vs perf vs product rethink). Make them out-of-the-box, not safe tweaks. Then commit to **one** extreme pick and state why it wins — like `nextreme-decision` but inside the fragment.

Reference: `references/improvement-axes.md` — how to make alternatives actually distinct.

Completion criterion: 3 distinct extreme alternatives listed + one committed pick with one-line “why this is the most insane win”.

### 5. Improve — Do Anything Inside the Picked Part

Implement the committed pick. You can do anything that leads to improvement — refactor, redesign, add deps, delete code, add tests, change API (with migration note if breaking), speed up, repolish UX. Keep blast radius to the picked part, but do not be tame inside it.

- Keep `main`’s tests green on the *picked* part’s scope; fix root causes, not symptoms.
- Follow Golden Rules — no AI slop leaves this step.

Completion criterion: the picked part is modified on the new branch, `validate` (tests / `validate_<artifact>.py` / `tsc` / `lint` whatever the fragment owns) is green, and no file outside the fragment was touched without an explicit note.

### 6. Proof — Before/After + Benchmarks (You Must Prove)

Build the proof pack the user asked for — what changed and what/how it was before, with numbers:

- **Diff:** `git diff --stat` + key `git diff` hunks (or screenshots for UX).
- **Before/after:** 2–3 concrete snippets or screenshots (e.g., “before: 6h batch, after: 4m streaming”).
- **Benchmarks:** whatever proves the win — `time`, `hey`, `pytest`, `tsc --noEmit`, `validate` output, Lighthouse, or a before/after table with `before | after | Δ`.

Reference: `scripts/proof_builder.py` — collects diff, snapshots, and benchmark stubs.

Completion criterion: proof pack exists as `proof/<slug>.md` (or PR description) with diff stat, 1–2 before/after pairs, and at least one measured proof (numbers, not adjectives).

### 7. Validate — No Silent Failure

Run the lightest validation that fully fits the fragment: tests, `tsc`, `lint`, `build`, `validate` script. If the baseline was red, your change must not make it worse — report the baseline.

Completion criterion: validation command output is pasted in proof, exit 0 (or baseline-red acknowledged).

### 8. Deliver — Branch + Proof, Not Vague Advice

Report: the branch name, the picked mode + fragment + why, the extreme pick + why it won, the proof pack path, and the one open risk.

Do not merge. Do not push unless the user says so — `git-guardrails` applies.

Completion criterion: report lists branch, mode, fragment, extreme pick, proof path, and open risk; no merge/push without explicit go-ahead.

---

## Quick Picks — What a “Part” Looks Like (Do Not Start From Trivia)

| Part (feature-flow) | Why it noticeably needs it | Extreme direction example |
|---|---|---|
| `ingestion pipeline (Kafka → Flink → Postgres)` | p95 6h, cost +22% | Incremental materialization, RocksDB, retract streams |
| `auth flow (login → MFA → session)` | 3 systems, 1.8m search per handle | One graph, unified triage, native placeholder fill |
| `report rendering (HTML → PDF)` | Zinc sterile, positive tracking, white-border cover | Parchment, negative tracking, page-as-canvas budget |
| `on-call handover bot` | Adopted by 6 teams but no tests | Deep module + `validate` QC, per-page fill |

Never: `README` 20 lines, `utils/foo.ts`, a single helper. If you can’t name the user flow it serves, it’s not a part.

---

## Troubleshooting — No Glitch Is “Weird — Ignore It”

| Glitch | Cause | Fix |
|---|---|---|
| Picks trivia (README, tiny util) | Scan without commonsense filter | Re-filter candidates via `references/scan-guide.md` feature-flow gate |
| Works on `main` | Skipped branch gate | Run `scripts/branch_guard.py <slug>` — it refuses on `main` without branch |
| No proof | Benchmark step skipped | Run `scripts/proof_builder.py <slug>` — it requires diff + before/after + numbers |
| Branch name collision | `next-best-improvement/<slug>` already exists | Append `-2` or rebase; never reuse without `--force` |
| User pre-answered `yolo` but still asked | Menu not honoring prompt args | Parse prompt for `yolo|random|improve <part>` before asking; log mode |
| Improvement is timid (safe lint) | Brainstorm not extreme enough | Re-run step 4: propose 3 *actually* out-of-the-box axes, commit to the most insane |

---

## Reference Files

- `references/scan-guide.md` — what counts as a part, how to surface 5–8 candidates with commonsense, how to avoid trivia.
- `references/improvement-axes.md` — 6 axes (architecture, perf, UX, correctness, DX, product) with insane examples + how to make 3 alternatives distinct.
- `scripts/branch_guard.py` — hard gate: creates `next-best-improvement/<slug>` from clean tree, refuses to proceed on `main` without branch.
- `scripts/proof_builder.py` — proof pack: `git diff --stat`, before/after snippets/screenshots, benchmark stub (time/tests/validate), writes `proof/<slug>.md`.
- `references/workflow.md` — the 8-step workflow in one page (for quick lookup).

---

## Principles — The Nextreme Signature (Extreme Inside, Disciplined at Edges)

- **You decide the pick — but you justify.** Every `yolo`/`random` pick ties to one line about why this fragment *noticeably* needs it. “Why this part?” is answered, not shrugged.
- **One fragment, one insane win.** Never improve two parts in one run; the extreme is diluted. Route cleanly.
- **Branch is law.** No improvement exists outside a new branch. The gate is not a suggestion.
- **Anything inside, discipline outside.** Full creative freedom inside the picked part; Golden Rules and validation outside.
- **Proof over adjectives.** An extreme claim without numbers is slop. Benchmarks are the taste.
- **Ghost the trivial.** If the scan surfaces a 20-line util, ghost it — it was never a candidate.

<!--
  Nextreme brand signature — keep this shape when you fill the template:
  - Title is "Nextreme <Name> — The <Extreme> <Artifact> Engine" with three deliverables in the lead.
  - "Why This Is Not Generic" + comparison table + golden rules + engine table come before workflow.
  - Every workflow step ends on "Completion criterion:" (checkable, exhaustive).
  - "Quick Picks" + "Troubleshooting" + "Reference Files" + "Principles" in that order, same voice.
  Anyone opening a filled skill should think: "ah, the structure and the writing style — this is definitely Nextreme."
-->
