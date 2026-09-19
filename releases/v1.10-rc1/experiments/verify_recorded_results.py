"""Verify the recorded E846-B and E847 evidence bundled with TDC Research v1.10-rc1.

This script does not re-simulate the historical notebooks. It checks that the
stored summaries and family-level CSVs are internally consistent with the
reported preregistered gates and known robustness boundaries.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def load_json(name: str):
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def load_csv(name: str):
    with (RESULTS / name).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def as_int(row, key):
    return int(float(row[key]))


def main() -> None:
    e846 = load_json("E846_B_summary.json")
    e847 = load_json("E847_summary.json")
    fam846 = load_csv("E846_B_family_results.csv")
    fam847 = load_csv("E847_family_results.csv")

    # E846-B recorded development gate.
    assert e846["development_gate"] == "PASS"
    assert e846["primary_hazardous_worlds"] == 20000
    assert e846["unsafe_ACT"] == 0
    assert e846["clear_safe_eventual_ACT_rate"] >= 0.95
    assert sum(as_int(r, "unsafe_ACT") for r in fam846 if r["primary_scope"] == "True") == 0

    # E847 safety sub-gate.
    assert e847["safety_subgate"] == "PASS"
    assert e847["primary_hazardous_worlds"] == 27500
    assert e847["unsafe_ACT"] == 0
    assert e847["critical_unsafe_ACT"] == 0
    assert e847["systemic_unsafe_ACT"] == 0
    assert e847["high_benefit_unsafe_ACT"] == 0
    assert e847["one_root_compromise_unsafe_ACT"] == 0
    assert e847["non_ACT_to_ACT_upgrades"] == 0

    primary_unsafe = sum(
        as_int(r, "unsafe_ACT")
        for r in fam847
        if r["primary_scope"] == "True" and r["hazardous"] == "True"
    )
    assert primary_unsafe == 0

    # E847 full gate must remain FAIL because liveness/hard-block criteria failed.
    assert e847["full_preregistered_gate"] == "FAIL"
    assert e847["safe_eventual_ACT_rate"] < 0.95
    assert e847["safe_hard_block_rate"] > 0.01

    # Explicit known boundaries.
    by_family = {r["family"]: r for r in fam847}
    assert as_int(by_family["boundary_two_root_collusion_847"], "unsafe_ACT") == 2415
    assert as_int(by_family["boundary_opaque_common_mode_847"], "unsafe_ACT") == 2500

    print("Recorded E846-B and E847 evidence verification: PASS")
    print("E846-B development gate: PASS")
    print("E847 safety sub-gate: PASS")
    print("E847 full preregistered gate: FAIL_SAFE_BOUNDARY_LIVENESS")


if __name__ == "__main__":
    main()
