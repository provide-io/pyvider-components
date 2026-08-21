#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The tfprotov6.11 demo components, driven through the protocol handlers.

These components exist to make the v6.11 RPCs observable from a real Terraform
run. The tests here assert the same behaviour in-process, so a regression is
caught without needing a CLI that supports `action`, `list`, or `state_store`
blocks — OpenTofu 1.12.5 supports none of them.
"""

from __future__ import annotations

import tempfile
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.conversion import marshal, unmarshal_identity
from pyvider.handler import ProviderHandler
from pyvider.protocols.tfprotov6.handlers.action_handlers import (
    PlanActionHandler,
    ValidateActionConfigHandler,
)
from pyvider.protocols.tfprotov6.handlers.config_handlers import (
    ValidateListResourceConfigHandler,
)
from pyvider.protocols.tfprotov6.handlers.get_metadata import GetMetadataHandler
from pyvider.protocols.tfprotov6.handlers.state_store_handlers import reset_state_stores

from pyvider.components.actions.echo import WRITTEN, EchoAction, FailingAction
from pyvider.components.list_resources.secret_notes import SecretNoteList
from pyvider.components.resources.secret_note import (
    _NOTES,
    NOTE_INDEX_ENV,
    SecretNoteResource,
    digest_of,
)
from pyvider.components.state_stores.filesystem_store import PyviderFileSystemStateStore

ACTION = "pyvider_echo"
LIST = "pyvider_secret_note"
STORE = "pyvider_filesystem_store"

pytestmark = pytest.mark.usefixtures(
    "discovered_components_session", "provider_in_hub", "provider_with_test_mode"
)


def errors(diagnostics: object) -> list[str]:
    return [d.summary for d in diagnostics if d.severity == pb.Diagnostic.ERROR]  # type: ignore[attr-defined]


@pytest.fixture(autouse=True)
def _clean(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    # The durable note index is shared by every provider process on the machine.
    # Without redirecting it, tests would see each other's notes and would
    # scribble into the developer's temp directory.
    monkeypatch.setenv(NOTE_INDEX_ENV, str(tmp_path / "note-index.json"))
    _NOTES.clear()
    WRITTEN.clear()
    reset_state_stores()
    yield
    _NOTES.clear()
    WRITTEN.clear()
    reset_state_stores()


def echo_config(**overrides: object) -> pb.DynamicValue:
    values: dict[str, object] = {"message": "hi", "path": None, "repeat": None, "defer": None}
    values.update(overrides)
    return marshal(values, schema=EchoAction.get_schema().block)


# --- discovery -------------------------------------------------------------


@pytest.mark.asyncio
async def test_metadata_advertises_all_three_component_types() -> None:
    response = await GetMetadataHandler(pb.GetMetadata.Request(), context=None)

    assert ACTION in {a.type_name for a in response.actions}
    assert LIST in {entry.type_name for entry in response.list_resources}
    assert STORE in {entry.type_name for entry in response.state_stores}


# --- actions ---------------------------------------------------------------


@pytest.mark.asyncio
async def test_action_validate_accepts_a_complete_config(tmp_path: Path) -> None:
    request = pb.ValidateActionConfig.Request(
        type_name=ACTION, config=echo_config(path=str(tmp_path / "log.txt"))
    )

    response = await ValidateActionConfigHandler(request, context=None)

    assert list(response.diagnostics) == []


@pytest.mark.asyncio
async def test_action_validate_reports_missing_required_values() -> None:
    request = pb.ValidateActionConfig.Request(type_name=ACTION, config=echo_config(message="", path=""))

    response = await ValidateActionConfigHandler(request, context=None)

    assert errors(response.diagnostics) == ["message is required", "path is required"]


@pytest.mark.asyncio
async def test_action_validate_rejects_a_non_positive_repeat(tmp_path: Path) -> None:
    request = pb.ValidateActionConfig.Request(
        type_name=ACTION, config=echo_config(path=str(tmp_path / "log.txt"), repeat=0)
    )

    response = await ValidateActionConfigHandler(request, context=None)

    assert errors(response.diagnostics) == ["repeat must be a positive number"]


@pytest.mark.asyncio
async def test_action_plan_warns_about_the_side_effect(tmp_path: Path) -> None:
    target = tmp_path / "log.txt"
    request = pb.PlanAction.Request(action_type=ACTION, config=echo_config(path=str(target)))

    response = await PlanActionHandler(request, context=None)

    assert [d.severity for d in response.diagnostics] == [pb.Diagnostic.WARNING]
    assert str(target) in response.diagnostics[0].summary


@pytest.mark.asyncio
async def test_action_defers_only_when_the_client_allows_it(tmp_path: Path) -> None:
    config = echo_config(path=str(tmp_path / "log.txt"), defer=True)

    allowed = pb.PlanAction.Request(action_type=ACTION, config=config)
    allowed.client_capabilities.deferral_allowed = True
    deferred = await PlanActionHandler(allowed, context=None)

    refused = await PlanActionHandler(pb.PlanAction.Request(action_type=ACTION, config=config), context=None)

    assert deferred.HasField("deferred")
    assert deferred.deferred.reason == pb.Deferred.ABSENT_PREREQ
    assert not refused.HasField("deferred")
    assert "does not allow deferrals" in errors(refused.diagnostics)[0]


@pytest.mark.asyncio
async def test_action_invoke_streams_progress_and_writes_the_file(tmp_path: Path) -> None:
    target = tmp_path / "log.txt"
    request = pb.InvokeAction.Request(
        action_type=ACTION, config=echo_config(message="hello", path=str(target), repeat=2)
    )

    events = [event async for event in ProviderHandler().InvokeAction(request, context=None)]

    assert [event.WhichOneof("type") for event in events] == [
        "progress",
        "progress",
        "progress",
        "completed",
    ]
    assert list(events[-1].completed.diagnostics) == []
    # The side effect is the point: a green completed event alone would not
    # prove the action body ran.
    assert target.read_text(encoding="utf-8").count("hello") == 2
    assert len(WRITTEN) == 2


@pytest.mark.asyncio
async def test_action_failure_still_completes_exactly_once() -> None:
    request = pb.InvokeAction.Request(
        action_type="pyvider_failing_action",
        config=marshal({"message": "x"}, schema=FailingAction.get_schema().block),
    )

    events = [event async for event in ProviderHandler().InvokeAction(request, context=None)]

    assert [event.WhichOneof("type") for event in events] == ["progress", "completed"]
    assert "rejected the request" in events[-1].completed.diagnostics[0].detail


@pytest.mark.asyncio
async def test_action_invoke_without_a_step_delay_still_writes_every_line(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The pause between steps is presentational, not part of the contract."""
    from pyvider.components.actions import echo

    monkeypatch.setattr(echo, "STEP_DELAY_SECONDS", 0)
    target = tmp_path / "fast.txt"
    request = pb.InvokeAction.Request(
        action_type=ACTION, config=echo_config(message="fast", path=str(target), repeat=3)
    )

    events = [event async for event in ProviderHandler().InvokeAction(request, context=None)]

    assert events[-1].WhichOneof("type") == "completed"
    assert target.read_text(encoding="utf-8").count("fast") == 3


