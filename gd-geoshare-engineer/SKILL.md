---
name: gd-geoshare-engineer
description: Inspect, decode, encode, compare, and safely modify Geometry Dash GDShare .gmd files while preserving unknown metadata and object properties.
---

# GDShare Engineer

Use this skill for byte/file work. It does not certify playability.

## Invariants

- Work on a copy; keep the original untouched.
- Preserve unknown outer plist entries, level-header tokens, object keys, ordering, and numeric precision whenever possible.
- A `.gmd` is an XML-like plist wrapper. `k4` contains URL-safe Base64 of gzip-compressed level text. The inner text is a header followed by semicolon-separated objects; each object is comma-separated key/value pairs. Human exports can contain opaque nonnumeric keys, so preserve unknown tokens.
- Treat the serialized wrapper as part of the format. The supplied known-good corpus is ASCII, single-line, and begins exactly `<?xml version="1.0"?><plist version="1.0" gjver="2.0"><dict>`. Never write a candidate with `ElementTree.write`, a plist serializer, pretty-printing, a BOM, or a replacement XML declaration. Read `../shared/references/serialization-integrity.md` before any encode/write.
- Key `1` is object ID, `2` x, `3` y, `6` rotation, `20` editor layer 1, `24` Z layer, `25` Z order, `32` legacy scale, `57` dot-separated group IDs, `64` don't fade, `67` don't enter, `103` high detail, and `135` hidden. Read `../shared/references/gmd-format.md` and `object-trigger-fields.md` before editing raw values.
- A valid decode/re-encode only proves structure. It does not prove that Geometry Dash accepts every semantic combination.
- For very large levels, a decoded count above 65,535 can coexist with `k48=65535` in reference exports. Treat that as a target-version compatibility warning, not automatic corruption or permission to rewrite metadata blindly. Import, save, re-export, and compare.

## Tools

```bash
python3 ../shared/scripts/gmd_codec.py decode level.gmd level-string.txt
python3 ../shared/scripts/gmd_codec.py encode template.gmd level-string.txt candidate.gmd --name "Candidate"
python3 ../shared/scripts/gmd_codec.py inspect-wrapper candidate.gmd
python3 ../shared/scripts/audit_gmd_corpus.py references/ template.gmd \
  --json corpus-audit.json --csv corpus-audit.csv
python3 ../shared/scripts/analyze_gmd.py level.gmd --json analysis.json --csv summary.csv
python3 ../shared/scripts/validate_gmd.py candidate.gmd --json validation.json
python3 ../shared/scripts/compare_gmd.py original.gmd candidate.gmd
python3 ../shared/scripts/audit_gmd_compatibility.py original.gmd candidate.gmd \
  --require-header-match --require-source-prefix --strict-z-layers --max-objects 65535
python3 ../shared/scripts/gate_gmd_release.py candidate.gmd \
  --container-template known-working-local.gmd \
  --content-baseline original.gmd --max-objects 65535
```

Use a local template exported by the installed GD/GDShare version. For a generated level, prefer a template with no online `k1` identity. Do not synthesize outer metadata from memory or transplant an online ID into a local build. Change only existing `k2`, `k4`, and `k48` fields unless a canary proves another mutation. Preserve `k34` and all unknown values. After programmatic generation: run the release gate, import under a new name, open in editor, save, re-export, and compare. If GD normalizes fields, treat its export as canonical.

For source-preserving procedural builds or approximate byte targets, read `../shared/references/large-level-production.md`. Never append arbitrary bytes to the container or duplicate meaningless objects to hit a number. If size must be tuned, change deterministic, removable high-detail content only after the functional build passes structural checks.

## Raw mutation policy

Prefer cloning known-good objects and modifying the minimum properties. Allocate new group/color/item IDs from a documented range. Never reuse an ID merely because it looks unused in a viewport; inspect all objects and trigger targets. For group remapping, include memberships and every trigger-specific reference, including center/parent/follow/spawn IDs. Abort if the mapping inventory is incomplete.

Key `24` is an enumerated Z layer, not an arbitrary signed depth. Conservative observed values are `-5,-3,-1,1,3,5,7,9,11,13`; use target-version donor records as authority. Put fine ordering in key `25`. A plain/empty editor after an apparently successful import is a fatal compatibility failure: the outer plist may be accepted while Geometry Dash rejects the wrapper or level string. First compare raw prologue, line breaks, outer key/tag order, local/online identity, `k34`, and template-only metadata; then bisect inner changes. Never trust generic XML validity or a decode/re-encode test alone.
