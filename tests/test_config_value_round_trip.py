#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Every configurable attribute must survive the round trip back to Terraform.

Terraform compares what a provider returns against what the configuration set,
attribute by attribute, and rejects the whole object on any difference:

    Provider produced invalid ephemeral resource instance
    .ttl_seconds: planned value cty.NullVal(cty.Number)
    does not match config value cty.NumberIntVal(300)

A result class that simply has no field for a settable attribute returns null for
it, which reads as exactly that. The RPC still succeeds, so a test that drives
open/renew/close over the protocol sees nothing wrong -- the contract being broken
is Terraform's, not the plugin protocol's, and only Terraform enforces it.

`pyvider_lease` shipped without `ttl_seconds` for this reason, after `path` had
already been fixed for the same reason. This is the structural check that catches
the next one without needing a Terraform binary in the loop.
"""

from __future__ import annotations

import attrs
import pytest
from pyvider.ephemerals import EphemeralResourceContext

from pyvider.components.ephemerals.lease import LeaseConfig, LeaseEphemeralResource


def _settable_attributes(component: type) -> set[str]:
    """Schema attributes a practitioner can set: required, or optional and not computed."""
    block = component.get_schema().block
    return {
        name
        for name, attr in block.attributes.items()
        if attr.required or (getattr(attr, "optional", False) and not attr.computed)
    }


def _result_fields(result_class: type) -> set[str]:
    return {f.name for f in attrs.fields(result_class)}


EPHEMERAL_COMPONENTS = [
    pytest.param(LeaseEphemeralResource, id="pyvider_lease"),
]


@pytest.mark.parametrize("component", EPHEMERAL_COMPONENTS)
def test_result_class_carries_every_settable_attribute(component: type) -> None:
    settable = _settable_attributes(component)
    missing = settable - _result_fields(component.result_class)

    assert not missing, (
        f"{component.__name__}.result_class has no field for {sorted(missing)}, so the "
        f"provider returns null for {'them' if len(missing) > 1 else 'it'} while the "
        f"configuration may have set a value. Terraform rejects the whole object with "
        f"'planned value does not match config value'."
    )


@pytest.mark.parametrize("component", EPHEMERAL_COMPONENTS)
def test_result_class_declares_nothing_the_schema_does_not(component: type) -> None:
    """A field with no schema attribute behind it cannot reach Terraform at all."""
    block = component.get_schema().block
    unknown = _result_fields(component.result_class) - set(block.attributes)

    assert not unknown, (
        f"{component.__name__}.result_class declares {sorted(unknown)}, which the schema "
        f"does not expose. Either add the attribute to the schema or drop the field."
    )


async def test_lease_echoes_a_configured_ttl_back_verbatim(tmp_path) -> None:
    """The specific regression: a set ttl_seconds comes back as itself, not as null."""
    resource = LeaseEphemeralResource()
    config = LeaseConfig(name="deploy-lock", path=str(tmp_path / "held.lease"), ttl_seconds=300)
    result, _private, _expires = await resource.open(
        EphemeralResourceContext(config=config, private_state=None)
    )

    assert result.ttl_seconds == 300


async def test_lease_leaves_an_unset_ttl_null(tmp_path) -> None:
    """And an omitted one stays null -- returning the default fails the same check."""
    resource = LeaseEphemeralResource()
    config = LeaseConfig(name="deploy-lock", path=str(tmp_path / "held.lease"))
    result, private, _expires = await resource.open(
        EphemeralResourceContext(config=config, private_state=None)
    )

    assert result.ttl_seconds is None, "an unset attribute must come back unset"
    assert private.ttl_seconds > 0, "the default still governs the lease itself"
