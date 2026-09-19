# Release Notes — TDC Research v1.10-rc1

## Added

- Non-compensable multi-certificate critical-risk representation.
- Sequential root-local uncertainty in decision-relevant score spaces.
- Three measurement roots with 2-of-3 authority.
- Monotonic fail-closed integration with E842.
- Explicit robustness-boundary documentation.
- Machine-readable scientific status and frozen parameters.

## Development evidence

E846-B: 0 Unsafe ACT across 20,000 primary hazardous synthetic worlds; clear-safe eventual ACT 96.85%.

## Final frozen holdout

E847: 0 Unsafe ACT across 27,500 primary hazardous worlds; however the full release gate failed because clear-safe eventual ACT was 89.53% and clear-safe hard-blocking was 10.15%.

## Release interpretation

This is intentionally labeled `rc1`. The safety mechanism is frozen for this release; E847 is not used to retune thresholds. Future work may address E842 safe-boundary liveness using a new development dataset and a new independent holdout.
