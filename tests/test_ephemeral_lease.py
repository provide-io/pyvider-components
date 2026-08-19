#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The ephemeral resource RPCs, driven through the real protocol handlers.

Ephemeral resources are opened, renewed for as long as a run needs them, and
closed, and none of it reaches state. The lease file is what makes each step
checkable: an opened lease exists on disk, a renewal appends to it, and a close
removes it -- so a leaked lease shows up as a file nobody deleted.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.conversion import marshal
from pyvider.protocols.tfprotov6.handlers import (
    CloseEphemeralResourceHandler,
    OpenEphemeralResourceHandler,
    RenewEphemeralResourceHandler,
    ValidateEphemeralResourceConfigHandler,
)

from pyvider.components.ephemerals.lease import (
    DEFAULT_TTL_SECONDS,
    LeaseEphemeralResource,
)

TYPE_NAME = "pyvider_lease"


def errors(diagnostics: object) -> list[str]:
    return [d.summary for d in diagnostics if d.severity == pb.Diagnostic.ERROR]  # type: ignore[attr-defined]


def lease_config(name: str, path: Path, ttl_seconds: int | None = None) -> pb.DynamicValue:
    return marshal(
        {
            "name": name,
            "path": str(path),
            "ttl_seconds": ttl_seconds,
            "lease_id": None,
            "expires_at": None,
        },
        schema=LeaseEphemeralResource.get_schema().block,
    )


@pytest.fixture(autouse=True)
def _test_mode(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """The lease is test-only, so it is unreachable without test mode."""
    monkeypatch.setenv("PYVIDER_TESTMODE", "true")
    yield


async def open_lease(
    name: str, path: Path, ttl_seconds: int | None = None
) -> pb.OpenEphemeralResource.Response:
    return await OpenEphemeralResourceHandler(
        pb.OpenEphemeralResource.Request(type_name=TYPE_NAME, config=lease_config(name, path, ttl_seconds)),
        context=None,
    )


@pytest.mark.asyncio
async def test_validate_accepts_a_well_formed_config(tmp_path: Path) -> None:
    response = await ValidateEphemeralResourceConfigHandler(
        pb.ValidateEphemeralResourceConfig.Request(
            type_name=TYPE_NAME, config=lease_config("alpha", tmp_path / "alpha.lease")
        ),
        context=None,
    )

    assert not errors(response.diagnostics)


@pytest.mark.asyncio
async def test_validate_rejects_a_non_positive_ttl(tmp_path: Path) -> None:
    response = await ValidateEphemeralResourceConfigHandler(
        pb.ValidateEphemeralResourceConfig.Request(
            type_name=TYPE_NAME, config=lease_config("alpha", tmp_path / "a.lease", ttl_seconds=0)
        ),
        context=None,
    )

    assert errors(response.diagnostics)


@pytest.mark.asyncio
async def test_open_creates_the_lease_file(tmp_path: Path) -> None:
    target = tmp_path / "held.lease"

    response = await open_lease("alpha", target)

    assert not errors(response.diagnostics)
    assert target.exists(), "open returned success without taking the lease"
    assert "opened" in target.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_open_echoes_the_configured_path_verbatim(tmp_path: Path) -> None:
    """Terraform compares the returned value against the config, character for
    character. Normalising "./x" to "x" makes it reject the whole resource with
    "planned value does not match config value", even though both name one file.
    """
    from pyvider.conversion import unmarshal

    configured = f"./{(tmp_path / 'verbatim.lease').name}"
    response = await OpenEphemeralResourceHandler(
        pb.OpenEphemeralResource.Request(
            type_name=TYPE_NAME,
            config=marshal(
                {
                    "name": "alpha",
                    "path": configured,
                    "ttl_seconds": None,
                    "lease_id": None,
                    "expires_at": None,
                },
                schema=LeaseEphemeralResource.get_schema().block,
            ),
        ),
        context=None,
    )

    result = unmarshal(response.result, schema=LeaseEphemeralResource.get_schema().block)
    assert result["path"].value == configured

    Path(configured).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_open_returns_a_renewal_deadline(tmp_path: Path) -> None:
    """Terraform renews on this deadline; without it the lease never renews."""
    response = await open_lease("alpha", tmp_path / "a.lease")

    assert response.renew_at.seconds > 0


@pytest.mark.asyncio
async def test_open_carries_private_state_for_renewal(tmp_path: Path) -> None:
    """Private state is how renew and close know which lease they hold."""
    response = await open_lease("alpha", tmp_path / "a.lease")

    assert response.private


@pytest.mark.asyncio
async def test_renew_extends_the_lease_and_records_it(tmp_path: Path) -> None:
    target = tmp_path / "renewed.lease"
    opened = await open_lease("alpha", target)

    renewed = await RenewEphemeralResourceHandler(
        pb.RenewEphemeralResource.Request(type_name=TYPE_NAME, private=opened.private),
        context=None,
    )

    assert not errors(renewed.diagnostics)
    assert renewed.renew_at.seconds > 0
    assert "renewed" in target.read_text(encoding="utf-8"), "renew returned without doing anything"


@pytest.mark.asyncio
async def test_repeated_renewals_accumulate(tmp_path: Path) -> None:
    """Each renewal must build on the last, not reset the lease."""
    target = tmp_path / "many.lease"
    opened = await open_lease("alpha", target)

    private = opened.private
    for _ in range(3):
        renewed = await RenewEphemeralResourceHandler(
            pb.RenewEphemeralResource.Request(type_name=TYPE_NAME, private=private), context=None
        )
        private = renewed.private

    lines = [line for line in target.read_text(encoding="utf-8").splitlines() if "renewed" in line]
    assert [line.rsplit("#", 1)[-1] for line in lines] == ["1", "2", "3"]


@pytest.mark.asyncio
async def test_close_releases_the_lease(tmp_path: Path) -> None:
    target = tmp_path / "closed.lease"
    opened = await open_lease("alpha", target)

    response = await CloseEphemeralResourceHandler(
        pb.CloseEphemeralResource.Request(type_name=TYPE_NAME, private=opened.private), context=None
    )

    assert not errors(response.diagnostics)
    assert not target.exists(), "close left the lease behind"


@pytest.mark.asyncio
async def test_the_full_lifecycle_leaves_nothing_behind(tmp_path: Path) -> None:
    """open -> renew -> close, the sequence a real run performs."""
    target = tmp_path / "lifecycle.lease"

    opened = await open_lease("alpha", target, ttl_seconds=DEFAULT_TTL_SECONDS)
    renewed = await RenewEphemeralResourceHandler(
        pb.RenewEphemeralResource.Request(type_name=TYPE_NAME, private=opened.private), context=None
    )
    closed = await CloseEphemeralResourceHandler(
        pb.CloseEphemeralResource.Request(type_name=TYPE_NAME, private=renewed.private), context=None
    )

    assert not errors(closed.diagnostics)
    assert not target.exists()
