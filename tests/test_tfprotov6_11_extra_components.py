#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The second pair of v6.11 demo components.

``pyvider_wait_for_file`` covers deferral driven by a real prerequisite and
work that genuinely takes time. ``pyvider_file_content`` covers a list
resource that declares its own identity schema and attaches per-result
warnings — neither of which the in-memory note components exercise.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.conversion import marshal, unmarshal_identity
from pyvider.handler import ProviderHandler
from pyvider.list_resources import ListResourceContext
from pyvider.protocols.tfprotov6.handlers.action_handlers import (
    PlanActionHandler,
    ValidateActionConfigHandler,
)
from pyvider.protocols.tfprotov6.handlers.config_handlers import (
    ValidateListResourceConfigHandler,
)

from pyvider.components.actions.wait_for_file import (
    DEFAULT_TIMEOUT_SECONDS,
    WaitForFileAction,
    WaitForFileConfig,
)
from pyvider.components.list_resources.file_contents import (
    DirectoryEntriesConfig,
    FileContentList,
)

WAIT_ACTION = "pyvider_wait_for_file"
DIR_LIST = "pyvider_file_content"

pytestmark = pytest.mark.usefixtures(
    "discovered_components_session", "provider_in_hub", "provider_with_test_mode"
)


def errors(diagnostics: object) -> list[str]:
    return [d.summary for d in diagnostics if d.severity == pb.Diagnostic.ERROR]  # type: ignore[attr-defined]


def wait_config(**overrides: object) -> pb.DynamicValue:
    values: dict[str, object] = {"path": "/tmp/x", "timeout_seconds": None}
    values.update(overrides)
    return marshal(values, schema=WaitForFileAction.get_schema().block)


def dir_config(**overrides: object) -> pb.DynamicValue:
    values: dict[str, object] = {"path": ".", "suffix": None, "include_hidden": None}
    values.update(overrides)
    return marshal(values, schema=FileContentList.get_schema().block)


@pytest.fixture
def populated(tmp_path: Path) -> Iterator[Path]:
    (tmp_path / "alpha.tf").write_text("a", encoding="utf-8")
    (tmp_path / "beta.tf").write_text("bb", encoding="utf-8")
    (tmp_path / "gamma.txt").write_text("ccc", encoding="utf-8")
    (tmp_path / ".hidden.tf").write_text("d", encoding="utf-8")
    (tmp_path / "subdir").mkdir()
    yield tmp_path


# --- wait_for_file: validation ---------------------------------------------


@pytest.mark.asyncio
async def test_wait_validate_accepts_a_path() -> None:
    request = pb.ValidateActionConfig.Request(type_name=WAIT_ACTION, config=wait_config())

    response = await ValidateActionConfigHandler(request, context=None)

    assert list(response.diagnostics) == []


@pytest.mark.asyncio
async def test_wait_validate_requires_a_path() -> None:
    request = pb.ValidateActionConfig.Request(type_name=WAIT_ACTION, config=wait_config(path=""))

    response = await ValidateActionConfigHandler(request, context=None)

    assert errors(response.diagnostics) == ["path is required"]


@pytest.mark.asyncio
async def test_wait_validate_rejects_a_non_positive_timeout() -> None:
    request = pb.ValidateActionConfig.Request(type_name=WAIT_ACTION, config=wait_config(timeout_seconds=0))

    response = await ValidateActionConfigHandler(request, context=None)

    assert errors(response.diagnostics) == ["timeout_seconds must be greater than zero"]


@pytest.mark.asyncio
async def test_wait_validate_reports_every_problem_at_once() -> None:
    request = pb.ValidateActionConfig.Request(
        type_name=WAIT_ACTION, config=wait_config(path="", timeout_seconds=-1)
    )

    response = await ValidateActionConfigHandler(request, context=None)

    assert errors(response.diagnostics) == [
        "path is required",
        "timeout_seconds must be greater than zero",
    ]


