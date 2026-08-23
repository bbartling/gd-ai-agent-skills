#!/usr/bin/env python3
"""Fail-closed release gate for generated GDShare candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit_gmd_corpus import audit
from gmd_codec import decode, get_typed_value, typed_values


def records(path: Path) -> tuple[str, list[str]]:
    _, encoded = get_typed_value(path, "k4")
    chunks = decode(encoded).split(";")
    return chunks[0], [record for record in chunks[1:] if record]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate")
    parser.add_argument("--container-template", required=True)
    parser.add_argument("--content-baseline")
    parser.add_argument("--max-objects", type=int, default=65535)
    parser.add_argument("--json")
    args = parser.parse_args()

    candidate = Path(args.candidate)
    template = Path(args.container_template)
    base = audit(candidate)
    errors, warnings = list(base["errors"]), list(base["warnings"])

    candidate_entries = typed_values(candidate)
    template_entries = typed_values(template)
    candidate_shape = [(key, tag) for key, tag, _ in candidate_entries]
    template_shape = [(key, tag) for key, tag, _ in template_entries]
    shape_exact = candidate_shape == template_shape
    if not shape_exact:
        errors.append("outer key order/type shape differs from the proven container template")

    allowed = {"k2", "k4", "k48"}
    candidate_map = {key: value for key, _, value in candidate_entries}
    template_map = {key: value for key, _, value in template_entries}
    unexpected = [key for key in template_map
                  if key not in allowed and candidate_map.get(key) != template_map[key]]
    if unexpected:
        errors.append(f"template metadata changed outside allowed keys: {unexpected}")
    if "k1" not in template_map and "k1" in candidate_map:
        errors.append("candidate reintroduced an online level ID into a local template")
    local_identity = "k1" not in candidate_map

    candidate_header, candidate_records = records(candidate)
    if len(candidate_records) > args.max_objects:
        errors.append(f"decoded count {len(candidate_records)} exceeds {args.max_objects}")
    declared = candidate_map.get("k48")
    if declared != str(len(candidate_records)):
        errors.append(f"generated candidate requires exact k48; got {declared!r}")

    header_exact = None
    source_prefix_exact = None
    if args.content_baseline:
        baseline_header, baseline_records = records(Path(args.content_baseline))
        header_exact = candidate_header == baseline_header
        source_prefix_exact = candidate_records[:len(baseline_records)] == baseline_records
        if not header_exact:
            errors.append("level header differs from the importable content baseline")
        if not source_prefix_exact:
            errors.append("importable baseline objects are not an exact candidate prefix")

    report = {
        "candidate": candidate.name,
        "passed": not errors,
        "known_good_wrapper": base["wrapper_exact"],
        "outer_shape_exact": shape_exact,
        "template_metadata_unchanged": not unexpected,
        "local_identity": local_identity,
        "objects": len(candidate_records),
        "declared_k48": declared,
        "header_exact": header_exact,
        "source_prefix_exact": source_prefix_exact,
        "errors": errors,
        "warnings": warnings,
        "evidence_limit": "PASS means statically release-gated, not imported, played, or verified in Geometry Dash.",
    }
    rendered = json.dumps(report, indent=2)
    if args.json:
        Path(args.json).write_text(rendered, encoding="utf-8")
    print(rendered)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
