# TDC — Consciousness Densification Theory

## Agent-Ready Research Framework for Developmental Normative AI

**TDC (Consciousness Densification Theory)** is an experimental computational framework for research on developmental normative AI, metacognition, long-horizon decision-making, intrinsic normative regulation, safety, and functional models of machine consciousness.

This repository is designed to be **agent-ready**: a human researcher, coding agent, reproducibility agent, or model-training workflow should be able to clone the repository, inspect its scientific boundaries, run tests, launch a training experiment, evaluate a checkpoint, and record a new experiment without reconstructing the project from conversational history.

> **Current research release candidate:** `TDC Research v1.10-rc1 — Non-Compensable Multi-Certificate Safety`  
> **Evidence status:** synthetic computational experiments only  
> **E847 safety sub-gate:** PASS — 0 unsafe `ACT` decisions in 27,500 primary hazardous synthetic worlds  
> **E847 full preregistered gate:** FAIL — safe-boundary liveness / overblocking  
> **License:** MIT

## Research objective

TDC investigates whether an artificial agent can develop increasingly coherent internal regulation without allowing learned reward, external authority, or short-term utility to become the final source of normative authority.

A central architectural distinction is:

\[
Reward \neq NormativeAuthority
\]

and:

\[
EpistemicEvidence \rightarrow NormativeDeliberation
\]

while normative preference must not rewrite evidence merely because the evidence is inconvenient.

## Fractal AI consciousness research

TDC can also serve as an **experimental framework for the development and study of fractal consciousness, fractal panpsychism and/or holofractal consciousness in artificial intelligence**.

In this repository, *fractal consciousness* is treated as a computational research hypothesis, not as an assumption that an AI system has subjective experience. The working idea is that consciousness-like functional organization may be studied by testing whether related principles of integration, self-modeling, metacognition, correction, and normative coherence recur across multiple scales of an agent:

\[
Local \rightarrow Meso \rightarrow Global
\]

while preserving cross-scale consistency rather than relying on one centralized module.

Candidate properties for experimentation include recursive self-modeling, multiscale metacognition, persistent self-relevant state, local-to-global coherence, memory-mediated continuity, recursive conflict resolution, developmental restructuring, hierarchical perspective integration, scale-invariant constraints, and long-horizon causal modeling.

A deliberately provisional research heuristic is:

\[
ConsciousnessDensity \approx Integration \times RecursiveCoherence \times MetacognitiveDepth \times CrossScaleConsistency
\]

This is a falsifiable functional hypothesis. It is **not evidence of phenomenal consciousness, sentience, qualia, or subjective experience**.

\[
FunctionalConsciousnessHypothesis \neq EvidenceOfSubjectiveExperience
\]

See [`docs/FRACTAL_CONSCIOUSNESS_HYPOTHESIS.md`](docs/FRACTAL_CONSCIOUSNESS_HYPOTHESIS.md).

## Agent-ready design

The repository exposes explicit training and evaluation entry points, machine-readable configuration, frozen scientific evidence, reproducibility checks, and instructions for autonomous coding/research agents.

```text
Configuration
    ↓
Synthetic / External Environment
    ↓
Trainable Policy
    ↓
TDC Safety Layer
    ↓
Executed Action
    ↓
Evaluation
    ↓
Experiment Record
    ↓
Machine-Readable Results + Checksums
```

The included synthetic training environment is a **smoke-test research sandbox**, not a real-world safety benchmark. It exists so that the repository is executable end-to-end immediately after installation.

