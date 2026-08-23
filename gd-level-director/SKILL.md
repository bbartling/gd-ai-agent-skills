---
name: gd-level-director
description: Plan and coordinate a complete Geometry Dash level or major refactor from a GDShare file, balancing gameplay, difficulty, visuals, animation, music sync, performance, and validation.
---

# GD Level Director

Deliver a playable level, not an object-count demo. Treat gameplay, readability, art, motion, sync, and performance as independent tracks with explicit gates.

## Mandatory anti-slop contract

Before planning or editing, read `../shared/references/anti-slop-readiness.md`. Its critical gates override aesthetic ambition. Never equate “the `.gmd` imports” with “the level is ready.” When in-game verification is unavailable, label the output **candidate build requiring GD import and playtest**.

A supposed demon with trivial inputs fails even if it looks polished. A dense animation showcase fails as a game if its collision path is broken. A working graybox fails presentation if the background is static filler and effects ignore the song. Satisfy all three axes—gameplay, difficulty, presentation—then validate their interaction.

## Required workflow

1. Preserve the input. Never overwrite the only `.gmd` copy. Decode and profile it with `../shared/scripts/analyze_gmd.py`; run `validate_gmd.py` before edits. For an extension, define the preserved source range, the handoff point, and which existing systems may be touched.
2. Write a section contract: time/measure range, game mode, speed, gravity, size, core mechanic, target difficulty, intensity, visual motif, foreground hazard layer, and transition.
3. Build or repair the collision layout first. Use `gd-layout-engineer` and read `../shared/references/layout-spacing.md`, `difficulty-game-modes.md`, and `difficulty-calibration.md`.
4. Require complete start-to-finish playability in an undecorated copy. Decoration may not conceal hitboxes or substitute for gameplay.
5. Create a group/layer/color-channel budget before animation. Use `gd-animation-engineer` and read `animation-systems.md` and `layering-performance.md`. Any multipart character, boss, vehicle, or destination needs an explicit parent/child hierarchy ledger before triggers are emitted.
6. Before scaling procedural density, create a small import canary from the exact target-version template. Import, open, save, and re-export it in Geometry Dash. If GD access is unavailable, keep the full build conservative: unchanged header, exact source prefix where applicable, donor-derived fields, enumerated Z layers, and object count below the chosen compatibility ceiling.
7. Decorate and animate one representative section to the presentation contract in `animation-cookbook.md`; validate readability and performance, then propagate the system. Avoid hand-authoring thousands of unique objects when a repeated module or owned trigger rig works.
8. Run structural validation, compatibility audit, before/after comparison, editor inspection, practice runs, normal-mode runs, and fresh-player testing. Use `gd-level-qa`.
9. Complete `../shared/templates/release-scorecard.md`. Export a new `.gmd`, retain a build report, and state what was actually tested. Never call static analysis a physics verification.

## Decision rules

- Difficulty comes from decision windows, safe corridor width, input density, mode transitions, visibility, speed, and consistency—not decoration count.
- Copy the principles of references, not their exact art, structures, or sequences.
- One section should teach a mechanic, develop it, combine it, then release tension. Do not introduce unrelated gimmicks every few seconds.
- Sync major gameplay changes and visual accents to a beat map. Avoid placing by x-coordinate alone when speed changes exist.
- Maintain a clean hitbox/readability layer above atmospheric art. Effects must support player timing.
- Prefer a small number of understandable animation rigs over thousands of unowned groups.
- Any generated result remains a candidate until imported and playtested in Geometry Dash.
- Never use a difficulty label as evidence. Name the mode-specific skill demand and report actual clear/death data.
- Never bulk-decorate a whole level before one full-quality section passes gameplay visibility, runtime motion, and performance checks.
- Never hide uncertainty behind object counts, trigger counts, or words such as “extreme,” “epic,” “professional,” or “fully validated.”
- If the user requests a target file size, treat it as a packaging budget—not a quality metric. Finish gameplay, art, and animation first; tune only optional high-detail density afterward.
- A finale must complete the dramatic promise: readable arrival, viewport-scale destination or payoff, controlled reveal, recovery space, and a clear finish. A tiny prop plus text is not a destination scene.
- If GD opens the candidate as a plain or empty level, stop all art/difficulty work. Treat it as rejection of the serialized level string, return to the last importable baseline, and bisect header changes, property enums, object systems, and density with import canaries.

## Routing

- File internals, lossless round trips, metadata, numeric properties: `gd-geoshare-engineer`.
- Spacing, click patterns, transitions, game-mode difficulty: `gd-layout-engineer`.
- Groups, pulses, movement, spawn loops, keyframes, cameras: `gd-animation-engineer`.
- Structural checks, playtest matrix, performance and regression: `gd-level-qa`.

Read `../shared/references/corpus-findings.md` before using the supplied corpus as evidence, `generation-workflow.md` before making a large refactor, and `large-level-production.md` for procedural extensions, boss systems, major destination reveals, or byte-size targets.
