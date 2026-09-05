"""Tests for behavior: __behavior__ — case: __case__

One behavior per file. This template fails honestly before implementation (NameError),
then passes with the smallest production code that satisfies the assertion.

Run:
  python -m pytest tests/test___behavior_snake__.py -q -v   # RED (should fail on behavior gap)
  python -m pytest -q                                      # GREEN (full suite)
"""
from __future__ import annotations

# Replace the import with the real module once it exists.
# Honest RED: behavior gap, in any of its three shapes —
#   (a) missing module or parent package ("No module named 'src.pricing'" / "'src'"),
#   (b) present module but missing symbol ("cannot import name 'calculate_tax'"),
#   (c) present symbol with wrong value (assertion diff below).
# Re-raise everything else (typos in unrelated names, syntax, dependency failures)
# so wiring mistakes are never mistaken for a behavior gap.
try:
    from src.__behavior_snake__ import __behavior_snake__  # type: ignore[import-not-found]
except ImportError as _tdd_exc:  # noqa: N806
    _attempted_module = "src.__behavior_snake__"
    _expected_target = "__behavior_snake__"
    _message = str(_tdd_exc)
    _missing = _tdd_exc.name or ""
    _honest_missing_module = (
        "No module named" in _message
        and (_missing == _attempted_module or _attempted_module.startswith(_missing + "."))
    )
    _honest_missing_symbol = (
        "cannot import name" in _message and f"'{_expected_target}'" in _message
    )
    if not (_honest_missing_module or _honest_missing_symbol):
        raise
    __behavior_snake__ = None  # type: ignore[assignment]

EXPECTED_FOR_HAPPY = 42  # TODO: replace with the real expected value for __case__

def test___behavior_snake_____case_snake__() -> None:
    assert __behavior_snake__ is not None, "behavior not yet implemented — RED: symbol missing"
    result = __behavior_snake__()  # type: ignore[operator]
    assert result == EXPECTED_FOR_HAPPY
