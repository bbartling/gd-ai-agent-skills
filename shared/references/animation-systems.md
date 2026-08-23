# Animation and trigger systems

## Rig contract

Before placing triggers, define a rig in a ledger:

| Field | Example |
|---|---|
| Rig | Section 03 piston |
| Visible groups | 320–326 |
| Center/parent groups | 327–329 |
| Controller groups | 330–334 |
| Color channels | 42–44 |
| Editor layers | 30–32 |
| Entry | x-trigger or spawn group 330 |
| Exit/reset | stop 333, reset pose 334 |
| Period | one beat |
| LDM | remove particles and secondary glow |

Use disjoint ranges by section and function. Keep controller triggers on dedicated editor layers and usually out of the visible path.

## Effect envelopes

Motion should have an envelope: anticipation → main action → settle. A beat pulse should have deliberate fade-in, hold, and fade-out. Camera shake should start and end around a specific impact. Repeated background motion should have a period tied to beats or measures. Random unbounded motion reads as noise.

## Spawn chains and loops

Make a root trigger that starts the rig. Spawn-triggered children should be grouped by phase. For loops, include a deliberate delayed return to the root/body and a stop/reset path when the section ends. Audit for zero-delay recursion and cross-section group collisions. Death, checkpoint, practice, and replay must reinitialize state.

## Transform rigs

- Move: group the moving assembly and keep collision behavior intentional. Decorative motion should not imply moving collision unless it is real.
- Rotate: use a dedicated center group and verify center placement. Nested rotations need explicit parent ownership.
- Scale: verify center, X/Y behavior, and collision implications. Avoid sudden scaling under the player unless designed and tested.
- Follow: distinguish target member group from followed/parent group.

### Assembly membership invariant

A visible child is not automatically moved by a conceptual parent. If a boss body is group 600 and an eye is locally controlled by 601, the eye should normally carry membership `600.601`. The body move targets 600; eye blinks or offsets target 601. Apply the same rule to jaws, crowns, weapons, wheels, windows, moon holes, orbiters, and other parts that need whole-assembly plus local motion. Verify membership on serialized objects and check that no controller-only group was accidentally placed on visible art.

For x-triggered ambient motion without a tested spawn loop, use paired excursions: baseline → offset → baseline. Pair alpha twinkles with restoration, and return camera zoom/offset/rotation to the intended section state at every handoff.

The Abducted corpus profile is transform-heavy; its architecture supports studying how move/rotate/scale are combined. Its extreme move maxima are not reusable defaults.

## Keyframe rigs

Use keyframes for character or scene poses that change multiple transforms together. Define a parent hierarchy, keyframe IDs/index order, duration/easing, loop closure, and reset pose. Preview art and controller nodes should remain isolated from collision objects. Skeletal Shenanigans contains 2,201 recognized keyframes and is the clearest supplied evidence for this style.

## Pulse, alpha, color, gradient

- Pulse supplies momentary accent; reserve long/persistent values for deliberate state.
- Alpha fades visibility; zero duration is an intentional cut. Ensure the target can later be restored.
- Toggle changes activation and can affect trigger systems; use it when a fade is not enough.
- Color channels make palettes maintainable. Avoid unique channel-per-object growth.
- Gradients can replace huge stacks of flat decoration, but audit layer, corner groups, and high-detail fallback.

Slaughterhouse is pulse-dominant; MOAI combines pulse and gradient heavily. Use each as a different pattern, not a reason to stack both everywhere.

## Camera and shader discipline

Camera zoom/rotation/offset/static effects should emphasize phrases and transitions. Test player path visibility during interpolation and on mobile aspect ratios where relevant. Shaders must have an exit/reset and cannot obscure the hazard silhouette. Strong effects belong around impacts, not across every input.

## Animation QA

Test from zero, a start position immediately before the rig, a checkpoint inside the rig, death during each phase, replay, and low-detail mode. Watch for stale opacity, displaced reset pose, duplicate loop starts, stop triggers missing controllers, and camera state leaking into the next section.
