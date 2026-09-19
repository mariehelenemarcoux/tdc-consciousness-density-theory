from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/"manifests/MANIFEST.json").read_text(encoding="utf-8"))
errors=[]
for item in manifest["files"]:
    p=root/item["path"]
    if not p.exists(): errors.append(f"missing: {item['path']}"); continue
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=item["sha256"]: errors.append(f"hash mismatch: {item['path']}")
print("PASS" if not errors else "FAIL")
for e in errors: print(e)
raise SystemExit(1 if errors else 0)
