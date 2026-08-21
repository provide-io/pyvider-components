# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-08-21

### Added

- **Demo components for the four tfprotov6.11 component types.** Terraform Plugin Protocol 6.11 added actions, list resources, state stores and gave ephemeral resources a renewal cycle. pyvider implemented all four; nothing installable exercised them. This release adds one worked example of each:
  - `pyvider_echo` and `pyvider_wait_for_file` actions. The second polls for a path with a bounded timeout and reports progress while it waits, which is the part of the action contract a trivial echo never reaches.
  - `pyvider_lease` ephemeral resource. Holds a lease file open across renewals and removes it on close, carrying the resolved path in private state so the configured value can be echoed back verbatim -- returning the resolved form instead is a different value to Terraform and it rejects the resource with "planned value does not match config value".
  - `pyvider_directory_entries` and `pyvider_secret_notes` list resources, each publishing its own identity schema.
  - `pyvider_fs` state store, backed by the filesystem with lease-aware locking.
- **`pyvider_secret_note` resource.** A write-only attribute that never lands in state, paired with `pyvider_secret_notes` so the list resource has something to list.
- **Terraform parity test suites** for string, numeric and collection functions, pinning this provider's answers to Terraform's own builtins.

### Fixed

- **`pyvider_local_directory` read no longer normalises away a `./` prefix.** `read()` returned the resolved path, which Terraform compares against the configured one and rejects when they differ.
- **Division by zero answers infinity, not an error**, matching Terraform.
- **Provider functions answer what Terraform's builtins answer** across the string and numeric surfaces the new parity suites cover.
- **`pyvider_secret_note` converges** and publishes its notes durably, rather than producing a fresh plan on every apply.
- **The lease's base class carries its type arguments.** `BaseEphemeralResource` is generic in result, private state and config; subclassing it bare left mypy with nothing to check the three hooks against and hid a Liskov violation in `validate`.

### Changed

- **Floors raised to the published 0.5.x suite**: `pyvider>=0.5.2` (list-resource identity schemas published under the resource's own name; functions and ephemerals no longer handed half-known arguments), `pyvider-cty>=0.5.0`, `plating>=0.5.0`.
- **`[tool.uv.sources]` removed.** The release workflow calls ci-tooling's `python-release.yml`, which has no `no-sources` input to pass, so a path source fails the release outright. Local sibling checkouts are installed with `uv pip install -e ../<repo>` instead. Every sibling in the suite says the same thing now.
- Documentation bundles adorned for the new component types and the duplicate `## Schema` headings removed from the hand-written templates.

### Removed

- Templates for two data sources that no longer exist (`pyvider_nested_data_processor`, `pyvider_nested_resource_test`).

## [0.4.0] - 2026-04-22

Released without a changelog entry at the time; recorded here for the history.

### Added

- Standard reusable provider components: the resource, data source and function patterns the suite's 0.4.0 release shipped against.