@pytest.mark.asyncio
async def test_wait_validate_hook_handles_a_missing_config() -> None:
    assert await WaitForFileAction().validate(None) == ["path is required"]


# --- wait_for_file: planning warns about an absent prerequisite -------------


@pytest.mark.asyncio
async def test_wait_plan_warns_but_does_not_defer_when_the_file_is_absent(tmp_path: Path) -> None:
    """Waiting is the action's job, so an absent file is not planned around.

    Terraform accepts an action deferral only for an unknown provider
    configuration (internal/plugin6/grpc_provider.go:1940-1957), so deferring
    here would be refused -- and untrue. `invoke` polls for the file instead.
    """
    request = pb.PlanAction.Request(
        action_type=WAIT_ACTION, config=wait_config(path=str(tmp_path / "not-there.txt"))
    )
    request.client_capabilities.deferral_allowed = True

    response = await PlanActionHandler(request, context=None)

    assert not response.HasField("deferred")
    assert not errors(response.diagnostics), errors(response.diagnostics)
    assert [d.severity for d in response.diagnostics] == [pb.Diagnostic.WARNING]
    assert "not-there.txt" in response.diagnostics[0].summary


@pytest.mark.asyncio
async def test_wait_plan_proceeds_when_the_file_exists(tmp_path: Path) -> None:
    target = tmp_path / "here.txt"
    target.write_text("x", encoding="utf-8")
    request = pb.PlanAction.Request(action_type=WAIT_ACTION, config=wait_config(path=str(target)))

    response = await PlanActionHandler(request, context=None)

    assert not response.HasField("deferred")
    assert list(response.diagnostics) == []


# --- wait_for_file: invocation ---------------------------------------------


@pytest.mark.asyncio
async def test_wait_invoke_returns_immediately_when_the_file_exists(tmp_path: Path) -> None:
    target = tmp_path / "here.txt"
    target.write_text("x", encoding="utf-8")
    request = pb.InvokeAction.Request(action_type=WAIT_ACTION, config=wait_config(path=str(target)))

    events = [event async for event in ProviderHandler().InvokeAction(request, context=None)]

    assert [event.WhichOneof("type") for event in events] == ["progress", "completed"]
    assert str(target) in events[0].progress.message
    assert list(events[-1].completed.diagnostics) == []


@pytest.mark.asyncio
async def test_wait_invoke_reports_a_timeout_as_a_completed_error(tmp_path: Path) -> None:
    request = pb.InvokeAction.Request(
        action_type=WAIT_ACTION,
        config=wait_config(path=str(tmp_path / "never.txt"), timeout_seconds=0.05),
    )

    events = [event async for event in ProviderHandler().InvokeAction(request, context=None)]

    assert events[-1].WhichOneof("type") == "completed"
    detail = events[-1].completed.diagnostics[0].detail
    assert "never.txt" in detail
    assert "0.05" in detail
    # Waiting emits progress before giving up, so the stall is visible.
    assert any(event.WhichOneof("type") == "progress" for event in events)


def test_the_default_timeout_is_a_sane_positive_value() -> None:
    assert DEFAULT_TIMEOUT_SECONDS > 0


@pytest.mark.asyncio
async def test_wait_invoke_uses_the_default_timeout_when_none_is_given(tmp_path: Path) -> None:
    target = tmp_path / "here.txt"
    target.write_text("x", encoding="utf-8")
    action = WaitForFileAction()
    ctx: ListResourceContext = None  # type: ignore[assignment]
    del ctx

    from pyvider.actions import ActionContext

    events = [
        event
        async for event in action.invoke(
            ActionContext(
                action_type=WAIT_ACTION,
                config=WaitForFileConfig(path=str(target), timeout_seconds=None),
            )
        )
    ]

    assert [event.message for event in events] == [f"{target} exists"]


