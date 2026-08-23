# High-impact animation cookbook

Use recipes as architectures. Derive timing, palette, geometry, and motif from the current song and theme; do not copy identifiable reference art.

## 1. Three-plane living background

Create far, mid, and near groups with different motion amplitudes and periods. Far motion is slow/subtle, mid motion follows phrases, and near framing reacts more sharply at transitions. Use shared color channels and limited motifs. Keep the player corridor higher contrast than all three planes. Stop or retarget the rig at section boundaries.

## 2. Beat-propagation wave

Divide a repeated structure into sequential groups. A root spawn activates short pulse/scale/move envelopes with small song-derived delays, producing travel across the scene. Define a loop period aligned to a beat/measure, plus stop/reset. Do not copy the corpus median delay blindly; calculate from BPM/subdivision.

## 3. Mechanical assembly

Build modular pistons, gears, panels, or jaws. Assign moving members, rotation centers, controller groups, and collision policy. Use anticipation, impact, recoil, and settle. Sync the impact to a strong accent; use shake sparingly. Decorative motion must not falsely imply a changing hitbox.

## 4. Character or creature performance

Use a parent hierarchy and keyframe poses for anticipation, primary action, overshoot, settle, idle, and exit. Isolate facial/details into optional high-detail groups. Provide reset pose and checkpoint behavior. Reserve keyframes for coordinated posing; do not use hundreds where one transform rig is clearer.

## 5. Palette and lighting transition

Prepare coordinated background/ground/object/glow channels. Begin anticipation before the phrase change, land the dominant change on the downbeat, then add short pulses for emphasis. Avoid full-screen flashes that hide the first input of the new section. Restore or hand off channels explicitly.

## 6. Portal transformation set piece

Telegraph a mode change with a visual funnel, camera framing, motif morph, and clean exit lane. The animation may build anticipation but cannot cover the portal or first required action. Test the transition from real approach extremes and with input held/released.

## 7. Destruction/reveal moment

Group fragments or panels, hide the revealed asset initially, then coordinate move/rotate/scale/alpha and a restrained camera accent. Use staggered timings, not a simultaneous object explosion. Stop offscreen controllers and keep fragments out of gameplay readability/collision unless intentional.

## 8. Boss or hero scene

Give the subject readable poses/states and a limited attack language. Tie state changes to phrases and gameplay responses. Separate spectacle from collision telegraphs. Track state with explicit groups/items and reset on death/checkpoint. A boss is not a pile of random moving hazards.

## 9. Ambient micro-motion

Use low-amplitude drift, bob, rotation, particles, or gradient movement to prevent static backgrounds. Periods should differ enough to avoid mechanical lockstep but remain controlled. This layer must be cheap, stoppable, and removable by LDM.

## 10. Camera punctuation

Use brief zoom/offset/rotation/shake around landings, impacts, reveals, and phrase transitions. Establish a neutral camera state and return to it. Never stack camera changes without knowing interpolation order and cleanup. If motion makes the route harder to see, reduce it before weakening gameplay.

## Composition checklist

For each major section, choose only what the song/theme needs:

- One ambient system.
- One recurring beat-accent system.
- One entry/exit transition.
- One gameplay-cue language.
- Optional hero moment at a meaningful peak.

Vary amplitude and density with musical intensity. Constant maximum motion destroys emphasis.

## Animation quality test

- Watch runtime once while ignoring gameplay: is motion composed, rhythmic, and layered?
- Watch again focusing only on the icon/path: are all inputs readable?
- Restart/die/practice through the rig: does every state reset?
- Enable LDM: is the scene still coherent and playable?
- Disable music temporarily: does motion still have intentional envelopes rather than jitter?
