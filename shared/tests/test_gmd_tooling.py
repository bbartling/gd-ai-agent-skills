#!/usr/bin/env python3
"""Regression tests for GDShare wrapper preservation."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from gmd_codec import (CANONICAL_PREFIX, decode, encode, encode_into_template,
                       replace_existing_value, wrapper_contract)


LEVEL = "kS38,1_40_2_125_3_255,kA11,0;1,1,2,348.778,3,16.1111,155,1;"


def wrapper(level: str = LEVEL) -> bytes:
    return (
        CANONICAL_PREFIX +
        b"<k>kCEK</k><i>4</i>" +
        b"<k>k2</k><s>OneBlockTest</s>" +
        b"<k>k4</k><s>" + encode(level).encode("ascii") + b"</s>" +
        b"<k>k48</k><i>1</i>" +
        b"<k>k34</k><s>UNCHANGED</s></dict></plist>"
    )


class GMDToolingTests(unittest.TestCase):
    def test_known_good_wrapper_contract(self):
        errors, warnings = wrapper_contract(wrapper())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_generic_xml_declaration_and_newline_fail(self):
        broken = wrapper().replace(
            b'<?xml version="1.0"?>',
            b"<?xml version='1.0' encoding='utf-8'?>\n",
            1,
        )
        errors, _ = wrapper_contract(broken)
        self.assertTrue(any("prologue" in item for item in errors))
        self.assertTrue(any("line breaks" in item for item in errors))

    def test_same_value_splice_is_byte_exact(self):
        original = wrapper()
        self.assertEqual(
            replace_existing_value(original, "k2", "OneBlockTest", "s"),
            original,
        )

    def test_unicode_name_stays_ascii_xml(self):
        updated = replace_existing_value(wrapper(), "k2", "Cheese Moon — V3", "s")
        self.assertIn(b"Cheese Moon &#8212; V3", updated)
        updated.decode("ascii")

    def test_template_encode_changes_only_allowed_values(self):
        original = wrapper()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "template.gmd"
            path.write_bytes(original)
            output = encode_into_template(path, LEVEL + "1,8,2,600,3,30;", name="V3")
        self.assertTrue(output.startswith(CANONICAL_PREFIX))
        self.assertNotIn(b"\n", output)
        self.assertIn(b"<k>k2</k><s>V3</s>", output)
        self.assertIn(b"<k>k48</k><i>2</i>", output)
        self.assertIn(b"<k>k34</k><s>UNCHANGED</s>", output)

    def test_payload_roundtrip_is_semantically_exact(self):
        self.assertEqual(decode(encode(LEVEL)), LEVEL)


if __name__ == "__main__":
    unittest.main()
