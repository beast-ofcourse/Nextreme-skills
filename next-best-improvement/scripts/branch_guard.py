#!/usr/bin/env python3
"""Hard gate: creates next-best-improvement/<slug> from a clean tree. Refuses to proceed on main without branch."""
import subprocess
import sys
import re

def run(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: branch_guard.py <slug>  # e.g. event-graph-ingest", file=sys.stderr)
        sys.exit(2)
    slug = sys.argv[1].strip().lower()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        print(f"Bad slug '{slug}' — use kebab-case [a-z0-9-]", file=sys.stderr)
        sys.exit(2)
    branch = f"next-best-improvement/{slug}"
    # dirty check
    status = run("git status --porcelain")
    if status:
        print("Dirty tree — stash or commit first:", file=sys.stderr)
        print(status, file=sys.stderr)
        sys.exit(2)
    # already on branch?
    current = run("git branch --show-current")
    if current == branch:
        print(f"Already on {branch}")
        return
    # exists?
    exists = subprocess.run(f"git rev-parse --verify {branch}", shell=True, capture_output=True).returncode == 0
    if exists:
        print(f"Branch {branch} already exists — checking out", file=sys.stderr)
        run(f"git checkout {branch}")
    else:
        run(f"git checkout -b {branch}")
    print(f"On branch {run('git branch --show-current')}")

if __name__ == "__main__":
    main()
