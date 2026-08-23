# Findings from the supplied GDShare corpus

## Scope and limits

All 11 supplied files were decoded and iterated object-by-object. The corpus contains 853,723 objects and 48,791 recognized triggers. Exact profiles are in `../evidence/corpus-analysis.json` and `corpus-summary.csv`.

These are descriptive observations, not universal difficulty standards. Filenames supplied difficulty/style labels, but static object data cannot independently confirm ratings, creator intent, song sync, collision behavior, or playability. Coordinates include art and offscreen trigger workspaces. “Gameplay marker spacing” in the JSON covers portals/orbs/pads/speed objects, not all hazards or collision surfaces.

## Per-file evidence

| File | Objects | Triggers | Unique groups | Grouped objects | Strongest signal |
|---|---:|---:|---:|---:|---|
| wave PROCESSING_EASY | 282 | 1 | 0 | 0% | Small static processing/art example; not evidence that easy levels need this count |
| impossible timing_HARDER | 127 | 4 | 1 | 12.6% | Tiny timing challenge; difficulty can exist with almost no decoration |
| Trouble_HARD | 12,093 | 555 | 156 | 85.9% | Moderate effect stack: move, pulse, alpha, camera, color |
| wallbreaker_HARDER | 22,555 | 1,041 | 245 | 32.1% | Alpha/move/scale-driven presentation with comparatively light grouping |
| world is blue_NORMAL | 51,015 | 583 | 182 | 81.8% | High visual object count but modest trigger count; atmosphere is not difficulty |
| Abducted | 78,106 | 7,836 | 1,849 | 90.5% | Transform-rich rigging: 2,702 moves, 1,067 alphas, 905 rotates |
| Skeletal Shenanigans | 80,495 | 8,844 | 1,821 | 82.8% | Keyframe character/scene animation: 2,201 keyframes and 1,604 rotates |
| MOAI | 117,272 | 9,547 | 3,120 | 76.3% | Move/pulse/gradient system: 2,958 moves, 1,814 pulses, 1,317 gradients |
| Slaughterhouse | 147,241 | 2,303 | 302 | 73.9% | Pulse-heavy atmosphere: 1,022 pulses; lower trigger/group breadth than showcases |
| GD GANGSTER RAP | 148,992 | 7,755 | 1,849 | 87.7% | Move/toggle/scale/alpha/color blend with relatively few spawn triggers |
| BACKFIRE BLACKFIRE | 195,545 | 10,322 | 4,234 | 90.4% | Largest and broadest: transform, pulse, toggle, spawn, gradient, camera systems |

## Robust conclusions

1. Object count and gameplay difficulty are independent. The 127-object harder example is more timing-focused than visually massive files.
2. Animation-heavy human levels assign groups extensively: five showcase files group roughly 76–91% of objects. Grouping is infrastructure, not decoration.
3. There is no single “human animation recipe.” Skeletal favors keyframes, Slaughterhouse pulses, Abducted transforms, and BACKFIRE combines many systems.
4. Short trigger timing is common in effect-heavy files. Median spawn delays in several showcases are about 0.10–0.16 seconds, but these values are corpus observations, not defaults. Timing must be derived from the actual song and effect.
5. Visual density varies independently from trigger density. `world is blue` has over 51k objects but only 583 recognized triggers.
6. Huge extreme values exist in raw properties. Treat them as special rigs, persistent effects, offscreen controllers, or encoding quirks until visually inspected; never convert maxima into design guidance.
7. Human files mix many editor conventions. Group numbers themselves do not reveal semantics. A generated project needs its own ledger.

## How an agent should use this evidence

- Select one or two reference files matching the requested purpose, then inspect their section-local trigger and group patterns. Do not average all files into a generic level.
- Use ratios and system composition to ask better questions: grouped-object share, triggers per thousand objects, transform/pulse/keyframe mix, high-detail share, and section density.
- Copy architectural ideas—rig ownership, layers, repeated motifs, effect envelopes—not identifiable art or gameplay sequences.
- Use counts as budgets and regression signals. Never use them as a substitute for editor viewing and playtesting.
