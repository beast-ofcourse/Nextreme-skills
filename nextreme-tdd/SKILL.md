---
name: nextreme-tdd
description: >
  Coach and enforce test-driven development as an extreme red-green-refactor loop — pin one behavior,
  write the smallest failing test, watch it fail for the right reason, make it pass with the smallest
  change, then refactor under green. Uses framework auto-detection (pytest, Vitest/Jest, Go test, Cargo test)
  with scaffold and verify harnesses. This is THE extreme skill for ANY TDD, test-first, red-green-refactor,
  failing-test-first, or characterization-test task — distinct from after-the-fact testing, coverage theater,
  or debugging an already-red suite. Trigger whenever the user says TDD, test-driven, red green refactor,
  write test before code, failing test first, characterization test, do this test-first, or starts coding a
  feature with no test in sight — even vague "make it testable" or "add tests for this behavior" without
  naming TDD. Also trigger for "pin the behavior" or "red green refactor".
  Do NOT trigger for debugging an already-failing suite, pure refactors with green cover, or CI/lint-only tasks.
license: MIT
compatibility: python>=3.9
---

# Nextreme TDD — The Extreme Red-Green-Refactor Engine

This skill produces **behavior-pinned, red-proven, refactor-safe TDD cycles** that survive review:
opened in `pytest`, `Vitest`/`Jest`, `go test`, or `cargo test` without out-of-order code, bloated fixtures, or green-theater tests.
Every cycle is a valid **behavior → RED → GREEN → REFACTOR** with disciplined naming, measured minimalism, and machine-checked order.
You get three deliverables: the **failing test (RED proof)**, the **minimal implementation (GREEN)**, and the **validation proof** (`verify_tdd.py` log).

You are **extreme and unbound inside the behavior** — the user does not pick the test shape — **you do**, per behavior from content.
A pure function gets a table-driven example; a stateful handler gets a characterization + invariant; an API boundary gets a contract + edge palette.
If they hand you production code first, you don't lecture — you scaffold its characterization test. If they give you one sentence, you pin the behavior from scratch
before a line of production code exists.

---

## Why This Is Not Generic

Most TDD coaching is bounded: one paragraph, one example, no harness — so every run drifts into test-after, vague assertions, and fixtures that hide the behavior.
Generic "write a test" prompts are order-blind: they generate code before proving RED, they assert `any` truthiness, they batch five behaviors in one test, and they never re-run.

This fuses the very core of the 4 best TDD systems on GitHub (2026) and refuses their bounds.

| Generic | This skill |
|---|---|
| Prose checklist you can ignore; code before test still lands | **Order-enforced loop** — `verify_tdd.py` fails the run if production code appears before RED proof; scaffold → run → show failure reason before GREEN |
| One example per behavior, no edge palette | **Behavior → examples + invariants + edges** per `references/test-patterns.md` (happy, edge, error, invariant — pick what the behavior earns) |
| One framework, one template, one shot | **Framework-auto-detected** (pytest/Vitest/Jest/go test/cargo test per `references/framework-matrix.md`) + scaffold templates + render-verify loop (2–3 iterations: test → run → fix) |
| "It passes" is green | **Green means suite green** — full suite re-run, no `any`, no silent `as`, assertion checks the behavior, not truthiness |

> If the behavior wants a better test shape that no reference names (e.g., property-based shrink inside a unit), invent it — but keep it behavior-pinned, RED-proven, and `verify_tdd.py` clean.

---

## Golden Code Quality Rules — ENFORCED

These are non-negotiable. Every test and every script this skill ships must pass them. Violation = task fails.

Keep code human-readable, small, and obvious. No AI slop.

* **Names tell the truth** — variables/functions reveal intent. No `data`, `info`, `result`, `handler`, `manager`, `helper`, `utils`, `foo`. A function that asserts tax rounding is `assert_tax_rounds_half_up`, not `check_result`.
* **One job per unit** — if you need "and" to describe what a function does, split it. A test that asserts parsing *and* persistence is two tests. Files own one domain.
* **Guard clauses over nesting** — early returns, fail fast. No pyramids, no `else` after `return`. Nesting past 2–3 levels is a signal to restructure.
* **No duplication** — never copy-paste. Third occurrence of the same assertion helper = must abstract. Two is coincidence, not a pattern.
* **No dead weight** — zero dead code, commented-out code, `console.log`, unused imports/vars. Delete, don't comment out.
* **Types are contracts** — no `any`, no silent `as` casts, narrow `unknown` explicitly. At an untyped boundary (`JSON.parse`, third-party API), a cast is allowed only alongside visible runtime validation.
* **Errors never silent** — every failure path is handled, returned, or logged with context. Never an empty catch, never a swallowed promise. A failed `detect_framework` logs what it looked for and where.
* **No magic** — no unexplained numbers or strings. Name every constant. No cryptic one-liners. `MAX_ASSERTS_PER_TEST = 3` not `3`.
* **Explicit dependencies** — no hidden globals, no surprise side effects. Inputs in, outputs out. Pure where possible.
* **Readability > cleverness** — code reads like prose: linear flow, consistent style, self-documenting. Comments explain why, not what.
* **No premature abstraction** — no wrappers, layers, or helpers you don't need today. YAGNI. Abstract on the real second pattern.
* **Leave it cleaner, not bigger** — boy-scout only on touched code.
* **State assumptions, don't guess silently** — if the spec is ambiguous, say what you assumed and why, in a comment or PR note.

