#!/usr/bin/env python3
"""Compare two GDShare files at useful structural levels."""
import argparse, json
from pathlib import Path
from analyze_gmd import profile

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("before"); ap.add_argument("after"); a=ap.parse_args()
    x,y=profile(Path(a.before)),profile(Path(a.after))
    keys=[("objects","object_count"),("triggers","trigger_count"),("unique_ids","unique_object_ids")]
    out={name:{"before":x[k],"after":y[k],"delta":y[k]-x[k]} for name,k in keys}
    for name,path in [("groups",("grouping","unique_groups")),("high_detail",("layering","high_detail"))]:
        a0=x[path[0]][path[1]]; b0=y[path[0]][path[1]]; out[name]={"before":a0,"after":b0,"delta":b0-a0}
    out["trigger_counts_before"]=x["trigger_counts"]; out["trigger_counts_after"]=y["trigger_counts"]
    print(json.dumps(out,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