# --- list resources --------------------------------------------------------


async def collect_list(**kwargs: object) -> list[pb.ListResource.Event]:
    request = pb.ListResource.Request(type_name=LIST, **kwargs)  # type: ignore[arg-type]
    return [event async for event in ProviderHandler().ListResource(request, context=None)]


@pytest.mark.asyncio
async def test_list_streams_every_note_by_default() -> None:
    _NOTES.update({"alpha": "a", "beta": "b"})

    events = await collect_list()

    assert [event.display_name for event in events] == ["alpha", "beta"]


@pytest.mark.asyncio
async def test_list_honours_the_name_prefix_filter() -> None:
    _NOTES.update({"alpha": "a", "beta": "b", "bravo": "c"})
    config = marshal({"name_prefix": "b", "include_archived": None}, schema=SecretNoteList.get_schema().block)

    events = await collect_list(config=config)

    assert [event.display_name for event in events] == ["beta", "bravo"]


@pytest.mark.asyncio
async def test_list_encodes_identity_from_the_managed_resource() -> None:
    _NOTES["alpha"] = "a"

    events = await collect_list()

    decoded = unmarshal_identity(events[0].identity, SecretNoteResource.get_identity_schema())
    assert decoded == {"name": "alpha"}


@pytest.mark.asyncio
async def test_list_includes_the_resource_object_only_on_request() -> None:
    _NOTES["alpha"] = "secret"

    without = await collect_list()
    with_object = await collect_list(include_resource_object=True)

    assert not without[0].HasField("resource_object")
    assert with_object[0].HasField("resource_object")


@pytest.mark.asyncio
async def test_list_stops_at_the_requested_limit() -> None:
    _NOTES.update({"a": "1", "b": "2", "c": "3"})

    events = await collect_list(limit=2)

    assert len(events) == 2


