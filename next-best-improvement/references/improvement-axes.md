# Improvement Axes — Make the 3 Alternatives Actually Distinct

When you brainstorm 3 extreme alternatives for the picked part, put each on a *different* axis. Safe tweaks on the same axis are not “out-of-the-box” — they are the same box.

| Axis | What insane looks like | Example for a slow report renderer |
|---|---|---|
| **Architecture** | Split god-file, deep module, flip data flow | 600-line handler → 3 deep modules, testable in isolation |
| **Performance** | Index, cache, stream, parallelize, cut N+1 | p95 6h → 4m incremental materialization |
| **UX / Visual** | Bento grid, editorial taste, motion, empty states | Zinc sterile → parchment + tracking iron law |
| **Correctness** | Harden types, eliminate `any`, invariant checks | 11 `any` → 0, plus `validate` at boundaries |
| **DX** | CLI polish, error messages, docs, QC | Every failure path logs with context, not silent |
| **Product** | Rethink the flow itself | Replace 3-step wizard with one-shot graph query |

**Rule:** Your 3 proposals must be on 3 different axes. If two are “faster cache” and “faster index,” one is not extreme. Make one *product* — the user will feel the difference.

**Commit:** After 3, pick one and state why it is the most insane win in one line — like `nextreme-decision` but inside the fragment.
