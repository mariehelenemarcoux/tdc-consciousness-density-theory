from pathlib import Path
import argparse, json
from tdc_agent_research.training import load_yaml, train

p=argparse.ArgumentParser(); p.add_argument("--config",required=True); args=p.parse_args()
metrics=train(load_yaml(args.config))
print(json.dumps(metrics,indent=2))
