# Skill Creation Workflow

The complete process for creating, testing, and improving a skill. Read this when you're running the full loop — not for a quick one-off skill, where the lean workflow in SKILL.md is enough.

## The core loop

- Decide what the skill should do and roughly how it should do it
- Write a draft
- Create a few test prompts and run the agent-with-access-to-the-skill on them
- Help the user evaluate the results, qualitatively and quantitatively
- Rewrite the skill based on feedback
- Repeat until satisfied
- Expand the test set and try again at larger scale

Figure out where the user is in this loop and jump in there. If they already have a draft, go straight to the eval/iterate part. If they say "don't run a bunch of evals, just vibe with me", do that instead. The order is flexible.

## Communicating with the user

Users range from first-time terminal users to seasoned engineers. Read context cues and phrase accordingly. "Evaluation" and "benchmark" are borderline but OK; for "JSON" and "assertion", wait for serious cues that the user knows them before using them unqualified. Briefly explain terms when in doubt.

## Capture intent

Start by understanding intent. If the conversation already contains a workflow to capture, extract from history first — tools used, sequence of steps, corrections, input/output formats — then fill gaps with the user and confirm before proceeding.

1. What should this skill enable the agent to do?
2. When should it trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from them; subjective outputs (writing style, art) often don't. Suggest the default, let the user decide.

## Interview and research

Proactively ask about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until this is ironed out. Check available MCPs; research in parallel via subagents if available, otherwise inline. Come prepared to reduce burden on the user.

## Write the SKILL.md

Fill in the components:

- **name** — skill identifier (lowercase, hyphens for spaces)
- **description** — when to trigger, what it does. The primary triggering mechanism. Include both what it does AND specific contexts for when to use it. All "when to use" info goes here, not in the body. Make it a little "pushy" — models under-trigger. Example: instead of "How to build a simple fast dashboard to display internal data", write "How to build a simple fast dashboard to display internal data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard'."
- **compatibility**: required tools, dependencies (optional, rarely needed)
- **the rest of the skill**

### Anatomy of a skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

### Progressive disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — in context whenever the skill triggers (<500 lines ideal)
3. **Bundled resources** — as needed (unlimited; scripts can execute without loading)

These are approximate; go longer if genuinely needed. Key patterns:
- Keep SKILL.md under 500 lines; if approaching the limit, add a layer of hierarchy with clear pointers about where to go next.
- Reference files clearly from SKILL.md with guidance on when to read them.
- For large reference files (>300 lines), include a table of contents.

**Domain organization**: when a skill supports multiple domains/frameworks, organize by variant — keep the core workflow and selection guidance in SKILL.md, move variant-specific details into separate reference files (e.g. `references/aws.md`, `references/gcp.md`, `references/azure.md`). The agent reads only the relevant file.

### Principle of lack of surprise

Skills must not contain malware, exploit code, or anything that compromises security. A skill's contents should not surprise the user in their intent. Don't create misleading skills or skills designed for unauthorized access, data exfiltration, or other malicious activity. (Roleplay skills are fine.)

### Writing patterns

- Prefer the **imperative form**.
- **Output formats**: state the exact template.
- **Examples**: include them; format as Input/Output pairs when useful.

### Writing style

Explain **why** things matter instead of heavy MUSTs. The model has theory of mind — given a good harness it goes beyond rote instructions. If you find yourself writing ALWAYS/NEVER in caps or rigid structures, that's a yellow flag: reframe and explain the reasoning. Make the skill general, not super-narrow to specific examples. Write a draft, then look at it with fresh eyes and improve it.

## Test cases

After the draft, come up with 2–3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user and confirm. Save to `evals/evals.json` (prompts only at first; add assertions later):

```json
{
  "skill_name": "example-skill",
  "evals": [
    { "id": 1, "prompt": "User's task prompt", "expected_output": "Description of expected result", "files": [] }
  ]
}
```

## Run and evaluate

This is one continuous sequence — don't stop partway. Put results in `<skill-name>-workspace/` as a sibling to the skill, organized by iteration (`iteration-1/`, `iteration-2/`) and test case (`eval-0/`, `eval-1/`). Create directories as you go.

### Step 1: Spawn all runs in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without (baseline). Launch everything at once so it finishes around the same time.

