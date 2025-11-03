# Global Partials for Pyvider Components

This directory contains reusable content blocks that can be injected into component documentation templates during the build process.

## Overview

Use global partials to maintain consistent messages, warnings, and links across all documentation. These are manually included where needed, giving template authors full control over placement.

## Available Partials

### `_global_header.md`
Inserted after the main title/heading. Typically contains status messages, warnings, or important notices that should appear early in the documentation.

**Usage:**
```markdown
# pyvider_example (Resource)

{{ global('global_header') }}

Rest of documentation...
```

**Current Content:**
- POC (Proof of Concept) status warning

### `_global_footer.md`
Inserted at the end of documentation. Typically contains common links, support information, or related resources.

**Usage:**
```markdown
...documentation content...

{{ global('global_footer') }}
```

**Current Content:**
- (Empty, ready for additional content like support links, related resources, etc.)

## Using Global Partials in Templates

In any component template (`*.tmpl.md`), reference global partials using:

```markdown
{{ global('global_header') }}
{{ global('global_footer') }}
```

### Typical Template Structure

```markdown
---
page_title: "Resource: pyvider_example"
subcategory: "Category"
---

# pyvider_example (Resource)

{{ global('global_header') }}

Brief description of the resource.

## Example Usage

{{ example("example") }}

## Argument Reference

{{ schema() }}

{{ global('global_footer') }}
```

### What Goes Where

**Header (after title):**
- POC status warnings
- Experimental feature notices
- Important status updates
- Breaking change notices

**Footer (at end):**
- Common support links
- Related documentation
- Community resources
- Import instructions (sometimes)

## Updating Global Content

1. Edit `_global_header.md` or `_global_footer.md`
2. Run the build: `make docs`
3. Changes automatically apply to all using templates

## Guidelines

- **Keep it concise:** Blocks should be brief and focused
- **Use standard markdown:** Must work in both MkDocs and Terraform Registry
- **No special syntax:** Avoid MkDocs-specific extensions or custom HTML
- **Use blockquotes:** Recommended format for notices: `> **emoji** Message`
- **Unicode emojis:** Preferred over emoji shortcodes (`:warning:`, etc.)

## Implementation Details

- Partials are injected during pre-processing before plating generates documentation
- Injection is marked with HTML comments showing the source
- Final output contains plain markdown (no special syntax)
- Process is idempotent: running build multiple times produces same result
- Use `make inject-partials-dry-run` to preview what would be injected
