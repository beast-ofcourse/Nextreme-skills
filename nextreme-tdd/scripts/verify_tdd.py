#!/usr/bin/env python3
"""Verify TDD order and quality: RED-proven, no-prod-before-RED, suite green, no slop.

Checks what eyes miss: order, not just color.
Exit 0 on strict pass; non-zero on the first hard failure (errors printed to stderr).

Why this exists: order is the contract. A green suite that never saw RED proves nothing.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

TRUTHINESS_PATTERNS: list[tuple[str, str]] = [
    (r"toBeTruthy\(\)", "Vitest/Jest truthiness — assert the value, not existence"),
    (r"toBeDefined\(\)", "toBeDefined without value — assert the behavior value"),
    (r"toBeFalsy\(\)", "toBeFalsy without value — assert the negated value"),
]

BARE_ASSERT_PATTERN = re.compile(r"^\s*assert\s+[a-zA-Z_][a-zA-Z0-9_]*\s*$", re.MULTILINE)

PROD_FILE_PATTERNS = [".py", ".ts", ".tsx", ".js", ".go", ".rs"]
TEST_FILE_HINTS = ["test_", ".test.", "_test.go", "__tests__", "tests/"]

def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for TDD verification."""
    parser = argparse.ArgumentParser(description="Verify TDD cycle")
    parser.add_argument("--strict", action="store_true", help="fail on any warning")
    parser.add_argument("--phase", choices=["red", "green", "refactor"], help="only check that phase")
    parser.add_argument("--since", default=None, help="git sha to diff since (proves no prod before RED)")
    parser.add_argument("--framework", choices=["pytest", "vitest", "jest", "go", "cargo"], help="override detected framework")
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="repo root")
    parser.add_argument("--red-log", type=Path, default=None, help="path to pasted RED log for offline check")
    parser.add_argument("--green-log", type=Path, default=None, help="path to pasted GREEN log for offline check")
    parser.add_argument("--proof", type=Path, default=None, help="path to ordered proof JSON {red_timestamp, green_timestamp, behavior} for timestamp ordering")
    return parser.parse_args()

def run_command(cwd: Path, command: list[str]) -> tuple[int, str, str]:
    """Run a command in a directory and return exit code, stdout, stderr.

    Missing executables (e.g. `npx` shim invisible to CreateProcess on Windows)
    return 127 with the error as output — never raise. A verifier that tracebacks
    instead of reporting is a broken gate.
    """
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    except OSError as exc:
        if sys.platform == "win32" and isinstance(exc, FileNotFoundError):
            # .cmd shims (npx, jest) are invisible to CreateProcess — retry via shell.
            try:
                result = subprocess.run(["cmd", "/c"] + command, cwd=cwd, capture_output=True, text=True)
                return result.returncode, result.stdout, result.stderr
            except OSError as exc2:
                return 127, "", f"command not runnable {command[0]!r}: {exc2}"
        return 127, "", f"command not runnable {command[0]!r}: {exc}"
    return result.returncode, result.stdout, result.stderr

def git_diff_stat(cwd: Path, since: str | None) -> str:
    """Get git diff stat for staged and unstaged changes."""
    base = f"{since}..HEAD" if since else "HEAD"
    # --stat for staged+unstaged vs HEAD
    code, out, _ = run_command(cwd, ["git", "diff", "--stat", base])
    if code != 0:
        code2, out2, _ = run_command(cwd, ["git", "diff", "--stat"])
        out = out2 if code2 == 0 else ""
    code3, unstaged, _ = run_command(cwd, ["git", "diff", "--stat"])
    code4, staged, _ = run_command(cwd, ["git", "diff", "--cached", "--stat"])
    combined = (unstaged + "\n" + staged).strip()
    return combined or out

def is_test_file(path: str) -> bool:
    """Check if a path looks like a test file."""
    lower = path.lower()
    return any(hint in lower for hint in TEST_FILE_HINTS)

def read_log_text(log_path: Path) -> str:
    """Read a captured log tolerantly: PowerShell `>` writes UTF-16LE, consoles write UTF-8."""
    raw = log_path.read_bytes()
    for encoding in ("utf-8-sig", "utf-16", "utf-8"):
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, ValueError):
            continue
    return raw.decode("utf-8", errors="ignore")

def is_prod_file(path: str) -> bool:
    """Check if a path looks like a production file (not a test file)."""
    lower = path.lower()
    if is_test_file(lower):
        return False
    return any(lower.endswith(ext) for ext in PROD_FILE_PATTERNS)

