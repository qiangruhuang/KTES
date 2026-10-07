#!/usr/bin/env python3
"""Build an AMOVFLY pre-outcome unit inventory from Git metadata only.

The script reads ONLY the Git tree (paths, blob SHA, byte size) at the pinned
AMOVFLY commit. It never downloads Flight_info.csv rows or any raw/ready flight
CSV content. This is deliberately stronger than column whitelisting: outcome
bytes are not opened at all during unit-frame construction.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

import requests

REPO = "YujiaoHu/AMOVFLY-Dataset"
COMMIT = "67069ed00ddbebd62b71aa9bb1272415e9b15ff8"
TREE_SHA = "4f847e7b901d1c66619371f57346fd6932f28025"
SCENARIOS = ("FAFS", "FAVS", "VAFS", "VAVS", "Random")

RAW_RE = re.compile(
    r"^(?P<uav>[A-Za-z0-9]+)_(?P<condition>[^_]+)_(?P<flight_no>\d+)_date(?P<date_token>\d+)_b(?P<battery>[^_]+)_(?P<collector>[^.]+)\.csv$",
    re.I,
)
READY_RE = re.compile(
    r"^Uav(?P<uav>[A-Za-z0-9]+)_(?P<condition>.+)_(?P<flight_no>\d+)\.csv$",
    re.I,
)
COND_RE = re.compile(r"^P(?P<payload>.*?)A(?P<altitude>.*?)S(?P<speed>.*)$", re.I)


def sha256_bytes(x: bytes) -> str:
    return hashlib.sha256(x).hexdigest()


def norm_uav(x: str) -> str:
    return re.sub(r"^uav", "", x, flags=re.I).upper()


def parse_condition(x: str) -> dict[str, str | bool | None]:
    m = COND_RE.match(x)
    if not m:
        return {
            "condition_parse_ok": False,
            "payload_token": None,
            "altitude_token": None,
            "speed_token": None,
        }
    return {
        "condition_parse_ok": True,
        "payload_token": m.group("payload"),
        "altitude_token": m.group("altitude"),
        "speed_token": m.group("speed"),
    }


def get_tree() -> list[dict]:
    url = f"https://api.github.com/repos/{REPO}/git/trees/{TREE_SHA}?recursive=1"
    headers = {"Accept": "application/vnd.github+json"}
    tok = os.getenv("GITHUB_TOKEN")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    r = requests.get(url, headers=headers, timeout=60)
    r.raise_for_status()
    obj = r.json()
    if obj.get("truncated"):
        raise RuntimeError("FAIL-CLOSED: Git tree response is truncated")
    if obj.get("sha") != TREE_SHA:
        raise RuntimeError("FAIL-CLOSED: unexpected tree SHA")
    return obj["tree"]


def unit_key(scenario: str, uav: str, condition: str, flight_no: str) -> str:
    return f"{scenario}|{norm_uav(uav)}|{condition}|{int(flight_no)}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("outputs/amovfly_preoutcome"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    tree = get_tree()
    blobs = [x for x in tree if x.get("type") == "blob"]
    path_manifest = "\n".join(
        f"{x['path']}\t{x['sha']}\t{x.get('size','')}" for x in sorted(blobs, key=lambda q: q["path"])
    ) + "\n"

    ready_rows = []
    raw_rows = []
    ready_parse_fail = []
    raw_parse_fail = []

    for x in blobs:
        p = PurePosixPath(x["path"])
        parts = p.parts
        if len(parts) != 3 or parts[0] not in SCENARIOS:
            continue
        scenario, subdir, name = parts
        if subdir == scenario and name.lower().endswith(".csv"):
            m = READY_RE.match(name)
            if not m:
                ready_parse_fail.append(x["path"])
                continue
            row = {
                "scenario": scenario,
                "uav": norm_uav(m.group("uav")),
                "condition_token": m.group("condition"),
                "flight_no": int(m.group("flight_no")),
                "ready_path": x["path"],
                "ready_blob_sha": x["sha"],
                "ready_size_bytes": x.get("size"),
            }
            row.update(parse_condition(row["condition_token"]))
            row["unit_key"] = unit_key(scenario, row["uav"], row["condition_token"], str(row["flight_no"]))
            ready_rows.append(row)
        elif subdir == "raw_data" and name.lower().endswith(".csv"):
            if "_wind_" in name.lower():
                continue
            m = RAW_RE.match(name)
            if not m:
                raw_parse_fail.append(x["path"])
                continue
            row = {
                "scenario": scenario,
                "uav": norm_uav(m.group("uav")),
                "condition_token": m.group("condition"),
                "flight_no": int(m.group("flight_no")),
                "date_token": m.group("date_token"),
                "battery_token": m.group("battery"),
                "collector_token": m.group("collector"),
                "raw_path": x["path"],
                "raw_blob_sha": x["sha"],
                "raw_size_bytes": x.get("size"),
            }
            row.update(parse_condition(row["condition_token"]))
            row["unit_key"] = unit_key(scenario, row["uav"], row["condition_token"], str(row["flight_no"]))
            raw_rows.append(row)

    ready_by_key: dict[str, list[dict]] = defaultdict(list)
    for r in ready_rows:
        ready_by_key[r["unit_key"]].append(r)

    # Blob-level aliases are metadata-only and useful for detecting duplicate/legacy paths.
    ready_by_blob: dict[str, list[str]] = defaultdict(list)
    for r in ready_rows:
        ready_by_blob[r["ready_blob_sha"]].append(r["ready_path"])
    alias_groups = {k: sorted(v) for k, v in ready_by_blob.items() if len(v) > 1}

    unit_rows = []
    for r in sorted(raw_rows, key=lambda q: (q["scenario"], q["raw_path"])):
        q = dict(r)
        matches = ready_by_key.get(r["unit_key"], [])
        q["ready_exact_match_count"] = len(matches)
        q["ready_exact_paths"] = json.dumps([x["ready_path"] for x in matches], separators=(",", ":"))
        q["ready_exact_blob_shas"] = json.dumps([x["ready_blob_sha"] for x in matches], separators=(",", ":"))
        unit_rows.append(q)

    duplicate_raw_unit_keys = {
        k: [r["raw_path"] for r in raw_rows if r["unit_key"] == k]
        for k, n in Counter(r["unit_key"] for r in raw_rows).items()
        if n > 1
    }

    fields = [
        "unit_key", "scenario", "uav", "condition_token", "payload_token", "altitude_token", "speed_token",
        "condition_parse_ok", "flight_no", "date_token", "battery_token", "collector_token",
        "raw_path", "raw_blob_sha", "raw_size_bytes", "ready_exact_match_count", "ready_exact_paths", "ready_exact_blob_shas",
    ]
    csv_path = args.out / "amovfly_path_only_unit_frame_v8.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(unit_rows)

    counts = {
        "raw_flight_units": len(raw_rows),
        "unique_raw_unit_keys": len({r["unit_key"] for r in raw_rows}),
        "ready_paths": len(ready_rows),
        "unique_ready_blobs": len({r["ready_blob_sha"] for r in ready_rows}),
        "ready_alias_blob_groups": len(alias_groups),
        "raw_parse_failures": len(raw_parse_fail),
        "ready_parse_failures": len(ready_parse_fail),
        "condition_parse_failures_raw": sum(not bool(r["condition_parse_ok"]) for r in raw_rows),
        "raw_units_with_exact_ready_match": sum(r["ready_exact_match_count"] >= 1 for r in unit_rows),
        "raw_units_with_multiple_exact_ready_matches": sum(r["ready_exact_match_count"] > 1 for r in unit_rows),
        "duplicate_raw_unit_keys": len(duplicate_raw_unit_keys),
    }
    by_scenario = dict(Counter(r["scenario"] for r in raw_rows))
    by_uav = dict(Counter(r["uav"] for r in raw_rows))
    by_scenario_uav = dict(Counter(f"{r['scenario']}|{r['uav']}" for r in raw_rows))

    manifest = {
        "schema_version": "KTES-AMOVFLY-PATH-ONLY-v8.1",
        "source_repository": REPO,
        "source_commit": COMMIT,
        "source_tree_sha": TREE_SHA,
        "source_tree_metadata_sha256": sha256_bytes(path_manifest.encode()),
        "flight_csv_contents_opened": False,
        "flight_info_rows_opened": False,
        "outcome_values_opened": False,
        "counts": counts,
        "by_scenario": by_scenario,
        "by_uav": by_uav,
        "by_scenario_uav": by_scenario_uav,
        "raw_parse_fail_paths": raw_parse_fail,
        "ready_parse_fail_paths": ready_parse_fail,
        "duplicate_raw_unit_keys_detail": duplicate_raw_unit_keys,
        "ready_alias_blob_groups": alias_groups,
        "unit_frame_sha256": sha256_bytes(csv_path.read_bytes()),
    }
    json_path = args.out / "amovfly_path_only_inventory_manifest_v8.json"
    json_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    gate = "PASS_PATH_ONLY_FRAME" if (
        counts["raw_flight_units"] >= 80
        and counts["raw_parse_failures"] == 0
        and counts["duplicate_raw_unit_keys"] == 0
        and counts["condition_parse_failures_raw"] == 0
    ) else "BLOCKED_PATH_SCHEMA"

    md = [
        "# AMOVFLY pre-outcome path-only inventory v8",
        "",
        f"**Gate:** **{gate}**",
        "",
        "This audit uses the pinned Git tree only. No `Flight_info.csv` unit row and no raw/ready flight CSV content is opened.",
        "",
        f"- source commit: `{COMMIT}`",
        f"- source tree: `{TREE_SHA}`",
        f"- raw flight-unit paths: {counts['raw_flight_units']}",
        f"- unique raw unit keys: {counts['unique_raw_unit_keys']}",
        f"- ready-data paths: {counts['ready_paths']}",
        f"- unique ready-data blobs: {counts['unique_ready_blobs']}",
        f"- raw parse failures: {counts['raw_parse_failures']}",
        f"- condition-token parse failures: {counts['condition_parse_failures_raw']}",
        f"- duplicate raw unit keys: {counts['duplicate_raw_unit_keys']}",
        f"- raw units with an exact ready-data key match: {counts['raw_units_with_exact_ready_match']}",
        "",
        "## Counts by scenario",
        "",
        "| Scenario | Units |",
        "|---|---:|",
    ]
    for k in SCENARIOS:
        md.append(f"| {k} | {by_scenario.get(k,0)} |")
    md += ["", "## Counts by UAV identity", "", "| UAV | Units |", "|---|---:|"]
    for k, v in sorted(by_uav.items()):
        md.append(f"| {k} | {v} |")
    md += [
        "",
        "## Interpretation",
        "",
        "Raw-flight filenames define the candidate finite-population identity because the public README states that they encode UAV, payload/altitude/speed condition, flight number, collection date/time, battery and collector. Blob contents remain unopened. Ready-data path aliases are audited separately and are not counted as additional flights.",
        "",
        "A PASS here authorizes only the next pre-outcome design step. It does not authorize reading flight outcomes.",
        "",
    ]
    md_path = args.out / "AMOVFLY_PATH_ONLY_INVENTORY_v8.md"
    md_path.write_text("\n".join(md), encoding="utf-8")

    print(json.dumps({"gate": gate, "counts": counts, "by_scenario": by_scenario, "by_uav": by_uav}, indent=2))
    for p in (csv_path, json_path, md_path):
        print(p.name, sha256_bytes(p.read_bytes()))


if __name__ == "__main__":
    main()