**Auto-rejected AI slop:** placeholder `TODO` without a ticket, generic scaffolding, empty `try/catch`, `lorem`-ish names, duplicated boilerplate, over-engineered factories/managers, unvalidated `as` casts at boundaries, silent assumptions about ambiguous specs, inconsistent style within one file, **and TDD-level slop:** a test that never failed, an assertion on truthiness (`expect(x).toBeTruthy()`), five behaviors in one test, a fixture that hides the behavior, `any` in the test, production code committed before RED log, a refactor without a green suite re-run.

---

## Framework Selection — You Decide

| Context | You Pick | Output | Why |
|---|---|---|---|
| **Python (default for `*.py`, `pyproject.toml`, `requirements.txt`)** | **`pytest`** — `tests/test_<behavior>.py` | `def test_<behavior>_<case>()` | Auto-discovery, fixtures, `assert` rewriting; `pytest -q` is the RED/GREEN prover |
| **TypeScript / JS (`package.json`, `vitest`/`jest`, `*.ts`)** | **`Vitest`** (fallback `Jest`) — `src/<name>.test.ts` | `it("should <behavior> when <case>")` | ESM-native, `vi` compat, `vitest run --reporter=verbose` proves RED reason |
| **Go (`go.mod`, `*.go`)** | **`go test`** — `*_test.go` | `func Test<Behavior>_<Case>(t *testing.T)` | Table-driven `t.Run`, `_test.go` convention, `go test -run` isolates RED |
| **Rust (`Cargo.toml`, `*.rs`)** | **`cargo test`** — `src/<name>.rs` `#[cfg(test)]` or `tests/` | `#[test] fn <behavior>_<case>()` | Built-in harness, `cargo test -- --nocapture` shows RED reason |
| **No manifest / new repo** | **Ask for 10s, default `pytest`** | Above | Don't stall; pick the lightest that fits the file extension, state assumption |

All ship: `scripts/detect_framework.py` + `scripts/scaffold_test.py` + `scripts/verify_tdd.py`. You choose per repo — state the one-line justification (e.g., "found `pyproject.toml` → pytest" or "found `package.json` with `vitest` → Vitest").

Reference: `references/framework-matrix.md` — manifest → framework map, install, and RED/GREEN commands.

---

## Core Workflow — Behavior-Pinned, Order-Enforced

Each step ends on a **completion criterion**. Do not proceed until it passes.

### 1. Triage — What Is This Behavior *For*?

Ask or infer: what user-visible behavior does this cycle lock down, who is the client, and what unit owns it (function, class, route handler)? Extract: behavior name (verb phrase), owning contract/file, and what's *not* in this cycle. If production code already exists, mark the order inverted — you will start with a characterization test, not a feature test.

Reference: `references/test-patterns.md` — behavior naming + scope.

Completion criterion: one sentence — "When `<client>` does `<action>`, `<unit>` shall `<outcome>`" — plus the target file/symbol; no production code written.

### 2. Detect — What Framework Owns This Repo?

Run the detector; don't guess.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/detect_framework.py --json
# local clone:
python nextreme-tdd/scripts/detect_framework.py --json
# → { "framework": "pytest", "manifest": "pyproject.toml", "test_dir": "tests", "command": "pytest -q" }
# flags: --manifest <path> (override), --framework pytest|vitest|jest|go|cargo (force)
```

It scans manifests (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`), lockfiles, and `tests/`/`src/` conventions. If ambiguous, it prints candidates and exits non-zero — you pick and pass `--framework`.

Reference: `references/framework-matrix.md` — detection rules + manual override.

Completion criterion: detector exits 0 with one framework + one GREEN command + one test path; or you logged the assumption ("no manifest, defaulting to pytest per `*.py`").

### 3. Pin — Name The One Behavior

Pin exactly one behavior for this cycle. Use the leading word **behavior** — every decision in this skill is "which behavior, what case of that behavior, what asserts that behavior." Write the behavior contract: inputs, outputs, invariants, and the edge palette this behavior earns (see reference).