def check_no_prod_before_red(diff_stat: str) -> list[str]:
    """Heuristically check for production diff before RED proof."""
    errors: list[str] = []
    if not diff_stat.strip():
        return errors
    prod_lines = [line for line in diff_stat.splitlines() if line.strip() and not is_test_file(line)]
    # Heuristic: if diff mentions src/, lib/, app/, pkg/, internal/ before RED, flag
    for line in prod_lines:
        if any(token in line for token in [" src/", " lib/", " app/", " pkg/", " internal/", ".py |", ".ts |", ".go |", ".rs |"]):
            # This is the working tree diff; strict mode treats any prod diff as "order not proven"
            # We emit a warning, not an error, unless --since proves it.
            errors.append(f"prod diff present before RED proof: {line.strip()} — run RED before touching prod")
            break
    return errors

def bare_assert_lines_py(content: str) -> list[int]:
    """Line numbers of Python asserts with no comparison inside (Name, Call, BinOp...).

    `assert result == 42` walks a Compare node and passes. `assert result`,
    `assert compute()`, `assert 1 + 1` contain no Compare and prove nothing — flag them.
    Unparseable files return [] (syntax is the suite's job, not this check's).
    """
    import ast as ast_lib
    try:
        tree = ast_lib.parse(content)
    except SyntaxError:
        return []
    flagged: list[int] = []
    for node in ast_lib.walk(tree):
        if isinstance(node, ast_lib.Assert):
            if not any(isinstance(child, ast_lib.Compare) for child in ast_lib.walk(node.test)):
                flagged.append(getattr(node, "lineno", 0))
    return flagged

def check_truthiness(test_files: list[Path]) -> list[str]:
    """Check test files for truthiness-only assertions and any usage."""
    errors: list[str] = []
    for test_file in test_files:
        if not test_file.exists() or not test_file.is_file():
            continue
        try:
            content = test_file.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"could not read {test_file}: {exc}")
            continue
        for pattern, message in TRUTHINESS_PATTERNS:
            if re.search(pattern, content):
                errors.append(f"{test_file}: truthiness pattern `{pattern}` — {message}")
        if test_file.suffix == ".py":
            for lineno in bare_assert_lines_py(content):
                errors.append(f"{test_file}:{lineno}: bare `assert` without comparison — assert the value")
        elif BARE_ASSERT_PATTERN.search(content):
            errors.append(f"{test_file}: bare `assert <name>` without comparison — assert the value")
        if re.search(r"\bany\b", content.lower()) and "verify:tdd allow-any" not in content:
            # Heuristic: `any` in TS/Python tests is often slop; allow escape hatch
            if re.search(r":\s*any\b", content) or re.search(r"\bAny\b", content):
                errors.append(f"{test_file}: `any`/`Any` in test — narrow to the real type")
    return errors

def check_one_behavior_per_file(test_files: list[Path]) -> list[str]:
    """Check that each test file covers only one behavior."""
    errors: list[str] = []
    for test_file in test_files:
        if not test_file.exists():
            continue
        try:
            content = test_file.read_text(encoding="utf-8")
        except OSError:
            continue
        if "verify:tdd allow-batch" in content:
            continue
        describe_count = len(re.findall(r"\bdescribe\s*\(", content))
        test_def_count = len(re.findall(r"\bdef\s+test_", content))
        go_test_count = len(re.findall(r"\bfunc\s+Test[A-Z]", content))
        rust_test_count = len(re.findall(r"#\[test\]", content))
        total_roots = describe_count + test_def_count + go_test_count + rust_test_count
        # A single behavior file with a Go table-driven inside one Test is fine (1 root).
        # Two distinct describes/test funcs for different behaviors is the batch we forbid.
        # Heuristic: flag files with ≥3 distinct roots (allow 2 for edge+happy grouping with justification)
        if total_roots >= 3:
            errors.append(
                f"{test_file}: {total_roots} top-level test roots — one behavior per file/describe. "
                f"Split behaviors or add `# verify:tdd allow-batch` with justification."
            )
    return errors

