#!/usr/bin/env python3
"""Structural and heuristic validator for GDShare files; no GD physics claim."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from analyze_gmd import decode_level, parse_object, plist_pairs, TRIGGERS

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("gmd"); ap.add_argument("--json"); a=ap.parse_args()
    errors=[]; warnings=[]; p=Path(a.gmd)
    try: outer=plist_pairs(p)
    except Exception as e: errors.append(f"outer plist unreadable: {e}"); outer={}
    data=""
    if outer:
        if "k4" not in outer: errors.append("missing k4 level payload")
        else:
            try: data=decode_level(outer["k4"])
            except Exception as e: errors.append(f"k4 decode failed: {e}")
    objects=[]
    if data:
        chunks=data.split(";")
        if not chunks[0].startswith("kS38,"): warnings.append("unexpected or newer header prefix; preserve it exactly")
        for index,chunk in enumerate(chunks[1:],1):
            if not chunk: continue
            fields=chunk.split(",")
            if len(fields)%2: errors.append(f"object {index}: odd key/value field count")
            o=parse_object(chunk); objects.append(o)
            if 1 not in o: errors.append(f"object {index}: missing object id key 1")
            for key in (2,3):
                if key in o:
                    try:
                        if not math.isfinite(float(o[key])): raise ValueError
                    except ValueError: errors.append(f"object {index}: invalid coordinate key {key}")
    groups=set(); targeted=[]; trigger_count=0
    for o in objects:
        groups.update(g for g in o.get(57,"").split(".") if g)
        try: oid=int(o.get(1,-1))
        except ValueError: oid=-1
        if oid in TRIGGERS:
            trigger_count+=1
            if 51 in o and o[51] not in ("","0"): targeted.append(o[51])
    missing=sorted(set(targeted)-groups,key=lambda x:int(x) if x.isdigit() else 10**9)
    if missing: warnings.append(f"{len(missing)} targeted group IDs have no visible key-57 member; may be intentional dynamic/trigger groups")
    declared=outer.get("k48")
    if declared and declared.isdigit() and int(declared)!=len(objects):
        if int(declared)==65535 and len(objects)>65535:
            warnings.append(
                f"k48 is capped at 65535 while decoded count is {len(objects)}; "
                "this occurs in some high-object references, but target-version import/save/re-export is still required"
            )
        else:
            warnings.append(f"k48 says {declared}; decoded count is {len(objects)}")
    report={"file":p.name,"valid_structure":not errors,"objects":len(objects),"triggers":trigger_count,
            "groups":len(groups),"unresolved_target_groups":missing[:100],"errors":errors[:100],"warnings":warnings}
    text=json.dumps(report,indent=2)
    if a.json: Path(a.json).write_text(text,encoding="utf-8")
    print(text); return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())
