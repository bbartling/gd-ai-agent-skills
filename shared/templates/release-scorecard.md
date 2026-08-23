# GD release scorecard

Scoring supports review; it never overrides a failed critical gate.

## Critical gates

- [ ] Imports, opens, saves, and re-exports in target GD/GDShare.
- [ ] Undecorated collision layout cleared from zero.
- [ ] All real-approach pad/orb/portal/speed/gravity/size/dual transitions tested.
- [ ] Full practice clear recorded.
- [ ] Normal-mode full clear/verification status stated accurately.
- [ ] Song/offset and sync through speed/time changes checked from zero.
- [ ] Trigger death/restart/checkpoint/LDM lifecycle checked.
- [ ] Readability and performance checked with full effects.
- [ ] Difficulty claim supported by play evidence; fresh-player result recorded.

If any required gate is unchecked, label the file a candidate and list the remaining work.

## Quality score (100)

| Area | Max | Score | Evidence |
|---|---:|---:|---|
| Gameplay continuity and state correctness | 20 | | |
| Spacing, transitions, and readability | 15 | | |
| Difficulty consistency and honesty | 15 | | |
| Song sync and pacing | 15 | | |
| Visual language, composition, and depth | 15 | | |
| Animation quality and memorable set pieces | 10 | | |
| Trigger maintainability/reset behavior | 5 | | |
| Runtime performance and LDM | 5 | | |
| **Total** | **100** | | |

## Automatic deductions / rejection notes

- Import-only “validation” presented as readiness:
- Trivial layout with inflated demon claim:
- Broken or perfect-start-only transition:
- Decoration obscures the path:
- Random/off-beat trigger or camera spam:
- Static filler or copied visual noise:
- Loop/state leakage after death:
- Unreported performance or sync limitation:

## Release statement

- Build filename/version:
- Evidence level reached:
- Target difficulty and confidence:
- Known limitations:
- Required next test:
- Final label: candidate / release candidate / ready / verified
