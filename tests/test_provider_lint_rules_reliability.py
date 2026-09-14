"""Reliability lint rules supplied by the first-party components."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from pyvider.cty import CtyNumber, CtyString, CtyValue
from pyvider.lint import LintContext, LintFinding, LintSelector

from pyvider.components.actions.wait_for_file import WaitForFileAction, WaitForFileConfig
from pyvider.components.ephemerals.lease import LeaseConfig, LeaseEphemeralResource
from pyvider.components.lint_rules import (
    ALL,
    LONG_ACTION_TIMEOUT,
    LONG_LIVED_LEASE,
    RELATIVE_STATE_STORE_PATH,
    RELIABILITY,
)
from pyvider.components.state_stores.filesystem_store import (
    FileSystemStoreConfig,
    PyviderFileSystemStateStore,
)


@dataclass(frozen=True)
class ReliabilityRuleCase:
    component: Callable[[], Any]
    trigger: object
    rule: str
    summary: str
    detail: str
    attribute_path: str


LEASE_CASE = ReliabilityRuleCase(
    component=LeaseEphemeralResource,
    trigger=LeaseConfig(name="example", path="/tmp/example", ttl_seconds=3601),
    rule=LONG_LIVED_LEASE,
    summary="Lease lifetime exceeds one hour",
    detail=(
        "A lease longer than one hour may be intentional for lengthy operations, but "
        "long-lived ephemeral values remain usable for longer if exposed. Set "
        "ttl_seconds to 3600 or less for a safer lease. Suppress with "
        "!provide-io/pyvider:long-lived-lease."
    ),
    attribute_path="ttl_seconds",
)

ACTION_CASE = ReliabilityRuleCase(
    component=WaitForFileAction,
    trigger=WaitForFileConfig(path="/tmp/example", timeout_seconds=301),
    rule=LONG_ACTION_TIMEOUT,
    summary="Action timeout exceeds five minutes",
    detail=(
        "A timeout longer than five minutes may be intentional for slow prerequisites, but it "
        "can leave Terraform waiting for an unresponsive action. Set timeout_seconds to 300 or "
        "less for a safer timeout. Suppress with !provide-io/pyvider:long-action-timeout."
    ),
    attribute_path="timeout_seconds",
)

STATE_STORE_CASE = ReliabilityRuleCase(
    component=PyviderFileSystemStateStore,
    trigger=FileSystemStoreConfig(path="state"),
    rule=RELATIVE_STATE_STORE_PATH,
    summary="State store path is relative",
    detail=(
        "A relative state store path may be intentional for a self-contained workspace, but it "
        "depends on the provider process's working directory. Set path to an absolute path for "
        "safer, predictable state storage. Suppress with "
        "!provide-io/pyvider:relative-state-store-path."
    ),
    attribute_path="path",
)


CASES = [
    pytest.param(LEASE_CASE, id="long_lived_lease"),
    pytest.param(ACTION_CASE, id="long_action_timeout"),
    pytest.param(STATE_STORE_CASE, id="relative_state_store_path"),
]


class _ComparisonFailure:
    def __gt__(self, other: object) -> bool:
        raise RuntimeError("comparison failed")


class _RenderFailure:
    def __str__(self) -> str:
        raise RuntimeError("render failed")


LEASE_SAFE_CONFIGS = [
    pytest.param(LeaseConfig(name="example", path="/tmp/example", ttl_seconds=3600), id="threshold"),
    pytest.param(SimpleNamespace(), id="omitted"),
    pytest.param(LeaseConfig(name="example", path="/tmp/example", ttl_seconds=None), id="null"),
    pytest.param(None, id="config_none"),
    pytest.param(
        SimpleNamespace(ttl_seconds=CtyValue.unknown(CtyNumber())),
        id="framework_unknown",
    ),
    pytest.param(SimpleNamespace(ttl_seconds=_ComparisonFailure()), id="comparison_failure"),
]

ACTION_SAFE_CONFIGS = [
    pytest.param(WaitForFileConfig(path="/tmp/example", timeout_seconds=300), id="threshold"),
    pytest.param(SimpleNamespace(), id="omitted"),
    pytest.param(WaitForFileConfig(path="/tmp/example", timeout_seconds=None), id="null"),
    pytest.param(None, id="config_none"),
    pytest.param(
        SimpleNamespace(timeout_seconds=CtyValue.unknown(CtyNumber())),
        id="framework_unknown",
    ),
    pytest.param(SimpleNamespace(timeout_seconds=_ComparisonFailure()), id="comparison_failure"),
]

STATE_STORE_SAFE_CONFIGS = [
    pytest.param(FileSystemStoreConfig(path=str(Path.cwd() / "pyvider-state")), id="absolute"),
    pytest.param(FileSystemStoreConfig(path="~/pyvider-state"), id="expanded_absolute"),
    pytest.param(SimpleNamespace(), id="omitted"),
    pytest.param(FileSystemStoreConfig(path=None), id="null"),
    pytest.param(None, id="config_none"),
    pytest.param(
        SimpleNamespace(path=CtyValue.unknown(CtyString())),
        id="framework_unknown",
    ),
    pytest.param(SimpleNamespace(path=_RenderFailure()), id="render_failure"),
]


async def _lint(case: ReliabilityRuleCase, config: object | None, *tokens: str) -> tuple[LintFinding, ...]:
    ctx = LintContext(config=config, selector=LintSelector.parse(tokens))
    return tuple(await case.component().lint(ctx))


@pytest.mark.asyncio
@pytest.mark.parametrize("case", CASES)
async def test_reliability_lint_rule(case: ReliabilityRuleCase) -> None:
    assert await _lint(case, case.trigger, case.rule) == (
        LintFinding(
            rule=case.rule,
            groups=(ALL, RELIABILITY),
            summary=case.summary,
            detail=case.detail,
            attribute_path=case.attribute_path,
        ),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize(
    ("selection", "expected"),
    [
        pytest.param("reliability_group", True, id="reliability_group"),
        pytest.param("all_group", True, id="all_group"),
        pytest.param("exact_exclusion", False, id="exact_exclusion"),
        pytest.param("default_disabled", False, id="default_disabled"),
    ],
)
async def test_reliability_lint_rule_selection(
    case: ReliabilityRuleCase, selection: str, expected: bool
) -> None:
    tokens = {
        "reliability_group": (RELIABILITY,),
        "all_group": (ALL,),
        "exact_exclusion": (ALL, f"!{case.rule}"),
        "default_disabled": (),
    }[selection]
    findings = await _lint(case, case.trigger, *tokens)
    assert bool(findings) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize("config", LEASE_SAFE_CONFIGS)
async def test_reliability_lint_rule_lease_safe(config: object | None) -> None:
    assert await _lint(LEASE_CASE, config, LONG_LIVED_LEASE) == ()


@pytest.mark.asyncio
@pytest.mark.parametrize("config", ACTION_SAFE_CONFIGS)
async def test_reliability_lint_rule_action_safe(config: object | None) -> None:
    assert await _lint(ACTION_CASE, config, LONG_ACTION_TIMEOUT) == ()


@pytest.mark.asyncio
@pytest.mark.parametrize("config", STATE_STORE_SAFE_CONFIGS)
async def test_reliability_lint_rule_state_store_safe(config: object | None) -> None:
    assert await _lint(STATE_STORE_CASE, config, RELATIVE_STATE_STORE_PATH) == ()


@pytest.mark.asyncio
async def test_relative_state_store_path_lint_performs_no_filesystem_io(monkeypatch) -> None:
    def fail(*args: object, **kwargs: object) -> None:
        raise AssertionError("lint accessed the filesystem")

    for operation in (
        "exists",
        "iterdir",
        "mkdir",
        "open",
        "read_text",
        "resolve",
        "stat",
        "unlink",
        "write_text",
    ):
        monkeypatch.setattr(Path, operation, fail)

    assert await _lint(STATE_STORE_CASE, STATE_STORE_CASE.trigger, RELATIVE_STATE_STORE_PATH)
