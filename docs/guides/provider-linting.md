# Provider linting

Pyvider Components provides opt-in rules for reviewing valid configurations. Provider linting is disabled by default.

## Enable rules

For a persistent project selection, add the following to `pyvider.toml`:

```toml
[lint]
rules = ["provide-io/pyvider:all"]
```

For one provider process, `PYVIDER_LINT` accepts a comma-separated selector list and completely overrides `[lint].rules` when present:

```shell
PYVIDER_LINT=provide-io/pyvider:security tofu validate
```

Presence matters. An explicitly empty environment value overrides the file and disables every provider rule for that process:

```shell
PYVIDER_LINT='' tofu validate
```

The precedence is:

```text
PYVIDER_LINT > [lint].rules > disabled
```

## API and transport status

`LintFinding`, `LintSelector`, and `LintContext` are supported Pyvider author APIs. OpenTofu's built-in linter remains experimental.

The current tfprotov6 protocol has no provider-lint wire message or provider selector hints. Consequently, `-lint` selects OpenTofu core rules only, while `[lint].rules` and `PYVIDER_LINT` select provider rules. Pyvider maps selected findings to ordinary warning diagnostics through a temporary compatibility bridge. The bridge preserves the detail and optional top-level attribute path, appends the rule ID to the summary, and leaves rule groups internal because the wire format cannot carry them. Components remain protocol-neutral.

## Validation reachability

OpenTofu validation reaches the provider, resource, data source, and ephemeral resource paths. OpenTofu core does not currently invoke the validation RPCs for list resources, actions, or state stores. TofuSoup calls all seven validation RPCs directly against the same packaged provider.

| Client                 | Provider | Resource | Data source | Ephemeral | List | Action | State store |
| ---------------------- | -------- | -------- | ----------- | --------- | ---- | ------ | ----------- |
| OpenTofu               | yes      | yes      | yes         | yes       | no   | no     | no          |
| TofuSoup direct client | yes      | yes      | yes         | yes       | yes  | yes    | yes         |

## Regenerate component reference pages

Use the supported wrapper to regenerate the published component pages in place:

```shell
python scripts/generate-component-docs.py --output-dir docs
```

The wrapper first runs default Plating generation and then runs provider-only generation, which is required because the default selection does not render the provider page. It snapshots the authored documentation configuration and restores `mkdocs.yml` byte-for-byte even if Plating fails. Generated component directories are ignored by Git, so an in-place run does not add generated pages to repository provenance.

For verification without retaining rendered pages, omit the option:

```shell
python scripts/generate-component-docs.py
```

When `--output-dir PATH` is omitted, the output is generated in and removed with a temporary directory.

## Rule catalog

Every rule belongs to the `provide-io/pyvider:all` group and one category group.

| Kind               | Rule                                           | Category group                   | Trigger                                                   |
| ------------------ | ---------------------------------------------- | -------------------------------- | --------------------------------------------------------- |
| Provider           | `provide-io/pyvider:insecure-tls`              | `provide-io/pyvider:security`    | `api_insecure_skip_verify` is explicitly `true`           |
| Resource           | `provide-io/pyvider:world-writable-directory`  | `provide-io/pyvider:security`    | `permissions` has the POSIX other-write bit (`& 0o002`)   |
| Data source        | `provide-io/pyvider:insecure-http`             | `provide-io/pyvider:security`    | `url`, compared case-insensitively, starts with `http://` |
| Ephemeral resource | `provide-io/pyvider:long-lived-lease`          | `provide-io/pyvider:reliability` | `ttl_seconds` is greater than `3600`                      |
| List resource      | `provide-io/pyvider:include-hidden-files`      | `provide-io/pyvider:security`    | `include_hidden` is explicitly `true`                     |
| Action             | `provide-io/pyvider:long-action-timeout`       | `provide-io/pyvider:reliability` | `timeout_seconds` is greater than `300`                   |
| State store        | `provide-io/pyvider:relative-state-store-path` | `provide-io/pyvider:reliability` | `path` is relative after `~` expansion                    |

## `provide-io/pyvider:world-writable-directory`

- **Trigger:** `permissions` has the POSIX other-write bit (`& 0o002`).

- **Groups:** `provide-io/pyvider:all`, `provide-io/pyvider:security`.

- **Remediation:** Set `permissions` to a mode without the POSIX other-write bit, such as `0o755`.

- **Suppress this rule:**

  ```shell
  PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:world-writable-directory' tofu validate
  ```

## `provide-io/pyvider:relative-state-store-path`

- **Trigger:** `path` is relative after `~` expansion.

- **Groups:** `provide-io/pyvider:all`, `provide-io/pyvider:reliability`.

- **Remediation:** Use an absolute `path`.

- **Suppress this rule:**

  ```shell
  PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:relative-state-store-path' tofu validate
  ```

## `provide-io/pyvider:long-lived-lease`

- **Trigger:** `ttl_seconds` is greater than `3600`.

- **Groups:** `provide-io/pyvider:all`, `provide-io/pyvider:reliability`.

- **Remediation:** Set `ttl_seconds` to `3600` or less.

- **Suppress this rule:**

  ```shell
  PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:long-lived-lease' tofu validate
  ```

## `provide-io/pyvider:long-action-timeout`

- **Trigger:** `timeout_seconds` is greater than `300`.

- **Groups:** `provide-io/pyvider:all`, `provide-io/pyvider:reliability`.

- **Remediation:** Set `timeout_seconds` to `300` or less.

- **Suppress this rule:**

  ```shell
  PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:long-action-timeout' tofu validate
  ```

## `provide-io/pyvider:insecure-tls`

- **Trigger:** `api_insecure_skip_verify` is explicitly `true`.

- **Groups:** `provide-io/pyvider:all`, `provide-io/pyvider:security`.

- **Remediation:** Set `api_insecure_skip_verify` to `false`.

- **Suppress this rule:**

  ```shell
  PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:insecure-tls' tofu validate
  ```

## `provide-io/pyvider:insecure-http`

- **Trigger:** `url`, compared case-insensitively, starts with `http://`.

- **Groups:** `provide-io/pyvider:all`, `provide-io/pyvider:security`.

- **Remediation:** Use an `https://` URL.

- **Suppress this rule:**

  ```shell
  PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:insecure-http' tofu validate
  ```

## `provide-io/pyvider:include-hidden-files`

- **Trigger:** `include_hidden` is explicitly `true`.

- **Groups:** `provide-io/pyvider:all`, `provide-io/pyvider:security`.

- **Remediation:** Set `include_hidden` to `false`.

- **Suppress this rule:**

  ```shell
  PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:include-hidden-files' tofu validate
  ```