@pytest.mark.asyncio
async def test_list_validation_rejects_a_blank_prefix() -> None:
    config = marshal({"name_prefix": "  ", "include_archived": None}, schema=SecretNoteList.get_schema().block)
    request = pb.ValidateListResourceConfig.Request(type_name=LIST, config=config)

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert errors(response.diagnostics) == ["name_prefix must not be empty; omit it to list every note"]


# --- state store -----------------------------------------------------------


@pytest.fixture
def store_config() -> Iterator[tuple[str, pb.DynamicValue]]:
    root = tempfile.mkdtemp()
    yield root, marshal({"path": root}, schema=PyviderFileSystemStateStore.get_schema().block)


@pytest.mark.asyncio
async def test_state_store_validate_requires_a_path() -> None:
    blank = marshal({"path": ""}, schema=PyviderFileSystemStateStore.get_schema().block)
    request = pb.ValidateStateStore.Request(type_name=STORE, config=blank)

    response = await ProviderHandler().ValidateStateStoreConfig(request, context=None)

    assert errors(response.diagnostics) == ["path is required"]


@pytest.mark.asyncio
async def test_state_store_validate_accepts_a_usable_path(
    store_config: tuple[str, pb.DynamicValue],
) -> None:
    _, config = store_config
    request = pb.ValidateStateStore.Request(type_name=STORE, config=config)

    response = await ProviderHandler().ValidateStateStoreConfig(request, context=None)

    assert list(response.diagnostics) == []


@pytest.mark.asyncio
async def test_state_store_validate_hook_requires_a_config_at_all() -> None:
    assert await PyviderFileSystemStateStore().validate(None) == ["path is required"]


@pytest.mark.asyncio
async def test_state_store_round_trips_state_through_the_negotiated_chunk_size(
    store_config: tuple[str, pb.DynamicValue],
) -> None:
    root, config = store_config
    handler = ProviderHandler()
    payload = b'{"version":4,"resources":[]}'

    configure = pb.ConfigureStateStore.Request(type_name=STORE, config=config)
    configure.capabilities.chunk_size = 8
    configured = await handler.ConfigureStateStore(configure, context=None)

    async def chunks() -> AsyncIterator[pb.WriteStateBytes.RequestChunk]:
        yield pb.WriteStateBytes.RequestChunk(
            meta=pb.RequestChunkMeta(type_name=STORE, state_id="prod"),
            bytes=payload,
            total_length=len(payload),
        )

    await handler.WriteStateBytes(chunks(), context=None)
    read = [
        response
        async for response in handler.ReadStateBytes(
            pb.ReadStateBytes.Request(type_name=STORE, state_id="prod"), context=None
        )
    ]

    assert configured.capabilities.chunk_size == 8
    assert b"".join(r.bytes for r in read) == payload
    assert all(len(r.bytes) <= 8 for r in read)
    assert (Path(root) / STORE / "prod.tfstate").is_file()


@pytest.mark.asyncio
async def test_state_store_refuses_a_contended_lock(
    store_config: tuple[str, pb.DynamicValue],
) -> None:
    _, config = store_config
    handler = ProviderHandler()
    await handler.ConfigureStateStore(
        pb.ConfigureStateStore.Request(type_name=STORE, config=config), context=None
    )
    request = pb.LockState.Request(type_name=STORE, state_id="prod", operation="apply")

    first = await handler.LockState(request, context=None)
    second = await handler.LockState(request, context=None)
    released = await handler.UnlockState(
        pb.UnlockState.Request(type_name=STORE, state_id="prod", lock_id=first.lock_id),
        context=None,
    )
    third = await handler.LockState(request, context=None)

    assert first.lock_id
    assert second.lock_id == ""
    assert errors(second.diagnostics) == ["State is already locked"]
    assert list(released.diagnostics) == []
    assert third.lock_id


# --- the resource the fixtures anchor on -----------------------------------


@pytest.mark.asyncio
async def test_generate_config_drops_computed_and_write_only_values() -> None:
    resource = SecretNoteResource()
    from pyvider.components.resources.secret_note import SecretNoteState

    generated = await resource.generate_config(
        SecretNoteState(name="alpha", secret_value=None, digest=digest_of("s"))
    )

    assert generated.name == "alpha"
    # digest is computed and secret_value is write-only; neither belongs in a
    # configuration a practitioner could write.
    assert generated.secret_value is None
    assert not hasattr(generated, "digest")


def test_secret_value_is_marked_write_only() -> None:
    attributes = SecretNoteResource.get_schema().block.attributes

    assert attributes["secret_value"].write_only is True
    assert attributes["digest"].computed is True


# 🧩🔧🔚
