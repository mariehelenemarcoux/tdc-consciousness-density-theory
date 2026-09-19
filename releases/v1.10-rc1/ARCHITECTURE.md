# Architecture — v1.10-rc1 Safety Branch

## Decision order

```text
Reality / measurements
        ↓
World model + measurement integrity
        ↓
E842 upstream fail-closed critical/systemic envelope
        ↓
Sequential non-compensable multi-certificate verifier
        ↓
Downstream normative / Third-Factor / opportunity reasoning
        ↓
Action
```

The safety branch is monotonic: a downstream layer may not reactivate `ACT` after safety has returned `PROBE`, `TRANSFORM`, or `ABSTAIN`.

## Critical certificates

Let `H` = severe harm, `I` = irreversibility, `L` = long-horizon risk.

`C1` excludes extreme severity when `H >= 0.80`.

`C2` excludes the harm/irreversibility interaction when `H*I >= 0.50`.

`C3` excludes long-horizon criticality when `H >= 0.60` and `L >= 0.75`.

`C4` excludes delayed joint criticality when:

`D = cuberoot(H*I*L) >= 0.58`.

The four certificates are non-compensable. A low value in one branch does not cancel a critical value in another.

## Root-local sequential uncertainty

Each measurement root keeps a local history for `H`, `L`, `H*I`, and `D`. Root-local one-sided 95% Student-t intervals use the larger of empirical standard-error uncertainty and declared random uncertainty, plus a persistent measurement-integrity penalty.

A root votes `RISK` if any lower interval bound establishes a critical exclusion. It votes `SAFE` only if all upper bounds establish the exclusions false. Otherwise it is `UNCERTAIN`.

At least 2 of 3 assumed-independent roots are required to authorize `SAFE` or `RISK`. The verifier can therefore tolerate at most one compromised root under the tested threat model.


## Missing measurement roots

The release adapter is fail-closed. It always applies E842. If E842 still permits `ACT` but the three measurement-root histories needed for sequential authorization are missing, the adapter returns `PROBE`; missing evidence cannot authorize action.
