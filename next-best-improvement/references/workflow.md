# Workflow — 8 Steps in One Page

1. **Scan** → 5–8 feature-flow candidates, no trivia.
2. **Branch** → `git checkout -b next-best-improvement/<slug>` (hard gate, must be new branch).
3. **Ask** → present 3-mode menu (1 specific, 2 yolo, 3 random), lock one fragment + mode.
4. **Brainstorm** → 3 insane alternatives on 3 axes, commit to one with “why this wins”.
5. **Improve** → do anything inside the picked part, keep blast radius small, Golden Rules.
6. **Proof** → `proof/<slug>.md` with diff stat, before/after, benchmarks (numbers, not adjectives).
7. **Validate** → tests / `validate` green (or baseline-red acknowledged), pasted in proof.
8. **Deliver** → report branch + mode + fragment + pick + proof path + open risk. No merge/push without go-ahead.

Each step ends on a **completion criterion** in `SKILL.md` — do not proceed until it passes.
