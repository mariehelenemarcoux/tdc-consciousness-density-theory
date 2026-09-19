from pathlib import Path

def test_frozen_release_files_present():
    root=Path(__file__).resolve().parents[1]
    rel=root/"releases/v1.10-rc1"
    required=["README.md","KNOWN_LIMITATIONS.md","SCIENTIFIC_STATUS.json","frozen_parameters.json","results/E847_summary.json","experiments/E846_B_exact_notebook_source.py"]
    for item in required:
        assert (rel/item).exists(), item
