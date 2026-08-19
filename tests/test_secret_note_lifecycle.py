#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The full CRUD lifecycle of pyvider_secret_note, through the real handlers.

This is the resource the v6.11 fixtures anchor on, so its behaviour under a
genuine plan/apply/read/destroy is what those fixtures are actually asserting.
The write-only guarantee is the point: the secret must reach the provider
during apply and must be absent from state afterwards.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.conversion import marshal, unmarshal
from pyvider.protocols.tfprotov6.handlers import (
    ApplyResourceChangeHandler,
    PlanResourceChangeHandler,
    ReadResourceHandler,
)

from pyvider.components.resources.secret_note import (
    _NOTES,
    SecretNoteConfig,
    SecretNoteResource,
    digest_of,
)

RESOURCE = "pyvider_secret_note"

pytestmark = pytest.mark.usefixtures(
    "discovered_components_session", "provider_in_hub", "provider_with_test_mode"
)


@pytest.fixture(autouse=True)
def _clean() -> Iterator[None]:
    _NOTES.clear()
    yield
    _NOTES.clear()


def config_value(name: str, secret: str) -> pb.DynamicValue:
    return marshal(
        {"name": name, "secret_value": secret, "digest": None},
        schema=SecretNoteResource.get_schema().block,
    )


def decode(value: pb.DynamicValue) -> dict[str, object]:
    cty = unmarshal(value, schema=SecretNoteResource.get_schema().block)
    return {key: cty[key] for key in ("name", "secret_value", "digest")}


async def create(name: str, secret: str) -> pb.ApplyResourceChange.Response:
    config = config_value(name, secret)
    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )
    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"

    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=RESOURCE,
            config=config,
            planned_state=plan.planned_state,
            planned_private=plan.planned_private,
        ),
        context=None,
    )
    assert not applied.diagnostics, f"apply failed: {applied.diagnostics}"
    return applied


@pytest.mark.asyncio
async def test_apply_computes_the_digest_from_the_secret() -> None:
    applied = await create("alpha", "correct horse")

    state = decode(applied.new_state)
    assert state["digest"].value == digest_of("correct horse")


@pytest.mark.asyncio
async def test_the_secret_is_absent_from_the_state_that_terraform_stores() -> None:
    applied = await create("alpha", "correct horse")

    state = decode(applied.new_state)
    # The whole point of write_only: usable during apply, never persisted.
    assert state["secret_value"].is_null
    assert state["name"].value == "alpha"


@pytest.mark.asyncio
async def test_the_secret_did_reach_the_provider_during_apply() -> None:
    await create("alpha", "correct horse")

    # The digest alone could be faked; the recorded note proves the plaintext
    # arrived, which is what distinguishes "write-only" from "dropped".
    assert _NOTES["alpha"] == "correct horse"


@pytest.mark.asyncio
async def test_read_keeps_the_secret_null_and_the_digest_intact() -> None:
    applied = await create("alpha", "correct horse")

    read = await ReadResourceHandler(
        pb.ReadResource.Request(type_name=RESOURCE, current_state=applied.new_state, private=applied.private),
        context=None,
    )

    assert not read.diagnostics
    state = decode(read.new_state)
    assert state["secret_value"].is_null
    assert state["digest"].value == digest_of("correct horse")


@pytest.mark.asyncio
async def test_updating_the_secret_changes_the_digest() -> None:
    first = await create("alpha", "first secret")
    second = await create("alpha", "second secret")

    assert decode(first.new_state)["digest"].value == digest_of("first secret")
    assert decode(second.new_state)["digest"].value == digest_of("second secret")
    assert _NOTES["alpha"] == "second secret"


@pytest.mark.asyncio
async def test_destroy_removes_the_note() -> None:
    applied = await create("alpha", "correct horse")
    null_config = marshal(None, schema=SecretNoteResource.get_schema().block)

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(
            type_name=RESOURCE,
            prior_state=applied.new_state,
            config=null_config,
            proposed_new_state=null_config,
        ),
        context=None,
    )
    destroyed = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=RESOURCE,
            prior_state=applied.new_state,
            config=null_config,
            planned_state=plan.planned_state,
        ),
        context=None,
    )

    assert not destroyed.diagnostics, f"destroy failed: {destroyed.diagnostics}"
    assert "alpha" not in _NOTES


# --- validation ------------------------------------------------------------


@pytest.mark.asyncio
async def test_validate_rejects_a_blank_name() -> None:
    errors = await SecretNoteResource()._validate_config(SecretNoteConfig(name="   ", secret_value="s"))

    assert errors == ["name must not be empty"]


