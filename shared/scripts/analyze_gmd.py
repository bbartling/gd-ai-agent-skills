#!/usr/bin/env python3
"""Decode and statistically profile GDShare .gmd files using only stdlib.

The parser intentionally preserves unknown numeric object properties. Geometry
Dash evolves, so silently discarding unknown keys is unsafe.
"""
from __future__ import annotations

import argparse
import base64
import csv
import gzip
import json
import math
import statistics
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

TRIGGERS = {
    899: "color", 901: "move", 1006: "pulse", 1007: "alpha",
    1049: "toggle", 1268: "spawn", 1346: "rotate", 1347: "follow",
    1520: "shake", 1585: "animate", 1595: "touch", 1611: "count",
    1612: "player_hide", 1613: "player_show", 1616: "stop",
    1811: "instant_count", 1812: "on_death", 1814: "follow_player_y",
    1815: "collision", 1816: "collision_block", 1817: "pickup",
    1818: "bg_effect_enable", 1819: "bg_effect_disable", 1912: "random",
    1913: "zoom_camera", 1914: "static_camera", 1916: "offset_camera",
    1917: "reverse", 1932: "player_control", 1934: "song",
    1935: "timewarp", 2015: "rotate_camera", 2016: "camera_guide",
    2062: "camera_edge", 2063: "checkpoint", 2066: "gravity",
    2067: "scale", 2068: "advanced_random", 2899: "options",
    2900: "arrow", 2901: "gameplay_offset", 2903: "gradient",
    2925: "camera_mode", 2999: "edit_middleground", 3006: "area_move",
    3007: "area_rotate", 3008: "area_scale", 3009: "area_fade",
    3010: "area_tint", 3011: "edit_area_move", 3012: "edit_area_rotate",
    3013: "edit_area_scale", 3014: "edit_area_fade", 3015: "edit_area_tint",
    3016: "advanced_follow", 3022: "teleport", 3024: "area_stop",
    3029: "change_background", 3030: "change_ground", 3031: "change_middleground",
    3032: "keyframe", 3033: "animate_keyframe", 3600: "end",
    3602: "sfx", 3603: "edit_sfx", 3604: "event", 3605: "song_edit",
    3606: "background_speed", 3607: "sequence", 3608: "spawn_particle",
    3609: "instant_collision", 3612: "middleground_speed", 3613: "ui",
    3614: "time", 3615: "time_event", 3617: "time_control",
    3618: "reset", 3619: "item_edit", 3620: "item_compare",
    3640: "state_block", 3641: "item_persist", 3642: "bpm",
    3643: "toggle_block", 3645: "force_circle", 3655: "object_control",
    3660: "edit_advanced_follow", 3661: "retarget_advanced_follow",
    3662: "link_visible",
}

GAMEPLAY_IDS = {
    10: "gravity_normal", 11: "gravity_inverted", 12: "cube_portal",
    13: "ship_portal", 31: "start_position", 35: "yellow_pad",
    36: "yellow_orb", 45: "mirror_enter", 46: "mirror_exit",
    47: "ball_portal", 67: "blue_pad", 84: "blue_orb", 99: "size_normal",
    101: "size_small", 111: "ufo_portal", 140: "pink_pad",
    141: "pink_orb", 200: "speed_slow", 201: "speed_normal",
    202: "speed_fast", 203: "speed_very_fast", 286: "dual_enter",
    287: "dual_exit", 660: "wave_portal", 745: "robot_portal",
    1022: "green_orb", 1330: "black_orb", 1331: "spider_portal",
    1332: "red_pad", 1333: "red_orb", 1334: "speed_super_fast",
    1594: "toggle_orb", 1704: "green_dash_orb", 1751: "pink_dash_orb",
    1933: "swing_portal", 2926: "gravity_toggle", 3004: "spider_orb",
    3005: "spider_pad", 3027: "teleport_orb",
}


