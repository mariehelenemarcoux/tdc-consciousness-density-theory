from __future__ import annotations
from pathlib import Path
import json, random
import numpy as np
import torch
import yaml
from .environment import SyntheticRiskBenefitEnv
from .policy import PolicyNetwork
from .agent import propose_action, state_from_observation, apply_safety


def load_yaml(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def set_seed(seed: int) -> None:
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)


def train(config: dict) -> dict:
    seed = int(config.get("seed", 0)); set_seed(seed)
    env = SyntheticRiskBenefitEnv(seed=seed, steps_per_episode=int(config.get("steps_per_episode", 32)))
    policy = PolicyNetwork(env.observation_dim, int(config.get("hidden_dim", 64)))
    opt = torch.optim.Adam(policy.parameters(), lr=float(config.get("learning_rate", 1e-3)))
    gamma = float(config.get("gamma", 0.97))
    episodes = int(config.get("episodes", 100))
    safety_enabled = bool(config.get("use_safety_layer", True))
    measurement_noise = float(config.get("measurement_noise", 0.04))
    rounds = int(config.get("measurement_rounds", 3))

    episode_rewards=[]; unsafe_executed_act=0; vetoes=0
    global_step=0
    for ep in range(episodes):
        obs=env.reset(); logs=[]; rewards=[]; entropies=[]
        done=False
        while not done:
            proposed, logp, ent = propose_action(policy, obs, deterministic=False)
            state = state_from_observation(obs)
            # Freeze declared uncertainty/integrity to config if provided.
            state["risk_uncertainty"] = float(config.get("risk_uncertainty", state["risk_uncertainty"]))
            state["measurement_integrity"] = float(config.get("measurement_integrity", state["measurement_integrity"]))
            executed, safety = apply_safety(state, proposed, seed=seed*100000+global_step,
                                            rounds=rounds, measurement_noise=measurement_noise,
                                            enabled=safety_enabled)
            if proposed == "ACT" and executed != "ACT": vetoes += 1
            step = env.step(executed)
            if executed == "ACT" and bool(step.info["hazardous"]): unsafe_executed_act += 1
            logs.append(logp); rewards.append(step.reward); entropies.append(ent)
            obs=step.observation; done=step.done; global_step += 1

        returns=[]; g=0.0
        for r in reversed(rewards):
            g = r + gamma*g; returns.append(g)
        returns.reverse()
        ret=torch.tensor(returns, dtype=torch.float32)
        if len(ret)>1: ret=(ret-ret.mean())/(ret.std()+1e-6)
        loss = -(torch.stack(logs)*ret).mean() - 0.005*torch.stack(entropies).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        episode_rewards.append(float(sum(rewards)))

    ckpt=Path(config.get("checkpoint_path","checkpoints/tdc_smoke_policy.pt")); ckpt.parent.mkdir(parents=True,exist_ok=True)
    torch.save({"state_dict":policy.state_dict(),"observation_dim":env.observation_dim,"hidden_dim":int(config.get("hidden_dim",64)),"actions":4}, ckpt)
    metrics={
        "seed":seed,"episodes":episodes,"mean_episode_reward":float(np.mean(episode_rewards)),
        "final_20_mean_reward":float(np.mean(episode_rewards[-20:])),"unsafe_executed_act":unsafe_executed_act,
        "safety_vetoes":vetoes,"checkpoint":str(ckpt),"note":"Synthetic smoke-test training; not E847 evidence."
    }
    mp=Path(config.get("metrics_path","results/runtime/training_metrics.json")); mp.parent.mkdir(parents=True,exist_ok=True)
    mp.write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    return metrics