- One behavior = one test file or one `describe`/`Test` block, not five.
- Name it truthfully: `calculate_tax_rounds_half_up`, not `test1`.
- If the repo already has the implementation, pin its *observable* behavior for a characterization test (input → output, no peeking at internals).

Reference: `references/test-patterns.md` — behavior contract template + edge palette (happy / edge / error / invariant).

Completion criterion: behavior contract written (inputs → outputs + invariants) and the file/symbol under test is named; the next step knows exactly what RED must prove.

### 4. RED — The Smallest Failing Test

Scaffold, then make it fail for the *right* reason.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/scaffold_test.py --behavior "<behavior>" --case "<first-case>"
# → writes tests/test_<behavior>.py (or .test.ts / _test.go) from templates/
```

Edit the scaffold to the smallest assertion that captures the behavior. Run it and **prove RED**:

```bash
pytest tests/test_<behavior>.py -q      # or vitest run --reporter=verbose / go test -run TestBehavior / cargo test
# expect: FAILED / unknown symbol / wrong result — not a typo
```

The failure must be the behavior gap (missing symbol or wrong value), not a syntax/import typo. Fix typos until the test *fails honestly*, then stop — don't "fix" it to green.

Reference: `references/validation.md` — what counts as honest RED.

Completion criterion: one test exists, it fails, you pasted the failure (unknown symbol or assertion diff), and `verify_tdd.py --phase red` would exit 0. No production code touched.

### 5. GREEN — The Smallest Passing Change

Write the minimal production code to turn that one test green. No extra branches, no speculative generalization — only what the failing assertion demands. Run the **full suite**, not just the new test.

```bash
pytest -q
# or vitest run --reporter=verbose
# or go test ./...
# or cargo test
```

Confirm: the new test passes and the suite is green. If the suite is red, fix — don't commit on red. If the fix feels clever, it's too big; shrink to the smallest that passes.

Completion criterion: the pinned test passes, the full suite is green (paste the GREEN log), and the diff is the smallest that achieves it. `verify_tdd.py --phase green` exits 0.

### 6. REFACTOR — Clean Under Green

Only now, with green protecting you, clean what this cycle touched: remove duplication you just introduced, name truths, drop dead weight, tighten types. After **every** tweak, re-run; stay green. Stop the moment the code is clean, not when it is clever. Do not add behavior in REFACTOR — if you see a new case, park it for the next behavior cycle.

Completion criterion: the suite stays green through every refactor tweak; duplication/dead weight from the cycle is gone; no new behavior added; `verify_tdd.py --phase refactor` exits 0 (green still, diff is net cleaner).

### 7. Verify — Prove The Order

Run the bundled verifier — it checks what eyes miss (order, not just color):

```bash
# skills.sh:
python ${CLAUDE_SKILL_DIR}/scripts/verify_tdd.py --strict
# local clone:
python nextreme-tdd/scripts/verify_tdd.py --strict
# flags:
# --phase red|green|refactor : check only that phase (CI-friendly)
# --since <sha>               : diff since sha (proves no prod before RED)
# --framework <name>          : override detection
```

It checks: RED log exists and is a behavior-gap failure (not typo), no production diff before RED timestamp, GREEN log is full-suite green, no `any`/truthiness-only assertions, assertions match the pinned behavior, and no batch-of-behaviors in one test (see `references/validation.md`).

Fix every error and rerun until clean. If code execution unavailable, use the manual checklist in `references/validation.md`.

Completion criterion: `verify_tdd.py --strict` exits 0 **and** you can show RED log + GREEN log + the behavior name in one glance.

### 8. Deliver — Behavior + Proof

Always:
1. **The RED test** — the smallest failing test that now passes (commit shows RED → GREEN).
2. **The minimal implementation** — the production diff that satisfied it.
3. **The proof** — RED log, GREEN log, `verify_tdd.py` output, and the one-line behavior sentence.

Do not deliver a refactor as a "feature." Do not batch three behaviors into one cycle — one behavior per cycle, tracer bullets, not cannonballs.

---

## Quick Picks — Starter Templates

Copy a template from `templates/` and fill; do not start from zero. Each is valid, runnable, and uses the framework's idioms — not filler.

| Need | Template | Why this one |
|---|---|---|
| Python unit | `python-pytest.test.py` → `tests/test_<behavior>.py` via `scaffold_test.py` | `pytest` + `assert` rewriting, `Test<Behavior>` class optional, no fixtures that hide the behavior |
| TypeScript / JS unit | `typescript-vitest.test.ts` → `src/<name>.test.ts` | `vitest` + `expect(...).toEqual(...)` (never `toBeTruthy`), `describe` per behavior |
| Go unit | `go.test.go` → `*_test.go` | Table-driven `t.Run` with named cases, no `any` (`interface{}`) in assertions |
| Rust unit | `rust.test.rs` → `tests/test_<behavior>.rs` or `#[cfg(test)]` | `cargo test` harness, `assert_eq!` on the behavior, not truthiness |

