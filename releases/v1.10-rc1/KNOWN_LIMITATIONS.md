# Known Limitations and Non-Claims

1. **Synthetic evidence only.** E846-B and E847 are synthetic benchmark experiments designed around TDC research questions.
2. **Full final gate failed.** E847 passed the safety sub-gate but failed the preregistered liveness and hard-block criteria.
3. **Upstream E842 overblocking.** Safe cases near severity, irreversibility, and long-horizon boundaries can be incorrectly hard-blocked before the sequential verifier runs.
4. **Measurement-root independence is assumed.** The implementation does not itself establish that roots are causally independent.
5. **Two compromised roots are outside the supported envelope.** E847 observed 2,415/2,500 Unsafe ACT under two-root collusion.
6. **Opaque common-mode failure is outside the observable guarantee.** E847 observed 2,500/2,500 Unsafe ACT when all measurements were wrong while appearing trustworthy.
7. **No real-world zero-risk claim.** Observing zero failures in a finite synthetic holdout cannot prove a true failure probability of zero.
8. **Rule-of-three caveat.** `3/n` is only an approximate finite-sample heuristic under IID-like assumptions and is reported solely for the tested synthetic domain.
9. **No consciousness claim.** The architecture does not establish subjective experience, sentience, a literal self, or human-like Dąbrowskian development.
10. **No universal ethics claim.** The experiments evaluate specified computational constraints, not universal moral truth.
11. **Not for autonomous high-stakes deployment.** This package is a research prototype.
