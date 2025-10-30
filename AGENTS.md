# Repository Guidelines

Contributors extend Pyvider’s standard component set; treat every change as production code that must interoperate with Terraform providers and the plating documentation pipeline.

## Project Structure & Module Organization
- Runtime modules live in `src/pyvider/components`, grouped by capability (data sources, resources, functions). Keep shared helpers close to their consumers.
- Acceptance and regression coverage sit in `tests/`, organized by domain (`tests/functions`, `tests/resources`, `tests/data_sources`, etc.) with reusable fixtures under `tests/fixtures`.
- Generated documentation is emitted into `docs/`; never hand-edit files there—regenerate with the Make targets. Long-form references and design notes belong in `docs/` or `BOOTSTRAP.md`.
- Example Terraform configurations reside in `examples/`, while operational scripts and automation live in `scripts/`. Avoid committing transient output under `dist/` or `output/` unless reproducing a release.

## Build, Test, and Development Commands
- `uv sync --all-groups` — create the Python 3.11 environment with runtime and dev extras.
- `source .venv/bin/activate` — activate the synced virtual environment before running tools.
- `uv run pytest` or `uv run pytest tests/functions` — execute the full or targeted test suite.
- `make docs-all` — regenerate all plated documentation; combine with `make docs-check` to inspect results.
- `make test` — run plating verification plus docs smoke tests; use before opening a PR.

## Coding Style & Naming Conventions
Follow PEP 8 and default to 4-space indentation. Module and file names stay `snake_case`; component identifiers mirror Terraform naming (`pyvider_<resource>`). Type hints are expected on public APIs. When templating plating resources, keep JSON/Jinja fragments minimal and document non-obvious logic with concise comments. Prefer pure functions and explicit dependencies over hidden globals.

## Testing Guidelines
Pytest drives validation (`python_files = test_*.py`, `python_functions = test_*`). Scope new tests under the matching domain folder and mark them with `@pytest.mark.unit`, `integration`, or `slow` from `pyproject.toml`. Ensure fixtures in `tests/fixtures` remain deterministic. Before pushing, run `uv run pytest -m "not slow"` and regenerate docs if components expose new surfaces.

## Commit & Pull Request Guidelines
History mixes emoji-prefixed automation and imperative human summaries (“Add test fixtures…”). Follow the imperative mood, keep the first line under ~72 characters, and add `[skip ci]` only for documentation-only changes. Pull requests should link related issues, describe testing (include command output snippets), attach screenshots for docs/UI diffs, and call out breaking changes or configuration migrations. Regenerate docs and update `README.md` or `docs/` whenever component behavior shifts.

## Component Documentation Workflow
Any new resource, data source, or function must ship with plating templates under `src/**/components/*.plating`. After authoring templates, run `make docs-all` and commit the generated Markdown. Validate that no `signature_markdown` placeholders leak into the output via `make test-docs`.
