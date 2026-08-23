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


def release_gate(candidate: Path, template: Path, *,
                 content_baseline: Path | None = None,
                 max_objects: int = 65535) -> dict:
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

    payload_available = True
    try:
        candidate_header, candidate_records = records(candidate)
    except (KeyError, ValueError, OSError, UnicodeError) as exc:
        payload_available = False
        candidate_header, candidate_records = "", []
        errors.append(f"candidate payload unavailable to release gate: {exc}")
    if len(candidate_records) > max_objects:
        errors.append(f"decoded count {len(candidate_records)} exceeds {max_objects}")
    declared = candidate_map.get("k48")
    if declared != str(len(candidate_records)):
        errors.append(f"generated candidate requires exact k48; got {declared!r}")

    header_exact = None
    source_prefix_exact = None
    if content_baseline:
        baseline_header, baseline_records = records(content_baseline)
        header_exact = payload_available and candidate_header == baseline_header
        source_prefix_exact = (
            payload_available
            and candidate_records[:len(baseline_records)] == baseline_records
        )
        if not header_exact:
            errors.append("level header differs from the importable content baseline")
        if not source_prefix_exact:
            errors.append("importable baseline objects are not an exact candidate prefix")

    return {
        "candidate": candidate.name,
        "passed": not errors,
        "known_good_wrapper": base["wrapper_exact"],
        "canonical_padded_k4": base["k4_base64_canonical"],
        "k4_length_mod4": base["k4_base64_length_mod4"],
        "k4_padding_chars": base["k4_padding_chars"],
        "k4_gzip_utf8_valid": base["k4_gzip_utf8_valid"],
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate")
    parser.add_argument("--container-template", required=True)
    parser.add_argument("--content-baseline")
    parser.add_argument("--max-objects", type=int, default=65535)
    parser.add_argument("--json")
    args = parser.parse_args()

    report = release_gate(
        Path(args.candidate),
        Path(args.container_template),
        content_baseline=Path(args.content_baseline) if args.content_baseline else None,
        max_objects=args.max_objects,
    )
    rendered = json.dumps(report, indent=2)
    if args.json:
        Path(args.json).write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