@pytest.mark.asyncio
async def test_wait_invoke_polls_quietly_between_progress_reports(tmp_path: Path) -> None:
    """Progress is reported every fifth poll, not on every one.

    A message per 100ms poll would drown the console; the quiet polls are the
    branch this pins down.
    """
    from pyvider.actions import ActionContext

    from pyvider.components.actions import wait_for_file

    target = tmp_path / "appears.txt"
    polls = 0
    real_exists = Path.exists

    def exists_after_a_few_polls(self: Path) -> bool:
        nonlocal polls
        if self == target:
            polls += 1
            return polls > 3
        return real_exists(self)

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(Path, "exists", exists_after_a_few_polls)
    monkeypatch.setattr(wait_for_file, "POLL_INTERVAL_SECONDS", 0.0)
    try:
        events = [
            event
            async for event in wait_for_file.WaitForFileAction().invoke(
                ActionContext(
                    action_type=WAIT_ACTION,
                    config=wait_for_file.WaitForFileConfig(path=str(target), timeout_seconds=5),
                )
            )
        ]
    finally:
        monkeypatch.undo()

    assert events[-1].message == f"{target} exists"
    # Three quiet polls happened, but only the first produced a message.
    assert sum(1 for e in events if "Waiting" in e.message) == 1


# --- file_content: listing ----------------------------------------------


async def collect(**kwargs: object) -> list[pb.ListResource.Event]:
    request = pb.ListResource.Request(type_name=DIR_LIST, **kwargs)  # type: ignore[arg-type]
    return [event async for event in ProviderHandler().ListResource(request, context=None)]


@pytest.mark.asyncio
async def test_directory_list_returns_visible_files_only(populated: Path) -> None:
    events = await collect(config=dir_config(path=str(populated)))

    # Sorted, dotfiles excluded, subdirectories excluded.
    assert [event.display_name for event in events] == ["alpha.tf", "beta.tf", "gamma.txt"]


@pytest.mark.asyncio
async def test_directory_list_filters_by_suffix(populated: Path) -> None:
    events = await collect(config=dir_config(path=str(populated), suffix=".tf"))

    assert [event.display_name for event in events] == ["alpha.tf", "beta.tf"]


@pytest.mark.asyncio
async def test_directory_list_can_include_hidden_files(populated: Path) -> None:
    events = await collect(config=dir_config(path=str(populated), include_hidden=True))

    assert ".hidden.tf" in [event.display_name for event in events]


@pytest.mark.asyncio
async def test_the_list_borrows_identity_from_the_managed_resource(populated: Path) -> None:
    """Terraform decodes results against the managed resource, not this class.

    It looks the managed type up by the list resource's own name and refuses
    without an identity schema on it, then decodes each result's identity
    against that schema (terraform/internal/plugin6/grpc_provider.go:1341-1345
    and :1420-1426). A list resource that answers with a shape of its own
    produces results Terraform cannot read.
    """
    from pyvider.components.resources.file_content import FileContentResource

    assert FileContentList.get_identity_schema() == FileContentResource.get_identity_schema()

    events = await collect(config=dir_config(path=str(populated), suffix=".tf"))

    decoded = unmarshal_identity(events[0].identity, FileContentList.get_identity_schema())
    assert decoded == {"filename": str(populated / "alpha.tf")}


@pytest.mark.asyncio
async def test_directory_list_includes_sizes_only_when_asked(populated: Path) -> None:
    without = await collect(config=dir_config(path=str(populated), suffix=".tf"))
    with_objects = await collect(
        config=dir_config(path=str(populated), suffix=".tf"), include_resource_object=True
    )

    assert not without[0].HasField("resource_object")
    assert with_objects[0].HasField("resource_object")


@pytest.mark.asyncio
async def test_directory_list_stops_at_the_limit(populated: Path) -> None:
    events = await collect(config=dir_config(path=str(populated)), limit=2)

    assert len(events) == 2


@pytest.mark.asyncio
async def test_directory_list_of_a_missing_directory_is_empty(tmp_path: Path) -> None:
    events = await collect(config=dir_config(path=str(tmp_path / "not-created")))

    assert events == []


