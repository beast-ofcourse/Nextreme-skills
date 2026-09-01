//! Tests for behavior: __behavior__ — case: __case__
//!
//! One behavior per file/module. This template fails honestly before implementation
//! (unresolved import / wrong value), then passes with the minimal code.
//!
//! Run:
//!   cargo test __behavior_snake__ -- --nocapture  # RED
//!   cargo test                                    # GREEN

// Before the function exists, `cargo test` fails to compile with "cannot find function" — honest RED.
// Comment the stub below before GREEN; the assertion's value diff is the second honest RED.
// fn __behavior_snake__() -> i32 { 0 }

const EXPECTED_FOR_HAPPY: i32 = 42; // TODO: replace with the real expected value for __case__

#[test]
fn __behavior_snake_____case_snake__() {
    let result = __behavior_snake__();
    assert_eq!(result, EXPECTED_FOR_HAPPY, "behavior __behavior__ case __case__ failed");
}
