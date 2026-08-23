# Difficulty by game mode

Use these as design variables, not numerical guarantees.

## Cube and robot

Difficulty knobs: landing width, ceiling clearance, jump height choice, orb/pad sequencing, hold-release differentiation, slope behavior, and recovery platform length. Robot adds variable jump height, so communicate whether the intended action is tap, medium hold, or full hold. Do not stack invisible timing requirements after an automatic pad.

## Ship and swing

Difficulty knobs: corridor height, sustained control length, gravity changes, slope curvature, speed, mini state, and entry velocity. Avoid instantaneous corridor centering after a portal. Give a settling zone or align the incoming trajectory. For harder play, narrow gradually and vary curvature with readable anchors rather than noisy micro-spikes.

## Wave

Difficulty knobs: corridor width, slope changes, click frequency, mini state, speed, gravity and visual contrast. Straight-fly-like corridors test steadiness; zigzag patterns test rhythm. Avoid decorative diagonals that look collidable when they are not. At higher speeds, advance visibility is part of fairness.

## Ball and spider

Difficulty knobs: surface spacing, timing window, gravity-toggle cadence, route ambiguity, and ceiling/floor alternation. Ensure landing surfaces are visually distinct. Spider teleports make camera and screen-relative readability especially important; do not hide the destination behind effects.

## UFO

Difficulty knobs: click cadence, altitude envelope, ceiling/floor alternation, and recovery after each bounce. Establish rhythm before syncopation. Do not require a corrective click before the player can see the portal exit.

## Duals

Difficulty comes from coordinating two states, not simply doubling obstacles. Track both paths' mode, gravity, size, entry phase, and required inputs. Test asymmetric death causes. Symmetrical art can obscure mechanically asymmetric paths.

## Difficulty bands

- Easy/Normal: broad windows, one idea at a time, generous portal exits, strong route cues.
- Hard/Harder: denser rhythm and combinations, but readable setups and recovery remain.
- Insane/Demon: tighter state control, faster combinations, deceptive rhythm only when visually taught, and intentional consistency requirements.
- Higher demon tiers: label the exact skill demanded—precision, memory, wave control, ship control, learny transitions, sustained input density—rather than claiming difficulty from counts.

The supplied corpus demonstrates that a 127-object timing challenge can be harder than a 51k-object atmospheric level. Never infer a band from object or trigger count.