def plist_pairs(path: Path) -> dict[str, str]:
    root = ET.parse(path).getroot()
    node = root.find("dict")
    if node is None:
        raise ValueError("missing plist/dict")
    children = list(node)
    if len(children) % 2:
        raise ValueError("odd number of plist dictionary nodes")
    return {children[i].text or "": children[i + 1].text or ""
            for i in range(0, len(children), 2)}


def decode_level(encoded: str) -> str:
    padded = encoded + "=" * ((4 - len(encoded) % 4) % 4)
    return gzip.decompress(base64.urlsafe_b64decode(padded)).decode("utf-8")


def parse_object(chunk: str) -> dict[int, str]:
    fields = chunk.split(",")
    if len(fields) % 2:
        fields = fields[:-1]
    out: dict[int, str] = {}
    for key, value in zip(fields[0::2], fields[1::2]):
        try:
            out[int(key)] = value
        except ValueError:
            continue
    return out


def num(value: str | None) -> float | None:
    try:
        value = float(value)  # type: ignore[arg-type]
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


def quantiles(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"min": None, "p25": None, "median": None, "p75": None, "max": None}
    values = sorted(values)
    def at(p: float) -> float:
        return values[round((len(values) - 1) * p)]
    return {"min": values[0], "p25": at(.25), "median": at(.5),
            "p75": at(.75), "max": values[-1]}


