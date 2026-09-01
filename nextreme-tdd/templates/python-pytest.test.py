"""Tests for behavior: __behavior__ — case: __case__

One behavior per file. This template fails honestly before implementation (NameError),
then passes with the smallest production code that satisfies the assertion.

Run:
  pytest tests/test___behavior_snake__.py -q -v   # RED (should fail on behavior gap)
  pytest -q                                      # GREEN (full suite)
"""
from __future__ import annotations

# Replace the import with the real module once it exists.
# Honest RED: missing target symbol. We catch ONLY the expected missing target,
# re-raising syntax/dependency errors so they are not mistaken for a behavior gap.
try:
    from src.__behavior_snake__ import __behavior_snake__  # type: ignore[import-not-found]
except ImportError as _tdd_exc:  # noqa: N806
    _expected_target = "__behavior_snake__"
    _message = str(_tdd_exc)
    # Only normalize the expected missing-target case; re-raise anything else (syntax, dep failure, init error).
    if _tdd_exc.name not in (_expected_target, f"src.{_expected_target}", None) and _expected_target not in _message and "src." + _expected_target not in _message:
        raise
    __behavior_snake__ = None  # type: ignore[assignment]

EXPECTED_FOR_HAPPY = 42  # TODO: replace with the real expected value for __case__

def test___behavior_snake_____case_snake__() -> None:
    assert __behavior_snake__ is not None, "behavior not yet implemented — RED: symbol missing"
    result = __behavior_snake__()  # type: ignore[operator]
    assert result == EXPECTED_FOR_HAPPY
