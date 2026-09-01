"""Tests for behavior: __behavior__ — case: __case__

One behavior per file. This template fails honestly before implementation (NameError),
then passes with the smallest production code that satisfies the assertion.

Run:
  pytest tests/test___behavior_snake__.py -q -v   # RED (should fail on behavior gap)
  pytest -q                                      # GREEN (full suite)
"""
from __future__ import annotations

# Replace the import with the real module once it exists.
# The import itself is the RED mechanism: before the symbol exists, this test fails
# with ModuleNotFoundError/ImportError — an honest behavior gap, not a typo.
try:
    from src.__behavior_snake__ import __behavior_snake__  # type: ignore[import-not-found]
except ImportError:
    # Fallback so the file still loads and the *assertion* fails, not the import.
    # The test will fail at call time with NameError — also an honest RED.
    __behavior_snake__ = None  # type: ignore[assignment]

EXPECTED_FOR_HAPPY = 42  # TODO: replace with the real expected value for __case__

def test___behavior_snake_____case_snake__() -> None:
    assert __behavior_snake__ is not None, "behavior not yet implemented — RED: symbol missing"
    result = __behavior_snake__()  # type: ignore[operator]
    assert result == EXPECTED_FOR_HAPPY
