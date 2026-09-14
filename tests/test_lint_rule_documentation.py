"""Contract tests for first-party lint rule documentation."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

from pyvider.components import lint_rules

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs/guides/provider-linting.md"

GENERATED_DOC_DIRECTORIES = (
    "actions",
    "ephemeral-resources",
    "list-resources",
    "providers",
    "state-stores",
)


@dataclass(frozen=True)
class RuleDocumentation:
    template: str
    trigger: str
    groups: tuple[str, str]
    remediation: str


RULE_DOCUMENTATION = {
    lint_rules.INSECURE_TLS: RuleDocumentation(
        template="src/pyvider/components/provider.plating/docs/pyvider.tmpl.md",
        trigger="`api_insecure_skip_verify` is explicitly `true`",
        groups=(lint_rules.ALL, lint_rules.SECURITY),
        remediation="Set `api_insecure_skip_verify` to `false`.",
    ),
    lint_rules.WORLD_WRITABLE_DIRECTORY: RuleDocumentation(
        template=(
            "src/pyvider/components/resources/local_directory.plating/docs/pyvider_local_directory.tmpl.md"
        ),
        trigger="`permissions` has the POSIX other-write bit (`& 0o002`)",
        groups=(lint_rules.ALL, lint_rules.SECURITY),
        remediation=("Set `permissions` to a mode without the POSIX other-write bit, such as `0o755`."),
    ),
    lint_rules.INSECURE_HTTP: RuleDocumentation(
        template=("src/pyvider/components/data_sources/http_api.plating/docs/pyvider_http_api.tmpl.md"),
        trigger="`url`, compared case-insensitively, starts with `http://`",
        groups=(lint_rules.ALL, lint_rules.SECURITY),
        remediation="Use an `https://` URL.",
    ),
    lint_rules.LONG_LIVED_LEASE: RuleDocumentation(
        template=("src/pyvider/components/ephemerals/lease.plating/docs/pyvider_lease.tmpl.md"),
        trigger="`ttl_seconds` is greater than `3600`",
        groups=(lint_rules.ALL, lint_rules.RELIABILITY),
        remediation="Set `ttl_seconds` to `3600` or less.",
    ),
    lint_rules.INCLUDE_HIDDEN_FILES: RuleDocumentation(
        template=(
            "src/pyvider/components/list_resources/file_contents.plating/docs/pyvider_file_content.tmpl.md"
        ),
        trigger="`include_hidden` is explicitly `true`",
        groups=(lint_rules.ALL, lint_rules.SECURITY),
        remediation="Set `include_hidden` to `false`.",
    ),
    lint_rules.LONG_ACTION_TIMEOUT: RuleDocumentation(
        template=("src/pyvider/components/actions/wait_for_file.plating/docs/pyvider_wait_for_file.tmpl.md"),
        trigger="`timeout_seconds` is greater than `300`",
        groups=(lint_rules.ALL, lint_rules.RELIABILITY),
        remediation="Set `timeout_seconds` to `300` or less.",
    ),
    lint_rules.RELATIVE_STATE_STORE_PATH: RuleDocumentation(
        template=(
            "src/pyvider/components/state_stores/filesystem_store.plating/docs/"
            "pyvider_filesystem_store.tmpl.md"
        ),
        trigger="`path` is relative after `~` expansion",
        groups=(lint_rules.ALL, lint_rules.RELIABILITY),
        remediation="Use an absolute `path`.",
    ),
}

GROUP_IDS = frozenset({lint_rules.ALL, lint_rules.SECURITY, lint_rules.RELIABILITY})
RULE_IDS = tuple(
    sorted(
        value
        for name, value in vars(lint_rules).items()
        if name.isupper() and isinstance(value, str) and value not in GROUP_IDS
    )
)


@pytest.mark.parametrize("rule", RULE_IDS, ids=lambda rule: rule.rpartition(":")[2])
def test_every_first_party_rule_is_documented(rule: str) -> None:
    """Every exported rule has complete guide and generated-doc source coverage."""
    case = RULE_DOCUMENTATION.get(rule)
    missing: list[str] = []
    if case is None:
        missing.append(f"test metadata for {rule}")
    else:
        suppression = f"PYVIDER_LINT='{lint_rules.ALL},!{rule}' tofu validate"
        expected = (rule, case.trigger, *case.groups, case.remediation, suppression)
        for path in (GUIDE, ROOT / case.template):
            content = path.read_text(encoding="utf-8") if path.exists() else ""
            missing.extend(f"{path.relative_to(ROOT)}: {text}" for text in expected if text not in content)

    assert not missing, "Missing lint documentation:\n" + "\n".join(missing)


@pytest.mark.parametrize("rule", RULE_IDS, ids=lambda rule: rule.rpartition(":")[2])
def test_component_lint_section_is_terminal(rule: str) -> None:
    """Lint guidance must not capture unrelated component sections beneath it."""
    case = RULE_DOCUMENTATION[rule]
    content = (ROOT / case.template).read_text(encoding="utf-8")
    lint_section = content.partition("## Provider linting")[2]
    trailing_headings = [line for line in lint_section.splitlines() if line.startswith("#")]

    assert not trailing_headings, f"Headings follow provider linting: {trailing_headings}"


def test_guide_contains_seven_rule_catalog_table() -> None:
    """The central guide provides a scan-friendly row for every rule."""
    guide = GUIDE.read_text(encoding="utf-8")
    table = "\n".join(line for line in guide.splitlines() if line.startswith("|"))

    missing = [rule for rule in RULE_IDS if rule not in table]

    assert not missing, f"Rules missing from guide catalog table: {missing}"


def test_guide_and_provider_template_document_selector_configuration() -> None:
    """Persistent rules, environment precedence, and empty disablement stay visible."""
    provider_template = ROOT / "src/pyvider/components/provider.plating/docs/pyvider.tmpl.md"
    expected = (
        "[lint]",
        'rules = ["provide-io/pyvider:all"]',
        "PYVIDER_LINT=provide-io/pyvider:security tofu validate",
        "PYVIDER_LINT='' tofu validate",
        "PYVIDER_LINT > [lint].rules > disabled",
        "completely overrides `[lint].rules` when present",
    )
    missing = []
    for path in (GUIDE, provider_template):
        content = path.read_text(encoding="utf-8")
        missing.extend(f"{path.relative_to(ROOT)}: {text}" for text in expected if text not in content)

    assert not missing, "Missing selector documentation:\n" + "\n".join(missing)


def test_guide_distinguishes_opentofu_and_tofusoup_reachability() -> None:
    """Direct-client coverage is not attributed to OpenTofu core."""
    guide = GUIDE.read_text(encoding="utf-8")
    expected = (
        "OpenTofu validation reaches the provider, resource, data source, and ephemeral resource paths.",
        "OpenTofu core does not currently invoke the validation RPCs for list resources, actions, or state stores.",
        "TofuSoup calls all seven validation RPCs directly against the same packaged provider.",
    )

    missing = [text for text in expected if text not in guide]

    assert not missing, "Missing reachability distinctions:\n" + "\n".join(missing)


def test_guide_states_api_and_transport_status() -> None:
    """Supported Pyvider APIs stay distinct from experimental OpenTofu transport."""
    guide = GUIDE.read_text(encoding="utf-8")
    expected = (
        "`LintFinding`, `LintSelector`, and `LintContext` are supported Pyvider author APIs.",
        "OpenTofu's built-in linter remains experimental.",
        "The current tfprotov6 protocol has no provider-lint wire message",
        "`-lint` selects OpenTofu core rules only",
        "ordinary warning diagnostics through a temporary compatibility bridge",
    )

    missing = [text for text in expected if text not in guide]

    assert not missing, "Missing API or transport status:\n" + "\n".join(missing)


def test_lint_guide_is_discoverable() -> None:
    """The guide is linked from both the documentation navigation and README."""
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    missing = []
    if "- Provider Linting: guides/provider-linting.md" not in mkdocs:
        missing.append("mkdocs navigation")
    if "[Provider linting](docs/guides/provider-linting.md)" not in readme:
        missing.append("README link")

    assert not missing, f"Provider linting guide missing from: {missing}"


def test_component_doc_generation_workflow_is_documented() -> None:
    """The supported retained and disposable generation interfaces stay explicit."""
    guide = GUIDE.read_text(encoding="utf-8")
    expected = (
        "python scripts/generate-component-docs.py --output-dir docs",
        "python scripts/generate-component-docs.py",
        "first runs default Plating generation and then runs provider-only generation",
        "The navigation target is the resolved output directory's sibling `mkdocs.yml`.",
        "When `--output-dir PATH` is omitted, the output is generated in and removed with a temporary directory.",
        "restores `mkdocs.yml` byte-for-byte even if Plating fails",
        "Generated component directories are ignored by Git",
    )

    missing = [text for text in expected if text not in guide]

    assert not missing, "Missing generation documentation:\n" + "\n".join(missing)


@pytest.mark.parametrize("directory", GENERATED_DOC_DIRECTORIES)
def test_generated_component_doc_directory_is_ignored(directory: str) -> None:
    """In-place Plating outputs do not dirty repository provenance."""
    candidate = f"docs/{directory}/generated.md"

    result = subprocess.run(["git", "check-ignore", "--quiet", candidate], cwd=ROOT, check=False)

    assert result.returncode == 0, f"Generated documentation is not ignored: {candidate}"
