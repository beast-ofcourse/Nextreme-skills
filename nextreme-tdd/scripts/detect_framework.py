#!/usr/bin/env python3
"""Detect the test framework that owns the repo.

Scans manifests and test conventions, then reports one framework + command + destination.
Exits non-zero when ambiguous so the caller can pass --framework explicitly.

Why this exists: TDD picks the *existing* harness; guessing wastes a cycle and produces a test the suite never runs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FRAMEWORKS: dict[str, dict[str, str]] = {
    "pytest": {
        "test_dir": "tests",
        "command": "pytest -q",
        "scoped": "pytest {file} -q -v",
        "template": "python-pytest.test.py",
    },
    "vitest": {
        "test_dir": "src",
        "command": "npx vitest run --reporter=verbose",
        "scoped": "npx vitest run {file} --reporter=verbose",
        "template": "typescript-vitest.test.ts",
    },
    "jest": {
        "test_dir": "src",
        "command": "npx jest --no-coverage",
        "scoped": "npx jest {file} --no-coverage",
        "template": "typescript-vitest.test.ts",
    },
    "go": {
        "test_dir": ".",
        "command": "go test ./...",
        "scoped": "go test -run {behavior} -count=1 ./...",
        "template": "go.test.go",
    },
    "cargo": {
        "test_dir": "tests",
        "command": "cargo test",
        "scoped": "cargo test {behavior} -- --nocapture",
        "template": "rust.test.rs",
    },
}

MANIFEST_SIGNALS: list[tuple[str, str]] = [
    ("pyproject.toml", "pytest"),
    ("setup.cfg", "pytest"),
    ("pytest.ini", "pytest"),
    ("uv.lock", "pytest"),
    ("poetry.lock", "pytest"),
    ("Cargo.toml", "cargo"),
    ("go.mod", "go"),
]

def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for framework detection."""
    parser = argparse.ArgumentParser(description="Detect test framework")
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="repo root to scan")
    parser.add_argument("--manifest", type=Path, default=None, help="force manifest path")
    parser.add_argument("--framework", choices=list(FRAMEWORKS), help="force framework")
    parser.add_argument("--json", action="store_true", help="emit JSON on stdout")
    return parser.parse_args()

def detect_from_manifest(cwd: Path, manifest_override: Path | None) -> str | None:
    """Detect framework from manifest files or file dominance."""
    if manifest_override is not None:
        if not manifest_override.exists():
            print(f"error: --manifest not found: {manifest_override}", file=sys.stderr)
            sys.exit(2)
        text = manifest_override.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        if "pytest" in lower or manifest_override.name in ("pyproject.toml", "setup.cfg", "pytest.ini"):
            return "pytest"
        if "vitest" in lower:
            return "vitest"
        if "jest" in lower:
            return "jest"
        if manifest_override.name == "Cargo.toml":
            return "cargo"
        if manifest_override.name == "go.mod":
            return "go"
        return None

    for manifest_name, framework in MANIFEST_SIGNALS:
        candidate = cwd / manifest_name
        if not candidate.exists():
            continue
        if framework == "pytest":
            # Only claim pytest when the manifest contains pytest-specific config/dependency;
            # otherwise preserve JS detection (e.g., package.json + Vitest) that follows.
            if manifest_name in ("pytest.ini",):
                return framework
            try:
                manifest_text = candidate.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            has_pytest_marker = (
                "pytest" in manifest_text
                or "[tool.pytest" in manifest_text
                or "pytest.ini" in manifest_text
            )
            if has_pytest_marker:
                return framework
            # No pytest marker — do not short-circuit; allow package.json/Vitest detection below
            continue
        # cargo / go are definitive
        return framework

    package_json = cwd / "package.json"
    if package_json.exists():
        try:
            content = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"error: package.json is invalid JSON: {exc}", file=sys.stderr)
            sys.exit(2)
        dev_deps: dict[str, str] = {}
        deps = content.get("dependencies") or {}
        dev = content.get("devDependencies") or {}
        if isinstance(deps, dict):
            dev_deps.update({k.lower(): v for k, v in deps.items()})
        if isinstance(dev, dict):
            dev_deps.update({k.lower(): v for k, v in dev.items()})
        if "vitest" in dev_deps:
            return "vitest"
        if "jest" in dev_deps:
            return "jest"
        # No test runner declared but package.json exists → assume vitest (modern default)
        return "vitest"

    # Fallback by file extension dominance
    python_files = list(cwd.rglob("*.py"))
    ts_files = list(cwd.rglob("*.ts")) + list(cwd.rglob("*.tsx")) + list(cwd.rglob("*.js"))
    go_files = list(cwd.rglob("*.go"))
    rs_files = list(cwd.rglob("*.rs"))
    counts = {"pytest": len(python_files), "vitest": len(ts_files), "go": len(go_files), "cargo": len(rs_files)}
    dominant = max(counts, key=lambda k: counts[k])
    if counts[dominant] == 0:
        return None
    return dominant

