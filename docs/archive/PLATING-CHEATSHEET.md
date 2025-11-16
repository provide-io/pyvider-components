# Plating Documentation Cheat Sheet

Quick reference for the pyvider-components documentation system.

---

## 🎯 Golden Rules

1. ❌ **NEVER** inline multi-line code in `.tmpl.md` files
2. ✅ **ALWAYS** use `{{ example('name') }}` to reference external `.tf` files
3. 📏 **Basic examples** ≤21 lines (shown in docs)
4. 📚 **Advanced examples** 27-157 lines (real-world patterns)
5. 📖 **Comprehensive examples** 73-113 lines (complete showcases)

---

## 📝 Template Syntax

```jinja2
# Component header and description
---
page_title: "Function: upper"
description: |-
  Convert a string to uppercase.
---

# upper (Function)

Brief description of what this does.

## Example Usage

{{ example('upper') }}         # Loads examples/upper.tf

## Signature

`upper(input_str: string) -> string`

## Schema

{{ schema() }}                 # Auto-generates schema table

## Parameters

- `input_str` (string) — Description

## Returns

Description of return value

## See Also

For more complex examples, see:
- `examples/advanced.tf` - Real-world patterns
- `examples/comprehensive.tf` - Complete showcase
```

---

## 🗂️ File Organization

```
component_name.plating/
├── docs/
│   ├── function_name.tmpl.md      # Template for each function
│   └── _partial.md                # Reusable snippets (optional)
└── examples/
    ├── function_name.tf           # Individual (7-15 lines)
    ├── basic.tf                   # Overview (10-21 lines)
    ├── advanced.tf                # Patterns (27-157 lines)
    └── comprehensive.tf           # Complete (73-113 lines)
```

---

## 🚀 Regenerate Documentation

### Method 1: Python API (Reliable)
```bash
python3 << 'EOF'
from plating.plating import Plating
from plating.types import PlatingContext
import asyncio

context = PlatingContext(provider_name="pyvider")
api = Plating(context, "pyvider.components")
result = asyncio.run(api.plate())

print(f"Generated {result.files_generated} files")
EOF
```

### Method 2: CLI (If configured)
```bash
plating plate --provider-name pyvider
```

**Output Location:** `docs/` directory
- `docs/functions/*.md` (25 files)
- `docs/data-sources/*.md` (5 files)
- `docs/resources/*.md` (5 files)
- `docs/index.md` (1 file)

---

## 🔍 Debugging Commands

### Verify Examples Exist
```bash
# List all example files
find src -path "*/examples/*.tf" -type f

# Check specific example
ls src/pyvider/components/functions/string_manipulation.plating/examples/upper.tf
```

### Check Templates
```bash
# Find all templates
find src -name "*.tmpl.md"

# Check for inline code (should return nothing)
grep -r '```terraform' src --include="*.tmpl.md"

# Verify example() usage
grep -r "{{ example(" src --include="*.tmpl.md"
```

### Inspect Generated Docs
```bash
# List generated files
ls -lh docs/functions/

# View generated doc
cat docs/functions/upper.md

# Count generated files
find docs -name "*.md" | wc -l
```

### Count Example Lines
```bash
# All examples sorted by size
find src -path "*/examples/*.tf" | xargs wc -l | sort -n

# Just basic examples
find src -path "*/examples/basic.tf" | xargs wc -l

# Just advanced examples
find src -path "*/examples/advanced.tf" | xargs wc -l
```

### Test Discovery
```bash
python3 << 'EOF'
from plating.discovery import PlatingDiscovery

discovery = PlatingDiscovery('pyvider.components')
bundles = discovery.discover_bundles()

print(f"Found {len(bundles)} bundles:")
for b in bundles[:10]:
    print(f"  - {b.name} ({b.component_type})")
    print(f"    Has template: {b.has_main_template()}")
    print(f"    Example count: {len(b.load_examples())}")
