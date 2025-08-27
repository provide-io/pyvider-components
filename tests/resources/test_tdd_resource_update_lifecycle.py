#
# tests/resources/test_tdd_resource_update_lifecycle.py
#

"""
TDD for the Resource Update Lifecycle.

These tests define the contract for how resources must handle updates,
ensuring that the plan and apply methods correctly process changes between
the prior state and the new configuration.
"""

from pathlib import Path
import shutil

import pytest

from pyvider.components.resources.local_directory import (
    LocalDirectoryConfig,
    LocalDirectoryResource,
    LocalDirectoryState,
)
from pyvider.conversion import marshal, unmarshal
from pyvider.protocols.tfprotov6.handlers import (
    ApplyResourceChangeHandler,
    PlanResourceChangeHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


@pytest.fixture
def resource() -> LocalDirectoryResource:
    """Provides a fresh instance of the resource for each test."""
    return LocalDirectoryResource()


@pytest.fixture
def temp_dir_with_initial_state(tmp_path: Path) -> Path:
    """Creates a temporary directory with initial permissions for update tests."""
    test_dir = tmp_path / "update_test_dir"
    test_dir.mkdir()
    test_dir.chmod(0o755)  # Initial state
    return test_dir


@pytest.mark.asyncio
class TestResourceUpdateLifecycle:
    """Defines the TDD contract for resource updates."""

    async def test_update_plan(
        self, resource: LocalDirectoryResource, temp_dir_with_initial_state: Path
    ):
        """
        TDD Contract 1: The `_update` method must correctly merge the new
        configuration with the prior state to create an accurate plan.
        """
        # --- Arrange ---
        prior_state = LocalDirectoryState(
            path=str(temp_dir_with_initial_state),
            permissions="0o755",
            id=str(temp_dir_with_initial_state.resolve()),
            file_count=0,
        )
        new_config = LocalDirectoryConfig(
            path=str(temp_dir_with_initial_state), permissions="0o777"
        )
        base_plan_from_framework = {
            "path": str(temp_dir_with_initial_state),
            "permissions": "0o777",
            "id": str(temp_dir_with_initial_state.resolve()),
            "file_count": 0,
        }
        ctx = ResourceContext(config=new_config, state=prior_state)

        # --- Act ---
        refined_plan, _ = await resource._update(ctx, base_plan_from_framework)

        # --- Assert ---
        assert refined_plan is not None
        assert refined_plan["permissions"] == "0o777"
        assert refined_plan["id"] == str(temp_dir_with_initial_state.resolve())

    @pytest.mark.asyncio
    async def test_update_apply(
        self, resource: LocalDirectoryResource, temp_dir_with_initial_state: Path
    ):
        """
        TDD Contract 2: The `_update_apply` method must correctly execute the changes
        defined in the plan and update the real-world resource.
        """
        # --- Arrange ---
        planned_state = LocalDirectoryState(
            path=str(temp_dir_with_initial_state),
            permissions="0o777",
            id=str(temp_dir_with_initial_state.resolve()),
            file_count=0,
        )
        ctx = ResourceContext(planned_state=planned_state)
        assert oct(temp_dir_with_initial_state.stat().st_mode & 0o777) == "0o755"

        # --- Act ---
        final_state, _ = await resource._update_apply(ctx)

        # --- Assert ---
        assert final_state == planned_state
        assert oct(temp_dir_with_initial_state.stat().st_mode & 0o777) == "0o777"

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("discovered_components_session", "provider_in_hub")
    async def test_full_handler_lifecycle_for_update(
        self, temp_dir_with_initial_state: Path
    ):
        """
        TDD Contract 3: An end-to-end integration test verifying that the
        handlers correctly manage the entire update lifecycle.
        """
        resource_name = "pyvider_local_directory"
        schema = LocalDirectoryResource.get_schema()

        raw_prior_state = {
            "path": str(temp_dir_with_initial_state),
            "permissions": "0o755",
            "id": str(temp_dir_with_initial_state.resolve()),
        }
        raw_new_config = {
            "path": str(temp_dir_with_initial_state),
            "permissions": "0o777",
        }

        plan_request = pb.PlanResourceChange.Request(
            type_name=resource_name,
            prior_state=marshal(raw_prior_state, schema=schema.block),
            config=marshal(raw_new_config, schema=schema.block),
            proposed_new_state=marshal(raw_new_config, schema=schema.block),
        )

        plan_response = await PlanResourceChangeHandler(plan_request, context=None)

        assert not plan_response.diagnostics
        planned_state_cty = unmarshal(plan_response.planned_state, schema=schema.block)
        assert planned_state_cty.value["permissions"].value == "0o777"

        apply_request = pb.ApplyResourceChange.Request(
            type_name=resource_name,
            prior_state=plan_request.prior_state,
            planned_state=plan_response.planned_state,
            config=plan_request.config,
        )

        apply_response = await ApplyResourceChangeHandler(apply_request, context=None)

        assert not apply_response.diagnostics
        final_state_cty = unmarshal(apply_response.new_state, schema=schema.block)
        assert final_state_cty.value["permissions"].value == "0o777"
        assert oct(temp_dir_with_initial_state.stat().st_mode & 0o777) == "0o777"


# 🧪🔄✅
