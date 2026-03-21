import pytest

from tests.memray.conftest import assert_allocation_within_threshold, run_memray_stress


@pytest.mark.memray
def test_env_datasource_memory(memray_output_dir, memray_baseline):
    bin_path, total_allocs = run_memray_stress("memray_env_datasource_stress", memray_output_dir)
    assert bin_path.exists()
    assert total_allocs > 0
    baseline = memray_baseline.get("env_datasource_total_allocations")
    assert_allocation_within_threshold(baseline, total_allocs, "env_datasource")
