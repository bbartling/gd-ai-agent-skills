# Validation and playtesting matrix

## Static file gates

- Outer XML parses and contains `k4`.
- Wrapper bytes match the proven target-version template: exact declaration, no BOM/newlines, unchanged key/tag order, unchanged unknown metadata, and no accidental online ID.
- `k4` Base64/gzip decodes.
- Inner header remains present.
- Every object has even key/value fields and an ID.
- Coordinates are finite.
- Declared and decoded object counts are reconciled.
- Key-24 Z-layer values are valid target-version enums rather than arbitrary depth numbers.
- Target groups without key-57 members are traced; they can be intentional controller groups.
- Before/after changes match the intended scope.
- Multipart assemblies have verified parent plus local-control membership; no child detaches when the parent moves.
- A same-value raw splice is byte-identical, and payload encode/decode is semantically lossless.

## Editor gates

- Import under a new name; original remains available.
- Level opens without crash/error.
- Beginning/end and each section render.
- Collision objects, portals, start positions, hidden helpers, editor layers, and Z ordering are present.
- GD can save and re-export the level.
- The editor contains the expected source and added objects; a created My Levels entry with a plain/empty editor is a failed import.

A static coordinate render may be used before import to inspect composition, density, whitespace, silhouettes, and section scale. Call it a spatial composition preview. It cannot verify opacity state, trigger order, camera interpolation, collision, song sync, or the runtime frame.

## Trigger gates

For every rig: starts once when intended, supports required multi-activation, stops, resets on death/restart, works from zero and nearby start positions, behaves in practice/checkpoints, does not leak camera/opacity/movement state, and degrades correctly in LDM.

## Gameplay gates

- Run every section from multiple entries.
- Run all portal/speed/size/gravity/dual transitions while entering high/low and holding/not holding.
- Complete practice and normal mode from zero.
- Record deaths by section and cause: execution, unreadable, transition, collision surprise, desync, frame drop.
- Test intended refresh/input conditions; note if only one setup was tested.
- Have a fresh player assess route clarity and difficulty consistency.

## Visual/performance gates

- Icon and hitboxes remain readable through flashes, camera moves, shaders, particles, and foreground art.
- Dense and trigger-burst sections meet runtime expectations on target hardware.
- LDM removes expense without removing gameplay information.
- No persistent flashes, uncontrolled loops, duplicate audio, or visual state after restart.
- The finale remains legible after the last hazard and delivers the promised destination/payoff at gameplay scale, not just in an editor overview.

## Release language

Allowed claims should match evidence: “structurally validated,” “imports and opens,” “section-tested,” “full practice clear,” “normal-mode clear,” or “verified by named tester/settings.” Never collapse these into “fully validated” without all relevant gates.
