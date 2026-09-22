"""Tests for reproducible component documentation generation."""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

from pyvider.components import lint_rules

ROOT = Path(__file__).resolve().parents[1]
MKDOCS = ROOT / "mkdocs.yml"
GENERATOR = ROOT / "scripts/generate-component-docs.py"

GENERATED_RULE_DOCS = {
    "providers/pyvider.md": (lint_rules.INSECURE_TLS, lint_rules.SECURITY),
    "resources/local_directory.md": (lint_rules.WORLD_WRITABLE_DIRECTORY, lint_rules.SECURITY),
    "data-sources/http_api.md": (lint_rules.INSECURE_HTTP, lint_rules.SECURITY),
    "ephemeral-resources/lease.md": (lint_rules.LONG_LIVED_LEASE, lint_rules.RELIABILITY),
    "list-resources/file_content.md": (lint_rules.INCLUDE_HIDDEN_FILES, lint_rules.SECURITY),
    "actions/wait_for_file.md": (lint_rules.LONG_ACTION_TIMEOUT, lint_rules.RELIABILITY),
    "state-stores/filesystem_store.md": (lint_rules.RELATIVE_STATE_STORE_PATH, lint_rules.RELIABILITY),
}


def _contains_provider_linting_guide(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("Provider Linting") == "guides/provider-linting.md":
            return True
        return any(_contains_provider_linting_guide(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_provider_linting_guide(item) for item in value)
    return False


def _load_generator_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("generate_component_docs", GENERATOR)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generator_writes_all_rule_docs_without_changing_authored_navigation(tmp_path: Path) -> None:
    """The retained-output workflow covers default and provider-only Plating modes."""
    output_dir = tmp_path / "component-docs"
    original_mkdocs = MKDOCS.read_bytes()
    navigation_target = output_dir.parent / "mkdocs.yml"
    navigation_target.write_bytes(original_mkdocs)

    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--output-dir", str(output_dir)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    missing: list[str] = []
    for relative_path, (rule, group) in GENERATED_RULE_DOCS.items():
        path = output_dir / relative_path
        content = path.read_text(encoding="utf-8") if path.exists() else ""
        suppression = f"PYVIDER_LINT='{lint_rules.ALL},!{rule}' tofu validate"
        missing.extend(
            f"{relative_path}: {expected}"
            for expected in (rule, lint_rules.ALL, group, suppression)
            if expected not in content
        )
    assert not missing, "Missing generated lint documentation:\n" + "\n".join(missing)

    parsed_mkdocs = yaml.safe_load(navigation_target.read_text(encoding="utf-8"))
    assert _contains_provider_linting_guide(parsed_mkdocs["nav"])
    assert navigation_target.read_bytes() == original_mkdocs
    assert MKDOCS.read_bytes() == original_mkdocs


def test_generator_uses_disposable_output_when_directory_is_omitted(tmp_path: Path) -> None:
    """An omitted output directory leaves neither generated docs nor config edits."""
    original_mkdocs = MKDOCS.read_bytes()
    environment = {**os.environ, "TMPDIR": str(tmp_path)}

    result = subprocess.run(
        [sys.executable, str(GENERATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert not list(tmp_path.iterdir())
    assert MKDOCS.read_bytes() == original_mkdocs


def test_generator_removes_generated_navigation_when_sibling_was_absent(tmp_path: Path) -> None:
    """Retained docs do not imply retaining a Plating-created navigation file."""
    output_dir = tmp_path / "component-docs"
    navigation_target = output_dir.parent / "mkdocs.yml"

    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--output-dir", str(output_dir)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert not navigation_target.exists()


def test_generator_help_defines_the_output_directory_interface() -> None:
    """The CLI advertises the retained-output option and disposable default."""
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--help"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    help_text = " ".join(result.stdout.split())
    assert "--output-dir PATH" in help_text
    assert "omit to generate in a disposable temporary directory" in help_text


@pytest.mark.parametrize("navigation_existed", [True, False], ids=["present", "absent"])
def test_generator_restores_navigation_state_when_plating_fails(
    tmp_path: Path, monkeypatch, navigation_existed: bool
) -> None:
    """A failed Plating subprocess cannot alter the sibling navigation state."""
    generator = _load_generator_module()
    output_dir = tmp_path / "component-docs"
    navigation_target = output_dir.parent / "mkdocs.yml"
    original_navigation = b"nav:\n  - Guides:\n      - Provider Linting: guides/provider-linting.md\n"
    if navigation_existed:
        navigation_target.write_bytes(original_navigation)

    def fail_after_rewriting_navigation(command, **kwargs):
        navigation_target.write_text("nav:\n  - generated.md\n", encoding="utf-8")
        raise subprocess.CalledProcessError(returncode=1, cmd=command)

    monkeypatch.setattr(generator.subprocess, "run", fail_after_rewriting_navigation)

    with pytest.raises(subprocess.CalledProcessError):
        generator.generate_component_docs(output_dir)
    if navigation_existed:
        assert navigation_target.read_bytes() == original_navigation
    else:
        assert not navigation_target.exists()
