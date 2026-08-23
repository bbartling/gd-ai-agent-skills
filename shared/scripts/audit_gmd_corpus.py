#!/usr/bin/env python3
"""Audit one or more GDShare files against corpus-derived import invariants."""
from __future__ import annotations

import argparse
import csv
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

from gmd_codec import (decode, encode, get_typed_value, replace_existing_value,
                       typed_values, wrapper_contract)


def gather(items: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in items:
        path = Path(item)
        paths.extend(sorted(child for child in path.iterdir() if child.is_file())
                     if path.is_dir() else [path])
    return paths


def audit(path: Path) -> dict:
    errors, warnings = wrapper_contract(path.read_bytes())
    result = {
        "file": path.name,
        "bytes": path.stat().st_size,
        "wrapper_exact": not errors,
        "encoding": None,
        "objects": 0,
        "declared_k48": None,
        "k48_status": None,
        "header_chars": 0,
        "trailing_semicolon": False,
        "same_value_splice_byte_exact": False,
        "payload_semantic_roundtrip": False,
        "has_online_level_id": False,
        "opaque_object_keys": [],
        "errors": list(errors),
        "warnings": list(warnings),
    }
    try:
        entries = typed_values(path)
        keys = [key for key, _, _ in entries]
        duplicates = sorted({key for key in keys if keys.count(key) > 1})
        if duplicates:
            result["errors"].append(f"duplicate outer keys: {duplicates}")
        result["has_online_level_id"] = "k1" in keys
        tag, encoded = get_typed_value(path, "k4")
        if tag != "s":
            result["errors"].append(f"k4 uses <{tag}> instead of <s>")
        result["encoding"] = "urlsafe-base64+gzip"
        level = decode(encoded)
        result["payload_semantic_roundtrip"] = decode(encode(level)) == level
        records = [record for record in level.split(";")[1:] if record]
        result["objects"] = len(records)
        result["header_chars"] = len(level.split(";", 1)[0])
        result["trailing_semicolon"] = level.endswith(";")
        if not result["trailing_semicolon"]:
            result["errors"].append("inner level string has no trailing semicolon")
        opaque_keys: set[str] = set()
        for index, record in enumerate(records, 1):
            fields = record.split(",")
            if len(fields) % 2:
                result["errors"].append(f"object {index} has an odd key/value field count")
                break
            if not fields or fields[0] != "1":
                result["errors"].append(f"object {index} does not begin with object-ID key 1")
                break
            for key, value in zip(fields[0::2], fields[1::2]):
                if not key.lstrip("-").isdigit():
                    opaque_keys.add(key)
                    continue
                if key in {"2", "3"}:
                    try:
                        if not math.isfinite(float(value)):
                            raise ValueError
                    except ValueError:
                        result["errors"].append(f"object {index} has invalid coordinate {value!r}")
                        break
        result["opaque_object_keys"] = sorted(opaque_keys)
        if opaque_keys:
            result["warnings"].append(
                f"preserve corpus-observed opaque object keys: {sorted(opaque_keys)}")
        outer = {key: value for key, _, value in entries}
        declared = outer.get("k48")
        result["declared_k48"] = declared
        if declared is None:
            result["k48_status"] = "absent"
        elif declared.isdigit() and int(declared) == len(records):
            result["k48_status"] = "exact"
        elif declared == "65535" and len(records) > 65535:
            result["k48_status"] = "known-cap"
            result["warnings"].append("k48 uses the observed 65,535 high-object cap")
        else:
            result["k48_status"] = "mismatch"
            result["warnings"].append(
                f"k48={declared!r} differs from decoded count {len(records)}")

        raw = path.read_bytes()
        for key in ("k2", "k4", "k48"):
            matches = [(tag, value) for name, tag, value in entries if name == key]
            if matches:
                tag, value = matches[0]
                raw = replace_existing_value(raw, key, value, tag)
        result["same_value_splice_byte_exact"] = raw == path.read_bytes()
        if not result["same_value_splice_byte_exact"]:
            result["errors"].append("lossless same-value splice changed wrapper bytes")
    except (ET.ParseError, KeyError, ValueError, OSError, UnicodeError) as exc:
        result["errors"].append(f"parse/decode failed: {exc}")
    result["valid"] = not result["errors"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--json")
    parser.add_argument("--csv")
    args = parser.parse_args()
    reports = [audit(path) for path in gather(args.inputs)]
    summary = {
        "files": len(reports),
        "passed": sum(item["valid"] for item in reports),
        "failed": sum(not item["valid"] for item in reports),
        "reports": reports,
        "evidence_limit": "Static corpus checks do not prove Geometry Dash import, runtime behavior, or playability.",
    }
    rendered = json.dumps(summary, indent=2)
    if args.json:
        Path(args.json).write_text(rendered, encoding="utf-8")
    if args.csv:
        with Path(args.csv).open("w", newline="", encoding="utf-8") as handle:
            fields = ["file", "bytes", "valid", "wrapper_exact", "encoding", "objects",
                      "declared_k48", "k48_status", "header_chars", "trailing_semicolon",
                      "same_value_splice_byte_exact", "payload_semantic_roundtrip",
                      "has_online_level_id", "error_count", "warning_count"]
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for item in reports:
                row = {key: item.get(key) for key in fields}
                row["error_count"] = len(item["errors"])
                row["warning_count"] = len(item["warnings"])
                writer.writerow(row)
    print(rendered)
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
