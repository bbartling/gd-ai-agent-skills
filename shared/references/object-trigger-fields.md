# Common object and trigger fields

This is a focused working map, not an exhaustive promise across every GD version. Unknown keys must survive round trips.

## General object keys

| Key | Meaning |
|---:|---|
| 1 | Object ID |
| 2, 3 | X, Y |
| 4, 5 | Flip X, flip Y |
| 6 | Rotation |
| 20, 61 | Editor layer 1 and 2 |
| 21, 22 | Color channel 1 and 2 |
| 24, 25 | Z layer and Z order |
| 32 | Legacy uniform scale |
| 34 | Group parent flag |
| 41–44 | HSV enabled/value for color 1/2 |
| 57 | Dot-separated group memberships |
| 64 | Don't fade |
| 67 | Don't enter |
| 96 | No glow |
| 103 | High detail |
| 108 | Linked group |
| 121 | No touch |
| 128, 129 | Scale X/Y |
| 131, 132 | Skew X/Y |
| 134 | Passable |
| 135 | Hidden |
| 274 | Parent groups |

Observed special-purpose objects include text object ID `914`, where key `31` stores Base64-encoded text, and end trigger ID `3600`, whose exact fields vary by target version. Clone known-good records from the target export instead of relying on these observations as a complete schema.

## Core trigger IDs

| ID | Trigger | Key fields commonly used |
|---:|---|---|
| 899 | Color | duration 10; RGB 7/8/9; opacity 35; channel 23; copy 50 |
| 901 | Move | duration 10; X/Y 28/29; easing 30; target group 51; target position 71 |
| 1006 | Pulse | RGB 7/8/9; fade-in/hold/fade-out 45/46/47; target 51; target type 52 |
| 1007 | Alpha | duration 10; opacity 35; target group 51 |
| 1049 | Toggle | target group 51; activate 56 |
| 1268 | Spawn | target group 51; delay 63; ordered 441; remaps 442 |
| 1346 | Rotate | duration 10; target 51; degrees 68; center 71; easing 30 |
| 1347 | Follow | duration 10; target 51; followed target 71; X/Y modifiers 72/73 |
| 1520 | Shake | duration 10; strength 75; interval 84 |
| 1585 | Animate | target 51; animation ID 76 |
| 1595 | Touch | target 51; hold 81; toggle 82; dual mode 89 |
| 1616 | Stop | target 51; mode 580 |
| 1815 | Collision | target 51; block A/B 80/95; activate 56 |
| 1913 | Zoom camera | duration 10; easing 30; zoom 371 |
| 1914 | Static camera | duration 10; target position 71; exit 110 |
| 2015 | Rotate camera | duration 10; degrees 68; easing 30 |
| 2067 | Scale | duration 10; target 51; center 71; scale X/Y 150/151 |
| 2903 | Gradient | corner groups 203–206; layer 202; gradient ID 209 |
| 3032 | Keyframe | duration 10; group 51; spawn group 71; key ID 373; index 374; auto layer 459 |
| 3602 | SFX | SFX ID 392; speed 404; volume 406; start/end 408/410; fades 409/411 |

General trigger flags include spawn-triggered key 62, spawn delay key 63 where applicable, multi-trigger key 87, order key 115, center-effect key 369, and control ID key 534. Do not apply a field to a trigger merely because another trigger uses the same number.

## Common gameplay object IDs

- Portals: cube 12, ship 13, ball 47, UFO 111, wave 660, robot 745, spider 1331, swing 1933.
- Gravity: normal 10, inverted 11, toggle 2926.
- Size: normal 99, mini 101.
- Speed: slow 200, normal 201, fast 202, very fast 203, super fast 1334.
- Orbs: yellow 36, blue 84, pink 141, green 1022, black 1330, red 1333, green dash 1704, pink dash 1751, spider 3004.
- Pads: yellow 35, blue 67, pink 140, red 1332, spider 3005.

Object ID catalogs change. Prefer cloning an object exported from the target GD version to inventing an unverified record.
