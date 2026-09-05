# Review Report — <target / branch>

Verdict: **ship** / **fix-first** / **blocked**

Scope: <branch vs base, or file list>
Intent: <one-line what the change claims to do>

## Findings

### Critical (blocks merge)

- [ ] `<file>:<line>` — <what breaks, blast radius>. Evidence: `<command output / quoted behaviour>`.

### Major

- [ ] `<file>:<line>` — <likely bug under real conditions>. Evidence: `<...>` .

### Minor

- [ ] `<file>:<line>` — <readability / naming / duplication>. Evidence: `<...>` .

## Unverified

- <PLAUSIBLE-but-unobserved area and the exact observation that would settle it — never blocks>

## Verification log (provenance — a gate without this is an assumption)

| Command | Exit | At |
|---|---|---|
| `<exact command>` | `<code>` | `<timestamp>` |

## Handoff prompt (copy-paste to fixing agent)

> Fix the findings in `review-report.md` in order — Criticals, then Majors, then Minors; touch nothing outside the findings.
> Target: `<branch vs base / file list>`.
> Per fix, quote the verification command and its exit code.
> Re-run the full suite on the final tree and report green before handing back for re-review.
