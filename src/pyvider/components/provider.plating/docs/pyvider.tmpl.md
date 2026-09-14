---
page_title: "Provider: pyvider"
description: |-
  Reference implementation of a Pyvider provider.
---

# pyvider (Provider)

Reference implementation of a Pyvider provider.

## Example Usage

{{ example("example") }}

{{ schema() }}

## Provider linting

Provider linting is disabled by default. To persistently enable all first-party
rules, set `[lint].rules` in `pyvider.toml`:

```toml
[lint]
rules = ["provide-io/pyvider:all"]
```

For one provider process, `PYVIDER_LINT` accepts comma-separated selectors and
completely overrides `[lint].rules` when present:

```shell
PYVIDER_LINT=provide-io/pyvider:security tofu validate
```

An explicitly empty value disables provider rules even when the file enables
them:

```shell
PYVIDER_LINT='' tofu validate
```

The precedence is `PYVIDER_LINT > [lint].rules > disabled`.

`provide-io/pyvider:insecure-tls` belongs to `provide-io/pyvider:all` and
`provide-io/pyvider:security`.

- **Trigger:** `api_insecure_skip_verify` is explicitly `true`.
- **Remediation:** Set `api_insecure_skip_verify` to `false`.
- **Suppress this rule:**

    ```shell
    PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:insecure-tls' tofu validate
    ```
