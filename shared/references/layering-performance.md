# Art layering, readability, and performance

## Functional layer stack

Keep functions separable even when the visual style is dense:

1. Collision and gameplay objects.
2. Hazard/readability outlines and route cues.
3. Foreground framing that does not cover inputs.
4. Main structures and characters.
5. Midground motifs.
6. Background atmosphere.
7. Particles, glow, gradients, shaders.
8. Offscreen controllers and test helpers on editor-only organizational layers.

Use Z layer/order for runtime composition and editor layers for maintainability. A high object count with poor layer ownership is not professional complexity.

## Modular decoration

Create a small vocabulary: structural module, edge/corner treatment, glow/shadow treatment, background motif, transition motif, and one hero asset per major section. Repeat with rotation, scale, color, crop, and controlled variations. This produces human coherence and makes performance tuning possible.

Do not paste identical dense clusters across the entire level. Alternate dense focal moments with negative space. Preserve contrast around the icon and upcoming hazards.

## Budgets

Set per-section budgets before decorating: total visible objects, simultaneous animated groups, particles, gradients, shader layers, and high-detail objects. Counts depend on target hardware and GD behavior; establish them empirically with representative stress sections.

The supplied animation files range from 78k to 196k total objects, but these totals are not recommendations. They include whole levels, art, helpers, and controllers. `world is blue` shows that 51k objects can coexist with only 583 recognized triggers, while BACKFIRE uses over 10k triggers. Optimize according to the actual bottleneck.

## Low-detail mode

High-detail should contain nonessential glow, particles, secondary outlines, microtexture, redundant gradients, and expensive background animation. LDM must keep collision, route cues, primary silhouettes, required state indicators, and sync-critical accents.

When an approximate output byte size is requested, this same nonessential high-detail pool is the only appropriate tuning surface. Do not make required art or gameplay high-detail merely to control file size, and do not confuse a larger compressed file with a richer composition.

## Performance test

Test the densest viewport, highest simultaneous trigger burst, transitions with loading/camera changes, death/restart, and low-detail mode. Record target device, refresh rate, resolution, and observed frame behavior. Static object analysis cannot substitute for runtime profiling.
