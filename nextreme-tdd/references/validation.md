# Validation — Strict Checklist

`scripts/verify_tdd.py --strict` automates these. If execution unavailable, check manually — every box must be ticked.

## 1. Honest RED (Behavior Gap, Not Typo)

RED is honest when the failure is **missing symbol** or **wrong value** for the pinned behavior:

- Honest: `NameError: name 'calculate_tax' is not defined`, `FAIL: got 10.01 want 10.02`, `expected 42 received 10`
- Dishonest (fix wiring, not counting as RED): `SyntaxError`, `ImportError` from wrong path, `ReferenceError: caluclate_tax` (typo in test), `ModuleNotFoundError` from bad relative import

Check: run the RED test alone and read the diff — is it about the behavior value? If not, fix the test and re-run.

## 2. No Production Diff Before RED Timestamp

Production code must not appear before RED proof. The verifier checks `git diff --stat` between `HEAD` and staged/working and compares timestamps (or `--since <sha>`):

- Fail if: a production file (`src/*.py`, `lib/*.ts`, `*.go`, `src/*.rs`) was modified before the RED log's time.
- Pass: only test files changed before RED; production diff appears only between RED and GREEN.

In manual mode: `git diff --stat` should show only `tests/*` / `*.test.*` / `*_test.go` before RED. If it shows `src/` before RED, the order was violated — reset prod and re-do.

## 3. GREEN Is Full Suite Green

- Run the **full** suite command per `framework-matrix.md`, not just the new file.
- Exit code 0 **and** summary shows `passed` with no failures/skipped-count surprise.
- No `any` / silent `as` introduced in production diff (grep `any` in `src/` for TS/Python type `Any`).

## 4. No Truthiness Theater

Every assertion checks **value**, not existence:

| Bad (fails this check) | Good |
|---|---|
| `assert result` | `assert result == 42` |
| `expect(x).toBeTruthy()` | `expect(x).toEqual(42)` |
| `if got != nil` (Go, when int) | `if got != 42 { t.Fatalf(...) }` |
| `assert!(result.is_ok())` (when value matters) | `assert_eq!(result.unwrap(), 42)` |

The verifier scans test files for `toBeTruthy`, `toBeDefined`, `assert.*truthy`, bare `assert` without comparison (heuristic — fix false positives by being explicit).

## 5. One Behavior Per Test Unit

- One behavior per `describe` / `Test<Behavior>` / `class Test<Behavior>` / file's primary export. One cycle = one behavior's happy *or* one edge *or* one error *or* one invariant — not all four.
- A test file with three unrelated `describe("a")`, `describe("b")`, `describe("c")` is a batch — split.
- Go table-driven is allowed **within** one behavior (multiple rows for the same behavior's edge palette), but not across behaviors.

Verifier heuristic: counts top-level `describe`/`Test*`/`def test_*` distinct names sharing a file; flags files with >1 behavior-like root (allow override with `# verify:tdd allow-batch` comment and justification).

## 6. Types Are Contracts in Tests Too

- No `any` in the test file (TS `any`, Python `Any` without `TypeGuard`, Go `interface{}` used as escape, Rust `unsafe` to bypass).
- At untyped boundaries (`JSON.parse`, `yaml.safe_load`, API response), the test narrows `unknown` via a visible parse/validate function before asserting — `as` appears only beside that validation.

## 7. Refactor Kept Green and Behavior-Free

- Every refactor tweak re-runs green.
- Diff from GREEN → REFACTOR is net cleaner (less duplication, clearer names) and adds no new branches/cases.
- If a refactor felt like it needed a new test, that new test is the *next* behavior cycle — park it.

## Manual Fallback (No Execution)

If you cannot run `verify_tdd.py`:

1. Paste RED log — highlight the behavior-gap line.
2. `git diff --stat` before vs after RED.
3. Paste GREEN log — full suite, exit 0.
4. List each assertion and name the behavior value it checks.
5. Confirm one behavior name per test file/describe.

All five present → manual pass.
