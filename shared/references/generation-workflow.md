# End-to-end AI generation and major-refactor workflow

## Phase 0 — Evidence and safety

- Duplicate the `.gmd` and retain the source filename/hash.
- Decode, validate, and profile every supplied reference.
- Identify which references are gameplay evidence and which are animation/art evidence.
- Define target GD/GDShare version and export a tiny local/template level from it. Record its raw wrapper hash and whether it has an online `k1` identity.

## Phase 1 — Design brief

Write: classic/platformer, song and offset, length, target difficulty range, allowed modes, intended player skills, theme, color script, animation ambition, target hardware, object/group budgets, and excluded mechanics. Resolve contradictions before building.

## Phase 2 — Section contract

Create a table per phrase: timestamps/measures, mode, speed, size, gravity, input rhythm, mechanic, difficulty cause, route/collision envelope, transition, visual motif, animation rigs, and test gate. Allocate group/color/editor-layer ranges.

## Phase 3 — Graybox

Construct start, finish, collision surfaces, hazards, orbs/pads, portals/speed/gravity, and minimal route cues. No elaborate decoration. Use start positions for iteration but repeatedly run from zero. Finish a complete playable spine before polishing.

## Phase 4 — Difficulty pass

Trace state into and out of each challenge. Repair blind transitions and accidental spikes. Make a death-cause ledger by section. Adjust one variable at a time. Obtain at least one fresh-player run appropriate to the target band.

## Phase 5 — Visual prototype

Decorate one representative section at full intended quality. Add its rigs, LDM, layers, and performance budget. Test readability/performance before propagating the visual language.

Before propagation, make an import canary. The recommended ladder is: byte-identical same-value splice, renamed raw-splice clone, source plus one donor object, one complete new system, representative section, full functional build, then optional density. Import/open/save/re-export each rung. A plain/empty editor means the payload or wrapper was rejected; inspect the serialized `k4` padding/alphabet/length before wrapper byte-shape and template identity, then bisect additions.

## Phase 6 — Production

Build reusable modules and named rigs. Keep controllers on dedicated editor layers. Audit group ownership after every section. Provide reset/stop behavior and transition cleanup. Maintain negative space and a stable hazard language.

For a large procedural extension, keep the original object records byte-for-byte where possible, append into a reserved coordinate/group/channel/layer range, use a fixed random seed, and emit the same build from the same inputs. Read [large-level-production.md](large-level-production.md) for hierarchy, boss/finale, preview, and size-target rules.

## Phase 7 — Packaging and validation

Encode into a new `.gmd` by raw-splicing `k2`, canonical padded `k4`, and exact `k48` into a proven local target-version template. Run `inspect-wrapper`, static validation, `gate_gmd_release.py`, `audit_gmd_compatibility.py`, the known-good/known-bad regression gate, and compare counts/systems. Import, open, save, re-export. Test all transitions, trigger lifecycles, normal/practice/LDM, performance, and full clears. Archive the build report with limitations.

## Refactor rules

When improving an existing level, preserve functioning gameplay until a replacement passes. Work section-by-section on copies. Establish a baseline profile and screenshots/video outside this package. If a mutation unexpectedly changes unrelated object/group/trigger counts, stop and investigate. Never “clean” unknown fields globally.

If reworking an early decorative field, separate passable visual layers from verified collision. Decorative near/mid/far motion can be replaced safely only when gameplay hazards and route state are inventoried first.

## Agent completion report

State: source used, files produced, sections changed, structural checks, editor import result, gameplay tests, devices/settings, unresolved warnings, and exact remaining human verification. “No parser errors” is not “level works.”
