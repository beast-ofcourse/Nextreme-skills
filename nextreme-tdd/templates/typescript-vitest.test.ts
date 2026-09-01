/**
 * Tests for behavior: __behavior__ — case: __case__
 *
 * One behavior per describe. This template fails honestly before implementation
 * (Cannot find module / undefined), then passes with the minimal code.
 *
 * Run:
 *   npx vitest run src/__behavior_kebab__.test.ts --reporter=verbose  # RED
 *   npx vitest run --reporter=verbose                                # GREEN
 */
import { describe, it, expect } from "vitest";

// Replace with the real module path once it exists.
// Before the file exists, Vitest reports "Cannot find module" — honest RED.
// The require fallback keeps the file loadable so the assertion fails on value, not wiring.
let behaviorImpl: (() => unknown) | undefined;
try {
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  behaviorImpl = require("./__behavior_kebab__").__behavior_snake__;
} catch {
  behaviorImpl = undefined;
}

const EXPECTED_FOR_HAPPY = 42; // TODO: replace with the real expected value for __case__

describe("__behavior__", () => {
  it("should __case_kebab__", () => {
    if (typeof behaviorImpl !== "function") {
      throw new Error("behavior not yet implemented — RED: symbol missing");
    }
    const result = behaviorImpl();
    expect(result).toEqual(EXPECTED_FOR_HAPPY);
  });
});
