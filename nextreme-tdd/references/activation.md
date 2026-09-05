# Activation — Making the Loop Fire Without Being Asked

Models default to implementation-first and under-trigger TDD. These hooks make the gate automatic. Adapt names to your agent; the events are the portable part.

## 1. Prompt-eval reminder (before every response)

On prompt submit, inject one line: "Does this task add or change behavior? If yes, route to `nextreme-tdd` before writing implementation." Measured effect on similar setups: skill activation roughly 20% → 84%. Costs one sentence of context; pays back in cycles that actually start at RED.

## 2. Post-change suite run (fast feedback)

After any test or source file write, run the framework's scoped command (`python -m pytest <file>`, `npx vitest run <file>`). Surfaces failures the moment they land. Cannot block — informational only.

## 3. Stop gate (the real enforcement)

When the turn ends, run the full suite. Non-zero exit blocks the stop and sends the agent back to GREEN. This is the gate that holds the line: no green suite, no finished turn. For heavy suites, scope the gate to the touched package and run full suite in CI.

## 4. What hooks must never do

Hooks run commands; they never weaken tests, never auto-commit, never skip the human's RED confirmation. A hook that edits assertions is reward hacking with automation.
