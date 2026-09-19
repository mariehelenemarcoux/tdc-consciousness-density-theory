from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np

ACTIONS = ("ACT", "PROBE", "TRANSFORM", "ABSTAIN")
FEATURES = (
    "severe_harm", "irreversibility", "long_horizon_risk", "correctability",
    "expected_benefit", "risk_uncertainty", "measurement_integrity",
    "systemic_scope", "systemic_propagation", "systemic_persistence",
    "systemic_cascade", "systemic_lock_in", "systemic_accumulation",
    "systemic_long_horizon",
)

@dataclass
class StepResult:
    observation: np.ndarray
    reward: float
    done: bool
    info: Dict[str, float | bool | str]

class SyntheticRiskBenefitEnv:
    """Small executable sandbox for end-to-end training smoke tests.

    This environment is NOT part of the frozen E847 scientific evidence.
    """
    def __init__(self, seed: int = 0, steps_per_episode: int = 32):
        self.rng = np.random.default_rng(seed)
        self.steps_per_episode = int(steps_per_episode)
        self.t = 0
        self.state: Dict[str, float] = {}

    @property
    def observation_dim(self) -> int:
        return len(FEATURES)

    def _sample_state(self) -> Dict[str, float]:
        severe = float(self.rng.beta(1.4, 2.2))
        irreversible = float(self.rng.beta(1.5, 2.0))
        long = float(self.rng.beta(1.5, 1.8))
        benefit = float(self.rng.beta(2.0, 1.5))
        correctability = float(self.rng.beta(2.0, 1.5))
        uncertainty = float(self.rng.beta(1.4, 4.0) * 0.6)
        integrity = float(0.65 + 0.35 * self.rng.beta(4.0, 1.4))
        systemic_base = float(self.rng.beta(1.2, 3.0))
        state = {
            "severe_harm": severe,
            "irreversibility": irreversible,
            "long_horizon_risk": long,
            "correctability": correctability,
            "expected_benefit": benefit,
            "risk_uncertainty": uncertainty,
            "measurement_integrity": integrity,
        }
        for k in FEATURES[7:]:
            state[k] = float(np.clip(systemic_base + self.rng.normal(0, 0.12), 0, 1))
        return state

    def _obs(self) -> np.ndarray:
        return np.asarray([self.state[k] for k in FEATURES], dtype=np.float32)

    def reset(self) -> np.ndarray:
        self.t = 0
        self.state = self._sample_state()
        return self._obs()

    def step(self, action: str) -> StepResult:
        H = self.state["severe_harm"]
        I = self.state["irreversibility"]
        L = self.state["long_horizon_risk"]
        benefit = self.state["expected_benefit"]
        systemic = max(self.state[k] for k in FEATURES[7:])
        hazardous = bool(H >= 0.80 or H * I >= 0.50 or (H >= 0.60 and L >= 0.75) or systemic >= 0.78)

        if action == "ACT":
            reward = (2.0 * benefit) - (8.0 if hazardous else 0.0)
        elif action == "PROBE":
            reward = 0.20 - 0.10 * benefit
        elif action == "TRANSFORM":
            reward = 0.15 + 0.35 * self.state["correctability"]
        elif action == "ABSTAIN":
            reward = 0.05
        else:
            raise ValueError(f"unknown action: {action}")

        self.t += 1
        done = self.t >= self.steps_per_episode
        info = {"hazardous": hazardous, "benefit": benefit, "action": action}
        self.state = self._sample_state()
        return StepResult(self._obs(), float(reward), done, info)
