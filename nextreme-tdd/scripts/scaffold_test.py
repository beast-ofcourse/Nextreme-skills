#!/usr/bin/env python3
"""Scaffold the smallest failing test file for one behavior + case.

Why this exists: scaffolding from a valid template prevents typo-RED and guarantees the
placeholder fails for the behavior gap (unknown symbol / value diff), not for wiring.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

FRAMEWORK_DESTINATIONS: dict[str, str] = {
    "pytest": "tests/test_{snake}.py",
    "vitest": "src/{kebab}.test.ts",
    "jest": "src/{kebab}.test.ts",
    "go": "{snake}_test.go",
    "cargo": "tests/test_{snake}.rs",
}

def to_snake(raw: str) -> str:
    """Convert raw behavior name to snake_case."""
    sanitized = re.sub(r"[^a-zA-Z0-9]+", "_", raw.strip())
    sanitized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", sanitized)
    return sanitized.strip("_").lower()

def to_kebab(raw: str) -> str:
    """Convert raw behavior name to kebab-case."""
    return to_snake(raw).replace("_", "-")

def to_pascal(raw: str) -> str:
    """Convert raw behavior name to PascalCase."""
    return "".join(part.capitalize() for part in to_snake(raw).split("_") if part)

def load_template(framework: str) -> Path:
    """Load template path for a given framework."""
    name_map: dict[str, str] = {
        "pytest": "python-pytest.test.py",
        "vitest": "typescript-vitest.test.ts",
        "jest": "typescript-vitest.test.ts",
        "go": "go.test.go",
        "cargo": "rust.test.rs",
    }
    template_name = name_map.get(framework)
    if template_name is None:
        print(f"error: unknown framework '{framework}'", file=sys.stderr)
        sys.exit(2)
    template_path = TEMPLATE_DIR / template_name
    if not template_path.exists():
        print(f"error: template missing: {template_path}", file=sys.stderr)
        sys.exit(2)
    return template_path

def infer_go_package(cwd: Path, destination: Path) -> str:
    """Infer Go package name from target directory's existing Go files."""
    package_dir = destination.parent
    if not package_dir.exists():
        package_dir = cwd
    for candidate in package_dir.glob("*.go"):
        if candidate.name.endswith("_test.go"):
            continue
        try:
            lines = candidate.read_text(encoding="utf-8", errors="ignore").splitlines()
            first_line = lines[0] if lines else ""
            if first_line.strip().startswith("package "):
                inferred = first_line.strip().split()[1]
                if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", inferred):
                    return inferred
        except OSError:
            continue
    # Fallback: directory basename sanitized for Go package rules (lowercase, no hyphen)
    raw = package_dir.name if package_dir != cwd else cwd.name
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "", raw.lower().replace("-", "_"))
    if sanitized and re.fullmatch(r"[a-z_][a-z0-9_]*", sanitized):
        return sanitized
    return "main"

def render_template(template_text: str, behavior: str, case: str, package_name: str | None = None) -> str:
    """Render template with behavior, case, and optional package placeholders."""
    snake = to_snake(behavior)
    kebab = to_kebab(behavior)
    pascal = to_pascal(behavior)
    case_snake = to_snake(case)
    case_kebab = to_kebab(case)
    replacements: dict[str, str] = {
        "__behavior__": behavior,
        "__behavior_snake__": snake,
        "__behavior_kebab__": kebab,
        "__behavior_pascal__": pascal,
        "__case__": case,
        "__case_snake__": case_snake,
        "__case_kebab__": case_kebab,
        "__package_name__": package_name or "main",
    }
    rendered = template_text
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered

def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for test scaffolding."""
    parser = argparse.ArgumentParser(description="Scaffold a failing test for one behavior")
    parser.add_argument("--behavior", required=True, help="behavior name, e.g., calculate_tax_rounds_half_up")
    parser.add_argument("--case", default="happy_path", help="case name within the behavior, e.g., happy_path")
    parser.add_argument("--framework", choices=["pytest", "vitest", "jest", "go", "cargo"], help="force framework")
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="repo root for destination")
    parser.add_argument("--out", type=Path, default=None, help="explicit output path (overrides convention)")
    parser.add_argument("--package", type=str, default=None, help="Go package name override (only for go framework)")
    parser.add_argument("--dry-run", action="store_true", help="print destination without writing")
    parser.add_argument("--force", action="store_true", help="overwrite existing file")
    return parser.parse_args()

def resolve_destination(cwd: Path, framework: str, behavior: str, explicit_out: Path | None) -> Path:
    """Resolve output path for scaffolded test file."""
    if explicit_out is not None:
        return (cwd / explicit_out).resolve() if not explicit_out.is_absolute() else explicit_out.resolve()
    pattern = FRAMEWORK_DESTINATIONS[framework]
    snake = to_snake(behavior)
    kebab = to_kebab(behavior)
    rendered = pattern.format(snake=snake, kebab=kebab)
    return (cwd / rendered).resolve()

def main() -> None:
    """Scaffold a failing test file for one behavior."""
    args = parse_args()
    cwd: Path = args.cwd.resolve()
    behavior: str = args.behavior.strip()
    case: str = args.case.strip()

    if not behavior:
        print("error: --behavior must be non-empty", file=sys.stderr)
        sys.exit(2)
    if not case:
        print("error: --case must be non-empty", file=sys.stderr)
        sys.exit(2)
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+", behavior):
        print(f"error: --behavior contains unsupported characters: {behavior!r}", file=sys.stderr)
        sys.exit(2)

    framework = args.framework
    if framework is None:
        # Call detect_framework inline to avoid import coupling
        import subprocess
        import json as json_lib
        detector = Path(__file__).resolve().parent / "detect_framework.py"
        result = subprocess.run(
            [sys.executable, str(detector), "--cwd", str(cwd), "--json"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stderr.strip() or "error: framework detection failed", file=sys.stderr)
            print("hint: pass --framework pytest|vitest|jest|go|cargo", file=sys.stderr)
            sys.exit(result.returncode or 1)
        try:
            payload = json_lib.loads(result.stdout)
        except json_lib.JSONDecodeError as exc:
            print(f"error: detector emitted invalid JSON: {exc}", file=sys.stderr)
            sys.exit(2)
        framework = payload.get("framework")
        if not isinstance(framework, str) or framework not in FRAMEWORK_DESTINATIONS:
            print(f"error: detector returned unknown framework: {framework!r}", file=sys.stderr)
            sys.exit(2)

    template_path = load_template(framework)
    destination = resolve_destination(cwd, framework, behavior, args.out)

    if args.dry_run:
        print(str(destination))
        return

    if destination.exists() and not args.force:
        print(f"error: destination exists: {destination} (pass --force to overwrite)", file=sys.stderr)
        sys.exit(1)

    template_text = template_path.read_text(encoding="utf-8")
    package_name: str | None = None
    if framework == "go":
        if args.package:
            package_name = args.package
        else:
            package_name = infer_go_package(cwd, destination)
    rendered = render_template(template_text, behavior, case, package_name)

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"error: could not create directory {destination.parent}: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        destination.write_text(rendered, encoding="utf-8")
    except OSError as exc:
        print(f"error: could not write {destination}: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"wrote {destination} (framework={framework} behavior={behavior} case={case})")
    try:
        rel_hint = str(destination.relative_to(cwd))
    except ValueError:
        rel_hint = str(destination)
    print(f"next: run RED with {rel_hint} then verify_tdd.py --phase red")

if __name__ == "__main__":
    main()