All templates are behavior-pinned (one behavior per file/`describe`), assertion-true (`__behavior__` placeholder fails honestly), and framework-correct. See `references/framework-matrix.md` for where each template lands.

---

## Troubleshooting — No Glitch Is "Weird — Ignore It"

| Glitch | Cause | Fix |
|---|---|---|
| `verify_tdd.py` fails `no RED proof` | Wrote code before test, or didn't run test | Go back to Step 4: scaffold → run → paste honest failure before touching prod |
| RED is `ModuleNotFoundError` / `Cannot find module` | Import typo, not behavior gap | Fix the import; the test must fail on *behavior* (unknown symbol or value diff), not wiring. See `references/validation.md` |
| RED is a typo (`SyntaxError`, `ReferenceError: foo is not defined` misspelling) | Typo in test, not behavior gap | Fix typo, re-run; honest RED is missing impl or wrong value |
| `verify_tdd.py` fails `truthiness assertion` | `toBeTruthy` / `assert x` without value | Assert the actual value: `assert result == 42` / `expect(result).toEqual(42)` |
| `verify_tdd.py` fails `batch behaviors` | Five cases in one test / one file covers three behaviors | Split: one behavior per test/case table; see `references/test-patterns.md` edge palette |
| `verify_tdd.py` fails `any in test` | `any` / `as` without validation in test | Narrow: use the real type; at boundaries add the parse + `verify_*` pattern |
| Test passes on first run (no RED) | Behavior already implemented or test is vacuous | Delete impl or tighten assertion — a test you never saw fail proves nothing |
| Suite green locally, red in CI | Missed framework (`vitest` vs `jest`, `pytest` vs `unittest`) | `detect_framework.py --json` again; lock with `--framework` and match CI command |
| Refactor broke green | Edited under red or changed behavior | Revert refactor tweak, re-run; refactor only under green, one tweak at a time |

---

## Reference Files

- `references/test-patterns.md` — behavior contract template, edge palette (happy / edge / error / invariant), example vs property guidance, naming truthfully.
- `references/framework-matrix.md` — manifest → framework map, install, scaffold destinations, and RED/GREEN commands.
- `references/validation.md` — strict checklist: honest RED, no prod before RED, suite green, no `any`/truthiness, one behavior per test, batch detection.
- `scripts/detect_framework.py` — repo → framework + test dir + command (manifest scan, `--json`, `--framework` override).
- `scripts/scaffold_test.py` — behavior + case → templated test file (framework-aware destination + `__behavior__` placeholder that fails honestly).
- `scripts/verify_tdd.py` — order + quality gate: RED proof, no-prod-before-RED, suite green, assertion fidelity, batch guard.
- `templates/` — 4 starters: `python-pytest.test.py`, `typescript-vitest.test.ts`, `go.test.go`, `rust.test.rs` (plus `README.md`).

---

## Principles — The Nextreme Signature (Unbound, but Not Unruly)

- **Behavior is the tracer bullet.** One behavior per cycle, one tracer at a time. "Which behavior?" is answered, not shrugged — and the next cycle answers it again.
- **RED before GREEN is law, not advice.** If production code lands before RED proof, the cycle is void — the verifier fails it, not a human. Order is the contract.
- **Smallest GREEN wins.** The pass that teaches the least teaches the most — the refactor under green cover is where taste lives, not in a clever premature abstraction.
- **No truthiness theater.** An assertion that would pass for the wrong value is a failed test. Assert the behavior's value, shape, and error — not its existence.
- **You decide the shape — but you justify.** Every framework/template/assertion choice ties to one line about the behavior. "Why this case?" is answered, not vibed.
- **No glitch is minor.** One unproven RED / one truthy assertion / one batch-of-five test is a credibility leak. Zero is the bar.

<!--
  Nextreme brand signature — keep this shape when you fill the template:
  - Title is "Nextreme <Name> — The <Extreme> Engine" with three deliverables in the lead.
  - "Why This Is Not Generic" + comparison table + golden rules + engine table come before workflow.
  - Every workflow step ends on "Completion criterion:" (checkable, exhaustive).
  - "Quick Picks" + "Troubleshooting" + "Reference Files" + "Principles" in that order, same voice.
  Anyone opening a filled skill should think: "ah, the structure and the writing style — this is definitely Nextreme."
-->
