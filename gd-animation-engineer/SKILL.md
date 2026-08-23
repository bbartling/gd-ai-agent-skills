---
name: gd-animation-engineer
description: Build maintainable Geometry Dash visual and animation systems using groups, layers, pulses, movement, spawn chains, cameras, gradients, and keyframes without harming gameplay readability.
---

# GD Animation Engineer

Design animation as rigs with ownership. Each rig needs: purpose, member groups, controller triggers, lifecycle, reset behavior, Z/editor layers, color channels, high-detail fallback, and a test start position.

For multipart assemblies, every child that must follow whole-body motion must belong to both the assembly parent group and its child-control group. Parent membership provides translation; the child group provides local motion such as eyes, jaw, cannon, orbit, or hit reaction. Audit the serialized memberships—not just the ledger—before packaging.

Read `../shared/references/anti-slop-readiness.md` and `animation-cookbook.md`. “Cool animation” means composed foreground/midground/background motion, beat-aware accents, controlled transitions, and one or more memorable set pieces—not random move triggers or a permanently shaking camera.

## Choose the simplest mechanism

- Pulse/color: beat accents and palette changes.
- Alpha/toggle: reveal, hide, state changes; alpha for fades, toggle for true activation changes.
- Move/rotate/scale: simple transforms; name a center group for rotation/scale.
- Spawn: timed orchestration and loops; define entry, body, delay, exit, and stop/reset.
- Follow/advanced follow: parented or simulated relationships.
- Keyframes: coordinated multi-property character/scene animation. Use when many transforms form a pose sequence, not for a single bob.
- Camera/shader: punctuation, never constant noise. Maintain hazard readability and motion comfort.

Read `../shared/references/animation-systems.md`, `layering-performance.md`, and `object-trigger-fields.md`.

## Presentation contract per major section

- One coherent visual motif with modular structures, not copied filler.
- At least three perceptible depth roles when the style supports them: foreground framing, midground subject/structure, and background atmosphere/parallax.
- A restrained ambient motion system, beat/sub-beat accents selected from the song map, and a deliberate entry/exit transition.
- Gameplay cues that remain more legible than decorative motion.
- A hero moment or recognizable animated idea at important musical peaks; do not demand a set piece every phrase.
- Reset/stop/LDM behavior for every expensive or stateful rig.

## Required controls

- Allocate group ranges by section and function; keep a ledger.
- Separate collision, gameplay cues, foreground, midground, background, UI, controllers, and test helpers.
- Make loop periods intentional and stop loops when their section ends.
- Avoid zero-delay recursive spawn cycles.
- Avoid huge offscreen moves as a default hiding mechanism; prefer alpha/toggle unless the move is intentional.
- For repeated drift or recoil, pair every displacement with a return to the authored baseline unless persistent displacement is deliberate. Otherwise x-triggered repeats accumulate and detach the scene over time.
- Add low-detail behavior for expensive particle, gradient, shader, and dense-art systems.
- Test effects off and on. If the route becomes unclear only when art is enabled, the art fails.
- Inspect runtime motion, not just a static editor viewport. A beautiful still frame with lifeless play mode fails animation QA.

Corpus evidence shows several distinct animation styles: transform-heavy rigs, pulse-heavy atmospheres, and keyframe-heavy character work. Do not force all three into every level.

Read `../shared/references/large-level-production.md` when building a boss, multipart hero prop, asteroid/debris field, or animated destination reveal. Use `../shared/templates/rig-hierarchy-ledger.csv` to make parent and local-control ownership explicit.
