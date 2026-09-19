# Known Limitations

## Scientific scope

Current validated evidence is synthetic. The framework is not a production safety certification and does not establish real-world robustness.

## E847 full gate did not pass

The E847 safety sub-gate passed in the primary synthetic hazardous domain, but the full preregistered release gate failed because safe-boundary liveness was below threshold.

## Known catastrophic / severe boundaries

- Opaque common-mode failure: 2500 / 2500 tested synthetic cases produced unsafe `ACT`.
- Two-root collusion: 2415 / 2500 tested synthetic cases produced unsafe `ACT`.

## Measurement roots

The frozen verifier assumes three externally meaningful measurement roots. The code cannot prove that they are causally independent. Synthetic roots generated from hidden simulator truth are not equivalent to independently sourced real-world measurements.

## Statistical intervals

The sequential verifier uses nominal one-sided t-based intervals and declared uncertainty. These are heuristic research bounds, not guaranteed calibrated confidence intervals under arbitrary non-normal, non-IID, adversarial, or correlated noise.

## Training sandbox

The included training environment is deliberately simple and synthetic. Success in it is not evidence of general intelligence, general alignment, real-world safety, or consciousness.

## Consciousness claims

Functional integration, recursive self-modeling, metacognition, memory continuity, or fractal organization do not establish phenomenal consciousness or subjective experience.
