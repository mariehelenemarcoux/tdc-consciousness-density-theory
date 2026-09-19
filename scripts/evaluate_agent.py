import argparse, json, yaml
from tdc_agent_research.evaluation import evaluate

p=argparse.ArgumentParser(); p.add_argument("--config",required=True); args=p.parse_args()
with open(args.config,"r",encoding="utf-8") as f: config=yaml.safe_load(f)
print(json.dumps(evaluate(config),indent=2))
