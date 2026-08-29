---
name: next-big-thing
description: Find the highest-impact big or medium implementation in a repository, clear the underbrush first, then defer to the human for the big build. Specifically scan the repo, ship the low-risk small stuff (optimizations, polishing, hardening, quick fixes) without waiting for approval, then present a fine-picked shortlist of feature candidates and implement the user-approved one through a proper workflow. Use when the user says "next big thing", "biggest move", "plan a major feature", "highest-impact project", "what should we build next" (large scope), or when a project needs a substantial, high-leverage build rather than a tiny tweak. Trigger proactively when the user wants direction on a large effort, not just the next small step. Opt-in loop "/next-big-thing loop N" repeats the full cycle N times.
license: MIT
---

# Next Big Thing

You find the highest-impact *big or medium* implementation in a repository. Unlike `next-best-thing`, which ships the single smallest high-leverage move, you think larger — but you earn the right to think large by clearing the safe wins first.

The shape of the work:

- **Small stuff ships without asking.** Optimizations, polishing, hardening, and quick fixes are low-risk and high-value; you do them autonomously, like a good maintainer.
- **Big features wait for a blessing.** The substantial, opinionated, multi-surface builds are proposed, not assumed. You fine-pick a shortlist and stop for the human's pick before writing the large change.

The leverage is in the two-tier split: by shipping the cheap wins yourself, you remove noise and build trust; by reserving the expensive, contested build for a human decision, you avoid unrequested large changes and analysis paralysis at once. The output of the scan phase is both shipped changes *and* a decision-ready shortlist — never just a document, never an unapproved rewrite.

## The workflow

### 1. Scan the whole repo
Read broadly before judging narrowly. Inspect the structure, entry points, tests, build, CI, and recent commit history. Establish what the project actually is and how it is developed.

Completion criterion: you can describe the project's purpose, its primary language/stack, its main surfaces (CLI/API/UI), and where the bulk of activity lives — from evidence, not assumption.

### 2. Enumerate candidates in two buckets
List every candidate move you found, then split it deliberately:

- **Feature candidates** — big or medium builds with the highest impact: new capabilities, restructurings, large UX or architectural moves. For each, jot the expected impact, the rough effort, and the surfaces it would touch.
- **Small-stuff candidates** — optimizations (speed/memory), polishing (UX/docs/consistency), hardening (security/reliability/error handling), and tiny fixes. These are low-risk and finishable in-session.

The split is the heart of the skill: it answers "what do I just do?" versus "what do I propose?".

Completion criterion: you hold two distinct lists — a feature shortlist of 3–7 concrete candidates (each with impact, effort, surfaces touched) and a small-stuff list of concrete finishable items. No candidate sits in both.

### 3. Ship the small stuff (no approval)
For each small-stuff candidate, make the change yourself — do not stop to ask. Keep the blast radius tight, match existing patterns, handle edge cases and errors explicitly, leave no dead weight, and follow the repo's contribution conventions (lint, tests, commit style). Run the lightest fitting verification after each.

This step is autonomous by design: the items here are cheap, safe, and clearly good. Pausing for approval on a typo fix or a missing test would waste the human's attention.

Completion criterion: every small-stuff item is complete, its relevant tests/build pass, and no unrelated code was touched. A consolidated summary of what shipped accompanies the work.

### 4. Fine-pick and present feature candidates
From the feature list, rank the candidates and surface a shortlist of the top 3–5, each with: expected impact, relative effort, key risk, and a recommended pick with its reasoning versus the runners-up. Then **stop and wait**. Do not begin the large build until the user selects one.

The gate exists because a big/medium implementation is expensive, opinionated, and hard to reverse: the human should place the bet, not the agent. Presenting a fine-picked shortlist (not the raw brainstorm) respects their time and makes the decision easy.

Completion criterion: a ranked shortlist is shown to the user; no implementation of any feature candidate has started; the agent is explicitly awaiting the user's selection.

Skip the user's approval if the user has explicitly said "yolo-decision", then you will pick the Extreme decision by yourself and Continue the worklow 

### 5. Implement the approved feature (proper workflow)
Once the user picks a candidate, build it through a real workflow rather than a single pass:

- **Design.** Spell out the approach: surfaces touched, data flow, contracts, and the edge cases you will handle. Confirm the plan is finishable in-scope before coding.
- **Implement.** Make small, proven changes; match existing patterns; handle errors and invalid input explicitly; remove dead weight; follow the repo's conventions. Keep the blast radius to the chosen feature only.
- **Verify.** Run the lightest verification that fits the change (tests, build, lint, type check, or a runtime check). Report what you changed, the impact you expected, and what you actually verified.

Completion criterion: the approved feature is complete, the relevant verification passed (or you explicitly state what could not be verified), unrelated code was untouched, and the report names the move, the evidence, and any residual risk.

## Opt-in Loop Mode

Run the full cycle more than once so the backlog of high-impact work keeps clearing. The loop is **strictly opt-in** — never loop unless the user explicitly opted in.

### Trigger
- Explicit count: `/next-big-thing loop 5` runs the full 5-step cycle **5 times**, each pass against the repo *as it stands after the previous cycle*.
- Natural-language equivalent (`"run this 3 times"`, `"keep going for 5 builds"`) counts as opt-in with that N.

### Opt-in gate (when no count was given)
If the user did not supply a loop count, ask exactly one clarifying question before starting:

> **Loop?** Single cycle (one approved build) — or loop N times? (suggest N from how much high-impact work the scan surfaced, typically 2–4)

Only loop after the user answers with a positive integer, or a plain "no" / "just one". Do not assume a loop.

### How each iteration runs
- Re-run steps 1–5 from scratch every pass. The repo changed, so the scan, the candidate split, and the shortlist must be freshly derived — never reuse an earlier list or ranking.
- The approval gate still applies every iteration: present the shortlist and wait for a pick before each big build.
- Decrement the remaining count by one after each completed build.
- Stop early (before N) if any of these hold:
  - verification fails and the build can't be made safe in-session,
  - no feature candidate clears the "finishable in-scope" bar,
  - the user says stop.

### Guardrails
- The small-stuff sweep stays autonomous every pass; the feature build stays gated every pass.
- Keep the same tight blast radius and contribution conventions every pass.
- Report each iteration's shipped small items, the chosen build, its evidence, and residual risk; end with a cumulative summary.

## Principles

- **Big builds need a blessing; small wins ship.** The split between autonomous and gated work is the whole point — don't collapse it by asking about trivia or by assuming a large change.
- **Evidence over instinct.** Inspect the repo before claiming what is wrong, missing, or worth building.
- **Impact is measured, not vibed.** State why a candidate matters and roughly how much.
- **Shortlist, don't dump.** Present a fine-picked few with a recommendation, not the raw brainstorm — the human decides the bet, fast.
- **Highest ratio among the big candidates wins — but the human places it.** Rank by impact per effort, then let the owner choose the wager.
