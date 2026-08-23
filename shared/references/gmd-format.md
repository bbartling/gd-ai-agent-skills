# GDShare `.gmd` format and safe round trips

## Container and byte contract

A GDShare level file is a plist-shaped XML document whose dictionary uses RobTop-style `<k>` keys. Important observed outer fields include:

- `k1`: level ID
- `k2`: level name
- `k3`: description where present
- `k4`: compressed/encoded inner level string
- `k7`: official difficulty code where present
- `k8`: official song ID
- `k23`: length code
- `k45`: custom song ID
- `k48`: object count where present

Presence and meaning vary by version and origin. Preserve all unknown fields and their XML value tags.

The wrapper's bytes are compatibility-relevant. All 11 supplied human reference levels plus the working `OneBlockTest` and source level were ASCII, single-line documents beginning exactly:

```text
<?xml version="1.0"?><plist version="1.0" gjver="2.0"><dict>
```

Two rejected generated candidates instead had an `encoding='utf-8'` declaration and a newline introduced by generic XML serialization. Valid XML is therefore not sufficient evidence. Preserve the template's declaration, whitespace, key order, value tags, unknown values, and closing bytes. Replace the text of existing scalar fields in the raw template; do not serialize the parsed tree. See `serialization-integrity.md`.

`k4` decoding is: add Base64 padding if absent → URL-safe Base64 decode → gzip decompress → UTF-8 text. Encoding reverses that process. The bundled codec uses deterministic gzip timestamps for stable output; Geometry Dash may normalize the export later.

## Inner level string

The first semicolon-delimited record is a header containing color channels and editor settings. Preserve it unless a field is specifically understood. Each later nonempty record is an object. Object records contain comma-separated numeric key/value pairs:

```text
1,1,2,150,3,150,57,12.13;
```

This represents object ID 1 at x=150, y=150, in groups 12 and 13. Values are text; keep their precision and do not sort or coerce fields unnecessarily. Key `24` is a Z-layer enum rather than arbitrary depth; conservative observed values are `-5,-3,-1,1,3,5,7,9,11,13`. Use key `25` for within-layer ordering and use a target-version donor as the final authority.

## Safe modification strategy

1. Validate and hash/retain the original.
2. Decode to a separate file.
3. Parse without discarding unknown keys or duplicate behavior you do not understand.
4. Apply the smallest possible mutation.
5. Update `k4` and `k48`; use a new name.
6. Validate, import into GD, open in editor, save, re-export.
7. Compare the GD-normalized export against the candidate and inspect differences.

For object counts above 65,535, do not assume `k48` is an unconstrained exact integer. Supplied high-object references can report `65535` while decoding to more objects. Preserve the target-version convention, emit a warning, and make GD's import/save/re-export the compatibility authority.

Avoid generic XML/plist writers, even if they can read `<k>` tags: they may change the declaration, quote style, whitespace, empty tags, order, or unknown values. A parser may be used for inspection, but final output must use byte-preserving scalar splices into a proven export.

## Empty-level fallback

GDShare can accept enough metadata to create an entry while the level opens as a plain/empty editor. A successful plist parse and gzip round trip therefore do not prove editor compatibility. Check the serialized wrapper first, then malformed header edits, invalid enum values, unsupported object/property combinations, count/capacity boundaries, and transformations that changed unknown source records.

Start from the last importable export and build an import ladder. Keep the header unchanged for the first extension, preserve source records exactly, add one donor-derived object/system at a time, and test import/open/save/re-export before increasing density. Use `../scripts/audit_gmd_compatibility.py` to enforce the conservative invariants when GD testing is temporarily unavailable.

## Group and reference hazards

Key 57 contains group memberships, but trigger target references use other keys. A global group remap must update target group, center group, follow group, parent group, spawn group, collision targets, item references where appropriate, and serialized remap lists. Key numbers are trigger-specific. If exact coverage is unknown, clone into a reserved unused range and do not remap existing systems.

## Compatibility

Use a template exported by the same GD/GDShare generation that will import the result. Retain backups. A structurally valid file can still fail because of version-specific object IDs, invalid combinations, capacity, or semantic trigger errors.

## Approximate file-size targets

Compressed `.gmd` byte size depends on gzip repetition, numeric precision, ordering, metadata, and content—not just object count. Build the meaningful level first. If the user supplied a budget such as “about 2 MB,” tune a deterministic pool of optional high-detail objects and regenerate from the same source; use a bounded search over that pool because compressed size is not perfectly linear. Never add trailing junk, opaque padding, or visually meaningless duplicates. Revalidate the winning build and keep gameplay, controllers, primary silhouettes, and route cues outside the tunable pool.
