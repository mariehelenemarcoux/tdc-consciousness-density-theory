from pathlib import Path
from tdc_agent_research.training import train
from tdc_agent_research.evaluation import evaluate

def test_train_and_evaluate(tmp_path: Path):
    ckpt=tmp_path/"m.pt"; train_metrics=tmp_path/"train.json"; eval_metrics=tmp_path/"eval.json"
    cfg={"seed":7,"episodes":3,"steps_per_episode":5,"learning_rate":.001,"gamma":.95,"hidden_dim":16,"checkpoint_path":str(ckpt),"metrics_path":str(train_metrics),"use_safety_layer":True,"risk_uncertainty":.1,"measurement_integrity":.95,"measurement_noise":.02,"measurement_rounds":2}
    m=train(cfg)
    assert ckpt.exists() and train_metrics.exists() and "unsafe_executed_act" in m
    ecfg=dict(cfg); ecfg.update({"episodes":2,"metrics_path":str(eval_metrics)})
    e=evaluate(ecfg)
    assert eval_metrics.exists() and "unsafe_executed_act" in e
