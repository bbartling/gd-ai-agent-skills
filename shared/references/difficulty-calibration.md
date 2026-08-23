# Practical difficulty calibration

Difficulty must be engineered and observed, not typed into a filename.

## Section difficulty card

For each section record:

- Mode, speed, size, gravity, dual state, camera behavior.
- Entry position/velocity and whether input may be held.
- Required action sequence using tap/hold/release and approximate musical timing.
- Primary skill: timing, reading, ship control, wave control, click pattern, dual coordination, memory, transition consistency, or endurance.
- Window reducers: corridor, landing width, obstacle spacing, moving geometry, camera, visibility, preceding forced motion.
- Recovery margin after each committed action.
- Expected learning: sight-readable, lightly learny, memory, or precision repetition.
- Observed attempts/deaths and failure causes.

## Calibration ladder

Begin with a version that is clearly survivable. Increase one variable at a time:

1. Reduce recovery space.
2. Narrow a corridor or landing.
3. Shift an input relative to the beat.
4. Increase speed or use mini state.
5. Add gravity/size/mode interaction.
6. Combine with a previously taught mechanic.
7. Increase sustained duration or consistency demand.

Do not tighten spacing, obscure visibility, increase speed, and add a portal simultaneously. If testing fails, the cause becomes unknowable.

## Portal/pad/orb sequence trace

For every sequence write:

```text
approach state -> activation object -> forced state change -> first free action
-> recovery surface/corridor -> next state
```

Run at least these plausible variants: early/late activation, high/low trajectory, held/released input, and the actual previous obstacle's extreme exits. For duals, trace both icons. A start position immediately before the sequence is a debugging aid, not evidence of fair integration.

## Difficulty evidence hierarchy

Weak: object counts, spikes, speed names, visual density, creator prediction.

Better: section state/action analysis and repeatable local clears.

Strong: full-run death distribution, normal-mode clears, multiple testers, stated refresh/input environment, and comparison with known player ability.

Use the strongest available evidence and label the rest as estimates.

## Preventing fake demon difficulty

A higher-tier layout needs sustained and intentional skill demand. It should not be a mostly basic level with several arbitrary chokepoints. Check:

- Does every major section contribute an appropriate challenge?
- Is the hardest 5% consistent with the rest, or merely broken?
- Are transitions learnable and repeatable rather than blind?
- Does the challenge survive removal of visual clutter?
- Can a capable tester explain why deaths occur?
- Is the claimed tier based on more than the builder's own expectation?

If not, downgrade the claim or rebuild the gameplay.

## Death-cause tuning

Classify deaths: intended execution, misunderstood cue, blind entry, unexpected collision, bad exit state, sync issue, performance issue, or test setup artifact. Increase intentional-execution deaths; reduce the other categories. A section that is “hard” mainly because of unreadability or inconsistent state is defective, not well calibrated.
