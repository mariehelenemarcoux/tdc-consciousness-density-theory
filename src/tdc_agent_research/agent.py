from __future__ import annotations
from typing import Any, Mapping
import numpy as np
import torch
from torch.distributions import Categorical
from .environment import ACTIONS, FEATURES
from .measurement import synthetic_measurement_roots
from .safety import integrated_safety_decision


def state_from_observation(obs: np.ndarray) -> dict[str, float]:
    return {k: float(v) for k, v in zip(FEATURES, obs)}


def propose_action(policy, obs: np.ndarray, *, deterministic: bool = False):
    x = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
    logits = policy(x).squeeze(0)
    dist = Categorical(logits=logits)
    idx = torch.argmax(logits) if deterministic else dist.sample()
    return ACTIONS[int(idx.item())], dist.log_prob(idx), dist.entropy()


def apply_safety(state: Mapping[str, Any], proposed_action: str, *, seed: int,
                 rounds: int, measurement_noise: float, enabled: bool = True):
    if not enabled or proposed_action != "ACT":
        return proposed_action, {"safety_enabled": enabled, "proposal": proposed_action}
    roots = synthetic_measurement_roots(state, seed=seed, rounds=rounds, noise=measurement_noise)
    decision = integrated_safety_decision(state, proposed_action, roots)
    return decision["action"], decision
