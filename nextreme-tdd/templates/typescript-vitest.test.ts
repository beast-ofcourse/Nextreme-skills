/**
 * Tests for behavior: __behavior__ — case: __case__
 *
 * One behavior per describe. This template fails honestly before implementation:
 * missing module → "Failed to resolve import" collection error;
 * missing export → "does not provide an export named" SyntaxError.
 * Both are behavior gaps, not wiring mistakes — wiring mistakes fail differently
 * (see references/validation.md). Then it passes with the minimal code.
 *
 * Run:
 *   npx vitest run src/__behavior_kebab__.test.ts --reporter=verbose  # RED
 *   npx vitest run --reporter=verbose                                # GREEN
 */
import { describe, it, expect } from "vitest";

// Static import on purpose: a missing module/export fails collection loudly,
// which IS the honest RED. No require() guard — vitest SSR require() cannot
// resolve extensionless .ts paths, so a require-based test could never go green.
import { __behavior_snake__ } from "./__behavior_kebab__";

const EXPECTED_FOR_HAPPY = 42; // TODO: replace with the real expected value for __case__

describe("__behavior__", () => {
  it("should __case_kebab__", () => {
    const result = __behavior_snake__();
    expect(result).toEqual(EXPECTED_FOR_HAPPY);
  });
});
