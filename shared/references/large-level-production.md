# Large procedural level production

Use this guide for source-preserving extensions, very high object counts, multipart bosses, large destination reveals, or approximate compressed-size targets. These constraints come from observed build failures that static validity alone did not catch.

## 1. Preserve and extend deliberately

Define three ranges before editing:

- **Preserved source:** original records retained unchanged unless a named repair requires touching them.
- **Repair window:** existing coordinates/systems that may be rebuilt, with collision and decorative ownership identified separately.
- **Extension:** new coordinates plus reserved group, color, item, and editor-layer ranges.

Keep the source payload and outer metadata as the base. Append or minimally replace object records; do not reconstruct unknown records from a lossy object model. Record a source hash, preserved object count, handoff coordinate, and new ID ranges in the build report.

Use a fixed seed for procedural variation. A rerun with the same source, brief, seed, and options should produce the same level string and file bytes. Determinism makes byte targeting, regression comparison, and repair possible.

## 2. Build systems before density

Complete in this order:

1. Continuous collision route and state transitions.
2. Primary silhouettes, route cues, and section palette.
3. Named animation rigs and lifecycle triggers.
4. Hero art, boss, and destination payoff.
5. Secondary atmosphere and microdetail.
6. Optional high-detail density used for performance/size tuning.

Do not use procedural repetition as a substitute for composition. Each section needs a focal hierarchy, negative space around inputs, a different density rhythm, and a deliberate entry/exit. Generate modules—asteroid, crater, cheese wedge, structure, star cluster—then compose variants at section scale.

## 3. Parent/child ownership for animated assemblies

Separate whole-assembly motion from local motion:

| Role | Example | Membership/target rule |
|---|---|---|
| Assembly parent | Boss body `600` | Every part that travels with the body includes group `600` |
| Local child | Eye `601` | Eye objects include `600.601`; blink/offset targets `601` |
| Local child | Cannon `604` | Cannon objects include `600.604`; recoil targets `604` |
| Center/helper | Rotation center `610` | Dedicated helper; do not assume visible body center is correct |
| Controller | Phase trigger `620` | Controller-only group/layer; never mixed into visible art accidentally |

Audit the emitted key-57 memberships. A correct ledger with incorrect serialized membership still produces detached parts. Where true parent/follow semantics are used, audit those target fields too.

Every repeating motion needs a stable baseline. Prefer paired moves and alpha restoration for deterministic x-triggered ambience. Use spawn loops only when their start, delay, stop, death, checkpoint, replay, and LDM behavior can be tested.

## 4. Boss encounter architecture

A boss is a gameplay-readable system, not only a character drawing:

- Keep real collision hazards stationary unless moving collision has been deliberately implemented and playtested.
- Animate separate telegraphs, muzzle flashes, projectiles, expressions, and camera accents around those hazards.
- Define phases with entry, attack grammar, escalation, health/state feedback, cleanup, and defeat.
- Tie health-bar changes to real interaction when possible. If the bar only decreases with progress, state that it is cinematic feedback rather than an interactive damage system.
- End every phase by restoring camera, palette, opacity, and assembly baseline before the next handoff.

Use [../templates/boss-destination-card.md](../templates/boss-destination-card.md) to record the phase and payoff contract.

## 5. Destination and finale payoff

The destination must read during play at the intended camera scale. Build from outside in:

1. Landmark silhouette occupying a meaningful part of the viewport.
2. Theme-defining material cues—holes, rind, craters, rivers, flags, characters, or orbiting chunks.
3. Approach framing and a readable reduction in hazard pressure.
4. Reveal envelope: anticipation, reveal, settle, celebration.
5. Landing/recovery space and a clear end trigger.

Connect the boss defeat or final mechanic to the reveal. Preserve enough screen time for a player—especially a child—to recognize and enjoy the promised destination before the level ends.

## 6. Layered fields and debris

For asteroid, cloud, traffic, or particle fields, create far/mid/near roles with different scale, contrast, motion, and density. Protect a readable route through negative space. Use hero objects with owned rotation/movement groups; keep background filler passable when collision has not been verified. Decorative motion must not falsely promise the position of a hazard hitbox.

## 7. Approximate compressed-size targets

Treat the target as a budget with a tolerance. The functional build is immutable during tuning. Put only nonessential stardust, microtexture, secondary craters, redundant glow, or similar objects in a deterministic high-detail pool.

Recommended search:

1. Generate the base plus zero optional objects and measure encoded bytes.
2. Generate an upper bound of optional objects and measure again.
3. If the target is bracketed, binary-search the optional-object count.
4. Because gzip size can move nonlinearly, evaluate nearby counts and choose the smallest absolute error inside the tolerance.
5. Regenerate the selected count from the fixed seed; validate and round-trip it again.

Never append arbitrary bytes, inject opaque comments, or clone identical offscreen objects to hit a number. Report actual bytes, object count, high-detail count, and tolerance. A larger file is not evidence of better art or harder gameplay.

## 8. Preview and evidence boundaries

A spatial composition preview may plot objects by coordinates, scale, color role, and known IDs. Use it to find empty sections, clutter, poor framing, detached pieces, undersized landmarks, and bad density transitions.

It does **not** execute triggers or simulate the game. It cannot prove opacity, camera, rotation centers, collision, input windows, song sync, LDM behavior, or restart state. Keep the build labeled **candidate requiring GD import and playtest** until those evidence levels are reached.

## 9. Packaging audit

- Source copy/hash retained; preserved and repaired ranges documented.
- Same source/seed/options reproduce the same candidate.
- No unresolved target groups unless individually explained.
- Parent/child serialized memberships audited.
- Repeated motion, alpha, and camera states return to their intended baseline.
- Primary collision, cues, boss state, and destination remain in LDM.
- `k48` treatment matches a target-version reference; count-cap warnings remain explicit.
- Candidate decodes, re-encodes, and compares without losing unknown data.
- Actual file size/counts reported without using them as quality evidence.
- GD import, save, re-export, section tests, and full-run status stated separately.
