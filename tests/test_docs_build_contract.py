"""Contracts for building the checked-in MkDocs site from a clean environment."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS_REQUIREMENT = "provide-testkit[docs]>=0.5.1"
STRICT_BUILD_COMMAND = "uv run --frozen --isolated --only-group docs mkdocs build --strict"


def _project_lock_entry(lock: dict[str, Any]) -> dict[str, Any]:
    return next(package for package in lock["package"] if package["name"] == "pyvider-components")


def test_docs_dependencies_are_declared_and_locked() -> None:
    """A clean docs build must not depend on packages from the developer environment."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))

    assert project["dependency-groups"]["docs"] == [DOCS_REQUIREMENT]

    project_lock = _project_lock_entry(lock)
    assert project_lock["dev-dependencies"]["docs"] == [{"name": "provide-testkit", "extra": ["docs"]}]
    assert project_lock["metadata"]["requires-dev"]["docs"] == [
        {"name": "provide-testkit", "extras": ["docs"], "specifier": ">=0.5.1"}
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
    guide = (ROOT / "docs/guides/provider-linting.md").read_text(encoding="utf-8")

    assert STRICT_BUILD_COMMAND in guide
