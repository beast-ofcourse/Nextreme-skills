# Validation — Strict Checklist

`scripts/verify_tdd.py --strict` automates these. If execution unavailable, check manually — every box must be ticked.

## 1. Honest RED (Behavior Gap, Not Typo)

RED is honest when the failure is **missing symbol** or **wrong value** for the pinned behavior:

- Honest: `NameError: name 'calculate_tax' is not defined`, `FAIL: got 10.01 want 10.02`, `expected 42 received 10`
- Honest (TypeScript/vitest, static import): `Cannot find module './<name>' ... Does the file exist?` (missing module), `does not provide an export named '<symbol>'` (missing export) — both are collection errors naming the behavior gap
- Dishonest (fix wiring, not counting as RED): `SyntaxError`, `ImportError` from wrong path, `ReferenceError: caluclate_tax` (typo in test), `ModuleNotFoundError` from bad relative import

Check: run the RED test alone and read the diff — is it about the behavior value? If not, fix the test and re-run.

## 2. No Production Diff Before RED (Manual Ordering Check)

The `verify_tdd.py` ordering check is **heuristic, not timestamp-proven**: it inspects `git diff --stat` for production files (`src/*.py`, `lib/*.ts`, `*.go`, `src/*.rs`) in the working tree and warns when a prod diff exists before a RED log is supplied. It does **not** prove temporal RED-before-GREEN from log timestamps.

- **Automated:** `verify_tdd.py` warns `prod diff present before RED proof` when a production file appears in `git diff --stat` without `--red-log`/`--green-log` proof artifacts. In `--strict` the warning becomes a failure only when the diff is unambiguous; otherwise it is a manual-review gate.
- **Timestamp-proven (optional):** supply `--red-log <red.log>` and `--green-log <green.log>` plus `--proof proof/<behavior>.json` (containing `{red_timestamp, green_timestamp, behavior}`) to claim timestamp ordering. Capture the green log verbose (`-v` / `--reporter=verbose`) so the behavior name appears in it — terse `-q` green logs name no tests and fail the proof check. The verifier validates `red_timestamp < green_timestamp` and that both logs contain the pinned behavior name. Without that artifact, do **not** claim automated timestamp ordering — treat ordering as a **manual check**.
- **Manual:** `git diff --stat` should show only `tests/*` / `*.test.*` / `*_test.go` before RED. If it shows `src/` before RED, reset prod and re-do, then re-run verification with the proof artifact.

## 3. GREEN Is Full Suite Green

- Run the **full** suite command per `framework-matrix.md`, not just the new file.
- Exit code 0 **and** summary shows `passed` with no failures/skipped-count surprise.
- For production code, check manually (`grep -R ":\s*any" src/` and `grep -R "\bas\b" src/`) — the automated verifier scans **test files only** for `any`/`Any` and silent `as`; production `any`/`as` remains a manual gate (see §6).

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

## 8. Test Frozen After RED (No Reward Hacking)

Once RED is approved, the test file is frozen — GREEN fixes go in the implementation only. The agent never makes red turn green by weakening the test: no deleted assertions, no added `.skip`/commented cases, no loosened matcher (`toEqual` → `toBeDefined`), no edited expected value. If the test itself was wrong, the human amends it explicitly — never the agent mid-task.

- Check: `git diff` on test files from RED → GREEN shows only additions needed for honesty (imports, wiring) — never weakened assertions.
- Skipped-count surprise in the GREEN log (`3 skipped` where RED had `0 skipped`) fails this check.

## Manual Fallback (No Execution)

If you cannot run `verify_tdd.py`:

1. Paste RED log — highlight the behavior-gap line.
2. `git diff --stat` before vs after RED.
3. Paste GREEN log — full suite, exit 0.
4. List each assertion and name the behavior value it checks.
5. Confirm one behavior name per test file/describe.

All five present → manual pass.
