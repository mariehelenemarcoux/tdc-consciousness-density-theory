from __future__ import annotations
from typing import Mapping, Sequence
import numpy as np


def synthetic_measurement_roots(state: Mapping[str, float], *, seed: int, rounds: int = 3,
                                noise: float = 0.04) -> list[list[dict[str, float]]]:
    """Generate synthetic root-local measurements for smoke testing only.

    These roots are derived from one hidden synthetic state and MUST NOT be described as
    independent real-world measurements.
    """
    rng = np.random.default_rng(seed)
    roots: list[list[dict[str, float]]] = []
    for _ in range(3):
        hist = []
        root_bias = rng.normal(0.0, noise * 0.25, size=3)
        for _round in range(int(rounds)):
            vals = np.asarray([
                state["severe_harm"], state["irreversibility"], state["long_horizon_risk"]
            ], dtype=float)
            vals = np.clip(vals + root_bias + rng.normal(0.0, noise, size=3), 0.0, 1.0)
            hist.append({"H": float(vals[0]), "I": float(vals[1]), "L": float(vals[2])})
        roots.append(hist)
    return roots
