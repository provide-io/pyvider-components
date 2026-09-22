"""Security lint rules supplied by the first-party components."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

import pytest
from pyvider.lint import LintContext, LintFinding, LintSelector

from pyvider.components.data_sources.http_api import HTTPAPIConfig, HTTPAPIDataSource
from pyvider.components.lint_rules import (
    ALL,
    INCLUDE_HIDDEN_FILES,
    INSECURE_HTTP,
    INSECURE_TLS,
    SECURITY,
    WORLD_WRITABLE_DIRECTORY,
)
from pyvider.components.list_resources.file_contents import DirectoryEntriesConfig, FileContentList
from pyvider.components.provider import PyviderProvider
from pyvider.components.resources.local_directory import LocalDirectoryConfig, LocalDirectoryResource


class _Unknown:
    """A framework-style unknown that must never be inspected."""

    def __bool__(self) -> bool:
        raise RuntimeError("unknown value was inspected")

    def __eq__(self, other: object) -> bool:
        raise RuntimeError("unknown value was compared")

    def __str__(self) -> str:
        raise RuntimeError("unknown value was rendered")


UNKNOWN = _Unknown()


@dataclass(frozen=True)
class SecurityRuleCase:
    component: Callable[[], Any]
    trigger: object
    safe: object
    omitted: object
    null: object
    unknown: object
    rule: str
    summary: str
    detail: str
    attribute_path: str
    extra_safe: tuple[object, ...] = ()


CASES = [
    pytest.param(
        SecurityRuleCase(
            component=PyviderProvider,
            trigger=SimpleNamespace(api_insecure_skip_verify=True),
            safe=SimpleNamespace(api_insecure_skip_verify=False),
            omitted=SimpleNamespace(),
            null=SimpleNamespace(api_insecure_skip_verify=None),
            unknown=SimpleNamespace(api_insecure_skip_verify=UNKNOWN),
            rule=INSECURE_TLS,
            summary="TLS certificate verification is disabled",
            detail=(
                "Skipping TLS certificate verification may be intentional for local development, "
                "but it permits man-in-the-middle attacks. Set api_insecure_skip_verify to false "
                "for safer connections. Suppress with !provide-io/pyvider:insecure-tls."
            ),
            attribute_path="api_insecure_skip_verify",
        ),
        id="insecure_tls",
    ),
    pytest.param(
        SecurityRuleCase(
            component=LocalDirectoryResource,
            trigger=LocalDirectoryConfig(path="/tmp/example", permissions="0o757"),
            safe=LocalDirectoryConfig(path="/tmp/example", permissions="0o755"),
            omitted=LocalDirectoryConfig(path="/tmp/example"),
            null=LocalDirectoryConfig(path="/tmp/example", permissions=None),
            unknown=SimpleNamespace(path="/tmp/example", permissions=UNKNOWN),
            rule=WORLD_WRITABLE_DIRECTORY,
            summary="Directory permissions are world-writable",
            detail=(
                "World-writable permissions may be intentional for a shared scratch directory, "
                "but any local user can modify its contents. Remove the POSIX other-write bit "
                "(for example, set permissions to 0o755) for a safer directory. Suppress with "
                "!provide-io/pyvider:world-writable-directory."
            ),
            attribute_path="permissions",
            extra_safe=(SimpleNamespace(path="/tmp/example", permissions="not-octal"),),
        ),
        id="world_writable_directory",
    ),
    pytest.param(
        SecurityRuleCase(
            component=HTTPAPIDataSource,
            trigger=HTTPAPIConfig(url="HTTP://api.example.test"),
            safe=HTTPAPIConfig(url="https://api.example.test"),
            omitted=SimpleNamespace(),
            null=SimpleNamespace(url=None),
            unknown=SimpleNamespace(url=UNKNOWN),
            rule=INSECURE_HTTP,
            summary="HTTP API uses an unencrypted connection",
            detail=(
                "Plain HTTP may be intentional for a local endpoint, but request data can be "
                "intercepted or changed. Set url to an https:// address for a safer connection. "
                "Suppress with !provide-io/pyvider:insecure-http."
            ),
            attribute_path="url",
        ),
        id="insecure_http",
    ),
    pytest.param(
        SecurityRuleCase(
            component=FileContentList,
            trigger=DirectoryEntriesConfig(path="/tmp/example", include_hidden=True),
            safe=DirectoryEntriesConfig(path="/tmp/example", include_hidden=False),
            omitted=DirectoryEntriesConfig(path="/tmp/example"),
            null=DirectoryEntriesConfig(path="/tmp/example", include_hidden=None),
            unknown=SimpleNamespace(path="/tmp/example", include_hidden=UNKNOWN),
            rule=INCLUDE_HIDDEN_FILES,
            summary="File listing includes hidden files",
            detail=(
                "Including hidden files may be intentional for configuration discovery, but it "
                "can expose secrets or metadata. Set include_hidden to false for safer listings. "
                "Suppress with !provide-io/pyvider:include-hidden-files."
            ),
            attribute_path="include_hidden",
        ),
        id="include_hidden_files",
    ),
]


async def _lint(case: SecurityRuleCase, config: object, *tokens: str) -> tuple[LintFinding, ...]:
    ctx = LintContext(config=config, selector=LintSelector.parse(tokens))
    return tuple(await case.component().lint(ctx))


@pytest.mark.asyncio
@pytest.mark.parametrize("case", CASES)
async def test_security_lint_rule(case: SecurityRuleCase) -> None:
    exact = await _lint(case, case.trigger, case.rule)
    assert exact == (
        LintFinding(
            rule=case.rule,
            groups=(ALL, SECURITY),
            summary=case.summary,
            detail=case.detail,
            attribute_path=case.attribute_path,
        ),
    )

    assert await _lint(case, case.trigger, SECURITY) == exact
    assert await _lint(case, case.trigger, ALL) == exact
    assert await _lint(case, case.trigger, ALL, f"!{case.rule}") == ()
    assert await _lint(case, case.trigger) == ()

    assert await _lint(case, case.safe, case.rule) == ()
    assert await _lint(case, case.omitted, case.rule) == ()
    assert await _lint(case, case.null, case.rule) == ()
    assert await _lint(case, case.unknown, case.rule) == ()
    for config in case.extra_safe:
        assert await _lint(case, config, case.rule) == ()
    assert f"!{case.rule}" in exact[0].detail
