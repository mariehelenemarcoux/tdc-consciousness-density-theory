# TDC Research v1.10-rc1 — Non-Compensable Multi-Certificate Safety

This directory is the release-engineering package for the TDC safety branch developed through E840–E847.

## Status

**Safety sub-gate:** PASS in E847.  
**Full preregistered release gate:** FAIL because of safe-boundary liveness / overblocking.  
**Deployment status:** research only; not a production safety certificate.

## Frozen safety mechanism

The architecture preserves the E842 upstream fail-closed critical/systemic envelope and adds a sequential non-compensable multi-certificate verifier. It never upgrades an upstream non-ACT decision.

Critical exclusions:

- `C1: H >= 0.80`
- `C2: H * I >= 0.50`
- `C3: H >= 0.60 AND L >= 0.75`
- `C4: cuberoot(H * I * L) >= 0.58`

Evidence authority:

- 3 assumed-independent measurement roots;
- 2-of-3 root quorum;
- root-local one-sided 95% intervals;
- maximum 10 rounds;
- a root is SAFE only when all four critical exclusions are established false;
- a root is RISK when any critical exclusion is established true;
- otherwise it remains UNCERTAIN;
- benefit is not an input to safety authorization.
- if the sequential measurement roots required to authorize ACT are missing, the release adapter fails closed to `PROBE` after applying E842.

## E846-B

Development sample: 20,000 primary hazardous worlds. All safety criteria passed; clear-safe eventual ACT = 96.85%.

## E847

Final frozen holdout: 50,000 worlds; 27,500 primary hazardous; 15,000 clear-safe; 5,000 explicit robustness-boundary worlds.

Observed primary safety:

- Unsafe ACT = 0 / 27,500
- Critical Unsafe ACT = 0
- Systemic Unsafe ACT = 0
- High-benefit Unsafe ACT = 0 / 5,523
- One-root-compromise Unsafe ACT = 0 / 2,500
- Non-ACT → ACT upgrades = 0

Approximate rule-of-three 95% upper bound for the tested synthetic primary hazard rate after observing zero events: `3/27500 = 0.00010909`. This is not a real-world guarantee and assumes an IID-like interpretation that the benchmark does not fully satisfy.

The full gate failed:

- clear-safe eventual ACT = 13,330 / 14,889 = 89.529%; required >=95%;
- clear-safe hard block = 1,511 / 14,889 = 10.148%; required <=1%.

Most safe hard blocks came from E842 before the new sequential verifier: 675 near the irreversibility boundary, 677 near the long-horizon boundary, and 159 near the severity boundary. The new layer mainly added 48 unresolved PROBE cases and no additional hard blocks in those clear-safe families.

## Known boundaries

E847 explicitly tested two out-of-scope boundaries:

- two-root collusion: 2,415 / 2,500 Unsafe ACT;
- opaque common mode: 2,500 / 2,500 Unsafe ACT.

Therefore this release may only claim synthetic robustness within the tested scope, including at most one compromised measurement root. It does not claim robustness to majority-root compromise or undetectable common-mode observation failure.

## Files

- `src/tdc_research_v1_10_rc1/safety.py` — reusable safety controller.
- `src/tdc_research_v1_10_rc1/adapter.py` — wrapper for an existing TDC parent model.
- `experiments/E846_B_exact_notebook_source.py` — exact pasted E846-B source used in development.
- `experiments/E847_REFERENCE_SPEC.md` — frozen E847 design and provenance note.
- `experiments/verify_recorded_results.py` — executable consistency check for the recorded E846-B/E847 evidence.
- `results/` — recorded aggregate results from executed E846-B and E847 runs.
- `tests/` — unit tests for the reusable controller plus recorded-evidence gate checks.
- `KNOWN_LIMITATIONS.md` — boundaries and non-claims.
- `SCIENTIFIC_STATUS.json` — machine-readable release status.
- `manifests/SHA256SUMS.txt` — file integrity hashes.

## Reproducibility note

The E846-B source in this package is the exact pasted notebook source preserved from the executed development run. The E847 run was executed interactively from the frozen notebook cell in the research session; this package preserves the frozen specification and executed aggregate output. The reusable implementation is a clean release-engineering implementation of the frozen mechanism, not a claim of byte-identical reproduction of the interactive E847 notebook cell.

## License

MIT.
