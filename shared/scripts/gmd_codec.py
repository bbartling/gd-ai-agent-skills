#!/usr/bin/env python3
"""Loss-conscious GDShare decoder/encoder.

Never edits an original unless the caller explicitly chooses the same output.
Unknown outer plist entries and unknown inner object keys are preserved.
"""
from __future__ import annotations
import argparse, base64, gzip, xml.etree.ElementTree as ET
from pathlib import Path

def pairs(path: Path):
    root = ET.parse(path).getroot(); node = root.find("dict")
    if node is None: raise ValueError("missing plist/dict")
    return root, node, list(node)

def get_value(children, key):
    for i in range(0, len(children), 2):
        if children[i].text == key: return children[i+1].text or ""
    raise KeyError(key)

def set_value(node, children, key, value, tag="s"):
    for i in range(0, len(children), 2):
        if children[i].text == key:
            children[i+1].text = str(value); return
    ET.SubElement(node, "k").text = key
    ET.SubElement(node, tag).text = str(value)

def decode(encoded):
    encoded += "=" * ((4-len(encoded)%4)%4)
    return gzip.decompress(base64.urlsafe_b64decode(encoded)).decode()

def encode(level):
    return base64.urlsafe_b64encode(gzip.compress(level.encode(), mtime=0)).decode().rstrip("=")

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    d=sub.add_parser("decode"); d.add_argument("gmd"); d.add_argument("output")
    e=sub.add_parser("encode"); e.add_argument("template"); e.add_argument("level_string"); e.add_argument("output"); e.add_argument("--name")
    c=sub.add_parser("clone"); c.add_argument("source"); c.add_argument("output"); c.add_argument("--name",required=True)
    a=ap.parse_args()
    if a.cmd=="decode":
        _,_,ch=pairs(Path(a.gmd)); Path(a.output).write_text(decode(get_value(ch,"k4")),encoding="utf-8")
    elif a.cmd=="clone":
        root,node,ch=pairs(Path(a.source)); set_value(node,ch,"k2",a.name); ET.ElementTree(root).write(a.output,encoding="utf-8",xml_declaration=True)
    else:
        root,node,ch=pairs(Path(a.template)); level=Path(a.level_string).read_text(encoding="utf-8")
        set_value(node,ch,"k4",encode(level)); set_value(node,ch,"k48",max(0,level.count(";")-1),"i")
        if a.name: set_value(node,ch,"k2",a.name)
        ET.ElementTree(root).write(a.output,encoding="utf-8",xml_declaration=True)
    return 0
if __name__=="__main__": raise SystemExit(main())
