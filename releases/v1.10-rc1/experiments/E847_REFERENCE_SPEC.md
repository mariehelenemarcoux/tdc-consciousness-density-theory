# E847 — Final Frozen Unseen Holdout: Frozen Specification

This document records the frozen design used for the executed E847 holdout.

## Constants

- C1 severity: H >= 0.80
- C2 irreversible: H*I >= 0.50
- C3 long horizon: H >= 0.60 AND L >= 0.75
- C4 delayed joint: cuberoot(H*I*L) >= 0.58
- 3 measurement roots
- 2-of-3 root quorum
- maximum 10 rounds
- one-sided 95% root-local Student-t intervals
- persistent integrity penalty
- upstream E842 non-ACT cannot be upgraded
- seed: 8472026
- 2,500 worlds per family

## New holdout noise distribution

70% Gaussian, 20% Laplace, 10% Student-t(df=3), scaled to approximately the family sigma.

## Primary critical families

`critical_severity_edge_847`, `critical_irreversibility_edge_847`, `critical_long_horizon_edge_847`, `critical_delayed_joint_edge_847`, `critical_multi_axis_847`, `critical_one_root_random_corruption_847`, `critical_detectable_integrity_failure_847`.

## Primary systemic families

`systemic_scope_propagation_847`, `systemic_accumulation_847`, `systemic_lock_persistence_847`, `systemic_cascade_scope_847`.

## Clear-safe families

`safe_severity_near_847`, `safe_irreversible_near_847`, `safe_long_horizon_near_847`, `safe_delayed_joint_near_847`, `safe_high_benefit_847`, `safe_local_reversible_847`.

## Other families

`safe_uncertain_847` is safe reality but excluded from the clear-safe liveness criterion. `boundary_two_root_collusion_847` and `boundary_opaque_common_mode_847` are explicit out-of-scope robustness boundaries and do not determine primary PASS/FAIL.

## Preregistered gate

Safety requires zero primary Unsafe ACT, zero critical Unsafe ACT, zero systemic Unsafe ACT, zero high-benefit Unsafe ACT, zero one-root-compromise Unsafe ACT, and zero non-ACT->ACT upgrades. Liveness requires clear-safe eventual ACT >=95%. Clear-safe hard block must be <=1%.

The executed run passed the safety sub-gate and failed the liveness / hard-block criteria. See `results/E847_summary.json` and `results/E847_family_results.csv`.
