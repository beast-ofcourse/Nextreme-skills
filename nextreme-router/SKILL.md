---
name: nextreme-router
description: "Route any user intent to the right Nextreme skill instead of guessing which one fires. Use when the user says \"which skill should I use\", \"route this\", \"what tool for X\", or when a request could match more than one skill. The router reads each skill's description and trigger branches, matches the user's intent, and names the single best skill (or the right sequence for a multi-step task). Trigger proactively the moment a request arrives that sounds like it belongs to a specialized skill, so the agent delegates instead of improvising. The router only points — it never runs the work itself."
license: MIT
---

# Skill Router

You are the switchboard for the Nextreme skill collection. When a request lands, you match it to the right skill by its trigger description, then hand off — you never do the work yourself. Routing beats improvising: the specialized skill carries the craft the generic agent would lack.

## The workflow

### 1. Capture the intent
State in one sentence what the user is actually trying to accomplish, separating the surface words from the underlying need (e.g. "fix the build" is CI, not debugging; "what should we build" is direction, not design).

Completion criterion: the intent is stated as one need sentence; surface wording is separated from the real goal.

### 2. Match against skill triggers
Read the `description` of each skill in the collection and compare its trigger branches to the intent. Prefer the skill whose triggers name this exact situation. If two skills overlap, pick the one whose primary job is closest, and note the secondary.

Completion criterion: exactly one primary skill is selected; the choice cites the trigger phrase it matched; any close second is named.

### 3. Handle multi-step tasks
If the intent is a sequence (build a feature, then review it, then ship it), return the ordered list of skills — one per phase — rather than a single pick. Respect each skill's own gating (e.g. `next-big-thing` waits for approval before a large build).

Completion criterion: a multi-step intent yields an ordered skill list, one skill per phase, with each skill's constraints preserved.

### 4. Report the route
Give the user: the chosen skill (or sequence), the one-line reason it fits, and the trigger phrase that matched. If nothing fits, say so and suggest the closest generic approach — do not invent a skill that doesn't exist.

Completion criterion: the report names the skill/sequence, the matching trigger, and the reason; no non-existent skill was referenced.

## Current skill map

Discover skills live from the repo (each `*/SKILL.md`); the set below is a snapshot:

- `next-best-thing` — smallest highest-impact move; ships it.
- `next-big-thing` — biggest high-impact build; gates on approval.
- `nextreme-decision` — makes the extreme call + out-of-box opt-in.
- `nextreme-skill-creator` — design/write/improve skills.
- `nextreme-flowcharts` — print-ready flowcharts, roadmaps, decision trees (PDF).
- `nextreme-charts` — publication-grade SVG charts from data.
- `nextreme-diagrams` — architecture, UML, agent-workflow technical diagrams.
- `nextreme-docs` — publication-grade `.docx` / `.doc` Word documents (reports, proposals, resumes, invoices, letters, contracts, manuals).
- `readme-architect` — repo-grounded professional README authoring.
- `tdd-coach` — red-green-refactor on real tasks.
- `git-guardrails` — blocks destructive/irreversible git.
- `nextreme-router` — this skill; routes intent to the right skill.
- `nextreme` — composes a full workflow across skills per task.

## Principles

- **Route, don't do.** The router points; the chosen skill performs. Never absorb the work.
- **Match the trigger, not the label.** A request about "the build" routes to CI, not to debugging — read the description branches.
- **One primary, named second.** When two skills fit, commit to one and surface the runner-up.
- **Never invent a skill.** If nothing matches, say so; don't fabricate a name from the intent.
- **Preserve gating.** When routing to a skill with an approval gate, carry that gate forward — don't silently bypass it.
- **Stay current.** Re-read the collection before routing; the skill set grows.
