---
name: gd-level-qa
description: Validate Geometry Dash GDShare level structure, gameplay, readability, difficulty consistency, trigger lifecycles, and performance before release.
---

# GD Level QA

Read `../shared/references/anti-slop-readiness.md` first. Use `../shared/templates/release-scorecard.md` for the final review. Critical failures cannot be averaged away by a high aesthetic score.

Separate evidence levels:

1. Static structure: plist parses, payload decodes, object pairs are valid.
2. Editor semantics: imports, opens, saves, groups/objects appear correctly.
3. Trigger behavior: animations start, stop, reset, and replay correctly.
4. Gameplay: full clears and transition-specific tests.
5. Human quality: blind readability, fun, difficulty consistency, sync.

Only claim the levels actually reached. Read `../shared/references/validation-playtesting.md`.

A rendered coordinate preview can reveal composition defects—empty bands, detached parts, bad scale, weak silhouettes, or missing destination payoff—but it is not evidence of runtime transforms, opacity, camera behavior, collision, sync, or playability. Label it **spatial composition preview**.

## Minimum run

```bash
python3 ../shared/scripts/validate_gmd.py candidate.gmd --json validation.json
python3 ../shared/scripts/compare_gmd.py baseline.gmd candidate.gmd
python3 ../shared/scripts/analyze_gmd.py candidate.gmd --json profile.json --csv profile.csv
```

Then import into Geometry Dash under a new name. Inspect beginning/end, every portal and speed change, groups, editor layers, high-detail objects, hidden helpers, song offset, and start positions. Test from zero, from each section boundary, after death/restart, and after practice checkpoints. Verify normal and low-detail configurations if provided.

Reject release for structural errors, missing/unintended geometry, impossible or blind transitions outside target intent, persistent trigger state after restart, uncontrolled loops, unreadable hazards, major frame drops, or an unverified full run. Warnings about target groups can be legitimate; resolve them by tracing dynamic trigger groups rather than deleting them automatically. A `k48=65535` warning on a larger decoded level may be a version-specific count cap; compare against a known target-version export and require an import/save/re-export instead of silently changing it.

Also reject inflated difficulty claims. Compare the requested tier with actual mode-specific demands, sustained input density, transition complexity, clear rates, and fresh-player feedback. Object count, spike count, visual noise, and level name are not difficulty evidence.

For major generated builds, also audit the checks in `../shared/references/large-level-production.md`: preserved-source boundary, deterministic rebuild, parent/child membership, baseline restoration, finale payoff, optional-detail size tuning, and candidate-versus-playtested labeling.
