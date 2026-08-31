#!/usr/bin/env python3
"""Proof pack: git diff --stat, before/after snippets, benchmark stub → proof/<slug>.md"""
import subprocess
import sys
import pathlib

def run(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip() + ("\n" + result.stderr.strip() if result.stderr.strip() else "")

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: proof_builder.py <slug> [--benchmark 'pytest -q']", file=sys.stderr)
        sys.exit(2)
    slug = sys.argv[1]
    benchmark_cmd = sys.argv[2] if len(sys.argv) > 2 else ""
    out = pathlib.Path(f"proof/{slug}.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    diff_stat = run("git diff --stat")
    diff = run("git diff --unified=2 | head -n 200")
    before_after = "<!-- Paste 1–2 before/after snippets or screenshots here -->\n"
    bench = run(benchmark_cmd) if benchmark_cmd else "(add benchmark output: time, hey, pytest, validate, etc.)"
    md = f"""# Proof — {slug}

## Branch
`{run('git branch --show-current')}`

## Diff stat
```
{diff_stat or '(no diff yet — did you modify the picked part?)'}
```

## Key diff (first 200 lines)
```
{diff or '(empty)'}
```

## Before / After
{before_after}
- **Before:** <describe or screenshot>
- **After:** <describe or screenshot>

## Benchmarks
```
{bench}
```

## Validation
```
{run('git status --porcelain') or '(clean)'}
```
"""
    out.write_text(md, encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
