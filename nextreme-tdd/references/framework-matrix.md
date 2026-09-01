# Framework Matrix — Manifest → Framework

Decision law: **you do, per repo, from evidence.** Don't ask the user which framework — detect it, state the justification, and lock it for the whole cycle.

## Detection Order (first match wins)

| Priority | Signal | Framework | Test Dir / File | RED / GREEN Command |
|---|---|---|---|---|
| 1 | `pyproject.toml` / `setup.cfg` + `pytest.ini` / `tests/` | **pytest** | `tests/test_<behavior>.py` | `pytest tests/test_<behavior>.py -q` (RED) → `pytest -q` (GREEN full suite) |
| 2 | `package.json` with `vitest` in `devDeps` | **Vitest** | `src/<name>.test.ts` or `tests/<name>.test.ts` | `npx vitest run <file> --reporter=verbose` → `npx vitest run --reporter=verbose` |
| 3 | `package.json` with `jest` in `devDeps` | **Jest** | `__tests__/<name>.test.ts` or `src/<name>.test.ts` | `npx jest <file> --no-coverage` → `npx jest --no-coverage` |
| 4 | `go.mod` + `*_test.go` | **go test** | `<pkg>/*_test.go` | `go test -run Test<Behavior> ./...` → `go test ./...` |
| 5 | `Cargo.toml` | **cargo test** | `src/<name>.rs` `#[cfg(test)]` or `tests/*.rs` | `cargo test <behavior> -- --nocapture` → `cargo test` |
| 6 | No manifest, `*.py` files dominate | **pytest** (default) | `tests/test_<behavior>.py` | `pytest -q` |
| 7 | No manifest, `*.ts`/`*.js` dominate | **Vitest** (default) | `src/<name>.test.ts` | `npx vitest run --reporter=verbose` |

Run `scripts/detect_framework.py --json` to get the machine answer:

```json
{ "framework": "pytest", "manifest": "pyproject.toml", "test_dir": "tests", "command": "pytest -q", "file_template": "python-pytest.test.py" }
```

## Override

If detection is ambiguous (e.g., both `pytest.ini` and `package.json` present):

```bash
python scripts/detect_framework.py --framework vitest --json
# or
python scripts/detect_framework.py --manifest ./backend/pyproject.toml --json
```

State the assumption in the cycle note: "repo has both Python and TS — pinning this behavior to `pytest` per `backend/` manifest."

## Install

```bash
# pytest
pip install "pytest>=8.0"

# Vitest / Jest (Node 18+)
npm install -D vitest  # or jest

# Go — no install, `go test` is built-in (Go 1.21+)

# Rust — no install, `cargo test` is built-in (Rust 1.70+)

# Optional — property-based (invariant buckets)
pip install "hypothesis>=6.0"
npm install -D fast-check
```

## Scaffold Destinations

`scripts/scaffold_test.py` resolves the destination per framework:

- `pytest` → `tests/test_<snake_behavior>.py` (created if `tests/` missing; adds `__init__.py` if package)
- `vitest`/`jest` → `src/<kebab-behavior>.test.ts` (falls back to `tests/` if `src/` absent; mirrors source structure)
- `go test` → `<package>/<snake>_test.go` (same package as target file if known, else `./<behavior>_test.go`)
- `cargo test` → `tests/test_<snake>.rs` (external integration test; for inline `#[cfg(test)]` add the module manually — scaffold always writes the external form)

Pass `--dry-run` to preview the path without writing. The previously documented `--integration` flag is not implemented; the scaffold always uses the external `tests/` destination.

## RED vs GREEN Commands (copy-paste)

Keep RED scoped to the new test (proves it fails alone); keep GREEN as full suite (proves no regression):

| Framework | RED (scoped) | GREEN (full suite) |
|---|---|---|
| pytest | `pytest tests/test_<behavior>.py -q -v` | `pytest -q` |
| Vitest | `npx vitest run src/<x>.test.ts --reporter=verbose` | `npx vitest run --reporter=verbose` |
| Jest | `npx jest src/<x>.test.ts --no-coverage` | `npx jest --no-coverage` |
| go test | `go test -run Test<Behavior> -count=1 ./...` | `go test ./...` |
| cargo test | `cargo test <behavior> -- --nocapture` | `cargo test` |

Paste both logs into the cycle proof. A RED that is actually a typo (`SyntaxError`, `ReferenceError` from misspelling) is not honest — fix wiring and re-run per `references/validation.md`.

## Monorepo Note

If the repo is a monorepo (`/frontend`, `/backend`, `/crates`), detection runs from the **behavior's owning directory**, not the repo root. `detect_framework.py` takes `--cwd <path>` so the pins stay local: backend Python vs frontend TS don't conflict.
