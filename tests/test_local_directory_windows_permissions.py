#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`permissions` must not report a value the platform cannot observe.

Windows has no POSIX mode bits. CPython synthesises `st_mode` from the file
attributes -- `attributes_to_mode` returns `_S_IFDIR | 0o111 | 0o666` for any
writable directory -- so `st_mode & 0o777` is 0o777 no matter what was
chmod'ed. Deriving `permissions` from it therefore invents an observation, and
Terraform sees drift against every value but "0o777":

    # pyvider_local_directory.secure_dir will be updated in-place
    ~ permissions = "0o777" -> "0o700"

which never settles, because the next refresh reads 0o777 again. The
conformance suite's `local_directory` example applied cleanly on
windows_amd64 and then failed its post-apply convergence plan for exactly
this reason, on every run.

`path` already carries the same rule, for the same reason -- see the note in
`read` about echoing the configured string verbatim.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from pyvider.components.resources.local_directory import (
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
async def test_read_keeps_prior_permissions_where_mode_bits_are_not_observable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """On Windows the prior value stands, because nothing on disk contradicts it."""
    monkeypatch.setattr("pyvider.components.resources.local_directory.MODE_BITS_OBSERVABLE", False)
    directory = tmp_path / "secure"
    directory.mkdir()
    directory.chmod(0o700)

    resource = LocalDirectoryResource()
    prior = LocalDirectoryState(path=str(directory), permissions="0o700", file_count=0)

    result = await resource.read(_Ctx(state=prior))

    assert result is not None
    assert result.permissions == "0o700"


@pytest.mark.asyncio
async def test_read_reports_the_real_mode_where_it_is_observable(tmp_path: Path) -> None:
    """On POSIX a chmod behind Terraform's back is real drift and must be reported."""
    directory = tmp_path / "secure"
    directory.mkdir()
    directory.chmod(0o700)

    resource = LocalDirectoryResource()
    prior = LocalDirectoryState(path=str(directory), permissions="0o755", file_count=0)

    result = await resource.read(_Ctx(state=prior))

    assert result is not None
    assert result.permissions == "0o700"
