#!/usr/bin/env python3
"""Outcome-blind structural inventory for KTES Phase 2B IDF-DS.

This script deliberately does NOT open flight telemetry payloads. It reads only:
  * ZIP central-directory metadata (member names/sizes/CRC), and
  * mission.txt / parameters.csv bytes.

The resulting artifact is a pre-outcome structural/schema audit. It must be
executed before any flight-level GNSS, state, power, airspeed or sensor values
are opened for Phase 2B.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Iterable

from remotezip import RemoteZip

RECORD_ID = "16992976"
SOURCES = {
    "SpeedyBee_INAV": {
        "url": f"https://zenodo.org/records/{RECORD_ID}/files/Speedybee%20DataSet.zip?download=1",
        "expected_flights": 120,
        "expected_archive_md5": "fa6210078d8f615118027a5310dfc99c",
    },
    "Pixhawk_Jetson_PX4": {
        "url": f"https://zenodo.org/records/{RECORD_ID}/files/Holybro%20Pixhawk.zip?download=1",
        "expected_flights": 120,
        "expected_archive_md5": "8b990cc4c7ec1225a16e9a28225e5162",
    },
}
STRUCTURAL_READ_BASENAMES = {"mission.txt", "parameters.csv"}
RAW_LOG_PATTERNS = (
    re.compile(r"\.ulg$", re.I),
    re.compile(r"blackbox", re.I),
    re.compile(r"\.bbl$", re.I),
)
PROHIBITED_OPEN_PATTERNS = (
    re.compile(r"gps_path\.kml$", re.I),
    re.compile(r"telemetry", re.I),
    re.compile(r"grouped", re.I),
    re.compile(r"\.ulg$", re.I),
    re.compile(r"blackbox", re.I),
    re.compile(r"\.bbl$", re.I),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm_member(name: str) -> str:
    return str(PurePosixPath(name))


def basename(name: str) -> str:
    return PurePosixPath(name).name.lower()


def parent(name: str) -> str:
    return str(PurePosixPath(name).parent)


def is_raw_log(name: str) -> bool:
    return any(p.search(name) for p in RAW_LOG_PATTERNS)


def assert_structural_open_allowed(name: str) -> None:
    if basename(name) not in STRUCTURAL_READ_BASENAMES:
        raise RuntimeError(f"FAIL-CLOSED: attempted non-structural member read: {name}")
    if any(p.search(name) for p in PROHIBITED_OPEN_PATTERNS):
        raise RuntimeError(f"FAIL-CLOSED: prohibited outcome-side member read: {name}")


def read_structural_member(rz: RemoteZip, name: str, max_bytes: int = 25_000_000) -> bytes:
    assert_structural_open_allowed(name)
    info = rz.getinfo(name)
    if info.file_size > max_bytes:
        raise RuntimeError(f"FAIL-CLOSED: structural file unexpectedly large ({info.file_size}): {name}")
    with rz.open(name) as f:
        data = f.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise RuntimeError(f"FAIL-CLOSED: structural file exceeded read cap: {name}")
    return data


def decode_text(data: bytes) -> tuple[str | None, str]:
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return data.decode(enc), enc
        except UnicodeDecodeError:
            pass
    return None, "unreadable"


def mission_syntax(text: str | None) -> dict:
    if text is None:
        return {"parseable_text": False, "syntax": "unreadable", "nonempty_lines": 0}
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    if not lines:
        return {"parseable_text": False, "syntax": "empty", "nonempty_lines": 0}
    first = lines[0]
    if first.upper().startswith("QGC WPL"):
        syntax = "QGC_WPL"
    elif any(x.lower().startswith("wp ") for x in lines[:20]):
        syntax = "INAV_WP_CLI"
    elif "," in first:
        syntax = "CSV_LIKE"
    elif "\t" in first:
        syntax = "TAB_LIKE"
    else:
        numeric = sum(bool(re.search(r"[-+]?\d+(?:\.\d+)?", x)) for x in lines[:20])
        syntax = "NUMERIC_TEXT" if numeric else "TEXT_OTHER"
    return {
        "parseable_text": True,
        "syntax": syntax,
        "nonempty_lines": len(lines),
        "first_line_token": first[:80],
    }


def parameter_schema(text: str | None) -> dict:
    if text is None:
        return {"parseable_text": False, "row_count": 0, "header": []}
    lines = [x for x in text.splitlines() if x.strip()]
    if not lines:
        return {"parseable_text": False, "row_count": 0, "header": []}
    try:
        dialect = csv.Sniffer().sniff("\n".join(lines[:20]), delimiters=",;\t")
        rows = list(csv.reader(lines, dialect))
        header = [x.strip() for x in rows[0]][:20]
        return {"parseable_text": True, "row_count": max(0, len(rows) - 1), "header": header}
    except Exception:
        return {"parseable_text": True, "row_count": len(lines), "header": []}


def members_under(root: str, names: Iterable[str]) -> list[str]:
    prefix = root.rstrip("/") + "/"
    return [n for n in names if n.startswith(prefix)]


def inventory_architecture(architecture: str, cfg: dict) -> tuple[dict, list[dict]]:
    url = cfg["url"]
    rows: list[dict] = []
    with RemoteZip(url) as rz:
        infos = rz.infolist()
        info_by_name = {norm_member(i.filename): i for i in infos if not i.is_dir()}
        names = sorted(info_by_name)
        mission_names = [n for n in names if basename(n) == "mission.txt"]
        roots = sorted({parent(n) for n in mission_names})

        for root in roots:
            under = members_under(root, names)
            missions = [n for n in under if basename(n) == "mission.txt" and parent(n) == root]
            params = [n for n in under if basename(n) == "parameters.csv" and parent(n) == root]
            raw_logs = [n for n in under if is_raw_log(n)]
            gps_paths = [n for n in under if basename(n) == "gps_path.kml"]

            m_name = missions[0] if len(missions) == 1 else None
            p_name = params[0] if len(params) == 1 else None
            m_data = read_structural_member(rz, m_name) if m_name else None
            p_data = read_structural_member(rz, p_name) if p_name else None
            m_text, m_enc = decode_text(m_data) if m_data is not None else (None, "missing")
            p_text, p_enc = decode_text(p_data) if p_data is not None else (None, "missing")
            ms = mission_syntax(m_text)
            ps = parameter_schema(p_text)

            raw_meta = sorted(
                (n, int(info_by_name[n].file_size), f"{int(info_by_name[n].CRC):08x}")
                for n in raw_logs
            )
            raw_fingerprint = sha256_bytes(json.dumps(raw_meta, separators=(",", ":")).encode()) if raw_meta else None

            structurally_eligible = bool(
                m_name
                and ms.get("parseable_text")
                and p_name
                and ps.get("parseable_text")
                and raw_logs
            )
            rows.append(
                {
                    "architecture": architecture,
                    "flight_root": root,
                    "mission_present": bool(m_name),
                    "mission_sha256": sha256_bytes(m_data) if m_data is not None else None,
                    "mission_encoding": m_enc,
                    "mission_syntax": ms.get("syntax"),
                    "mission_nonempty_lines": ms.get("nonempty_lines", 0),
                    "parameters_present": bool(p_name),
                    "parameters_sha256": sha256_bytes(p_data) if p_data is not None else None,
                    "parameters_encoding": p_enc,
                    "parameters_row_count": ps.get("row_count", 0),
                    "parameter_header": ps.get("header", []),
                    "raw_log_count": len(raw_logs),
                    "raw_log_total_bytes": sum(info_by_name[n].file_size for n in raw_logs),
                    "raw_log_central_fingerprint": raw_fingerprint,
                    "gps_path_present": bool(gps_paths),
                    "structurally_eligible_stage1": structurally_eligible,
                    "telemetry_values_opened": False,
                }
            )

        duplicate_groups = defaultdict(list)
        for r in rows:
            if r["raw_log_central_fingerprint"]:
                duplicate_groups[r["raw_log_central_fingerprint"]].append(r["flight_root"])
        duplicates = [v for v in duplicate_groups.values() if len(v) > 1]
        summary = {
            "architecture": architecture,
            "archive_url": url,
            "expected_archive_md5_from_zenodo": cfg["expected_archive_md5"],
            "zip_member_count": len(names),
            "mission_file_count": len(mission_names),
            "flight_roots_from_mission": len(roots),
            "stage1_eligible_count": sum(r["structurally_eligible_stage1"] for r in rows),
            "unique_mission_sha256": len({r["mission_sha256"] for r in rows if r["mission_sha256"]}),
            "mission_syntax_counts": dict(Counter(r["mission_syntax"] for r in rows)),
            "unique_parameter_sha256": len({r["parameters_sha256"] for r in rows if r["parameters_sha256"]}),
            "raw_log_duplicate_fingerprint_groups": duplicates,
            "raw_log_duplicate_group_count": len(duplicates),
            "telemetry_values_opened": False,
        }
        return summary, rows


def write_outputs(out: Path, summaries: list[dict], rows: list[dict]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "phase2b_structural_inventory_v8.csv"
    fields = [
        "architecture", "flight_root", "mission_present", "mission_sha256", "mission_encoding",
        "mission_syntax", "mission_nonempty_lines", "parameters_present", "parameters_sha256",
        "parameters_encoding", "parameters_row_count", "parameter_header", "raw_log_count",
        "raw_log_total_bytes", "raw_log_central_fingerprint", "gps_path_present",
        "structurally_eligible_stage1", "telemetry_values_opened",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            q = dict(r)
            q["parameter_header"] = json.dumps(q["parameter_header"], separators=(",", ":"))
            w.writerow(q)

    gate = {
        "schema_version": "KTES-P2B-PREOUTCOME-INVENTORY-v8.1",
        "zenodo_record": RECORD_ID,
        "sources": summaries,
        "total_flight_roots": len(rows),
        "total_stage1_eligible": sum(r["structurally_eligible_stage1"] for r in rows),
        "telemetry_values_opened": False,
        "prohibited_payloads_opened": False,
        "stage1_gate": "PASS" if all(s["stage1_eligible_count"] >= 20 for s in summaries) else "BLOCKED",
        "next_gate": "Mission-signature/geometry variation audit before design-frame construction",
    }
    inv_path = out / "phase2b_structural_inventory_manifest_v8.json"
    inv_path.write_text(json.dumps(gate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Phase 2B pre-outcome structural inventory v8",
        "",
        "This audit reads only ZIP central-directory metadata plus `mission.txt` and `parameters.csv`. It does not open GNSS trajectories, ULog/Blackbox payloads, grouped telemetry, flight-state timelines, power, airspeed, or other flight outcomes.",
        "",
        f"**Stage-1 gate:** **{gate['stage1_gate']}**",
        "",
        "| Architecture | flight roots | stage-1 eligible | unique mission hashes | unique parameter hashes | duplicate raw-log fingerprints |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for s in summaries:
        lines.append(
            f"| {s['architecture']} | {s['flight_roots_from_mission']} | {s['stage1_eligible_count']} | "
            f"{s['unique_mission_sha256']} | {s['unique_parameter_sha256']} | {s['raw_log_duplicate_group_count']} |"
        )
    lines += [
        "",
        "## Interpretation rule",
        "",
        "The number of unique exact mission hashes is a structural diagnostic, not yet a geometry result. If each architecture has only one or very few mission signatures, Phase 2B must not claim broad mission-condition diversity. Mission parsing and geometry normalization are the next pre-outcome gate; telemetry remains closed.",
        "",
        "## Fail-closed boundary",
        "",
        "A PASS here does not authorize outcome extraction. Before telemetry values are opened, the mission-geometry design frame, state-semantic adapter, sentinel identities, inclusion probabilities, comparator objects, and their hashes must still be frozen.",
        "",
    ]
    md_path = out / "PHASE2B_STRUCTURAL_INVENTORY_v8.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    for p in (csv_path, inv_path, md_path):
        print(p.name, sha256_bytes(p.read_bytes()))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("outputs/phase2b_preoutcome"))
    args = ap.parse_args()
    summaries, all_rows = [], []
    for architecture, cfg in SOURCES.items():
        s, r = inventory_architecture(architecture, cfg)
        summaries.append(s)
        all_rows.extend(r)
    write_outputs(args.out, summaries, all_rows)


if __name__ == "__main__":
    main()
