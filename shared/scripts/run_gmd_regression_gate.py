#!/usr/bin/env python3
"""Run one release gate plus known-good/known-bad GDShare regressions."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_gmd_corpus import audit, gather
from gate_gmd_release import release_gate


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def case(path: Path, expected: str, required_error: str | None = None) -> dict:
    report = audit(path)
    observed = "pass" if report["valid"] else "fail"
    expectation_met = observed == expected
    if expected == "fail" and required_error:
        expectation_met = expectation_met and any(
            required_error in error for error in report["errors"]
        )
    return {
        "file": path.name,
        "sha256": digest(path),
        "expected": expected,
        "observed": observed,
        "expectation_met": expectation_met,
        "required_error": required_error,
        "objects": report["objects"],
        "k4_length_mod4": report["k4_base64_length_mod4"],
        "k4_padding_chars": report["k4_padding_chars"],
        "errors": report["errors"],
        "warnings": report["warnings"],
    }


def check_manifest(path: Path, good_cases: list[dict], bad_cases: list[dict]) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for key, observed_cases in (("known_good", good_cases), ("known_bad", bad_cases)):
        expected = {item["file"]: item["sha256"] for item in data.get(key, [])}
        observed = {item["file"]: item["sha256"] for item in observed_cases}
        missing = sorted(set(expected) - set(observed))
        unexpected = sorted(set(observed) - set(expected))
        mismatched = sorted(
            name for name in set(expected) & set(observed)
            if expected[name] != observed[name]
        )
        if missing:
            errors.append(f"{key} missing manifest files: {missing}")
        if unexpected:
            errors.append(f"{key} has unexpected files: {unexpected}")
        if mismatched:
            errors.append(f"{key} SHA-256 mismatch: {mismatched}")
    return {"file": str(path), "passed": not errors, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--container-template", required=True)
    parser.add_argument("--content-baseline")
    parser.add_argument("--max-objects", type=int, default=65535)
    parser.add_argument("--known-good", nargs="+", required=True)
    parser.add_argument("--known-bad", nargs="+", required=True)
    parser.add_argument("--known-bad-error", default="padding was stripped")
    parser.add_argument("--manifest")
    parser.add_argument("--json")
    args = parser.parse_args()

    candidate = Path(args.candidate)
    release = release_gate(
        candidate,
        Path(args.container_template),
        content_baseline=Path(args.content_baseline) if args.content_baseline else None,
        max_objects=args.max_objects,
    )
    good_cases = [case(path, "pass") for path in gather(args.known_good)]
    bad_cases = [
        case(path, "fail", args.known_bad_error)
        for path in gather(args.known_bad)
    ]
    manifest = (
        check_manifest(Path(args.manifest), good_cases, bad_cases)
        if args.manifest else {"file": None, "passed": True, "errors": []}
    )
    passed = (
        release["passed"]
        and manifest["passed"]
        and all(item["expectation_met"] for item in good_cases)
        and all(item["expectation_met"] for item in bad_cases)
    )
    report = {
        "passed": passed,
        "candidate_release_gate": release,
        "manifest": manifest,
        "known_good": {
            "passed": sum(item["expectation_met"] for item in good_cases),
            "total": len(good_cases),
            "cases": good_cases,
        },
        "known_bad": {
            "passed": sum(item["expectation_met"] for item in bad_cases),
            "total": len(bad_cases),
            "cases": bad_cases,
        },
        "evidence_limit": (
            "Static regression PASS does not replace a Geometry Dash import/open test. "
            "A known-bad file passes only when the gate rejects it for the required reason."
        ),
    }
    rendered = json.dumps(report, indent=2)
    if args.json:
        Path(args.json).write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
