#!/usr/bin/env python3
"""Lossless-wrapper GDShare decoder/encoder.

GDShare's importer is stricter than a generic XML parser. Human exports in the
reference corpus are compact, single-line documents with an exact XML prologue.
Do not serialize a parsed tree: splice only explicitly requested values into the
original bytes so declarations, whitespace, ordering, tags, and unknown data stay
byte-for-byte unchanged.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path


CANONICAL_PREFIX = b'<?xml version="1.0"?><plist version="1.0" gjver="2.0"><dict>'
CANONICAL_SUFFIX = b"</dict></plist>"


def base64_contract(encoded: str) -> list[str]:
    """Return fatal errors for the corpus-proven k4 Base64 representation.

    Python's URL-safe decoder accepts repaired padding. Geometry Dash did not
    accept three generated files whose required trailing ``=`` was stripped.
    Validation must therefore inspect the serialized value before decoding it.
    """
    errors: list[str] = []
    try:
        raw = encoded.encode("ascii")
    except UnicodeEncodeError:
        return ["Base64 value is not ASCII"]
    if not raw:
        return ["Base64 value is empty"]
    if len(raw) % 4:
        errors.append(
            f"Base64 length {len(raw)} is not divisible by 4; required padding was stripped"
        )
    padding = len(raw) - len(raw.rstrip(b"="))
    if padding > 2:
        errors.append(f"Base64 has {padding} trailing padding characters; at most 2 are valid")
    body = raw[:-padding] if padding else raw
    if b"=" in body:
        errors.append("Base64 padding appears before the end of the value")
    allowed = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    invalid = sorted(set(body) - set(allowed))
    if invalid:
        errors.append(f"Base64 contains invalid URL-safe bytes: {invalid}")
    if errors:
        return errors
    try:
        decoded = base64.b64decode(raw, altchars=b"-_", validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        return [f"Base64 decode failed: {exc}"]
    if base64.urlsafe_b64encode(decoded) != raw:
        errors.append("Base64 is not in canonical padded URL-safe form")
    return errors


def pairs(path: Path):
    root = ET.parse(path).getroot()
    node = root.find("dict")
    if node is None:
        raise ValueError("missing plist/dict")
    children = list(node)
    if len(children) % 2:
        raise ValueError("odd number of plist dictionary nodes")
    for index in range(0, len(children), 2):
        if children[index].tag != "k":
            raise ValueError(f"dictionary node {index} is not a <k>")
    return root, node, children


def typed_values(path: Path) -> list[tuple[str, str, str]]:
    _, _, children = pairs(path)
    return [
        (children[index].text or "", children[index + 1].tag,
         children[index + 1].text or "")
        for index in range(0, len(children), 2)
    ]


def get_value(children, key):
    for index in range(0, len(children), 2):
        if children[index].text == key:
            return children[index + 1].text or ""
    raise KeyError(key)


def get_typed_value(path: Path, key: str) -> tuple[str, str]:
    matches = [(tag, value) for name, tag, value in typed_values(path) if name == key]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {key!r} entry; found {len(matches)}")
    return matches[0]


def wrapper_contract(raw: bytes) -> tuple[list[str], list[str]]:
    """Return fatal errors and cautions for the observed GDShare byte contract."""
    errors, warnings = [], []
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append("UTF-8 BOM is not present in known-good GDShare exports")
    if not raw.startswith(CANONICAL_PREFIX):
        errors.append("wrapper does not use the known-good exact compact XML prologue")
    if not raw.endswith(CANONICAL_SUFFIX):
        errors.append("wrapper does not end exactly with </dict></plist>")
    if b"\r" in raw or b"\n" in raw:
        errors.append("wrapper contains line breaks; known-good exports are single-line")
    try:
        raw.decode("ascii")
    except UnicodeDecodeError:
        warnings.append("wrapper is not pure ASCII; verify target importer behavior")
    return errors, warnings


def _value_pattern(key: str) -> re.Pattern[bytes]:
    key_bytes = re.escape(key.encode("ascii"))
    return re.compile(
        rb"(?P<open><k>" + key_bytes +
        rb"</k><(?P<tag>[A-Za-z][A-Za-z0-9]*)>)(?P<value>.*?)(?P<close></(?P=tag)>)",
        re.DOTALL,
    )


def replace_existing_value(raw: bytes, key: str, value: str,
                           expected_tag: str | None = None) -> bytes:
    """Replace one existing scalar without changing any other byte."""
    pattern = _value_pattern(key)
    matches = list(pattern.finditer(raw))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one serialized {key!r}; found {len(matches)}")
    match = matches[0]
    tag = match.group("tag").decode("ascii")
    if expected_tag is not None and tag != expected_tag:
        raise ValueError(f"{key!r} has <{tag}> but <{expected_tag}> was required")
    escaped = html.escape(str(value), quote=False).encode("ascii", "xmlcharrefreplace")
    return raw[:match.start("value")] + escaped + raw[match.end("value"):]


def decode(encoded: str) -> str:
    errors = base64_contract(encoded)
    if errors:
        raise ValueError("; ".join(errors))
    compressed = base64.b64decode(encoded.encode("ascii"), altchars=b"-_", validate=True)
    return gzip.decompress(compressed).decode("utf-8")


def repair_missing_padding(encoded: str) -> str:
    """Repair only missing terminal padding after proving gzip/UTF-8 integrity."""
    if "=" in encoded:
        raise ValueError("repair accepts only an unpadded Base64 value")
    missing = (-len(encoded)) % 4
    if missing not in (1, 2):
        raise ValueError("value does not have a repairable Base64 padding deficit")
    repaired = encoded + "=" * missing
    # Strict decode verifies alphabet, canonical representation, gzip CRC and UTF-8.
    decode(repaired)
    return repaired


def encode(level: str) -> str:
    compressed = gzip.compress(level.encode("utf-8"), compresslevel=9, mtime=0)
    # Keep RFC 4648 padding. Every supplied working export has len(k4) % 4 == 0.
    return base64.urlsafe_b64encode(compressed).decode("ascii")


def object_count(level: str) -> int:
    return len([record for record in level.split(";")[1:] if record])


def encode_into_template(template: Path, level: str, *, name: str | None = None) -> bytes:
    """Encode into a proven wrapper while preserving its byte grammar exactly."""
    raw = template.read_bytes()
    errors, _ = wrapper_contract(raw)
    if errors:
        raise ValueError("unsafe template wrapper: " + "; ".join(errors))
    raw = replace_existing_value(raw, "k4", encode(level), "s")
    raw = replace_existing_value(raw, "k48", str(object_count(level)), "i")
    if name is not None:
        raw = replace_existing_value(raw, "k2", name, "s")
    return raw


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    decode_parser = sub.add_parser("decode")
    decode_parser.add_argument("gmd")
    decode_parser.add_argument("output")
    encode_parser = sub.add_parser("encode")
    encode_parser.add_argument("template")
    encode_parser.add_argument("level_string")
    encode_parser.add_argument("output")
    encode_parser.add_argument("--name")
    clone_parser = sub.add_parser("clone")
    clone_parser.add_argument("source")
    clone_parser.add_argument("output")
    clone_parser.add_argument("--name", required=True)
    inspect_parser = sub.add_parser("inspect-wrapper")
    inspect_parser.add_argument("gmd")
    repair_parser = sub.add_parser("repair-padding")
    repair_parser.add_argument("source")
    repair_parser.add_argument("output")
    repair_parser.add_argument("--name")
    args = parser.parse_args()

    if args.cmd == "decode":
        _, _, children = pairs(Path(args.gmd))
        Path(args.output).write_text(decode(get_value(children, "k4")), encoding="utf-8")
    elif args.cmd == "clone":
        source = Path(args.source)
        raw = replace_existing_value(source.read_bytes(), "k2", args.name, "s")
        Path(args.output).write_bytes(raw)
    elif args.cmd == "encode":
        level = Path(args.level_string).read_text(encoding="utf-8")
        raw = encode_into_template(Path(args.template), level, name=args.name)
        Path(args.output).write_bytes(raw)
    elif args.cmd == "repair-padding":
        source = Path(args.source)
        tag, encoded = get_typed_value(source, "k4")
        if tag != "s":
            raise ValueError(f"k4 uses <{tag}> instead of <s>")
        repaired = repair_missing_padding(encoded)
        raw = replace_existing_value(source.read_bytes(), "k4", repaired, "s")
        if args.name is not None:
            raw = replace_existing_value(raw, "k2", args.name, "s")
        Path(args.output).write_bytes(raw)
    else:
        path = Path(args.gmd)
        errors, warnings = wrapper_contract(path.read_bytes())
        try:
            _, encoded = get_typed_value(path, "k4")
            errors.extend(base64_contract(encoded))
            if not errors:
                decode(encoded)
        except (ET.ParseError, KeyError, ValueError, OSError, UnicodeError) as exc:
            errors.append(f"k4 parse/decode failed: {exc}")
        print(f"file={path.name}")
        print(f"known_good_wrapper={str(not errors).lower()}")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARNING: {item}")
        return 1 if errors else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
