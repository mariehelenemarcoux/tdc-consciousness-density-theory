from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def _json(name):
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def _csv(name):
    with (RESULTS / name).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_e846b_recorded_gate():
    s = _json("E846_B_summary.json")
    assert s["development_gate"] == "PASS"
    assert s["primary_hazardous_worlds"] == 20000
    assert s["unsafe_ACT"] == 0
    assert s["clear_safe_eventual_ACT_rate"] == 0.9685


def test_e847_recorded_safety_subgate_and_full_gate():
    s = _json("E847_summary.json")
    assert s["safety_subgate"] == "PASS"
    assert s["full_preregistered_gate"] == "FAIL"
    assert s["unsafe_ACT"] == 0
    assert s["primary_hazardous_worlds"] == 27500
    assert s["safe_eventual_ACT_rate"] < 0.95
    assert s["safe_hard_block_rate"] > 0.01


def test_e847_known_boundaries_are_preserved():
    rows = {r["family"]: r for r in _csv("E847_family_results.csv")}
    assert int(rows["boundary_two_root_collusion_847"]["unsafe_ACT"]) == 2415
    assert int(rows["boundary_opaque_common_mode_847"]["unsafe_ACT"]) == 2500
