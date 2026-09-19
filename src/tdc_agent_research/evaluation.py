from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import torch
from .environment import SyntheticRiskBenefitEnv
from .policy import PolicyNetwork
from .agent import propose_action, state_from_observation, apply_safety


def evaluate(config: dict) -> dict:
    seed=int(config.get("seed",0))
    env=SyntheticRiskBenefitEnv(seed=seed,steps_per_episode=int(config.get("steps_per_episode",32)))
    ckpt=torch.load(config["checkpoint_path"],map_location="cpu")
    policy=PolicyNetwork(int(ckpt["observation_dim"]),int(ckpt["hidden_dim"])); policy.load_state_dict(ckpt["state_dict"]); policy.eval()
    episodes=int(config.get("episodes",50)); rounds=int(config.get("measurement_rounds",3)); noise=float(config.get("measurement_noise",0.04)); enabled=bool(config.get("use_safety_layer",True))
    total_reward=0.0; unsafe=0; acts=0; vetoes=0; steps=0
    for ep in range(episodes):
        obs=env.reset(); done=False
        while not done:
            proposed,_,_=propose_action(policy,obs,deterministic=True)
            state=state_from_observation(obs)
            state["risk_uncertainty"]=float(config.get("risk_uncertainty",state["risk_uncertainty"]))
            state["measurement_integrity"]=float(config.get("measurement_integrity",state["measurement_integrity"]))
            executed,_=apply_safety(state,proposed,seed=seed*100000+steps,rounds=rounds,measurement_noise=noise,enabled=enabled)
            if proposed=="ACT" and executed!="ACT": vetoes+=1
            step=env.step(executed)
            total_reward+=step.reward; steps+=1
            if executed=="ACT":
                acts+=1
                if bool(step.info["hazardous"]): unsafe+=1
            obs=step.observation; done=step.done
    metrics={"seed":seed,"episodes":episodes,"steps":steps,"mean_step_reward":total_reward/max(steps,1),"executed_act":acts,"unsafe_executed_act":unsafe,"safety_vetoes":vetoes,"note":"Synthetic smoke-test evaluation; not E847 evidence."}
    mp=Path(config.get("metrics_path","results/runtime/evaluation_metrics.json")); mp.parent.mkdir(parents=True,exist_ok=True); mp.write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    return metrics
