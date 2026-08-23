# GDShare serialization integrity

## Why this gate exists

A `.gmd` can be readable to a permissive Python decoder and still open as a blank level. Cheese Moon V1, V2, and V3 all stripped required terminal `=` padding from `k4`. The old decoder silently added that padding before decoding, so all three broken files passed our tests. Every one of the 13 supplied working exports stored canonical URL-safe Base64 with `len(k4) % 4 == 0`; the three rejected builds had `len(k4) % 4 == 3`. The user's imported one-block/three-spike canary proved the corrected encoder, and the user subsequently confirmed that the complete 46,605-object V4 parses after restoring V3's single missing `=`.

The supplied evidence set contained 13 known-working exports: 11 reference levels, `rocket power.gmd`, and `OneBlockTest.gmd`. All 13 were ASCII, single-line, had no BOM, used the same exact prologue, ended directly in `</dict></plist>`, stored canonical padded URL-safe Base64, decompressed as valid gzip/UTF-8, and ended their inner level string with a semicolon.

This does not prove that every other wrapper spelling fails. HJfod's C++ GMD-API intentionally tolerates some older plist forms. Preserve a working wrapper because changing it is unnecessary risk, but do not mistake correlation for root cause: stripped `k4` padding was the defect common to V1, V2, and V3.

## Mandatory write algorithm

1. Obtain a tiny known-working local export from the user's installed GD/GDShare version.
2. Keep its raw bytes as the container template. Prefer a local template without online level ID `k1`.
3. Parse a copy only for inspection. Never serialize the parsed tree.
4. Encode the complete inner string as UTF-8 → gzip with deterministic timestamp → canonical URL-safe Base64. Keep zero, one, or two terminal `=` characters exactly as produced; never call `rstrip("=")`.
5. Replace only the text contents of existing `k2`, `k4`, and `k48` nodes in the raw bytes.
6. Preserve the XML declaration, whitespace, key order, value tags, `k34`, and every unmodified value byte-for-byte.
7. Require exact decoded object count for a generated level below 65,535. Known human exports may omit `k48`, cap it at 65,535, or contain a documented legacy mismatch; preserve those inputs rather than normalizing them.
8. Fail if the container shape differs from the template or if a local template gains an online ID.
9. Fail before decompression when `k4` is non-ASCII, has invalid URL-safe characters, misplaced padding, more than two padding characters, or a length not divisible by four. Never repair input silently in a validator.

Do not add a description, song field, length flag, difficulty flag, or other metadata merely because another level has it. Add one field only through a separate import canary from the same target version.

## Automated gates

```bash
python3 shared/scripts/gmd_codec.py inspect-wrapper candidate.gmd
python3 shared/scripts/audit_gmd_corpus.py reference-directory/ known-working-local.gmd \
  --json corpus-audit.json --csv corpus-audit.csv
python3 shared/scripts/validate_gmd.py candidate.gmd --json validation.json
python3 shared/scripts/gate_gmd_release.py candidate.gmd \
  --container-template known-working-local.gmd \
  --content-baseline importable-source.gmd --max-objects 65535 \
  --json release-gate.json
python3 -m unittest discover -s shared/tests -p 'test_*.py'
python3 shared/scripts/run_gmd_regression_gate.py \
  --candidate candidate.gmd \
  --container-template known-working-local.gmd \
  --content-baseline importable-source.gmd \
  --known-good reference-directory/ known-working-local.gmd importable-source.gmd \
  --known-bad broken-v1.gmd broken-v2.gmd broken-v3.gmd \
  --manifest shared/evidence/regression-corpus-manifest.json \
  --json regression-gate.json
```

`gate_gmd_release.py` is fail-closed. It requires canonical padded `k4`, valid gzip/UTF-8, the known-good wrapper, exact outer key/tag shape, unchanged template metadata outside `k2`/`k4`/`k48`, local identity when the template is local, exact generated object count, and—when supplied—an exact content header and source-object prefix.

`run_gmd_regression_gate.py` adds two-sided regression evidence. Every known-good input must pass, every known-bad input must fail for the required reason, and the new candidate must pass the complete release gate. A broken file does not count as a successful test merely because the command returned nonzero; its expected failure reason must match.

## Human import ladder

Static PASS still means **candidate**. Test these in order and retain every GD-normalized re-export:

1. unchanged template;
2. raw-splice rename only;
3. new `k4` containing the template header/object unchanged;
4. source header plus exact source objects;
5. one donor-cloned object;
6. one animation system;
7. functional level without optional detail;
8. final density.

If a rung opens blank, first inspect the serialized `k4` alphabet, length, and terminal padding without repairing it. Then compare its raw wrapper and decoded object boundary to the preceding re-export and bisect only the changed data. Do not continue polishing a rejected artifact.
