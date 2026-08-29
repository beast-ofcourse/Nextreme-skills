# Nextreme Skills

A focused collection of reusable agent skills. Each skill lives in its own directory as a single `SKILL.md` (plus `references/` when the body needs to stay lean).

## Skills

| Skill | What it does | Invoke when |
| --- | --- | --- |
| [`next-best-thing`](next-best-thing/) | Finds the **single smallest** change with the highest impact and ships it. | "next best thing", "smallest high-leverage step", "what should I do next" |
| [`next-big-thing`](next-big-thing/) | Finds the **highest-impact big/medium** build: ships low-risk small stuff autonomously, then gates a feature shortlist on your approval. | "next big thing", "plan a major feature", "biggest move" |
| [`nextreme-skill-creator`](nextreme-skill-creator/) | Designs, writes, and improves skills with rigorous craft (predictability, triggering, hierarchy, pruning). | "create a skill", "improve this skill", "why doesn't my skill trigger" |

## How the two "next thing" skills differ

- **`next-best-thing`** thinks *small*: one shippable move, no approval gate, opt-in loop for repeated small wins.
- **`next-big-thing`** thinks *large*: clears the safe wins itself, then **stops and waits** for you to pick the big build before writing it.

## Layout

```
.
├── README.md                      # this index
├── AGENTS.md                      # Engineering Operating System (EOS) + skill catalog
├── next-best-thing/               # smallest-high-impact skill
├── next-big-thing/                # biggest-high-impact skill (gated)
├── nextreme-skill-creator/        # skill authoring craft + workflow
│   └── references/                # glossary.md, workflow.md
├── evals/                         # trigger-test prompts per skill
│   ├── next-best-thing.json
│   ├── next-big-thing.json
│   └── nextreme-skill-creator.json
└── templates/                     # shared SKILL.md scaffolding
    └── SKILL.md
```

## Authoring a new skill

Copy `templates/SKILL.md`, fill the frontmatter, and follow the craft in `nextreme-skill-creator`. Add matching prompts to `evals/`.