- **With-skill run**: point the subagent at the skill path, the eval prompt, and where to save outputs.
- **Baseline run**: same prompt, no skill (new skill), or the old version (improving an existing skill — snapshot it first).

Write an `eval_metadata.json` per test case with a descriptive name (not "eval-0"), the prompt, and empty assertions for now.

### Step 2: Draft assertions while runs are in progress

Draft quantitative assertions for each test case and explain them to the user. Good assertions are objectively verifiable and have descriptive names. Subjective skills are better evaluated qualitatively — don't force assertions onto things that need human judgment.

### Step 3: Capture timing data as runs complete

When each subagent task completes, save `total_tokens` and `duration_ms` to `timing.json` in the run directory immediately — this data comes through the task notification and isn't persisted elsewhere.

### Step 4: Grade, aggregate, and review

1. **Grade each run** — evaluate each assertion against the outputs. For programmatically checkable assertions, write and run a script rather than eyeballing.
2. **Aggregate into a benchmark** — produce pass rate, time, and tokens per configuration, with mean ± stddev and the delta.
3. **Analyst pass** — surface patterns the aggregate hides: assertions that always pass regardless of skill (non-discriminating), high-variance evals (possibly flaky), time/token tradeoffs.
4. **Show the user** — present the qualitative outputs and the quantitative benchmark, and get their feedback.

### Step 5: Read the feedback

Focus improvements on the test cases where the user had specific complaints. Empty feedback means it was fine.

## Improve the skill

This is the heart of the loop.

1. **Generalize from feedback.** You're iterating on a few examples to build a skill used a million times. If the skill only works for those examples, it's useless. Rather than overfit changes or constrictive MUSTs, try different metaphors or patterns of working.
2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Read the transcripts, not just the final outputs — if the skill makes the agent waste time, cut the parts causing it.
3. **Explain the why.** Transmit understanding into the instructions. If you find yourself writing ALWAYS/NEVER in caps, reframe and explain the reasoning.
4. **Look for repeated work across test cases.** If all test runs independently wrote the same helper script, bundle it once into `scripts/` and tell the skill to use it.

Take your time — thinking time isn't the blocker. Write a draft revision, then look at it anew and improve.

### The iteration loop

1. Apply improvements.
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baselines.
3. Review with the user.
4. Read the new feedback, improve again, repeat.

Keep going until the user is happy, the feedback is all empty, or you're not making meaningful progress.

## Advanced: blind comparison

For a rigorous comparison between two versions ("is the new version actually better?"), give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won. Optional, requires subagents; most users won't need it.

## Description optimization

The description is the primary trigger. After creating or improving a skill, offer to optimize it for better triggering accuracy.

1. **Generate trigger eval queries** — 20 realistic queries, a mix of should-trigger and should-not-trigger. The should-trigger set covers different phrasings of the same intent, including cases where the user doesn't name the skill. The should-not-trigger set should be near-misses — queries sharing keywords but needing something different — not obviously irrelevant ones.
2. **Review with the user** — let them edit, toggle, add/remove before running.
3. **Run the optimization loop** — evaluate the current description, propose improvements based on failures, re-evaluate, iterate. Split into train/test to avoid overfitting; select the best description by test score.
4. **Apply the result** — update the SKILL.md frontmatter, show before/after, report the scores.

### How triggering works

Skills appear in the agent's `available_skills` list with name + description, and the agent decides whether to consult a skill based on that description. The agent only consults skills for tasks it can't easily handle on its own — simple one-step queries may not trigger even with a perfect description. Complex, multi-step, or specialized queries reliably trigger when the description matches. So eval queries should be substantive enough that the agent would actually benefit from the skill.

## Package and present

Package the skill into a distributable `.skill` file and direct the user to it so they can install it.

## Environment notes

- **With subagents**: the full parallel workflow works.
- **No subagents** (e.g. chat-only agents): run test cases one at a time yourself; skip baseline runs and quantitative benchmarking; present results inline in the conversation; skip description optimization and blind comparison.
- **No browser/display**: write a standalone HTML review file instead of starting a server; feedback comes back as a file.
- **Updating an existing skill**: preserve the original name; copy to a writeable location before editing if the installed path is read-only; stage before packaging.

## Reference files

- `references/glossary.md` — the full domain model: every term and failure mode defined.