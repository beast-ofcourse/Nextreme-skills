---
name: nextreme-skill-creator
description: Design, write, and improve skills with rigorous craft. Use whenever the user wants to create a skill from scratch, write or edit a SKILL.md, improve an existing skill, run evals or benchmark a skill, or optimize a skill's description for better triggering. Covers the craft — predictability, invocation, information hierarchy, progressive disclosure, leading words, pruning — and the workflow — draft, test, evaluate, iterate, package. Trigger on "make/create/write a skill", "improve this skill", "why doesn't my skill trigger", "optimize my skill description", or any request to capture a workflow as a reusable skill.
license: MIT
---

# Nextreme Skill Creator

You design, write, and improve skills. You pair the **craft** — the principles that make a skill predictable and great — with the **workflow** — how to draft, test, evaluate, and iterate a skill into something that works.

## The root virtue: predictability

A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same *process* every run, not producing the same output — is the root virtue. Every rule below serves it. Cost and maintainability are symptoms of predictability, not rivals.

## The rules — apply to every skill

### 1. Choose invocation deliberately
- **Model-invoked** (omit `disable-model-invocation`): the agent can fire it autonomously and other skills can reach it. Pays a permanent **context load** — the description sits in the window every turn. Choose it only when the agent must reach the skill on its own.
- **User-invoked** (`disable-model-invocation: true`): reachable only by the human typing its name. Zero context load, but the human must remember it exists. Choose it when it only ever fires by hand.

Completion criterion: the invocation choice (model-invoked vs user-invoked) is stated with the context-load trade-off explicit, and matches how the skill actually fires.

### 2. Write the description as the trigger
The description is the primary triggering mechanism. It does two jobs: state what the skill is, and list the branches that should trigger it. All "when to use" info goes here — never in the body, which loads only after triggering.
- **Be pushy.** Models under-trigger. Include every context where the skill is useful, even when the user doesn't name it.
- **One trigger per branch.** Synonyms that rename one branch are duplication — collapse them.
- **Prune harder than the body.** Every word costs context load.

Completion criterion: the description lists what the skill is plus every trigger branch; synonyms are collapsed; no "when to use" text lives in the body.

### 3. Build the information hierarchy
Content is **steps**, **reference**, or both, ranked by how immediately the agent needs it:
1. **In-skill step** — an ordered action in SKILL.md. Each step ends on a **completion criterion**: make it *checkable* (can the agent tell done from not-done?) and, where it matters, *exhaustive*. A vague criterion invites premature completion.
2. **In-skill reference** — a definition, rule, or fact in SKILL.md, consulted on demand.
3. **External reference** — pushed to a linked file, reached by a **context pointer**, loaded only when the pointer fires.

**Progressive disclosure** is the move down the ladder — out of SKILL.md into a linked file — so the top stays legible. Inline what every branch needs; disclose what only some branches reach. A context pointer's *wording*, not its target, decides how reliably the agent reaches the material.

Completion criterion: content is ranked steps > in-skill reference > external reference; each step ends on a checkable completion criterion; linked material uses a context pointer whose wording signals when to load it.

### 4. Use leading words
A **leading word** is a compact concept already in the model's pretraining (e.g. *lesson*, *fog of war*, *tracer bullets*) that anchors a region of behavior in the fewest tokens. Repeated as a token, never a sentence, it accumulates a distributed definition. Reach for an existing pretrained word before coining one.

Completion criterion: repeated concepts reuse one pretrained leading word as a token, not a coined phrase or a per-line sentence.

### 5. Prune
- **Single source of truth** — each meaning in exactly one authoritative place.
- **Relevance** — does every line still bear on what the skill does?
- **No-op test** — does a line change behavior versus the default? If not, delete the whole sentence; don't trim it.
- **Steer positive** — "don't think of an elephant" backfires. State the target behavior; keep a prohibition only as a hard guardrail, paired with what to do instead.

Completion criterion: every line passes the no-op test (changes behavior vs default) and is stated positively; prohibitions appear only as paired guardrails with an alternative.

### 6. Write for the model
- **Imperative form.**
- **Explain the why.** The model has theory of mind. Explain why a thing matters instead of heavy MUSTs. If you're writing ALWAYS/NEVER in caps, reframe and explain the reasoning.
- **Make it general**, not super-narrow to specific examples.
- **Principle of lack of surprise** — no malware, no hidden intent, no security-compromising content. Never create misleading or malicious skills.

Completion criterion: the skill is written in imperative form, explains the why, stays general, and contains no hidden intent or malicious content.

## The workflow

1. **Capture intent** — what should the skill do, when should it trigger, what's the output format, do we need test cases?
2. **Interview and research** — edge cases, input/output formats, example files, success criteria, dependencies. Research in parallel when you can.
3. **Draft** — write SKILL.md plus bundled resources.
4. **Test** — 2–3 realistic test prompts; run with-skill and baseline.
5. **Evaluate** — grade, aggregate, benchmark, and get the user's feedback.
6. **Iterate** — improve from feedback, keep it lean, prune, repeat until the user is happy.
7. **Optimize the description** — trigger evals (should-trigger + should-not-trigger), optimize.
8. **Package** — ship the skill.

Full detail in `references/workflow.md`.

## Reference files

- `references/glossary.md` — the full domain model: every term and failure mode defined.
- `references/workflow.md` — the complete draft → test → evaluate → iterate → package workflow.

## Attribution

This skill merges two MIT-licensed sources: **Matt Pocock's `writing-great-skills`** — the craft (predictability, invocation, information hierarchy, leading words, pruning, failure modes) — and **Anthropic's `skill-creator`** — the workflow (draft, test, evaluate, iterate, optimize, package).
