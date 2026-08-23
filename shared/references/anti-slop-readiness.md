# Anti-slop readiness contract

This contract exists because AI-generated GDShare files often import successfully while still being poor Geometry Dash levels: broken or trivial layouts, bad block spacing, arbitrary difficulty labels, pad/portal sequences that only work from a perfect start position, static or noisy visuals, and triggers unrelated to the song.

## The word “ready” is gated

A `.gmd` may be called **ready** only when every critical gate below has direct evidence. Otherwise call it a **candidate**, **graybox**, **visual prototype**, or **structurally valid build**.

### Gate A — Artifact integrity

- A new file imports, opens, saves, and re-exports through the target GD/GDShare version.
- The original remains intact.
- Expected objects, metadata, song/offset, and section endpoints survive the round trip.

Static validation alone passes only this gate's precheck.

### Gate B — Complete gameplay spine

- Collision geometry exists continuously from start to finish.
- All pads, orbs, portals, speed/gravity/size changes, teleports, and dual transitions are tested from their real preceding approach.
- The route has no accidental auto stretches, dead clicks, blind forced inputs, impossible exits, empty filler, or unintentional skips.
- The undecorated layout has been cleared from zero in normal mode.

### Gate C — Difficulty honesty

- The builder names the actual skills being tested by section and game mode.
- Challenge is sustained at the target band rather than created by one accidental choke point.
- Start-position practice and full-run results are recorded.
- A demon label requires in-game evidence and appropriate execution/learning demands. Spikes, speed, visual clutter, and object count do not prove hardness.

### Gate D — Song and pacing

- Song identity and offset are confirmed.
- A timestamp/measure section map exists.
- Inputs, transitions, palette changes, and major effects serve phrase/beat structure.
- Sync is checked from zero through every speed/time change; local start-position sync is insufficient.

### Gate E — Finished presentation

- Structures use a coherent modular visual language rather than sparse blocks or pasted noise.
- Gameplay remains readable above decoration.
- Important sections have depth, ambient motion, beat accents, transitions, and selectively memorable hero moments appropriate to the style.
- Runtime animation—not only static editor appearance—has been inspected.

### Gate F — Trigger lifecycle and performance

- Every stateful rig has entry, body, stop, reset, death/restart, checkpoint/practice, and LDM behavior where relevant.
- No zero-delay recursion, duplicate loop start, state leakage, stuck opacity, runaway camera, or uncontrolled audio.
- Dense and burst sections run acceptably on stated target hardware/settings.

### Gate G — Human play evidence

- Full practice clear and normal-mode clear status are reported honestly.
- A fresh player appropriate to the target difficulty has assessed route readability and difficulty consistency.
- Remaining uncertainties are named; a numeric score never overrides a critical gate.

## Required iteration loop

Use this loop per section before copying its pattern:

1. **Specify:** complete entry state, mechanic, intended input rhythm, difficulty cause, exit state, visual role, and song landmark.
2. **Graybox:** build only collision/gameplay objects and minimal cues.
3. **Play:** test from real preceding gameplay; record death causes.
4. **Calibrate:** change one spacing/timing/state variable at a time.
5. **Dress:** add the modular art and animation rig.
6. **Replay:** repeat the same tests with full effects and LDM.
7. **Freeze or repair:** propagate only a section that passes; never mass-produce an unproven template.

## AI stop conditions

Stop and report a blocker rather than pretending completion when:

- The agent cannot import or playtest but the user asked for a ready/verified level.
- Song/audio needed for sync is unavailable or ambiguous.
- The target GD version or template is incompatible.
- Physics-critical object behavior is unknown.
- A source round trip drops unknown data.
- Full-run evidence contradicts the requested difficulty.

The proper output can still be a strong candidate with exact next tests. The improper output is an untested file described as finished.

## Anti-patterns that automatically fail review

- “Imports with no errors, therefore complete.”
- Difficulty created by random close spikes or impossible-looking microgaps.
- Long flat cube runs with occasional orbs described as demon gameplay.
- Pad and portal piles without a traced player-state sequence.
- Decorations placed before collision layout, then used to hide broken geometry.
- Thousands of objects with no coherent modular language or depth hierarchy.
- Random pulse/move/shake spam, permanent camera effects, or triggers off-beat.
- Animations that work once from an editor start position but break after death.
- Copying a famous level's identifiable art/gameplay instead of learning its system design.
