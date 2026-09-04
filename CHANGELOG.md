# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0] - 2026-09-04

### Breaking

- **The list resource `pyvider_directory_entry` is now `pyvider_file_content`.** A configuration naming the old type stops resolving and must be renamed.

  It could never have worked under the old name. Terraform resolves a list resource's results against the managed resource type of the *same name*, and refuses to list at all when there is none: `resourceSchema, ok := schema.ResourceTypes[r.TypeName]; if !ok || resourceSchema.Identity == nil` (`internal/plugin6/grpc_provider.go:1341-1345`). No managed `pyvider_directory_entry` exists, so `terraform query` answered "Identity schema not found for resource type pyvider_directory_entry; this is a bug in the provider" and nothing else. Publishing an identity schema under the list resource's own name does not satisfy it either -- `ResourceTypes` is built from `resource_schemas` merged with the identity schemas by name.

  A list resource is another way to find instances of a managed resource, not a type of its own, so it takes that resource's name. The listed values are the managed resource's own attributes now -- `filename`, `content`, `exists` and `content_hash` -- rather than a shape peculiar to listing.

### Added

- **`pyvider_file_content` declares an identity schema.** `filename` identifies a file, and Terraform requires the managed resource to carry one before it will list it. This is the other half of the rename: the name alone is not enough.

### Fixed

- **Three examples never stopped planning changes.** `pyvider_private_state_verifier` and `pyvider_provider_config_reader` each built a `pyvider_file_content` body containing `timestamp()`, which is re-evaluated on every plan, so the resource never matched the state it had just written -- `apply` succeeded and the next plan reported "0 to add, 1 to change, 0 to destroy", for ever. `pyvider_http_api` did the same and additionally stamped one into a data source header, re-reading the source every plan too. An example that is permanently about to change teaches the reader to write one, so the calls are gone.

  Nothing had noticed because nothing re-planned: `soup stir` gained its convergence check after 0.6.1 and only released it in 0.7.0.

- **Two examples say they cannot converge, because they cannot.** `pyvider_http_api` records how long each live call to httpbin.org took, and a measured duration differs on every read. `pyvider_env_variables` reports the environment the provider was launched with, and Terraform gives every launch its own -- `PLUGIN_CLIENT_CERT` is the automatic-mTLS certificate go-plugin mints per run, with `PLUGIN_MIN_PORT`, `PLUGIN_MAX_PORT` and `TF_PLUGIN_MAGIC_COOKIE` alongside it. Both declare `converges = false`, which is a true reading rather than a value invented during apply.

- **The state-store examples say they need a build with experiments enabled.** They carry the `-enable-pluggable-state-storage-experiment` flag, and Terraform compiles experiments into alpha and dev builds only: a stable release refuses the flag rather than ignoring it, so the example failed at `init` with a report reading "No specific error messages found in log. The failure may have been a crash." `experiments = true` states the requirement and `soup stir` 0.7.0 skips with the reason.

- **The list-resource examples name the command that reads them.** Both said to run `tofu query`. OpenTofu has no query command at any version, so the instruction could not be followed; `terraform query` is the one that reads `*.tfquery.hcl`, and it arrived in Terraform 1.14.

### Changed

- **Runtime floors now name the versions this package is actually tested against**: `pyvider>=0.6.2` (was `>=0.5.2`), `pyvider-cty>=0.5.3` (was `>=0.5.0`), `pyvider-rpcplugin>=0.4.2` (was `>=0.4.0`), `plating>=0.6.1` (was `>=0.5.0`) and `provide-foundation>=0.4.3` (was `>=0.4.0`). Every one of them sat below what the lock resolves, so the published metadata described a combination nothing here had ever run. Verified at the declared minimums with `uv lock --resolution lowest-direct`.

## [0.6.1] - 2026-08-25

### Added

- **`pyvider_secret_note` declares the version floor write-only attributes need.** Its `secret_value` is write-only, so the provider returns it null -- which is what write-only means. OpenTofu 1.10.6 has no concept of one and enforces the ordinary rule that a planned value must equal its config value, so it fails with `planned an invalid value for ...secret_value: planned value cty.NullVal(cty.String) does not match config value`, blaming the provider for behaving correctly. Measured rather than assumed: 1.10.6 fails, 1.11.0 and 1.12.5 both plan cleanly, so the floor is 1.11.0 for both implementations. `soup stir` 0.6.1 reads it and skips instead of reporting a phantom provider bug.

## [0.6.0] - 2026-08-24

### Added

- **Constrained examples declare what they need to run.** Six `.plating` bundles now carry an `examples/_requirements.meta.toml`, and `soup stir` 0.6.0 acts on it: a directory it cannot run here is skipped with the declared reason instead of run and failed.

  The OpenTofu exclusions are measured, not assumed. Against OpenTofu 1.12.5, `action` and `state_store` blocks are rejected outright with "Unsupported block type", while the ephemeral resource and ordinary resource examples get only "Missing required provider" -- meaning those parse fine and merely want the provider installed. That is the real shape of the long-standing "44 of 48": the four unreachable directories are the three actions and the state store, not everything tfprotov6.11 touched.

  `pyvider_filesystem_store` additionally records the flag it needs at `init` (`-enable-pluggable-state-storage-experiment`), which is the specific gap that left the state store unreachable. Two constraints that were previously only prose in a doc template are now declared where a runner can read them: `pyvider_http_api`'s examples call the live httpbin.org, and `pyvider_timed_token` and `pyvider_private_state_verifier` need `PYVIDER_PRIVATE_STATE_SHARED_SECRET` or they fail with "Private state shared secret not configured", which reads like a bug rather than a prerequisite.

### Changed

- **Five components are no longer `test_only`.** `pyvider_lease`, `pyvider_filesystem_store`, `pyvider_wait_for_file`, `pyvider_echo` and `pyvider_directory_entry` are served by a published provider now. Each does real work against the real world -- a TTL lease with renewal, a durable filesystem state store, a bounded wait on a path, an echo action, and a list resource over actual filesystem entries -- so gating them behind `PYVIDER_TESTMODE` hid working functionality rather than protecting anyone from a fixture. The provider's published surface goes from 34 components to 39.

  Still `test_only`, because they exist to exercise the protocol rather than to be used: the five `nested_data_test_suite` components, `pyvider_failing_action` (it fails on purpose), `pyvider_private_state_verifier`, and `pyvider_secret_note` with its paired list resource.

- **The promoted components are filed outside "Test Mode".** Their templates still declared `subcategory: "Test Mode"` by hand, so publishing them would have put five usable components on a registry page marked unreachable -- the same mismatch 0.5.1 fixed for `pyvider_warning_example`. `pyvider_filesystem_store` is State Storage, `pyvider_lease` is Coordination, `pyvider_echo` is Utility, and `pyvider_wait_for_file` and `pyvider_directory_entry` join File Operations. "Test Mode" now covers exactly the nine components still registered `test_only`.

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