def find_manifest_for_framework(cwd: Path, framework: str) -> str | None:
    """Find manifest file for a given framework."""
    mapping: dict[str, list[str]] = {
        "pytest": ["pyproject.toml", "setup.cfg", "pytest.ini", "requirements.txt"],
        "vitest": ["package.json"],
        "jest": ["package.json"],
        "go": ["go.mod"],
        "cargo": ["Cargo.toml"],
    }
    for name in mapping.get(framework, []):
        if (cwd / name).exists():
            return name
    return None

def main() -> None:
    """Main entry point for framework detection."""
    args = parse_args()
    cwd: Path = args.cwd.resolve()

    if not cwd.exists() or not cwd.is_dir():
        print(f"error: --cwd not a directory: {cwd}", file=sys.stderr)
        sys.exit(2)

    if args.framework is not None:
        framework = args.framework
        manifest = find_manifest_for_framework(cwd, framework)
        details = FRAMEWORKS[framework]
        payload = {
            "framework": framework,
            "manifest": manifest,
            "test_dir": details["test_dir"],
            "command": details["command"],
            "scoped_command": details["scoped"],
            "file_template": details["template"],
            "cwd": str(cwd),
        }
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"framework: {framework} (forced)  manifest: {manifest or '—'}  command: {details['command']}")
        return

    detected = detect_from_manifest(cwd, args.manifest)
    if detected is None:
        print(
            "error: could not detect framework — no manifest and no dominant language.\n"
            "hint: pass --framework pytest|vitest|jest|go|cargo explicitly, or add a manifest.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Ambiguity: both Python and JS present with manifests
    has_python_manifest = any((cwd / name).exists() for name in ["pyproject.toml", "setup.cfg", "pytest.ini"])
    has_js_manifest = (cwd / "package.json").exists()
    has_go = (cwd / "go.mod").exists()
    has_cargo = (cwd / "Cargo.toml").exists()
    manifest_count = sum([has_python_manifest, has_js_manifest, has_go, has_cargo])
    if manifest_count > 1 and args.manifest is None:
        print(
            f"warning: multiple manifests detected (python={has_python_manifest} js={has_js_manifest} go={has_go} cargo={has_cargo}) — "
            f"picking '{detected}' by priority. Pass --manifest or --framework to lock.",
            file=sys.stderr,
        )

    details = FRAMEWORKS[detected]
    manifest = find_manifest_for_framework(cwd, detected)
    payload = {
        "framework": detected,
        "manifest": manifest,
        "test_dir": details["test_dir"],
        "command": details["command"],
        "scoped_command": details["scoped"],
        "file_template": details["template"],
        "cwd": str(cwd),
    }
    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"framework: {detected}  manifest: {manifest or '—'}  command: {details['command']}  template: {details['template']}")

if __name__ == "__main__":
    main()
