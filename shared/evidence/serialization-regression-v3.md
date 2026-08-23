# Serialization regression evidence — Cheese Moon V3

## Known-working corpus

The V3 audit covered all 11 originally supplied reference files plus `rocket power.gmd` and the user's working `OneBlockTest.gmd`: 13/13 passed the wrapper, decode, record-pairing, coordinate, trailing-semicolon, same-value byte-splice, and semantic payload round-trip gates.

Observed human variations are preserved rather than “fixed”:

- four very large exports report the observed `k48=65535` cap;
- three exports omit `k48`;
- one export reports a legacy one-object mismatch and contains an opaque `kA2` object property.

## Rejected candidates versus V3

| Build | Known-good compact wrapper | Newline-free | Static release gate |
|---|---:|---:|---:|
| Cheese Moon V1 | No | No | Fail |
| Cheese Moon V2 | No | No | Fail |
| Cheese Moon V3 | Yes | Yes | Pass |

V1 and V2 were generated with a generic XML tree serializer. It changed the exact `<?xml version="1.0"?>` prologue to an encoding-bearing declaration and inserted a newline. V3 uses a byte-preserving splice into `OneBlockTest.gmd`; its outer key/type shape matches that local template exactly, its unknown metadata is unchanged, it has no online `k1`, its decoded object count exactly equals `k48`, and its content header/source prefix match `rocket power.gmd`.

These checks isolate a concrete serialization regression, but only a Geometry Dash import/open/save/re-export proves importer acceptance.
