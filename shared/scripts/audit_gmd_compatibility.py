#!/usr/bin/env python3
"""Compare a generated GDShare candidate to an importable baseline.

This checks conservative extension invariants that a normal structural parser
cannot prove. It still cannot replace a Geometry Dash import/open/save test.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from analyze_gmd import decode_level, parse_object, plist_pairs


SAFE_Z_LAYERS = {"-5", "-3", "-1", "1", "3", "5", "7", "9", "11", "13"}


def load(path: Path):
    outer = plist_pairs(path)
    level = decode_level(outer["k4"])
    chunks = level.split(";")
    records = [record for record in chunks[1:] if record]
    return outer, chunks[0], records, [parse_object(record) for record in records], len(level)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline")
    parser.add_argument("candidate")
    parser.add_argument("--require-header-match", action="store_true")
    parser.add_argument("--require-source-prefix", action="store_true")
    parser.add_argument("--strict-z-layers", action="store_true")
    parser.add_argument("--max-objects", type=int)
    parser.add_argument("--json")
    args = parser.parse_args()

    baseline_path = Path(args.baseline)
    candidate_path = Path(args.candidate)
    errors, warnings = [], []
    try:
        b_outer, b_header, b_records, b_objects, b_chars = load(baseline_path)
        c_outer, c_header, c_records, c_objects, c_chars = load(candidate_path)
    except Exception as exc:
        report = {"compatible_structure": False, "errors": [f"decode failed: {exc}"], "warnings": []}
        print(json.dumps(report, indent=2))
        return 1

    header_match = b_header == c_header
    prefix_match = c_records[:len(b_records)] == b_records
    if args.require_header_match and not header_match:
        errors.append("candidate changed the known-importable level header")
    elif not header_match:
        warnings.append("candidate changed the level header; import-test the header mutation before scaling")
    if args.require_source_prefix and not prefix_match:
        errors.append("candidate does not preserve the baseline object records as an exact prefix")
    elif not prefix_match:
        warnings.append("baseline object prefix changed; confirm that every replacement belongs to the repair scope")

    z_counts = Counter(obj.get(24, "") for obj in c_objects if 24 in obj)
    invalid_z = {value: count for value, count in z_counts.items() if value not in SAFE_Z_LAYERS}
    if invalid_z:
        message = f"candidate uses unrecognized Z-layer enum values: {invalid_z}"
        (errors if args.strict_z_layers else warnings).append(message)

    declared = c_outer.get("k48")
    if not declared or not declared.isdigit() or int(declared) != len(c_records):
        errors.append(f"candidate k48={declared!r} does not exactly match decoded count {len(c_records)}")
    if args.max_objects is not None and len(c_records) > args.max_objects:
        errors.append(f"candidate has {len(c_records)} objects, above requested maximum {args.max_objects}")

    baseline_ids = {obj.get(1, "") for obj in b_objects}
    candidate_ids = {obj.get(1, "") for obj in c_objects}
    baseline_keys = {key for obj in b_objects for key in obj}
    candidate_keys = {key for obj in c_objects for key in obj}

    report = {
        "baseline": baseline_path.name,
        "candidate": candidate_path.name,
        "compatible_structure": not errors,
        "header_exact": header_match,
        "source_prefix_exact": prefix_match,
        "baseline_objects": len(b_records),
        "candidate_objects": len(c_records),
        "added_objects": len(c_records) - len(b_records),
        "declared_k48": declared,
        "candidate_file_bytes": candidate_path.stat().st_size,
        "baseline_decoded_chars": b_chars,
        "candidate_decoded_chars": c_chars,
        "z_layers": dict(sorted(z_counts.items(), key=lambda item: int(item[0]))),
        "unrecognized_z_layers": invalid_z,
        "new_object_ids": sorted(candidate_ids - baseline_ids, key=lambda value: int(value) if value.isdigit() else 10**9),
        "new_object_keys": sorted(candidate_keys - baseline_keys),
        "errors": errors,
        "warnings": warnings,
        "evidence_limit": "A passing report does not prove Geometry Dash import, runtime triggers, collision, sync, or playability.",
    }
    output = json.dumps(report, indent=2)
    if args.json:
        Path(args.json).write_text(output, encoding="utf-8")
    print(output)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