@pytest.mark.asyncio
async def test_validate_rejects_an_empty_secret() -> None:
    errors = await SecretNoteResource()._validate_config(SecretNoteConfig(name="alpha", secret_value=""))

    assert errors == ["secret_value must not be empty"]


@pytest.mark.asyncio
async def test_validate_accepts_a_complete_config() -> None:
    errors = await SecretNoteResource()._validate_config(SecretNoteConfig(name="alpha", secret_value="s"))

    assert errors == []


@pytest.mark.asyncio
async def test_validate_ignores_attributes_that_are_absent() -> None:
    assert await SecretNoteResource()._validate_config(SecretNoteConfig()) == []


# --- the guard that catches a stripped write-only value --------------------


@pytest.mark.asyncio
async def test_apply_without_the_secret_fails_loudly() -> None:
    """If write-only values stop arriving, this must not silently succeed.

    Storing an empty secret and a digest of "" would look like a working
    resource while quietly discarding the practitioner's input.
    """
    from pyvider.resources.context import ResourceContext

    resource = SecretNoteResource()
    ctx = ResourceContext(config=SecretNoteConfig(name="alpha", secret_value=None))

    with pytest.raises(ValueError, match="write-only attributes must survive"):
        await resource._create_apply(ctx)


@pytest.mark.asyncio
async def test_read_of_absent_state_returns_nothing() -> None:
    from pyvider.resources.context import ResourceContext

    assert await SecretNoteResource().read(ResourceContext(state=None)) is None


@pytest.mark.asyncio
async def test_deleting_a_note_that_was_never_created_is_harmless() -> None:
    from pyvider.resources.context import ResourceContext

    from pyvider.components.resources.secret_note import SecretNoteState

    await SecretNoteResource()._delete_apply(ResourceContext(state=SecretNoteState(name=None)))
    await SecretNoteResource()._delete_apply(ResourceContext(state=SecretNoteState(name="ghost")))


# --- the create/update bodies, driven directly ----------------------------
#
# The handler-driven tests above cover these end to end. These pin the bodies
# down directly, so a failure says which method broke rather than only that
# the lifecycle did.


@pytest.mark.asyncio
async def test_create_apply_records_the_note_and_computes_the_digest() -> None:
    from pyvider.resources.context import ResourceContext

    from pyvider.components.resources.secret_note import SecretNoteState

    state, private = await SecretNoteResource()._create_apply(
        ResourceContext(
            config=SecretNoteConfig(name="alpha", secret_value="s3cret"),
            planned_state=SecretNoteState(name="alpha", secret_value=None, digest=None),
        )
    )

    assert state is not None
    assert state.digest == digest_of("s3cret")
    assert private is None
    assert _NOTES["alpha"] == "s3cret"


@pytest.mark.asyncio
async def test_create_marks_the_digest_unknown_at_plan_time() -> None:
    from pyvider.resources.context import ResourceContext

    plan, private = await SecretNoteResource()._create(
        ResourceContext(config=SecretNoteConfig(name="alpha", secret_value="s")), {"name": "alpha"}
    )

    assert plan is not None
    # Unknown until apply: the digest cannot be known before the secret is.
    assert plan["digest"].is_unknown
    assert private is None


@pytest.mark.asyncio
async def test_update_marks_the_digest_unknown_too() -> None:
    from pyvider.resources.context import ResourceContext

    plan, private = await SecretNoteResource()._update(
        ResourceContext(config=SecretNoteConfig(name="alpha", secret_value="s")), {"name": "alpha"}
    )

    assert plan is not None
    assert plan["digest"].is_unknown
    assert private is None


@pytest.mark.asyncio
async def test_update_apply_recomputes_the_digest() -> None:
    from pyvider.resources.context import ResourceContext

    from pyvider.components.resources.secret_note import SecretNoteState

    _NOTES["alpha"] = "old"
    state, _ = await SecretNoteResource()._update_apply(
        ResourceContext(
            config=SecretNoteConfig(name="alpha", secret_value="new secret"),
            planned_state=SecretNoteState(name="alpha", secret_value=None, digest=None),
        )
    )

    assert state is not None
    assert state.digest == digest_of("new secret")
    assert _NOTES["alpha"] == "new secret"


@pytest.mark.asyncio
async def test_read_returns_the_state_it_was_given() -> None:
    from pyvider.resources.context import ResourceContext

    from pyvider.components.resources.secret_note import SecretNoteState

    existing = SecretNoteState(name="alpha", secret_value=None, digest="abc")

    assert await SecretNoteResource().read(ResourceContext(state=existing)) is existing


# --- generate_config -------------------------------------------------------


@pytest.mark.asyncio
async def test_generate_config_of_absent_state_defers_to_the_framework_default() -> None:
    assert await SecretNoteResource().generate_config(None) is None


# 🧩🔧🔚
