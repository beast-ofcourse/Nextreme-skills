---
name: git-guardrails
description: Stop destructive and irreversible git operations before they run, and suggest the safe alternative. Use when the user says "guard my git", "block force push", "don't let me reset --hard", "safe git workflow", or before any command touching history, remotes, or untracked files. Intercepts pushes/force-pushes, reset --hard, clean -f, branch -D, checkout over dirty work, and amend-on-shared-history; explains the risk and offers a reversible path. Trigger proactively whenever a proposed git command is history-rewriting or could drop uncommitted work.
license: MIT
---

# Git Guardrails

You put a fence around the git commands that can't be undone. Most git damage is one typo away — a force-push to `main`, a `reset --hard` over uncommitted work, a `clean -f` that deletes a day. The guardrail is not to forbid, but to make the irreversible explicit and offer the reversible route.

## The workflow

### 1. Read the proposed command
Capture the exact git command the user is about to run (or just ran). If it's not git, or it's read-only (`status`, `log`, `diff`), do nothing — guardrails only fire on mutating or history-touching ops.

Completion criterion: the command is captured verbatim, or the skill confirms it is read-only and takes no action.

### 2. Classify the risk
Map the command to a risk tier:
- **Destructive / irreversible:** `push --force` (or `-f`), `reset --hard`, `clean -f`/`-fd`, `branch -D`, `restore --staged --worktree` over uncommitted changes, `checkout`/`switch` that would discard dirty work.
- **History-rewriting on shared branch:** `commit --amend`, `rebase`/`merge` with `--no-ff` after push.
- **Safe:** anything local and recoverable.

Completion criterion: the command has exactly one risk tier assigned from the list above; if it matches none, it is treated as safe.

### 3. Intercept or pass
If the command is **safe**, let it proceed. If it is **destructive or history-rewriting**, stop and report: the exact risk, what it could destroy, and a reversible alternative (e.g. `push --force-with-lease` instead of `-f`; `git stash` before `reset`; `branch -d` after merge). Do not execute the destructive command.

Completion criterion: a destructive/history-rewriting command is not run; the user sees the risk, the blast radius, and at least one safer alternative.

### 4. Offer the safe path
For each blocked command, give the concrete replacement and when it is actually fine (e.g. `--force-with-lease` is safe solo, never on shared `main`). Keep it to a few lines — the user is mid-flow.

Completion criterion: the reply contains the exact safer command and the one condition under which the original would be acceptable.

## Principles

- **Intercept the irreversible, pass the safe.** Guardrails that nag on `git add` get disabled; fire only on real risk.
- **Always show the reversible route.** A block without an alternative is just friction. Name the safe command.
- **State the blast radius.** "This drops uncommitted work in 3 files" beats "dangerous".
- **Never run it for them.** The guardrail reports; the human executes the safe version. Autonomy stops at the fence.
- **Tier, don't binary.** Not every risky command is equal — force-push to `main` is worse than `--amend` on a private branch, and the advice reflects that.
