# Layout and spacing engineering

## Coordinate reasoning

The familiar editor grid helps construction, but a number of blocks is not a stable difficulty unit. The same gap changes with game speed, mode physics, mini state, gravity, slope/orb state, entry velocity, hold history, and refresh/input behavior. Treat a placement as a state transition:

```text
(entry mode, speed, size, gravity, position, velocity, held state)
  + (available action window and input)
  -> (exit state and recovery margin)
```

Build from safe envelopes. Tighten vertical clearance, horizontal window, input timing, or recovery—not all at once. Preserve enough approach distance to read and stabilize after a portal.

## Human-looking phrase construction

Within a musical phrase:

1. Establish a visual lane and one mechanic.
2. Demonstrate it safely once.
3. Repeat with a controlled variation.
4. Combine it with one previously learned element.
5. End with a release, landing, or obvious transition.

Avoid random saw scatter, identical jumps for 20 seconds, portals directly on blind hazards, pads whose launch collides with decoration, and orb chains with no visual distinction between tap/hold/release intent.

## Readability budget

- Show the intended corridor before the input deadline.
- Use consistent hazard language and solid/decorative separation.
- Place portals so their effect is visible and the exit has setup room.
- Keep foreground effects away from the player's immediate collision silhouette.
- Telegraphed difficulty can be hard; hidden state is usually unfair.
- Camera motion must not invalidate learned spatial cues at the same instant as a tight input unless intentionally targeted and tested.

## Transition checklist

For each portal/speed/gravity/size/camera change, test: entry alignment, held-button behavior, dual asymmetry, immediate collision, exit velocity, first required input, visibility time, and death-restart consistency. Test the transition from at least two plausible prior trajectories, not just a start position placed perfectly before it.

## Difficulty shaping

Chart intensity by section from 1–10 and identify the mechanical cause. A good curve can rise, peak, breathe, and return; it need not increase monotonically. If one short transition causes most deaths, repair setup/readability before weakening the whole level.
