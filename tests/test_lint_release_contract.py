"""Release contract for the first-party provider lint rules."""

import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULE_CONSTANTS = (
    "INSECURE_TLS",
    "WORLD_WRITABLE_DIRECTORY",
    "INSECURE_HTTP",
    "LONG_LIVED_LEASE",
    "INCLUDE_HIDDEN_FILES",
    "LONG_ACTION_TIMEOUT",
    "RELATIVE_STATE_STORE_PATH",
)


def test_lint_release_requires_the_corrected_public_stack() -> None:
    """Published metadata must not resolve an older or shared-root dependency."""
    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert '"pyvider>=0.8.0"' in project
    assert '"pyvider-cty>=0.6.2"' in project
    assert '"pyvider-rpcplugin>=0.5.5"' in project


def test_release_wheel_smoke_exercises_all_public_lint_exports() -> None:
    """TestPyPI verification must exercise the installed wheel's public lint API."""
    workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")

    for rule in RULE_CONSTANTS:
        assert rule in workflow
    for public_api in (
        "ALL",
        "LintContext",
        "LintSelector",
        "PyviderProvider",
        "asyncio.run",
    ):
        assert public_api in workflow
    assert "pyvider.lint._runner" not in workflow


def test_lint_rules_are_prepared_as_0_8_0() -> None:
    """Release metadata must name every rule and the framework contract."""
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "0.8.0"

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    section = changelog.partition("## [0.8.0] - 2026-09-22")[2].partition("\n## [")[0]
    assert section
    for rule in (
        "insecure-tls",
        "world-writable-directory",
        "insecure-http",
        "long-lived-lease",
        "include-hidden-files",
        "long-action-timeout",
        "relative-state-store-path",
    ):
        assert rule in section
    for statement in (
        "disabled by default",
        "PYVIDER_LINT",
        "unknown",
        "pyvider>=0.8.0",
        "pyvider-cty>=0.6.2",
        "pyvider-rpcplugin>=0.5.5",
        "all seven",
        "OpenTofu",
        "uv pip install --force-reinstall 'pyvider>=0.8.0' 'pyvider-components>=0.8.0'",
    ):
        assert statement in section


def test_lint_guide_diagrams_selection_and_seven_validation_surfaces() -> None:
    """The release guide must make rule selection and coverage visually explicit."""
    guide = (ROOT / "docs/guides/provider-linting.md").read_text(encoding="utf-8")

    for text in (
        "```mermaid",
        "flowchart LR",
        "Provider",
        "Resource",
        "Data source",
        "Ephemeral resource",
        "List resource",
        "Action",
        "State store",
        "TofuSoup direct results",
        "Pyvider warning diagnostics",
    ):
        assert text in guide


def test_built_wheel_contains_lint_rules_without_owning_pyvider_root(tmp_path: Path) -> None:
    """The artifact contributes components without replacing Pyvider's root files."""
    source = tmp_path / "source"
    shutil.copytree(
        ROOT,
        source,
        ignore=shutil.ignore_patterns(
            ".git",
            ".hypothesis",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            ".venv",
            "*.egg-info",
            "build",
            "dist",
            "site",
        ),
    )
    output = tmp_path / "dist"
    subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(output)],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    )
    wheel = next(output.glob("pyvider_components-0.8.0-*.whl"))

    with zipfile.ZipFile(wheel) as archive:
        members = set(archive.namelist())

    assert "pyvider/components/lint_rules.py" in members
    assert "pyvider/components/provider.py" in members
    assert "pyvider/components/py.typed" in members
    assert "pyvider/__init__.py" not in members
    assert "pyvider/py.typed" not in members
