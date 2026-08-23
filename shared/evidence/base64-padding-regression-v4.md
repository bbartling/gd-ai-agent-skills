# Base64 padding regression — Cheese Moon V4 gate

## Observed failure

The old encoder called `rstrip("=")` on `k4`. The old decoder then calculated and added missing padding before decoding, so it accepted files that Geometry Dash rejected as blank levels.

| Evidence set | Files | `len(k4) % 4` | Gate result |
|---|---:|---:|---|
| Supplied working exports | 13 | `0` for all | Pass |
| Cheese Moon V1–V3 | 3 | `3` for all | Fail: required padding stripped |
| One-block/three-spike canary | 1 | `0`, ending `==` | Pass; imported and opened in Geometry Dash |
| Cheese Moon V4 | 1 | `0`, ending `=` | Pass; user confirmed the complete level parses in Geometry Dash |

The 13 working files comprise the 11 uploaded famous/gameplay references, `OneBlockTest.gmd`, and `rocket power.gmd`. The corpus is not redistributed; the regression suite records hashes and derived results only.

## Red/green contract

Red behavior:

- encoder removes terminal padding;
- validator repairs missing padding silently;
- broken V1–V3 are incorrectly accepted.

Green behavior:

- encoder keeps canonical RFC 4648 padding;
- validator checks the serialized value before decoding;
- any `k4` length not divisible by four is fatal;
- misplaced/excess padding and non-URL-safe characters are fatal;
- known-good files must pass;
- known-bad files must fail for the expected padding reason;
- a new candidate must pass the complete template, payload, count, header, and source-prefix release gate.

The GitHub workflow runs the synthetic unit tests on every push and pull request. Run `run_gmd_regression_gate.py` locally with the permission-safe external corpus to exercise the full 13-good/3-bad matrix.

The V4 confirmation closes the blank-level regression: the same 46,605-object decoded content rejected in V3 was accepted after restoring its single required terminal `=`. Gameplay, trigger behavior, performance, and difficulty still require separate in-game testing.