@pytest.mark.asyncio
async def test_a_file_that_cannot_be_read_is_returned_with_a_warning(
    populated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_stat = Path.stat

    def selective_stat(self: Path, *args: object, **kwargs: object) -> object:
        # Every stat of this one entry fails, which is what the real race looks
        # like: iterdir() saw it, then it vanished. Failing only the bare call
        # would tie the test to a Python version -- 3.11's is_file() calls stat
        # bare, 3.12+ passes follow_symlinks -- and pass for the wrong reason on
        # whichever half of that the developer happens to run.
        if self.name == "beta.tf":
            raise OSError("permission denied")
        return real_stat(self, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(Path, "stat", selective_stat)

    events = await collect(config=dir_config(path=str(populated), suffix=".tf"), include_resource_object=True)

    # The unreadable entry is still listed -- dropping it would misreport the
    # directory -- but it carries a warning explaining what is missing.
    beta = next(event for event in events if event.display_name == "beta.tf")
    assert [d.severity for d in beta.diagnostic] == [pb.Diagnostic.WARNING]
    assert "could not read beta.tf" in beta.diagnostic[0].summary


# --- file_content: validation -------------------------------------------


@pytest.mark.asyncio
async def test_directory_validate_accepts_an_existing_directory(populated: Path) -> None:
    request = pb.ValidateListResourceConfig.Request(type_name=DIR_LIST, config=dir_config(path=str(populated)))

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert list(response.diagnostics) == []


@pytest.mark.asyncio
async def test_directory_validate_requires_a_path() -> None:
    request = pb.ValidateListResourceConfig.Request(type_name=DIR_LIST, config=dir_config(path=""))

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert errors(response.diagnostics) == ["path is required"]


@pytest.mark.asyncio
async def test_directory_validate_rejects_a_path_that_is_a_file(populated: Path) -> None:
    target = populated / "alpha.tf"
    request = pb.ValidateListResourceConfig.Request(type_name=DIR_LIST, config=dir_config(path=str(target)))

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert errors(response.diagnostics) == [f"path '{target}' is not a directory"]


@pytest.mark.asyncio
async def test_directory_validate_accepts_a_directory_that_does_not_exist_yet(
    tmp_path: Path,
) -> None:
    request = pb.ValidateListResourceConfig.Request(
        type_name=DIR_LIST, config=dir_config(path=str(tmp_path / "later"))
    )

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert list(response.diagnostics) == []


@pytest.mark.asyncio
async def test_directory_validate_hook_handles_a_missing_config() -> None:
    assert await FileContentList().validate(None) == ["path is required"]
    assert await FileContentList().validate(DirectoryEntriesConfig(path=None)) == ["path is required"]


# 🧩🔧🔚


def test_every_list_resource_has_a_managed_resource_that_carries_identity() -> None:
    """The pairing Terraform requires, checked for the whole component set.

    A list resource is reachable only through a managed type of the same name:

        resourceSchema, ok := schema.ResourceTypes[r.TypeName]
        if !ok || resourceSchema.Identity == nil {
            ... "Identity schema not found for resource type %s; this is a bug
            in the provider - please report it there"

    (terraform/internal/plugin6/grpc_provider.go:1341-1345). `pyvider_file_content`
    shipped for a release as `pyvider_directory_entry`, with no managed resource
    of that name and an identity schema of its own, so every attempt to list it
    failed on that line. Nothing in-process noticed, because registration
    succeeds either way and only a real host looks the managed type up.
    """
    from pyvider.protocols.tfprotov6.handlers.utils import get_all_components

    listed = set(get_all_components("list_resource"))
    assert listed, "no list resources were discovered, so this proves nothing"

    for name in listed:
        managed = get_all_components("resource").get(name)
        assert managed is not None, (
            f"list resource {name!r} has no managed resource of that name; Terraform "
            f"fails its ListResource call before the provider is asked for anything"
        )
        assert managed.get_identity_schema() is not None, (
            f"managed resource {name!r} declares no identity schema, which Terraform "
            f"requires before it will list it"
        )
