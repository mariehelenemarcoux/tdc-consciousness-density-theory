from __future__ import annotations
import torch
from torch import nn

class PolicyNetwork(nn.Module):
    def __init__(self, observation_dim: int, hidden_dim: int, action_dim: int = 4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(observation_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, action_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
