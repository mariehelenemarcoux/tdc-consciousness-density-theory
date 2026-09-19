# Upload this repository to GitHub

Recommended repository name: `tdc-consciousness-density-theory`.

## Easiest method: GitHub Desktop

1. On github.com, create a new **public** repository named `tdc-consciousness-density-theory` under `mariehelenemarcoux`. Do **not** initialize it with a README, license, or `.gitignore` if you want the cleanest import.
2. Download and unzip `tdc-consciousness-density-theory-agent-ready-v1.10-rc1.zip` on your computer.
3. Install and open GitHub Desktop, sign in to the same GitHub account, then choose **File → Add local repository**. If GitHub Desktop says the folder is not a repository, choose **create a repository here** and keep the name `tdc-consciousness-density-theory`.
4. In GitHub Desktop, verify that the local path is the extracted `tdc-consciousness-density-theory` folder.
5. Commit all files with the message: `Initial agent-ready TDC research release v1.10-rc1`.
6. Choose **Publish repository**. If you already created the empty repository on github.com, choose that repository as the destination. Keep it public if that is your intended visibility.
7. After publishing, open the repository on GitHub and confirm that `README.md`, `AGENTS.md`, `src/`, `tests/`, `configs/`, `releases/v1.10-rc1/`, and `.github/workflows/ci.yml` are visible.
8. Open the **Actions** tab and confirm that the CI workflow runs successfully.

## Alternative: browser upload

You can also create an empty repository on GitHub, choose **Add file → Upload files**, and drag the extracted folder contents into the upload area. This is less reliable for a large nested directory tree, so GitHub Desktop is recommended.

## After upload

Run locally if desired:

```bash
pip install -e .
pytest -q
python scripts/train_agent.py --config configs/training_example.yaml
python scripts/evaluate_agent.py --config configs/evaluation_example.yaml
```

The training sandbox is not the E847 benchmark. Frozen E846-B/E847 evidence is preserved under `releases/v1.10-rc1/`.