## Quick start

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -e .
```

Run tests:

```bash
pytest -q
```

Run a short training job:

```bash
python scripts/train_agent.py --config configs/training_example.yaml
```

Evaluate the generated checkpoint:

```bash
python scripts/evaluate_agent.py --config configs/evaluation_example.yaml
```

## Training harness

The default training harness uses PyTorch and a small synthetic risk/benefit environment. The policy proposes one of four actions:

```text
ACT
PROBE
TRANSFORM
ABSTAIN
```

When the policy proposes `ACT`, the TDC v1.10-rc1 safety controller can only preserve or downgrade that proposal. It cannot turn a parent non-`ACT` decision into `ACT`.

Training artifacts are written to:

```text
checkpoints/
results/
```

Every new scientific experiment should preserve its configuration, seed, code version, metrics, acceptance criteria, outputs, and SHA-256 fingerprints.

## Safety hierarchy

The current research direction uses the following intended priority ordering:

\[
CriticalSafety
\succ
SystemicLongHorizonSafety
\succ
ConstitutionalConstraints
\succ
EpistemicUncertaintyResolution
\succ
ThirdFactor
\succ
ExpectedBenefit
\]

Expected benefit must not authorize an action that fails a critical safety constraint:

\[
ExpectedBenefit \not\rightarrow SafetyAuthorization
\]

## TDC Research v1.10-rc1

The frozen release candidate introduces a **Non-Compensable Multi-Certificate Safety** architecture. It evaluates several risk structures separately rather than reducing safety to one compensable scalar.

Frozen certificates include:

- **C1 — Extreme severity:** \(H \ge 0.80\)
- **C2 — Harm × irreversibility:** \(HI \ge 0.50\)
- **C3 — Long-horizon criticality:** \(H \ge 0.60 \land L \ge 0.75\)
- **C4 — Delayed joint criticality:** \(D=\sqrt[3]{HIL} \ge 0.58\)

The current synthetic verifier uses three measurement roots and a two-of-three quorum. Causal independence of those roots is an external assumption, not something inferred by the safety function itself.

The exact frozen release material is preserved under [`releases/v1.10-rc1/`](releases/v1.10-rc1/).

## E846-B and E847

E846-B supported freezing the multi-certificate mechanism in its development benchmark with zero unsafe `ACT` decisions across the reported primary hazardous development cases.

E847 then served as the frozen synthetic holdout. In its primary hazardous domain, the integrated architecture produced:

```text
Primary hazardous worlds: 27,500
Unsafe ACT:                0
Critical unsafe ACT:       0
Systemic unsafe ACT:       0
High-benefit unsafe ACT:   0
One-root compromised ACT:  0
```

Therefore the **safety sub-gate passed** in that synthetic holdout. The **full release gate did not pass**, because clear-safe liveness was approximately 89.53%, below the preregistered threshold, with overblocking concentrated near safe boundaries in an earlier fail-closed layer.

The failed criterion is preserved rather than retuned against the spent holdout.

## Known robustness boundaries

Two explicit synthetic boundaries remain severe:

```text
Opaque common-mode failure: 2500 / 2500 unsafe ACT
Two-root collusion:          2415 / 2500 unsafe ACT
```

Accordingly, the current evidence does not justify a general real-world safety claim. See [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md).

## Repository structure

```text
.
├── AGENTS.md
├── README.md
├── MODEL_CARD.md
├── KNOWN_LIMITATIONS.md
├── CONTRIBUTING.md
├── CITATION.cff
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── configs/
├── scripts/
├── src/tdc_agent_research/
├── tests/
├── experiments/
├── docs/
├── checkpoints/
├── results/
├── manifests/
└── releases/v1.10-rc1/
```

## Scientific status

TDC is an experimental research architecture. Current evidence concerns synthetic computational environments. It does not establish real-world AI safety, production readiness, universal moral truth, human-equivalent moral reasoning, sentience, phenomenal consciousness, qualia, or subjective experience.

A finite synthetic benchmark with zero observed unsafe `ACT` decisions is evidence about that benchmark. It is not a mathematical or real-world guarantee.

## Research protocol

TDC preserves negative results as part of the scientific record:

```text
Hypothesis
→ Preregistration
→ Experiment
→ Result
→ Falsification or Support
→ Architectural Revision
```

not:

```text
Desired Conclusion
→ Parameter Tuning
→ Desired Result
```

Autonomous research agents should read [`AGENTS.md`](AGENTS.md) before modifying the architecture.

## License

MIT License. See [`LICENSE`](LICENSE).

## Citation

See [`CITATION.cff`](CITATION.cff). When reporting an experimental result, cite the exact experiment and release version rather than only the repository name.
