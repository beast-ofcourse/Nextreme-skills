---
name: tdd-coach
description: "Deprecated alias for nextreme-tdd — forwards to the extreme red-green-refactor engine. Use nextreme-tdd for TDD, test-first, red-green-refactor, failing-test-first, or characterization-test tasks."
license: MIT
---

# TDD Coach — Deprecated Alias

This skill is **deprecated**. Use [`nextreme-tdd`](../nextreme-tdd/) instead.

`nextreme-tdd` is the extreme successor to `tdd-coach`: it keeps the same RED → GREEN → REFACTOR rhythm but adds framework auto-detection (`pytest`/`Vitest`/`Jest`/`go test`/`cargo test`), failing-test scaffolding (`scaffold_test.py`), order-enforced verification (`verify_tdd.py --strict`), and 4 starter templates.

**Migration:** Replace skill reference `tdd-coach` with `nextreme-tdd`. All trigger phrases (`TDD this`, `red-green-refactor`, `write test before code`, `failing test first`, `characterization test`) now route to `nextreme-tdd`.

> Compatibility shim — this file exists so `npx skills add beast-ofcourse/Nextreme-skills --skill tdd-coach` and existing docs linking to `tdd-coach/` continue to resolve. It will be removed in a future major version.
