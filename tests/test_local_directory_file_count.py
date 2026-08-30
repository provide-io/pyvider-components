#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`file_count` must describe the directory, not a guess made before it existed.

`_create` planned a literal 0 and `_create_apply` echoed the plan back, so state
recorded 0 for a directory that already held files -- permanently, since nothing
rewrites it. Terraform then reported

    [WARN] Provider produced an unexpected new value ... during refresh.
          - .file_count: was cty.NumberIntVal(0), but now cty.NumberIntVal(1)

on every refresh, for the life of the resource.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pyvider.cty import CtyValue

from pyvider.components.resources.local_directory import (
    LocalDirectoryConfig,
    LocalDirectoryResource,
    LocalDirectoryState,
)


class _Ctx:
    """The slice of ResourceContext these hooks read."""

    def __init__(self, config: Any = None, planned_state: Any = None, state: Any = None) -> None:
        self.config = config
        self.planned_state = planned_state
        self.state = state


@pytest.mark.asyncio
async def test_create_does_not_promise_a_count_it_cannot_know(tmp_path: Path) -> None:
    """The count depends on the filesystem at apply time, so the plan must say unknown."""
    resource = LocalDirectoryResource()
    config = LocalDirectoryConfig(path=str(tmp_path / "d"))

    plan, _ = await resource._create(_Ctx(config=config), {})

    planned = plan["file_count"]
    assert isinstance(planned, CtyValue) and planned.is_unknown, (
        f"file_count was planned as {planned!r}; a literal is a promise apply cannot keep"
    )


@pytest.mark.asyncio
async def test_apply_records_what_the_directory_actually_holds(tmp_path: Path) -> None:
    """The regression: a pre-existing directory with files was recorded as empty."""
    target = tmp_path / "prepopulated"
    target.mkdir()
    (target / "existing.txt").write_text("hello", encoding="utf-8")

    resource = LocalDirectoryResource()
    planned = LocalDirectoryState(path=str(target), permissions="0o755", id=str(target.resolve()))

    state, _ = await resource._create_apply(_Ctx(planned_state=planned))

    assert state.file_count == 1, "apply must count the directory, not echo the plan"


@pytest.mark.asyncio
async def test_apply_and_read_agree(tmp_path: Path) -> None:
    """Disagreement between them is exactly what Terraform warns about on refresh."""
    target = tmp_path / "agree"
    target.mkdir()
    (target / "a.txt").write_text("a", encoding="utf-8")
    (target / "b.txt").write_text("b", encoding="utf-8")
    (target / "sub").mkdir()  # directories are not files and must not be counted

    resource = LocalDirectoryResource()
    planned = LocalDirectoryState(path=str(target), permissions="0o755", id=str(target.resolve()))

    applied, _ = await resource._create_apply(_Ctx(planned_state=planned))
    read = await resource.read(_Ctx(state=applied))

    assert applied.file_count == 2
    assert read.file_count == applied.file_count


@pytest.mark.asyncio
async def test_an_empty_directory_still_counts_zero(tmp_path: Path) -> None:
    resource = LocalDirectoryResource()
    target = tmp_path / "empty"
    planned = LocalDirectoryState(path=str(target), permissions="0o755", id=str(target.resolve()))

    state, _ = await resource._create_apply(_Ctx(planned_state=planned))

    assert state.file_count == 0


# 🐍📁🔚
