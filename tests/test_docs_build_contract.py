"""Contracts for building the checked-in MkDocs site from a clean environment."""

from __future__ import annotations

import shlex
import shutil
import subprocess
import tomllib
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS_REQUIREMENTS = ["provide-foundry>=0.0.1", "provide-testkit[docs]>=0.5.1"]
STRICT_BUILD_COMMAND = "uv run --frozen --isolated --only-group docs python scripts/build-docs.py"


def _project_lock_entry(lock: dict[str, Any]) -> dict[str, Any]:
    return next(package for package in lock["package"] if package["name"] == "pyvider-components")


def _documented_strict_build_command() -> str:
    guide = (ROOT / "docs/guides/provider-linting.md").read_text(encoding="utf-8")
    marker = (
        "Build the complete documentation site from the locked, isolated documentation dependency group:\n"
    )
    command_block = guide.split(marker, maxsplit=1)[1]
    return command_block.split("```shell\n", maxsplit=1)[1].splitlines()[0]


def _copy_tracked_source(destination: Path) -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    for encoded_path in tracked:
        if not encoded_path:
            continue
        relative_path = Path(encoded_path.decode())
        source = ROOT / relative_path
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def test_docs_dependencies_are_declared_and_locked() -> None:
    """A clean docs build must not depend on packages from the developer environment."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))

    assert project["dependency-groups"]["docs"] == DOCS_REQUIREMENTS

    project_lock = _project_lock_entry(lock)
    assert project_lock["dev-dependencies"]["docs"] == [
        {"name": "provide-foundry"},
        {"name": "provide-testkit", "extra": ["docs"]},
    ]
    assert project_lock["metadata"]["requires-dev"]["docs"] == [
        {"name": "provide-foundry", "specifier": ">=0.0.1"},
        {"name": "provide-testkit", "extras": ["docs"], "specifier": ">=0.5.1"},
    ]


def test_every_configured_local_theme_asset_exists() -> None:
    """Theme branding referenced by MkDocs must be part of the source tree."""
    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))

    missing: list[str] = []
    for key in ("logo", "favicon"):
        configured = config.get("theme", {}).get(key)
        if isinstance(configured, str) and "://" not in configured:
            asset = ROOT / "docs" / configured
            if not asset.is_file():
                missing.append(f"theme.{key}: {configured}")

    assert not missing, "Missing configured theme assets:\n" + "\n".join(missing)


def test_strict_docs_build_command_is_documented() -> None:
    """Contributors get the same isolated, lockfile-backed build used for verification."""

    assert _documented_strict_build_command() == STRICT_BUILD_COMMAND


def test_documented_strict_build_succeeds_from_tracked_clean_source(tmp_path: Path) -> None:
    """The documented command must recreate ignored Foundry scaffolding in a clean checkout."""
    clean_source = tmp_path / "source"
    _copy_tracked_source(clean_source)

    result = subprocess.run(
        shlex.split(_documented_strict_build_command()),
        cwd=clean_source,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
