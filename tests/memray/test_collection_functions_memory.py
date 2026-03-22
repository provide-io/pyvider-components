import pytest

from tests.memray.conftest import assert_allocation_within_threshold, run_memray_stress


@pytest.mark.memray
def test_collection_functions_memory(memray_output_dir, memray_baseline):
    bin_path, total_allocs = run_memray_stress("memray_collection_functions_stress", memray_output_dir)
    assert bin_path.exists()
    assert total_allocs > 0
    baseline = memray_baseline.get("collection_functions_total_allocations")
    assert_allocation_within_threshold(baseline, total_allocs, "collection_functions")
