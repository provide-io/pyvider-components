# 🚀 Quick Bootstrap - Pyvider Components Documentation System

**Copy this into your next chat to get started quickly.**

---

## Current State (2025-10-27)

The documentation system uses **plating** to generate docs from templates + examples.

### 🔑 Core Rules

1. **NO inline code in templates** - Use `{{ example('name') }}` instead
2. **Basic examples ≤21 lines** - Keep them scannable for docs
3. **Complex examples in separate files** - advanced.tf, comprehensive.tf
4. **Templates reference examples** - Never hardcode terraform blocks

### 📁 Structure

```
.plating/
├── docs/
│   └── function_name.tmpl.md     # Uses {{ example('function_name') }}
└── examples/
    ├── function_name.tf           # 7-15 lines - shown in docs
    ├── basic.tf                   # 10-21 lines - overview
    ├── advanced.tf                # 27-157 lines - real-world patterns
    └── comprehensive.tf           # 73-113 lines - complete showcase
```

### 🎯 Template Jinja2 Functions

```jinja2
{{ schema() }}              # Renders schema table
{{ example('name') }}       # Includes examples/name.tf
{{ include('file') }}       # Static partial
{{ render('file') }}        # Dynamic partial
```

### 🚀 Regenerate Docs and Examples

```bash
# Build docs and executable examples
./scripts/build.sh

# Force rebuild (overwrite existing)
./scripts/build.sh --overwrite
```

**Output:**
- 36 documentation files in `docs/` directory
- 131 executable examples in `examples/` directory (organized by component type)

**Manual Method (Python API):**
```python
python3 << 'EOF'
from plating.plating import Plating
from plating.types import PlatingContext
import asyncio
context = PlatingContext(provider_name="pyvider")
api = Plating(context, "pyvider.components")
asyncio.run(api.plate())
EOF
```

### 📊 Current Examples

**Source Examples** (in `.plating/examples/`):
- **64 total example files**
- **2,588 total lines**
- **36 basic examples** (7-21 lines)
- **8 advanced examples** (27-157 lines)
- **8 comprehensive examples** (73-113 lines)

**Generated Executable Examples** (in `examples/`):
- **131 complete terraform configurations**
- Each with provider block, main.tf, and README.md
- Organized by component type (data_source/, resource/, function/)
- Cleaned to remove plating framework duplicates

### 🎯 Example Types

| File | Lines | Purpose | In Docs? |
|------|-------|---------|----------|
| `upper.tf` | 7 | Single function | ✅ Via `{{ example('upper') }}` |
| `basic.tf` | 16 | Multi-function | ⚠️ Optional |
| `advanced.tf` | 103 | Real-world | ❌ Referenced in text |
| `comprehensive.tf` | 113 | Complete showcase | ❌ Exploration |

### 🔧 Key Files

**Config:**
```toml
# pyproject.toml
[tool.plating]
provider_name = "pyvider"
```

**Templates:** All use `{{ example() }}` - zero inline code
- ✅ `src/*/docs/*.tmpl.md` (30+ files updated)

**Examples:** 63 files organized by complexity
- ✅ Individual: `upper.tf`, `lower.tf`, etc. (7-15 lines)
- ✅ Basic: Multi-function overview (10-21 lines)
- ✅ Advanced: Real-world patterns (27-157 lines)
- ✅ Comprehensive: Complete features (73-113 lines)

### 🐛 Gotchas

1. **CLI doesn't auto-discover** - Use Python API or `--provider-name pyvider`
2. **Package vs import name** - Use `pyvider.components` (not `pyvider-components`)
3. **Example must match** - `{{ example('upper') }}` needs `examples/upper.tf`
4. **Git auto-commits** - Don't rollback, don't mention Claude in commits
5. **Plating duplication bug** - Multiple functions in one `.plating` directory causes plating to generate ALL examples for ALL functions. Our build script cleans this up automatically.

### 📝 Common Tasks

**Build docs and examples:**
```bash
./scripts/build.sh            # Build if not exists
./scripts/build.sh --overwrite # Force rebuild
```

**Check example exists:**
```bash
ls src/pyvider/components/functions/*/examples/upper.tf
```

**Find inline code (should be empty):**
```bash
grep -r '```terraform' src --include="*.tmpl.md"
```

**Count example lines:**
```bash
find src -path "*/examples/*.tf" | xargs wc -l | sort -n
```

**List generated docs:**
```bash
ls docs/functions/ docs/data-sources/ docs/resources/
```

**Test an executable example:**
```bash
cd examples/function/upper/upper
terraform init
terraform plan
```

### 🎯 Next Steps Ideas

1. Add "See also: advanced.tf" to templates
2. Create missing advanced examples (file_info, etc.)
3. Test all `{{ example() }}` references resolve
4. Add EXAMPLES.md guides in each .plating/examples/

---

**Full details:** See `HANDOFF.md` for comprehensive documentation

**Last Updated:** 2025-10-27
