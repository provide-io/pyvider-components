# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.3] - 2026-08-23

### Fixed

- **`pyvider_lease` dropped the `ttl_seconds` it was given.** The schema lets a practitioner set `ttl_seconds`, but `LeaseResult` had no field for it, so the ephemeral resource opened with that attribute null and Terraform rejected the whole resource: a value the configuration set came back unset. `open()` now echoes `ctx.config.ttl_seconds` verbatim rather than the internally defaulted value, so a config that omits it still reads back as omitted.
- **`pyvider_filesystem_store`'s example could not be applied.** It set `path = "${path.module}/tfstate"`, but Terraform decodes a `state_store` block with a nil `*hcl.EvalContext` -- the same treatment `backend` blocks get -- so no variable, function or `path.module` reference resolves inside one. The example now uses a literal relative path and says why.

A structural test now asserts the general case behind the first bug: every attribute a component's schema lets a practitioner set must have a matching field on the result class, so the next component that forgets one fails in CI instead of at `terraform apply`.

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
- **One unreadable entry no longer fails a whole directory listing.** `pyvider_directory_entries` guarded the size lookup but not the `is_file()` test above it; an entry that `iterdir()` saw and that then vanished raised OSError out of the stream, so every other file in the directory went unreported.
- **The lease's base class carries its type arguments.** `BaseEphemeralResource` is generic in result, private state and config; subclassing it bare left mypy with nothing to check the three hooks against and hid a Liskov violation in `validate`.

### Changed

- **Floors raised to the published 0.5.x suite**: `pyvider>=0.5.2` (list-resource identity schemas published under the resource's own name; functions and ephemerals no longer handed half-known arguments), `pyvider-cty>=0.5.0`, `plating>=0.5.0`.
- **`[tool.uv.sources]` removed.** The release workflow calls ci-tooling's `python-release.yml`, which has no `no-sources` input to pass, so a path source fails the release outright. Local sibling checkouts are installed with `uv pip install -e ../<repo>` instead. Every sibling in the suite says the same thing now.
- Documentation bundles adorned for the new component types and the duplicate `## Schema` headings removed from the hand-written templates.

### Removed

- Templates for two data sources that no longer exist (`pyvider_nested_data_processor`, `pyvider_nested_resource_test`).

## [0.5.2] - 2026-08-21

### Changed

- **`pyvider_fs` is renamed `pyvider_filesystem_store`.** It was the only abbreviated name among twenty-two components, and it disagreed with its own class (`PyviderFileSystemStateStore`), module (`filesystem_store.py`) and bundle directory (`filesystem_store.plating`). That mismatch was not only cosmetic: plating matches a bundle to its component, and no prefixing rule gets from `filesystem_store` to `pyvider_fs`, so the state store's examples were never compiled. Safe to rename because the component is `test_only` -- a published provider never served it under either name.

### Fixed

- **`pyvider_secret_note`'s example was a stub.** It carried `# Configuration options here` in place of the two required attributes, and an output referencing `.id`, which is not in the schema. Applying it failed with `Missing required argument`. It now exercises the write-only flow it exists to demonstrate: `secret_value` sent but never persisted, `secret_version` as the change signal, `digest` as the output.
- **The private-state shared secret is documented.** `pyvider_timed_token` and `pyvider_private_state_verifier` both keep encrypted private state, and the provider refuses to without `PYVIDER_PRIVATE_STATE_SHARED_SECRET` (or `private_state_shared_secret` in `pyvider.toml`). The requirement appeared nowhere in the documentation or the examples, so a reader copying either example met `Private state shared secret not configured` with nothing to explain it. Both pages now carry a Prerequisites section ahead of the example.

Both found by running the generated examples through `soup stir` against the packaged provider, which nothing had done before: 41 of 41 directories now apply.

## [0.5.1] - 2026-08-21

### Fixed

- **`pyvider_warning_example` is no longer filed under "Test Mode".** It is registered `@register_resource("pyvider_warning_example")` with no `test_only`, and `tofu providers schema -json` confirms a published provider serves it -- but its template's frontmatter declared `subcategory: "Test Mode"` by hand, so the one usable resource in that group was documented as though it were unreachable. It was the only one of the fifteen templates declaring that subcategory where the component did not match.

## [0.5.0] - 2026-08-21 (documentation corrections)

### Fixed

- **`pyvider_nested_resource_test` and `pyvider_nested_data_processor` are documented again.** Their templates lived in a `data_sources/*.plating` bundle, so plating rendered them into `docs/data-sources/` and they were removed as "data sources that no longer exist". They do exist -- `nested_data_test_suite.py` declares five components, three data sources plus one resource and one function -- and the templates now sit in bundles matching the types they document.
- **Ten component pages linked to example files instead of showing them.** A `## Examples` section listed `[basic.tf](examples/basic.tf)` and friends, which resolve to `docs/<type>/examples/*.tf` -- files that were never written there, and links that cannot resolve at all on a registry page. They now render inline through `{{ example("basic") }}`, the same helper the other fifty pages already used. 35 broken links, and `mkdocs --strict` aborted the build over them.

## [0.4.0] - 2026-04-22

Released without a changelog entry at the time; recorded here for the history.

### Added

- Standard reusable provider components: the resource, data source and function patterns the suite's 0.4.0 release shipped against.
