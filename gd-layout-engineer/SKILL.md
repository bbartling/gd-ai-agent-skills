---
name: gd-layout-engineer
description: Design or refactor playable Geometry Dash layouts with mode-aware spacing, readable transitions, musical pacing, and evidence-based difficulty progression.
---

# GD Layout Engineer

Build collision gameplay before decoration. Request or infer a target difficulty range, song/offset, classic versus platformer, intended refresh/input assumptions, allowed game modes, and desired length. Record assumptions if unavailable.

Read `../shared/references/anti-slop-readiness.md` and `difficulty-calibration.md` before claiming a layout is ready or assigning a demon tier.

## Section method

For every 4–16 second phrase, complete the section card in `../shared/templates/section-card.md`: mode, speed, gravity, size, camera behavior, entry state, exact input vocabulary, intended rhythm, safe corridor, fail states, transition cue, and exit state. Use teach → develop → combine → release. Reuse a mechanic enough for learning while changing one variable at a time.

## Spacing method

Do not select gaps from a universal table. Effective difficulty depends on speed, gravity, size, slope/orb/pad state, entry velocity, hold duration, previous input, camera, and visibility. Begin with conservative spacing, test the full approach, then tighten one variable at a time. Maintain setup distance after portals and speed changes. Never judge a jump from an isolated screenshot.

Every pad, orb, portal, and speed change needs an **approach → activation → exit → recovery** trace. Test early/late/high/low/held/released entries that are plausible from the preceding gameplay. A sequence is not valid merely because a perfectly placed start position can survive it.

Read `../shared/references/layout-spacing.md`, `difficulty-game-modes.md`, and `music-section-design.md`. Use the checklists rather than copying corpus coordinates: the corpus mixes art objects, trigger workspaces, and playable objects, so global x/y statistics are not collision geometry.

## Acceptance gate

- Every transition is survivable without foreknowledge or has a deliberate, clearly telegraphed learning purpose appropriate to the target difficulty.
- Hitboxes and intended path remain readable with effects enabled.
- No accidental auto sections, dead clicks, blind entries, or single-frame-looking choke points unless explicitly targeted and independently verified.
- Difficulty spikes are identified by section; the hardest section does not exceed the target band without user approval.
- The entire layout is cleared in normal mode, not only with start positions.
- The measured hardest sections arise from intended mechanics, not accidental blind entrances, inconsistent decoration, or broken pad/portal exits.
- A requested demon tier has sustained, mode-appropriate execution or learning demands; a few spikes added to basic cube jumps do not qualify.