def is_excluded(test_path: Path, repo_root: Path) -> bool:
    """Check if a test path should be excluded (templates, caches)."""
    try:
        relative = test_path.relative_to(repo_root)
    except ValueError:
        return True
    parts = relative.parts
    excluded_dirs = {"templates", ".git", ".hg", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
    return any(part in excluded_dirs for part in parts)

def check_ordered_proof(proof_path: Path | None, red_log: Path | None, green_log: Path | None) -> list[str]:
    """Validate timestamp ordering from proof artifact, not git diff stat."""
    errors: list[str] = []
    if proof_path is None:
        return errors
    if not proof_path.exists():
        errors.append(f"--proof not found: {proof_path}")
        return errors
    try:
        import json as json_lib
        payload = json_lib.loads(proof_path.read_bytes().decode("utf-8-sig"))
    except Exception as exc:
        errors.append(f"invalid proof JSON {proof_path}: {exc}")
        return errors
    red_ts = payload.get("red_timestamp")
    green_ts = payload.get("green_timestamp")
    behavior = payload.get("behavior")
    if not red_ts or not green_ts:
        errors.append(f"proof {proof_path} missing red_timestamp/green_timestamp")
        return errors
    if red_ts >= green_ts:
        errors.append(f"proof ordering failed: red_timestamp {red_ts} >= green_timestamp {green_ts}")
    if behavior and red_log and red_log.exists():
        red_content = read_log_text(red_log)
        if behavior not in red_content and behavior.lower() not in red_content.lower():
            errors.append(f"proof behavior '{behavior}' not found in RED log")
    if behavior and green_log and green_log.exists():
        green_content = read_log_text(green_log)
        if behavior not in green_content and behavior.lower() not in green_content.lower():
            errors.append(
                f"proof behavior '{behavior}' not found in GREEN log "
                "(capture the green log verbose, e.g. python -m pytest -v, so test names appear)"
            )
    return errors

def collect_test_files(cwd: Path) -> list[Path]:
    """Collect test files while excluding templates and non-test Rust sources."""
    patterns = [
        "tests/test_*.py",
        "tests/*.test.ts",
        "tests/*.test.js",
        "src/*.test.ts",
        "src/*.test.js",
        "*_test.go",
        "tests/test_*.rs",
        "src/*.rs",
    ]
    files: list[Path] = []
    for pat in patterns:
        # Use rglob for simple patterns to catch nested, glob for explicit dirs
        if pat in ("tests/test_*.py", "tests/*.test.ts", "tests/*.test.js", "src/*.test.ts", "src/*.test.js", "tests/test_*.rs"):
            files.extend(cwd.glob(pat))
            # Also rglob to catch nested monorepo layouts (e.g., packages/*/src/*.rs)
            files.extend(cwd.rglob(pat.replace("tests/", "").replace("src/", "")) if "tests/" in pat or "src/" in pat else [])
        elif pat == "*_test.go":
            files.extend(cwd.rglob(pat))
        elif pat == "src/*.rs":
            # Include all Rust source; inline #[cfg(test)] will be detected via heuristics later
            files.extend(cwd.glob(pat))
            files.extend(cwd.rglob("src/*.rs"))
        else:
            files.extend(cwd.rglob(pat) if "/" not in pat else cwd.glob(pat))
    # Also brute-force the common exact paths
    for found in cwd.rglob("test_*.py"):
        if found not in files:
            files.append(found)
    for found in cwd.rglob("*.test.ts"):
        if found not in files:
            files.append(found)
    for found in cwd.rglob("*_test.go"):
        if found not in files:
            files.append(found)
    # Deduplicate and keep only files under cwd
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in files:
        resolved = path.resolve()
        if resolved not in seen and resolved.is_file():
            seen.add(resolved)
            if not is_excluded(resolved, cwd.resolve()):
                # For Rust inline tests, only keep src/*.rs files that actually contain a test marker
                if resolved.suffix == ".rs" and "src" in resolved.parts:
                    try:
                        txt = resolved.read_text(encoding="utf-8", errors="ignore")
                        if "#[test]" not in txt and "#[cfg(test)]" not in txt:
                            # No inline test marker — not a test file, skip for batch/truthiness checks
                            # but keep for suite trigger? We'll keep a marker file to trigger cargo test anyway
                            # Instead, mark as non-test for filtering but ensure cargo still runs if any Rust file exists
                            continue
                    except OSError:
                        continue
                unique.append(resolved)
    # If no test files but Rust sources exist, ensure cargo test still considered: keep one sentinel
    if not unique:
        # Check if any Rust source with inline test exists elsewhere via rglob that we filtered out
        rust_with_test = [p for p in cwd.rglob("src/*.rs") if p.is_file() and not is_excluded(p.resolve(), cwd.resolve())]
        for candidate in rust_with_test:
            try:
                if "#[test]" in candidate.read_text(encoding="utf-8", errors="ignore") or "#[cfg(test)]" in candidate.read_text(encoding="utf-8", errors="ignore"):
                    unique.append(candidate.resolve())
                    break
            except OSError:
                continue
    # Filter to only recent/modified + existent; if none, return empty (no batch error)
    return sorted(unique)

def verify_suite_green(cwd: Path, framework: str | None, test_files: list[Path]) -> list[str]:
    """Verify the full test suite is green for the detected framework."""
    # Skip suite check when no test files exist — nothing to stay green
    if not test_files:
        return []
    commands: dict[str, list[str]] = {
        # python -m keeps cwd on sys.path (bare pytest does not) — src-layout safe.
        "pytest": [sys.executable, "-m", "pytest", "-q"],
        "vitest": ["npx", "vitest", "run", "--reporter=verbose"],
        "jest": ["npx", "jest", "--no-coverage"],
        "go": ["go", "test", "./..."],
        "cargo": ["cargo", "test"],
    }
    if framework is not None and framework in commands:
        code, out, err = run_command(cwd, commands[framework])
        combined = (out + err).lower()
        if "no tests" in combined or "no test" in combined:
            # No tests collected — not a suite failure, just empty (warned elsewhere if needed)
            return []
        if code != 0:
            return [f"suite not green for {framework}: {combined[:800]}"]
        return []
    return []

def main() -> None:
    """Main entry point for TDD verification."""
    args = parse_args()
    cwd: Path = args.cwd.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not cwd.exists() or not cwd.is_dir():
        print(f"error: --cwd not a directory: {cwd}", file=sys.stderr)
        sys.exit(2)

    # Resolve framework for green check
    framework = args.framework
    if framework is None:
        detector = Path(__file__).resolve().parent / "detect_framework.py"
        code, out, err = run_command(cwd, [sys.executable, str(detector), "--cwd", str(cwd), "--json"])
        if code == 0:
            try:
                import json as json_lib
                payload = json_lib.loads(out)
                framework = payload.get("framework")
            except Exception:
                framework = None

    # Collect test files
    test_files = collect_test_files(cwd)

    # Phase: red → check order + honest RED guidance (offline if logs provided)
    if args.phase in (None, "red"):
        # Timestamp ordering is only proven via --proof artifact; diff stat is heuristic + manual
        if args.proof is not None:
            proof_errors = check_ordered_proof(args.proof, args.red_log, args.green_log)
            if proof_errors:
                errors.extend(proof_errors)
            else:
                # Proof validated — still run diff heuristic as informational warning
                diff_stat = git_diff_stat(cwd, args.since)
                order_warnings = check_no_prod_before_red(diff_stat)
                warnings.extend(order_warnings)
        else:
            diff_stat = git_diff_stat(cwd, args.since)
            order_warnings = check_no_prod_before_red(diff_stat)
            warnings.extend(order_warnings)
            # Only require timestamp proof when a TDD cycle is actually being validated (logs or test files present)
            has_cycle_evidence = bool(args.red_log or args.green_log or test_files)
            if has_cycle_evidence and args.strict and not args.red_log and not args.green_log:
                warnings.append("ordering not timestamp-proven: supply --proof {red_timestamp, green_timestamp, behavior} + --red-log/--green-log for strict RED-before-GREEN proof; current check is heuristic diff stat (manual review required)")
            elif has_cycle_evidence and args.strict and (args.red_log or args.green_log) and not args.proof:
                warnings.append("ordering heuristic only: supply --proof for timestamp ordering; without it, RED-before-GREEN is a manual check, not automated verification")
        if args.red_log is not None:
            if not args.red_log.exists():
                errors.append(f"--red-log not found: {args.red_log}")
            else:
                red_content = read_log_text(args.red_log)
                if "syntaxerror" in red_content.lower() and "assert" not in red_content.lower():
                    warnings.append("RED log looks like a SyntaxError typo, not a behavior gap — fix wiring and re-run RED")
                if "modulenotfounderror" in red_content.lower() or "cannot find module" in red_content.lower():
                    warnings.append(
                        "RED log is a missing-module import error — if the missing module is the seam "
                        "target's own package (from-scratch cycle; the template normalizes it), confirm the "
                        "failure line is the behavior gap, otherwise fix the import path before counting as RED"
                    )

    # Phase: green + refactor → truthiness, batch, suite green
    if args.phase in (None, "green", "refactor"):
        truthiness_errors = check_truthiness(test_files)
        errors.extend(truthiness_errors)
        batch_errors = check_one_behavior_per_file(test_files)
        # Batch is a warning in non-strict, error in strict
        if args.strict:
            errors.extend(batch_errors)
        else:
            warnings.extend(batch_errors)

        green_errors = verify_suite_green(cwd, framework, test_files)
        # Suite green failures are errors in strict, warnings otherwise
        if green_errors:
            if args.strict:
                errors.extend(green_errors)
            else:
                warnings.extend(green_errors)

    if warnings:
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) — fix and rerun verify_tdd.py --strict", file=sys.stderr)
        sys.exit(1)

    if warnings and args.strict:
        print(f"\n{len(warnings)} warning(s) in --strict — treat as errors", file=sys.stderr)
        sys.exit(1)

    print(f"verify_tdd: OK (framework={framework or 'unknown'} test_files={len(test_files)} strict={args.strict})")
    if test_files:
        for test_file in test_files[:5]:
            print(f"  - {test_file.relative_to(cwd) if test_file.is_relative_to(cwd) else test_file}")

if __name__ == "__main__":
    main()
