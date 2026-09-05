/**
 * Tests for behavior: __behavior__ — case: __case__
 *
 * One behavior per describe. This template fails honestly before implementation
 * (missing target symbol / undefined), then passes with the minimal code.
 *
 * Run:
 *   npx vitest run src/__behavior_kebab__.test.ts --reporter=verbose  # RED
 *   npx vitest run --reporter=verbose                                # GREEN
 */
import { describe, it, expect } from "vitest";

// Replace with the real module path once it exists.
// Honest RED is a behavior gap in one of two shapes:
//   (a) the EXPECTED module itself is missing ("Cannot find module './<name>'"),
//   (b) the module loads but the EXPECTED export is absent.
// A loader error for any OTHER module (typo'd unrelated import) is re-thrown —
// it is a wiring mistake, not a behavior gap.
let behaviorImpl: (() => unknown) | undefined;
let _tddError: unknown;
try {
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  behaviorImpl = require("./__behavior_kebab__").__behavior_snake__;
} catch (caught) {
  _tddError = caught;
  const message = caught instanceof Error ? caught.message : String(caught);
  const expectedModule = "__behavior_kebab__";
  const expectedExport = "__behavior_snake__";
  const loaderMentionsExpected =
    (message.includes("Cannot find module") || message.includes("Cannot find package")) &&
    message.includes(expectedModule);
  const exportMissing = message.includes(expectedExport);
  const isExpectedMissing = loaderMentionsExpected || exportMissing;
  if (!isExpectedMissing) {
    throw caught;
  }
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
