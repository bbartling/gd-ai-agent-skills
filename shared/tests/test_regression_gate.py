#!/usr/bin/env python3
"""Red/green regression coverage for blank-level Base64 failures."""
from __future__ import annotations

import sys
import tempfile
import unittest
import json
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from audit_gmd_corpus import audit
from gate_gmd_release import release_gate
from gmd_codec import (CANONICAL_PREFIX, encode, encode_into_template,
                       replace_existing_value)
from run_gmd_regression_gate import check_manifest


LEVEL = (
    "kS38,1_40_2_125_3_255,kA11,0;"
    "1,1,2,348.778,3,16.1111,155,1;"
    "1,8,2,450,3,15,6,0,96,1,64,1,67,1,155,18;"
)


def wrapper(encoded: str, count: int = 2) -> bytes:
    return (
        CANONICAL_PREFIX
        + b"<k>kCEK</k><i>4</i>"
        + b"<k>k2</k><s>Regression</s>"
        + b"<k>k4</k><s>" + encoded.encode("ascii") + b"</s>"
        + b"<k>k48</k><i>" + str(count).encode("ascii") + b"</i>"
        + b"<k>k34</k><s>UNCHANGED</s></dict></plist>"
    )


class RegressionGateTests(unittest.TestCase):
    def test_historical_stripped_padding_is_known_bad(self):
        padded = encode(LEVEL)
        self.assertTrue(padded.endswith("="), "regression fixture must require padding")
        with tempfile.TemporaryDirectory() as directory:
            broken = Path(directory) / "broken.gmd"
            broken.write_bytes(wrapper(padded.rstrip("=")))
            report = audit(broken)
        self.assertFalse(report["valid"])
        self.assertTrue(any("padding was stripped" in item for item in report["errors"]))

    def test_known_good_padded_payload_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            good = Path(directory) / "good.gmd"
            good.write_bytes(wrapper(encode(LEVEL)))
            report = audit(good)
        self.assertTrue(report["valid"], report["errors"])
        self.assertTrue(report["k4_base64_canonical"])
        self.assertEqual(report["k4_base64_length_mod4"], 0)

    def test_release_gate_cannot_score_around_codec_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            template = Path(directory) / "template.gmd"
            candidate = Path(directory) / "candidate.gmd"
            template.write_bytes(wrapper(encode(LEVEL)))
            candidate.write_bytes(encode_into_template(template, LEVEL, name="Candidate"))
            raw = candidate.read_bytes()
            padded = encode(LEVEL)
            self.assertTrue(padded.endswith("="), "regression fixture must require padding")
            raw = replace_existing_value(raw, "k4", padded.rstrip("="), "s")
            candidate.write_bytes(raw)
            report = release_gate(candidate, template, content_baseline=template)
        self.assertFalse(report["passed"])
        self.assertFalse(report["canonical_padded_k4"])
        self.assertTrue(any("padding was stripped" in item for item in report["errors"]))

    def test_manifest_locks_corpus_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.json"
            manifest.write_text(json.dumps({
                "known_good": [{"file": "good.gmd", "sha256": "abc"}],
                "known_bad": [{"file": "bad.gmd", "sha256": "def"}],
            }), encoding="utf-8")
            passed = check_manifest(
                manifest,
                [{"file": "good.gmd", "sha256": "abc"}],
                [{"file": "bad.gmd", "sha256": "def"}],
            )
            failed = check_manifest(
                manifest,
                [{"file": "good.gmd", "sha256": "changed"}],
                [{"file": "bad.gmd", "sha256": "def"}],
            )
        self.assertTrue(passed["passed"])
        self.assertFalse(failed["passed"])
        self.assertTrue(any("SHA-256 mismatch" in item for item in failed["errors"]))


if __name__ == "__main__":
    unittest.main()
