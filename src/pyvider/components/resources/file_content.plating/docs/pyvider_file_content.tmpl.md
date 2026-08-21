---
page_title: "Resource: pyvider_file_content"
subcategory: "File Operations"
description: |-
  Manages the content of a file on the local filesystem
---

# pyvider_file_content (Resource)

The `pyvider_file_content` resource allows you to create, read, update, and delete files on the local filesystem. It automatically tracks content changes using SHA256 hashing and provides atomic write operations to ensure file integrity.

This resource enables declarative file management within your Terraform configurations, allowing you to create configuration files, render templates, and maintain files as part of your infrastructure-as-code workflow. With automatic content tracking and atomic writes, you can confidently manage files knowing that changes are properly detected and updates are performed safely.

## Capabilities

This resource enables you to:

- **Configuration files**: Create and manage application configuration files as code
- **Template rendering**: Generate files from dynamic content using Terraform expressions
- **Atomic file operations**: Ensure file writes are safe and complete, preventing partial writes
- **Content tracking**: Monitor file changes with automatic SHA256 hash calculation
- **Lifecycle management**: Full CRUD (Create, Read, Update, Delete) operations for files
- **Import existing files**: Bring existing files under Terraform management
- **Content validation**: Track when file content changes and trigger updates
- **Dependency management**: Coordinate file creation with other resources using depends_on

## Example Usage

{{ example("example") }}

## Examples

Explore these examples to see the resource in action:

- **[example.tf](examples/example.tf)** - Basic file creation
- **[basic.tf](examples/basic.tf)** - Simple configuration file management
- **[advanced.tf](examples/advanced.tf)** - Complex content generation patterns
- **[template.tf](examples/template.tf)** - Dynamic template rendering
- **[lifecycle.tf](examples/lifecycle.tf)** - Lifecycle management and dependencies

{{ schema() }}

## Computed Attributes

The resource provides the following computed attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `exists` | bool | Whether the file currently exists on the filesystem |
| `content_hash` | string | SHA256 hash of the file content for change detection |

## Import

Files can be imported into Terraform state using either the CLI or configuration-based import.

### CLI Import

```bash
terraform import pyvider_file_content.example /path/to/existing/file.txt
```

### Configuration Import (Terraform 1.5+)

```terraform
import {
  to = pyvider_file_content.example
  id = "/path/to/existing/file.txt"
}

resource "pyvider_file_content" "example" {
  filename = "/path/to/existing/file.txt"
  content  = "existing content will be read during import"
}
```

### Import Process

During import, the resource will:
1. Read the current file content from the specified path
2. Calculate the SHA256 hash of the content
3. Set the `exists` attribute to `true`
4. Store the content and hash in Terraform state

Note: The `content` attribute in your configuration should match the existing file content to avoid drift detection on the next apply.
