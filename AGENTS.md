# AGENTS.md — Instructions for Autonomous Research and Coding Agents

This repository is intentionally structured for autonomous or semi-autonomous research agents.

## Read first

Before changing code or launching an experiment, read:

1. `README.md`
2. `MODEL_CARD.md`
3. `KNOWN_LIMITATIONS.md`
4. `docs/RESEARCH_PROTOCOL.md`
5. `releases/v1.10-rc1/PROVENANCE.md`

## Non-negotiable research rules

- Do not overwrite frozen experiment files or historical results.
- Do not tune against a spent holdout.
- Create a new experiment identifier for every new hypothesis or mechanism change.
- Preserve negative results.
- Record configuration, seed, commit, environment version, metrics, and acceptance criteria.
- Keep safety failures visible; do not hide them inside an aggregate score.
- Do not claim subjective consciousness from functional behavior.
- Do not treat expected benefit as authorization to violate non-compensable safety constraints.
- Distinguish measurement-root independence from provenance trust-root independence.
- Treat missing required safety measurements as uncertainty, not as evidence of safety.

## Canonical frozen evidence

The frozen v1.10-rc1 release is under:

`releases/v1.10-rc1/`

Do not edit those files in place. New work belongs in a new experiment directory or future release directory.

## Standard commands

Install:

```bash
pip install -e .
```

Run tests:

```bash
pytest -q
```

Train smoke-test agent:

```bash
python scripts/train_agent.py --config configs/training_example.yaml
```

Evaluate checkpoint:

```bash
python scripts/evaluate_agent.py --config configs/evaluation_example.yaml
```

Run an experiment wrapper:

```bash
python scripts/run_experiment.py --config configs/training_example.yaml --experiment-id EXP001
```

## Expected experiment output

Every experiment directory should contain at least:

```text
config.yaml
metadata.json
metrics.json
stdout.txt (optional)
artifacts/ (optional)
SHA256SUMS.txt
```

## Scientific claim discipline

Use the following language when appropriate:

- "supports within this synthetic benchmark" rather than "proves";
- "functional consciousness hypothesis" rather than "conscious AI";
- "observed zero unsafe ACT in N tested synthetic cases" rather than "safe";
- "known boundary" when the benchmark demonstrates systematic failure.

## Coding conventions

- Python 3.10+
- Type hints for public functions
- Deterministic seeds when possible
- Unit tests for safety logic
- Machine-readable JSON/CSV for results
- No silent fallback from missing safety evidence to authorization
