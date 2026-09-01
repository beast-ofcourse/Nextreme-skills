# Templates — nextreme-tdd

Copy via `scaffold_test.py`; do not start from zero. Each template is runnable and fails honestly before implementation.

| Need | Template | Destination (via scaffold) |
|---|---|---|
| Python | `python-pytest.test.py` | `tests/test_<behavior>.py` |
| TypeScript / JS (Vitest/Jest) | `typescript-vitest.test.ts` | `src/<behavior>.test.ts` |
| Go | `go.test.go` | `./<behavior>_test.go` or `<pkg>/*_test.go` |
| Rust | `rust.test.rs` | `tests/test_<behavior>.rs` or inline `#[cfg(test)]` |

Usage:

```bash
python nextreme-tdd/scripts/scaffold_test.py --behavior calculate_tax_rounds_half_up --case happy_path
# → writes the templated file, then:
pytest tests/test_calculate_tax_rounds_half_up.py -q -v   # RED
pytest -q                                                 # GREEN after you write the minimal impl
```

Each file is one behavior, one tracer bullet. Third helper copy → extract.
