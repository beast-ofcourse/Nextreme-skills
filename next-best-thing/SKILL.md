---
name: next-best-thing
description: "Find the smallest next change that yields the highest impact in a repository, then ship it. Use when the user says \"next best thing\", \"what should I do next\", \"smallest high-impact step\", \"what's the highest-leverage change\", or when a project feels stuck and needs the one right move. The move can be anything: a feature, an optimization, a speedup, tightening, polishing, or hardening. Trigger proactively when the user wants direction, not a full plan. Opt-in loop: \"/next-best-thing loop N\" repeats the workflow N times, one best move per iteration."
license: MIT
---

# Next Best Thing

You find the single smallest change in a repository that produces the highest impact, then you make it. Not the biggest plan, not the roadmap — the *next* thing, small enough to finish, large enough to matter.

### Core Rule
```
- It could be anything , a feature, a brainstorm idea , optimization, speed, performace, polishing , hardening , tightening and improving something.
```
The leverage is in the constraint: by refusing to enumerate everything that could be done and instead committing to the one move with the best impact-per-effort ratio, you avoid analysis paralysis and produce visible progress. The output is a change, not a document.

## The workflow

### 1. Scan the whole repo
Read broadly before judging narrowly. Inspect the structure, the entry points, the tests, the build, the CI, and the recent commit history. Establish what the project actually is and how it is developed.

Completion criterion: you can describe the project's purpose, its primary language/stack, its main surfaces (CLI/API/UI), and where the bulk of activity lives — from evidence, not assumption.

### 2. Enumerate candidate moves
List candidate next moves across every category: features, optimizations, speedups, tightening (debt cleanup), polishing (UX/docs), hardening (security/reliability/error handling). For each, jot the expected impact and the rough effort.

Completion criterion: you have a short list (3–7) of concrete, distinct candidates, each with a one-line impact estimate and a relative effort estimate.

### 3. Pick by impact-per-effort
Rank candidates by impact divided by effort. Choose the one with the best ratio that is also genuinely small — finishable in this session. Reject anything that would become a multi-day project; a smaller, shippable move beats a perfect one you never land.

Completion criterion: exactly one move is selected, with a stated reason comparing it against the runners-up.

### 4. Implement the move
Make the change. Keep the blast radius tight. Match existing patterns, handle edge cases and errors explicitly, leave no dead weight, and follow the repo's contribution conventions (lint, tests, commit style).

Completion criterion: the change is complete, the relevant tests/build pass, and no unrelated code was touched.

### 5. Verify and report
Run the lightest verification that fits the change (tests, build, lint, type check, or a runtime check). Report what you changed, the impact you expected, and what you actually verified.

Completion criterion: verification succeeded (or you explicitly state what could not be verified), and the report names the move, the evidence, and any residual risk.

## Opt-in Loop Mode

Run the workflow more than once in a row so the repo keeps improving move by move. The loop is **strictly opt-in** — never loop unless the user explicitly opted in.

### Trigger
- Explicit count: `/next-best-thing loop 5` runs the full 5-step workflow **5 times**, each pass against the repo *as it stands after the previous move*.
- Natural-language equivalent (`"run this 3 times"`, `"keep going for 5 iterations"`) counts as opt-in with that N.

### Opt-in gate (when no count was given)
If the user did not supply a loop count, ask exactly one clarifying question before starting:

> **Loop?** No loop (single best move) — or loop N times? (suggest N from how much low-hanging fruit the scan surfaced, typically 3–5)

Only loop after the user answers with a positive integer, or a plain "no" / "just one". Do not assume a loop.

### How each iteration runs
- Re-run steps 1–5 from scratch every pass. The previous move changed the repo, so the next scan and candidate list must be freshly derived — never reuse the earlier candidate list or ranking.
- Decrement the remaining count by one after each completed move.
- Stop early (before N) if any of these hold:
  - verification fails and the move can't be made safe in-session,
  - no candidate clears the "genuinely small / finishable" bar (the repo is clean for now),
  - the user says stop.

### Guardrails
- One move per iteration. Never batch a candidate list into a single pass.
- Keep the same tight blast radius and contribution conventions every pass.
- Report each iteration's move, evidence, and residual risk; end with a short cumulative summary of all moves shipped.

## Principles

- **Small beats perfect.** A shippable improvement now outranks a flawless plan later.
- **Evidence over instinct.** Inspect the repo before claiming what is wrong or missing.
- **One move at a time.** Do not batch the candidate list into this session's work.
- **Impact is measured, not vibed.** State why a move matters and roughly how much.
- **Highest ratio wins.** The "best" next thing is the best *impact per unit effort*, not the largest impact.