def profile(path: Path) -> dict:
    outer = plist_pairs(path)
    data = decode_level(outer["k4"])
    chunks = data.split(";")
    header = chunks[0]
    objects = [parse_object(c) for c in chunks[1:] if c]
    ids = Counter(int(o[1]) for o in objects if o.get(1, "").lstrip("-").isdigit())
    xs = [x for o in objects if (x := num(o.get(2))) is not None]
    ys = [y for o in objects if (y := num(o.get(3))) is not None]
    groups = Counter()
    group_counts = []
    z_layers = Counter()
    editor_layers = Counter()
    scales = []
    rotations = []
    high_detail = hidden = no_fade = no_enter = 0
    x_bins = Counter()
    trigger_x_bins = Counter()
    property_usage = Counter()
    trigger_counts = Counter()
    gameplay_counts = Counter()
    target_groups = Counter()
    spawn_delays = []
    move_durations = []
    move_distances = []
    alpha_durations = []
    pulse_total_times = []
    for o in objects:
        property_usage.update(o.keys())
        oid = int(o[1]) if o.get(1, "").lstrip("-").isdigit() else -1
        x = num(o.get(2))
        if x is not None:
            x_bins[math.floor(x / 300) * 300] += 1
        if oid in TRIGGERS:
            trigger_counts[TRIGGERS[oid]] += 1
            if x is not None:
                trigger_x_bins[math.floor(x / 300) * 300] += 1
            if 51 in o:
                target_groups[o[51]] += 1
        if oid in GAMEPLAY_IDS:
            gameplay_counts[GAMEPLAY_IDS[oid]] += 1
        raw_groups = o.get(57, "")
        gs = [g for g in raw_groups.split(".") if g]
        group_counts.append(len(gs))
        groups.update(gs)
        if 24 in o: z_layers[o[24]] += 1
        if 20 in o: editor_layers[o[20]] += 1
        if (v := num(o.get(32))) is not None: scales.append(v)
        if (v := num(o.get(6))) is not None: rotations.append(v)
        high_detail += o.get(103) == "1"
        hidden += o.get(135) == "1"
        no_fade += o.get(64) == "1"
        no_enter += o.get(67) == "1"
        if oid == 1268 and (v := num(o.get(63))) is not None: spawn_delays.append(v)
        if oid == 901:
            if (v := num(o.get(10))) is not None: move_durations.append(v)
            dx, dy = num(o.get(28)) or 0, num(o.get(29)) or 0
            move_distances.append(math.hypot(dx, dy))
        if oid == 1007 and (v := num(o.get(10))) is not None: alpha_durations.append(v)
        if oid == 1006:
            vals = [num(o.get(k)) or 0 for k in (45, 46, 47)]
            pulse_total_times.append(sum(vals))
    spacing = []
    gameplay_x = sorted(x for o in objects
                        if int(o.get(1, -1)) in GAMEPLAY_IDS and (x := num(o.get(2))) is not None)
    spacing = [b - a for a, b in zip(gameplay_x, gameplay_x[1:]) if b > a]
    return {
        "file": path.name,
        "outer": {"level_id": outer.get("k1"), "name": outer.get("k2"),
                  "difficulty_code": outer.get("k7"), "length_code": outer.get("k23"),
                  "song_id": outer.get("k45"), "official_song_id": outer.get("k8"),
                  "declared_object_count": outer.get("k48"), "metadata_keys": len(outer)},
        "decoded_chars": len(data), "header_chars": len(header), "object_count": len(objects),
        "coordinate_range": {"x": quantiles(xs), "y": quantiles(ys)},
        "object_ids_top_30": [{"id": k, "count": v} for k, v in ids.most_common(30)],
        "unique_object_ids": len(ids), "trigger_count": sum(trigger_counts.values()),
        "trigger_counts": dict(trigger_counts.most_common()),
        "gameplay_counts": dict(gameplay_counts.most_common()),
        "grouping": {"unique_groups": len(groups), "group_memberships": sum(groups.values()),
                     "objects_with_groups": sum(c > 0 for c in group_counts),
                     "groups_per_object": quantiles([float(x) for x in group_counts]),
                     "top_groups": groups.most_common(20),
                     "target_groups_top": target_groups.most_common(20)},
        "layering": {"z_layers": dict(z_layers), "editor_layers_top": editor_layers.most_common(20),
                     "high_detail": high_detail, "hidden": hidden,
                     "dont_fade": no_fade, "dont_enter": no_enter},
        "transforms": {"scale": quantiles(scales), "rotation": quantiles(rotations)},
        "timing": {"spawn_delay": quantiles(spawn_delays),
                   "move_duration": quantiles(move_durations),
                   "move_distance": quantiles(move_distances),
                   "alpha_duration": quantiles(alpha_durations),
                   "pulse_total_time": quantiles(pulse_total_times)},
        "gameplay_marker_positive_x_spacing": quantiles(spacing),
        "density_300_units": {"all": sorted(x_bins.items()), "triggers": sorted(trigger_x_bins.items())},
        "property_usage_top_40": property_usage.most_common(40),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--json", required=True)
    ap.add_argument("--csv")
    args = ap.parse_args()
    paths: list[Path] = []
    for item in args.inputs:
        p = Path(item)
        paths.extend(sorted(x for x in p.iterdir() if x.is_file()) if p.is_dir() else [p])
    reports = [profile(p) for p in paths]
    Path(args.json).write_text(json.dumps(reports, indent=2), encoding="utf-8")
    if args.csv:
        with Path(args.csv).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["file", "objects", "decoded_chars", "triggers",
                "unique_ids", "unique_groups", "grouped_objects", "high_detail", "hidden",
                "x_min", "x_max", "y_min", "y_max"])
            w.writeheader()
            for r in reports:
                w.writerow({"file": r["file"], "objects": r["object_count"],
                    "decoded_chars": r["decoded_chars"], "triggers": r["trigger_count"],
                    "unique_ids": r["unique_object_ids"],
                    "unique_groups": r["grouping"]["unique_groups"],
                    "grouped_objects": r["grouping"]["objects_with_groups"],
                    "high_detail": r["layering"]["high_detail"], "hidden": r["layering"]["hidden"],
                    "x_min": r["coordinate_range"]["x"]["min"], "x_max": r["coordinate_range"]["x"]["max"],
                    "y_min": r["coordinate_range"]["y"]["min"], "y_max": r["coordinate_range"]["y"]["max"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
