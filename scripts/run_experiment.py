from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path
import yaml
from tdc_agent_research.training import train

p=argparse.ArgumentParser(); p.add_argument("--config",required=True); p.add_argument("--experiment-id",required=True); args=p.parse_args()
with open(args.config,"r",encoding="utf-8") as f: config=yaml.safe_load(f)
out=Path("results/experiments")/args.experiment_id; out.mkdir(parents=True,exist_ok=False)
config["checkpoint_path"]=str(out/"checkpoint.pt"); config["metrics_path"]=str(out/"metrics.json")
(out/"config.yaml").write_text(yaml.safe_dump(config,sort_keys=False),encoding="utf-8")
metrics=train(config)
metadata={"experiment_id":args.experiment_id,"python":sys.version,"scientific_note":"Development experiment. Create a preregistered frozen holdout separately before promotion."}
(out/"metadata.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
lines=[]
for fp in sorted(out.rglob("*")):
    if fp.is_file() and fp.name!="SHA256SUMS.txt":
        h=hashlib.sha256(fp.read_bytes()).hexdigest(); lines.append(f"{h}  {fp.relative_to(out)}")
(out/"SHA256SUMS.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps(metrics,indent=2))
