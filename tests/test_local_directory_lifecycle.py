#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import shutil
import sys
from pathlib import Path

import pytest
from pyvider.resources.context import ResourceContext

from pyvider.components.resources.local_directory import (
    LocalDirectoryConfig,
    LocalDirectoryResource,
    LocalDirectoryState,
)


@pytest.fixture
def temp_dir() -> Path:
    path = Path("/tmp/pyvider_test_dir")
    if path.exists():
        shutil.rmtree(path)
    yield path
    if path.exists():
        shutil.rmtree(path)


@pytest.fixture
def resource() -> LocalDirectoryResource:
    return LocalDirectoryResource()


@pytest.mark.skipif(sys.platform == "win32", reason="Unix file permissions not enforced on Windows")
@pytest.mark.asyncio
async def test_create_lifecycle_contract(resource: LocalDirectoryResource, temp_dir: Path):
    # 1. Define the configuration with the CANONICAL format.
    config = LocalDirectoryConfig(path=str(temp_dir), permissions="0o775")
    create_context = ResourceContext(config=config, state=None)
    base_plan = {"path": config.path, "permissions": config.permissions}

    # 2. Get the plan.
    planned_state_dict, _ = await resource._create(create_context, base_plan)
    planned_state = resource.state_class(**planned_state_dict)

    # 3. Assert the plan matches the config exactly.
    assert isinstance(planned_state, LocalDirectoryState)
    assert planned_state.path == str(temp_dir)
    assert planned_state.permissions == "0o775"
    assert planned_state.id == str(temp_dir.resolve())
    assert planned_state.file_count == 0

    # 4. Apply the plan.
    apply_context = ResourceContext(config=config, planned_state=planned_state)
    final_state, _ = await resource._create_apply(apply_context)

    # 5. The final state must be identical to the planned state.
    assert final_state == planned_state

    # 6. Verify the real world.
    assert temp_dir.exists()
    assert oct(temp_dir.stat().st_mode & 0o777) == "0o775"

    # 7. Verify the read operation.
    read_context = ResourceContext(config=None, state=final_state)
    read_state = await resource.read(read_context)
    assert read_state is not None
    assert read_state.permissions == "0o775"


@pytest.mark.skipif(sys.platform == "win32", reason="Unix file permissions not enforced on Windows")
@pytest.mark.asyncio
async def test_read_preserves_dot_slash_prefixed_path(
    resource: LocalDirectoryResource,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A `./`-prefixed path must survive create-then-read unchanged.

    This is what `${path.module}/name` produces whenever the module is the
    working directory -- the single most common spelling of a relative path
    in a real Terraform config. `read()` used to do `path=str(Path(...))`,
    and pathlib normalises `Path("./x")` to `x` when stringified, so the
    value read back after apply never matched what the practitioner wrote.
    Terraform then reported a plan that was never empty: the same one
    attribute drifting on every single `terraform plan`, forever.
    """
    monkeypatch.chdir(tmp_path)
    configured_path = "./dotslash_dir"

    config = LocalDirectoryConfig(path=configured_path, permissions="0o755")
    create_context = ResourceContext(config=config, state=None)
    base_plan = {"path": config.path, "permissions": config.permissions}

    planned_state_dict, _ = await resource._create(create_context, base_plan)
    planned_state = resource.state_class(**planned_state_dict)
    assert planned_state.path == configured_path

    apply_context = ResourceContext(config=config, planned_state=planned_state)
    final_state, _ = await resource._create_apply(apply_context)
    assert final_state is not None
    assert final_state.path == configured_path

    read_context = ResourceContext(config=None, state=final_state)
    read_state = await resource.read(read_context)
    assert read_state is not None
    assert read_state.path == configured_path, (
        "read() must echo the configured path exactly -- a plan that keeps "
        "reporting drift on 'path' here is the perpetual-diff bug"
    )


# 🧩🔧🔚
