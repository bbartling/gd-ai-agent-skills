#!/usr/bin/env python3
"""Create a minimal one-block plus three-spike GDShare import canary."""
from __future__ import annotations

import argparse
from pathlib import Path

from gmd_codec import decode, encode, encode_into_template, get_typed_value


def build(template: Path, name: str) -> tuple[bytes, str]:
    tag, encoded = get_typed_value(template, "k4")
    if tag != "s":
        raise ValueError(f"k4 uses <{tag}> instead of <s>")
    source = decode(encoded)
    chunks = source.split(";")
    header = chunks[0]
    records = [record for record in chunks[1:] if record]
    if len(records) != 1:
        raise ValueError(
            f"canary template must contain exactly one source object; found {len(records)}"
        )

    # Object 8 is an ordinary upright spike. These conservative flags are
    # donor-derived from the supplied working Trouble_HARD export. Vary only
    # the textual spelling of a zero-degree rotation until gzip produces a k4
    # value that requires visible RFC 4648 padding; Geometry Dash acceptance of
    # that file directly exercises the regression that broke Cheese Moon V1-V3.
    for zero in ("0", "0.0", "0.00", "0.000", "0.0000", "0.00000"):
        spikes = [
            "1,8,2,450,3,15,96,1,64,1,67,1,155,18",
            "1,8,2,480,3,15,96,1,64,1,67,1,155,18",
            f"1,8,2,510,3,15,6,{zero},96,1,64,1,67,1,155,18",
        ]
        level = header + ";" + ";".join(records + spikes) + ";"
        if encode(level).endswith("="):
            return encode_into_template(template, level, name=name), zero
    raise RuntimeError("unable to construct a padded deterministic canary")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("template", help="known-working one-object local .gmd")
    parser.add_argument("output")
    parser.add_argument("--name", default="ONE BLOCK THREE SPIKE CODEC TEST")
    args = parser.parse_args()
    raw, zero = build(Path(args.template), args.name)
    output = Path(args.output)
    output.write_bytes(raw)
    _, encoded = get_typed_value(output, "k4")
    print(f"output={output}")
    print("objects=4")
    print("source_objects_preserved=1")
    print("added_spikes=3")
    print(f"k4_chars={len(encoded)}")
    print(f"k4_padding={len(encoded) - len(encoded.rstrip('='))}")
    print(f"zero_rotation_spelling={zero}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
