import pytest
from wrknv.memray.runner import run_memray_stress


@pytest.mark.memray
def test_collection_functions_memory(memray_output_dir, memray_baseline, memray_baselines_path):
    run_memray_stress(
        script="scripts/memray/memray_collection_functions_stress.py",
        baseline_key="collection_functions_total_allocations",
        output_dir=memray_output_dir,
        baselines=memray_baseline,
        baselines_path=memray_baselines_path,
    )
