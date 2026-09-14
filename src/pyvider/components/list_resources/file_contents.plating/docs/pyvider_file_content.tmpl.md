---
page_title: "List Resource: pyvider_file_content"
subcategory: "File Operations"
description: |-
  Lists files in a directory.
---

# pyvider_file_content (List Resource)

Lists files in a directory.

List resources are queried with `terraform query` from a `.tfquery.hcl` file
rather than planned or applied. The schema below is the `config` block of the
`list` block, not the schema of the managed resource being listed.

## Example Usage

{{ example("example") }}

{{ schema() }}

## Provider linting

`provide-io/pyvider:include-hidden-files` belongs to
`provide-io/pyvider:all` and `provide-io/pyvider:security`.

- **Trigger:** `include_hidden` is explicitly `true`.
- **Remediation:** Set `include_hidden` to `false`.
- **Suppress this rule:**

    ```shell
    PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:include-hidden-files' tofu validate
    ```
