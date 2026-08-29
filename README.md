<p align="center">
  <img src="banner.svg" alt="Nextreme Skills" width="720" />
</p>

# Nextreme Skills

A focused, **agent-agnostic** collection of reusable AI-agent skills. Each skill lives in its own directory as a single `SKILL.md` (plus `references/` when the body needs to stay lean). They carry no tool ACLs and no agent-specific subagent ids — state behavior, not permissions — so any agent can run them.

## Skills

| Skill | What it does | Invoke when |
| --- | --- | --- |
| [`next-best-thing`](next-best-thing/) | Finds the **single smallest** change with the highest impact and ships it. | "next best thing", "smallest high-leverage step", "what should I do next" |
| [`next-big-thing`](next-big-thing/) | Finds the **highest-impact big/medium** build: ships low-risk small stuff autonomously, then gates a feature shortlist on your approval. | "next big thing", "plan a major feature", "biggest move" |
| [`nextreme-decision`](nextreme-decision/) | Makes the **most extreme, highest-leverage** call on anything — commits to ONE recommendation, then offers an out-of-the-box alternative. | "decide for me", "make the extreme call", "settle this" |
| [`nextreme-architect`](nextreme-architect/) | Spec-driven system architect: interviews (or takes a `yolo` mandate), then writes the buildable blueprint — no implementation. | "architect this", "plan the system", "write the spec" |
| [`nextreme`](nextreme/) | Pair programmer that **composes** the right Nextreme-skill workflow for any multi-phase software task. | "pair with me", "full workflow for X", "build this with me" |
| [`skill-router`](skill-router/) | Routes any user intent to the **right** Nextreme skill instead of guessing which one fires. | "which skill should I use", "route this" |
| [`nextreme-skill-creator`](nextreme-skill-creator/) | Designs, writes, and improves skills with rigorous craft (predictability, triggering, hierarchy, pruning). | "create a skill", "improve this skill", "why doesn't my skill trigger" |
| [`tdd-coach`](tdd-coach/) | Coaches test-driven development: failing test first, smallest pass, then refactor. | "TDD this", "red-green-refactor", "write the test before the code" |
| [`git-guardrails`](git-guardrails/) | Stops destructive, irreversible git operations before they run and suggests the safe path. | "guard my git", "block force push", "don't let me reset --hard" |
| [`high-quality-flowcharts`](high-quality-flowcharts/) | Produces publication-grade flowcharts, roadmaps, process diagrams, decision trees, and taxonomy maps as print-ready PDF (HTML+SVG). | "flowchart", "roadmap", "decision tree", "process diagram" |
| [`ultimate-charts`](ultimate-charts/) | Generates publication-grade SVG charts from data (Vega-Lite/Vega, QuickChart, ECharts) for every chart type. | "chart", "bar chart", "line chart", "visualize this data" |
| [`ultimate-diagrams`](ultimate-diagrams/) | Generates system architecture, UML, AI/agent workflows, C4, and event-driven technical diagrams (SVG/PDF). | "system diagram", "architecture diagram", "UML", "sequence diagram" |
| [`readme-architect`](readme-architect/) | Writes a repo-grounded, professional `README.md` after investigating the actual codebase. | "write a README", "make my repo look professional", "add docs" |

## How the "next thing" skills differ

- **`next-best-thing`** thinks *small*: one shippable move, no approval gate, opt-in loop for repeated small wins.
- **`next-big-thing`** thinks *large*: clears the safe wins itself, then **stops and waits** for you to pick the big build before writing it.

## Install

Skills are installed per-agent from this repo (skills.sh indexes it via the `agent-skills` topic):

```bash
# one skill
npx skills add beast-ofcourse/Nextreme-skills --skill nextreme-decision

# everything
npx skills add beast-ofcourse/Nextreme-skills --all
```

Or copy a skill folder into your agent's skills directory. Each `SKILL.md` is self-contained.

## Layout

```
.
├── README.md                       # this index
├── banner.svg                      # repo banner
├── AGENTS.md                       # Engineering Operating System (EOS) + skill catalog
├── next-best-thing/                # smallest-high-impact skill
├── next-big-thing/                 # biggest-high-impact skill (gated)
├── nextreme-decision/              # extreme decision-maker
├── nextreme-architect/             # spec-driven planning (portable)
├── nextreme/                       # pair-programmer workflow composer
├── skill-router/                   # intent -> skill router
├── nextreme-skill-creator/         # skill authoring craft + workflow
│   └── references/                 # glossary.md, workflow.md
├── tdd-coach/                      # test-driven development coach
├── git-guardrails/                 # git safety rails
├── evals/                          # trigger-test prompts per skill
│   ├── next-best-thing.json
│   ├── next-big-thing.json
│   └── nextreme-skill-creator.json
└── templates/                      # shared SKILL.md scaffolding
    └── SKILL.md
```

## Authoring a new skill

Copy `templates/SKILL.md`, fill the frontmatter, and follow the craft in `nextreme-skill-creator`. Add matching prompts to `evals/`.

## License

MIT. Each skill is MIT-licensed (see its `SKILL.md` frontmatter).
