# Test Patterns — Behavior First

Every TDD cycle pins **one behavior**. A behavior is a verb phrase the client can observe:
`calculate_tax_rounds_half_up`, `parse_amount_rejects_overflow`, `route_retries_on_timeout`.

## Behavior Contract

Write before RED:

```text
Behavior: When <client> <action> with <input>, <unit> shall <outcome>.
Inputs:   <typed inputs + constraints>
Outputs:  <typed outputs + errors>
Invariants: <must hold for all cases, e.g., "rounded value is multiple of 0.01">
Not in this cycle: <what you park>
```

One sentence + inputs/outputs/invariants. If you need "and" to describe the behavior, it's two behaviors — split.

## Leading Word: behavior

Repeat **behavior** as the token for every decision: which behavior, what case of that behavior, what asserts that behavior. Don't coin synonyms (`scenario`, `feature-under-test`). The repetition focuses the run.

## Edge Palette — What Cases Does This Behavior Earn?

Pick what the behavior earns, not a generic checklist. Four buckets:

| Bucket | When it earns it | Example |
|---|---|---|
| **Happy** | Always — the canonical path | `amount=10.015 → 10.02` |
| **Edge** | Domain has boundaries (limits, empty, off-by-one) | `amount=0`, `amount=max_cents+1`, `empty list` |
| **Error** | Contract rejects or fails | `amount="abc" → ValueError`, `timeout → retry` |
| **Invariant** | Property that must hold across inputs | `round(x) % 0.01 == 0`, `parse(format(x)) == x` |

First cycle → one **happy** RED. Next cycles → one edge/error/invariant at a time. Never batch three buckets into one test file's first RED — that's a cannonball, not a tracer bullet.

## Example vs Property

- **Example** (default, 90%): one input → one output assertion. Choose when behavior is a known mapping. Template: `assert result == expected`.
- **Property / Invariant** (when behavior generalizes): holds for many inputs (e.g., fuzz, property-based). Use `hypothesis` (Python), `fast-check` (TS), `quickcheck` (Rust). Keep the property small; one invariant per test.

## Naming Truthfully

Name reveals the behavior and the case:

- Good: `test_calculate_tax_rounds_half_up`, `it("should round half up when amount ends in .015")`, `TestParseAmount_RejectsOverflow`
- Bad: `test1`, `test_tax`, `handler` — slop, rejected

Function name tells a reader what broke when it fails. If the name doesn't mention the case, it's vague.

## One Behavior Per Test Unit

- Python/`pytest`: one `def test_<behavior>_<case>` per case; optional `class Test<Behavior>` groups the palette.
- TypeScript/`vitest`: one `describe("<behavior>")` per behavior, one `it("should <case>")` per palette entry.
- Go: one `func Test<Behavior>(t *testing.T)` with `t.Run("<case>", …)` table — table is fine, but one behavior per `Test` function, not three behaviors in one table.
- Rust: one `#[test] fn <behavior>_<case>()` per case; helpers are extracted, not copied.

Third occurrence of same helper → extract. Two is coincidence.

## Assertions That Prove Behavior

Assert **value**, not existence:

- Python: `assert result == 42`, not `assert result`
- TypeScript: `expect(result).toEqual(42)`, not `toBeTruthy()`
- Go: `if got != want { t.Fatalf(...) }`, not `if got == nil`
- Rust: `assert_eq!(result, 42)`

At untyped boundaries (`JSON.parse`, API response), narrow `unknown` explicitly — parse + validate, then assert the narrowed type. A silent `as` is the same violation as `any`.

## Characterization Tests (Order Inverted)

If production code already exists before you arrived, don't delete it to force RED. Pin its **observable** behavior and write a characterization test that captures the current output. Run → GREEN (it already passes) → then write the *next* behavior's RED. Document the assumption: "characterization of existing `<unit>` — not a fresh behavior."