EOF
```

---

## 📏 Example Size Guidelines

| Type | Lines | Purpose | Usage |
|------|-------|---------|-------|
| **Individual** | 7-15 | Single function demo | `{{ example('upper') }}` |
| **Basic** | 10-21 | Multi-function overview | `{{ example('basic') }}` |
| **Advanced** | 27-157 | Real-world patterns | Referenced in text |
| **Comprehensive** | 73-113 | Complete feature set | Referenced in text |
| **Specialized** | 42-92 | Specific use case | Referenced in text |

---

## 🎨 Example Template Patterns

### Minimal Function Example (7-10 lines)
```hcl
# examples/upper.tf
locals {
  result = provider::pyvider::upper("hello")  # "HELLO"
}

output "upper_example" {
  value = local.result
}
```

### Basic Multi-Function (10-21 lines)
```hcl
# examples/basic.tf
locals {
  text = "Hello World"

  upper = provider::pyvider::upper(local.text)
  lower = provider::pyvider::lower(local.text)
}

output "basic_examples" {
  value = {
    upper = local.upper
    lower = local.lower
  }
}
```

### Advanced Pattern (27-157 lines)
```hcl
# examples/advanced.tf
# Real-world pattern: Email normalization pipeline
locals {
  emails = ["  JOHN@EXAMPLE.COM  ", "jane@Example.COM"]

  normalized = [
    for email in local.emails :
    provider::pyvider::lower(
      provider::pyvider::replace(email, " ", "")
    )
  ]
}

# More complex patterns...
```

---

## 🛠️ Creating New Examples

### 1. Create Individual Function Example
```bash
# File: src/pyvider/components/functions/my_function.plating/examples/my_function.tf
cat > src/.../my_function.tf << 'EOF'
locals {
  result = provider::pyvider::my_function("input")
}

output "my_function_example" {
  value = local.result
}
EOF
```

### 2. Create Template
```bash
# File: src/pyvider/components/functions/my_function.plating/docs/my_function.tmpl.md
cat > src/.../my_function.tmpl.md << 'EOF'
---
page_title: "Function: my_function"
description: |-
  Short description here.
---

# my_function (Function)

Longer description here.

## Example Usage

{{ example('my_function') }}

## Signature

`my_function(input: string) -> string`

## Parameters

- `input` (string, required) — Description

## Returns

Description of return value
EOF
```

### 3. Test
```bash
# Regenerate docs
python3 -c "from plating.plating import Plating; ..."

# Verify output
cat docs/functions/my_function.md
```

---

## 🐛 Common Issues

### Example Not Rendering

**Problem:** `{{ example('upper') }}` shows empty or error

**Check:**
```bash
# 1. File exists?
ls src/*/examples/upper.tf

# 2. File has content?
cat src/*/examples/upper.tf

# 3. Template correct?
grep "example('upper')" src/*/docs/*.tmpl.md
```

### Template Not Found

**Problem:** Component not generating docs

**Check:**
```bash
# 1. .plating directory exists?
find src -name "*.plating" -type d

# 2. Has docs/ directory?
find src -path "*/.plating/docs" -type d

# 3. Has .tmpl.md files?
find src -name "*.tmpl.md"

# 4. Discovery finds it?
python3 -c "from plating.discovery import PlatingDiscovery; ..."
```

### Inline Code in Template

**Problem:** Found inline terraform blocks

**Fix:**
1. Extract code to `examples/name.tf`
2. Replace inline code with `{{ example('name') }}`
3. Verify: `grep -r '```terraform' src --include="*.tmpl.md"`

---

## 📦 Project Config

```toml
# pyproject.toml
[tool.plating]
provider_name = "pyvider"
```

---

## 🔗 Quick Links

- **Full Handoff:** `HANDOFF.md`
- **Bootstrap Guide:** `BOOTSTRAP.md`
- **Plating Source:** `/REDACTED_ABS_PATH`
- **Generated Docs:** `docs/`

---

**Last Updated:** 2025-10-27
