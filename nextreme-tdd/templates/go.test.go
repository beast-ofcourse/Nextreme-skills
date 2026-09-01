// Tests for behavior: __behavior__ — case: __case__
//
// One behavior per Test function. Table-driven within the behavior is fine.
// This template fails honestly before implementation (undefined symbol).
//
// Run:
//   go test -run Test__behavior_pascal__ -count=1 ./...  # RED (fails on undefined)
//   go test ./...                                         # GREEN (full suite)
package __package_name__

import "testing"

// TODO: replace with the real function signature for __behavior__.
// Before the function exists, `go test` fails to compile with "undefined: __behavior_snake__" — honest RED.
// Keeping the test compile-fail is the desired RED; comment the stub below before GREEN.
// func __behavior_snake__() int { return 0 }

func Test__behavior_pascal_____case_snake__(t *testing.T) {
	// RED gate: if the symbol is still missing, the file won't compile — that's the honest RED.
	// After GREEN, this assertion proves the happy path value.
	const want = 42 // TODO: replace with the real expected value for __case__
	got := __behavior_snake__()
	if got != want {
		t.Fatalf("behavior __behavior__ case __case__: got %v want %v", got, want)
	}
}
