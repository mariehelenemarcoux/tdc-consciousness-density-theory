# Provenance

This package distinguishes executed historical evidence from release-engineering reconstruction.

- `experiments/E846_B_exact_notebook_source.py` is copied byte-for-byte from the user-provided E846-B notebook source attachment used in the research session.
- E846-B and E847 aggregate results in `results/` are transcribed from the executed outputs provided in the research session.
- The reusable module under `src/` is a clean release-engineering implementation of the frozen mechanism.
- The exact interactive E847 notebook cell was not available as a mounted source file when this package was assembled, so this package does not label the release-engineering reference as a byte-identical historical rerun.
- No result values in `results/` were re-simulated or altered while assembling this package.

- `experiments/verify_recorded_results.py` and `tests/test_recorded_evidence.py` verify the stored evidence and release gates; they do not claim to re-simulate E847 byte-for-byte.


## Release-engineering hardening

The reusable adapter adds a fail-closed handling rule for missing measurement-root histories: after E842, unresolved ACT authorization becomes `PROBE`. This does not alter the recorded E846-B/E847 evidence; it prevents missing release inputs from bypassing the sequential safety layer.
