# GDShare serialization integrity

## Why this gate exists

A `.gmd` can be semantically readable to Python and still open as a blank level. In the V1/V2 Cheese Moon incident, both candidates parsed, decompressed, contained tens of thousands of valid-looking objects, and round-tripped their `k4` payload. They nevertheless differed from every supplied human export at the outer byte layer: a generic XML writer changed the declaration and inserted a newline.

The supplied evidence set contained 13 known-working exports: 11 reference levels, `rocket power.gmd`, and `OneBlockTest.gmd`. All 13 were ASCII, single-line, had no BOM, used the same exact prologue, ended directly in `</dict></plist>`, decoded as URL-safe Base64 plus gzip, and ended their inner level string with a semicolon.

This does not prove that every other wrapper spelling fails. It proves that changing a known-working wrapper is an unnecessary compatibility risk and that generic XML validity is too weak a release gate.

## Mandatory write algorithm

1. Obtain a tiny known-working local export from the user's installed GD/GDShare version.
2. Keep its raw bytes as the container template. Prefer a local template without online level ID `k1`.
3. Parse a copy only for inspection. Never serialize the parsed tree.
4. Encode the complete inner string as UTF-8 → gzip with deterministic timestamp → URL-safe Base64.
5. Replace only the text contents of existing `k2`, `k4`, and `k48` nodes in the raw bytes.
6. Preserve the XML declaration, whitespace, key order, value tags, `k34`, and every unmodified value byte-for-byte.
7. Require exact decoded object count for a generated level below 65,535. Known human exports may omit `k48`, cap it at 65,535, or contain a documented legacy mismatch; preserve those inputs rather than normalizing them.
8. Fail if the container shape differs from the template or if a local template gains an online ID.

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
```

`gate_gmd_release.py` is fail-closed. It requires the known-good wrapper, exact outer key/tag shape, unchanged template metadata outside `k2`/`k4`/`k48`, local identity when the template is local, exact generated object count, and—when supplied—an exact content header and source-object prefix.

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

If a rung opens blank, compare its raw wrapper and decoded object boundary to the preceding re-export, then bisect only the changed data. Do not continue polishing a rejected artifact.
