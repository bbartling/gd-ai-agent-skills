# Music sync and section design

## Build a time map first

Record song ID/file, verified offset, BPM changes, time signature assumptions, and phrase landmarks. Create a section table with timestamps, measures, intensity, instrumentation, gameplay mode/speed, mechanic, palette, and transition.

Do not map time to x with one constant when speed portals, timewarp, camera behavior, or platformer mode alter progression. Prefer in-editor song guidelines/BPM tools and measured playhead checks. Verify sync after every speed change from the beginning, not only a local start position.

## Sync hierarchy

- Phrase/section changes: mode, speed, palette, camera framing, major set piece.
- Measure/downbeat: structure change, strong movement, gradient/palette shift.
- Beat: pulse, hazard cadence, repeated motif.
- Subdivision: small particles or micro accents, used sparingly.

Gameplay sync is stronger when inputs express rhythm, not when every percussion sound creates a flash. Leave visual silence so important accents read.

## Intensity mapping

Visual and gameplay intensity should broadly follow the song, but perfect mirroring is not mandatory. Use anticipation before drops, breathing room after peaks, and recurring motifs when themes return. A transition should begin early enough for the player to read its new state before the first tight input.

## Verification

Test with music enabled from zero, after pause/resume, in practice mode, and from editor playtest. Note platform/audio latency assumptions. If sync depends on a custom song version, identify the exact song/offset rather than embedding guesses in coordinates.
