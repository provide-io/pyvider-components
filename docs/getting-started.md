# Getting Started with Pyvider Components

**Welcome to pyvider-components** - a learning and reference library containing 100+ example components for the [Pyvider framework](https://github.com/provide-io/pyvider).

## What You'll Learn

This guide will help you:

- Understand what pyvider-components is (and isn't)
- Navigate the 100+ component examples
- Study your first component from source to usage
- Explore components by category and complexity
- Build your own components using these as templates

**Time to complete:** 15-20 minutes

---

## Understanding Pyvider Components

### What is pyvider-components?

**Pyvider-components is a reference library for learning** - a collection of working examples that demonstrate how to build Terraform provider components using the Pyvider framework.

Think of it as:

- 📚 **A textbook** with 100+ working code examples
- 🔍 **Reference material** for building your own providers
- 🧪 **A test environment** for experimenting with patterns
- 🏗️ **Starting templates** you can adapt and customize

### What it is NOT

❌ **Not a production provider** - Don't use this directly in production Terraform
❌ **Not a package to import** - It's for studying and learning, not importing
❌ **Not feature-complete** - It's educational, showing patterns not exhaustive functionality

### The Three Types of Components

Pyvider components come in three flavors:

| Type | Purpose | Example |
|------|---------|---------|
| **Data Sources** | Read external data into Terraform | `pyvider_env_variables`, `pyvider_http_api` |
| **Resources** | Manage infrastructure/files | `pyvider_file_content`, `pyvider_local_directory` |
| **Functions** | Transform and compute values | `add()`, `upper()`, `lens_jq()` |

You'll explore all three types in this guide.

---

## Relationship to Production

```
┌─────────────────────────┐
│   pyvider (framework)   │  ← Core framework you'll use
└───────────┬─────────────┘
            │
            ├─────────────────────────────────────┐
            │                                     │
┌───────────▼─────────────┐     ┌───────────────▼──────────────┐
│   pyvider-components    │────▶│  terraform-provider-pyvider  │
│   (THIS LIBRARY)        │     │  (production provider)       │
│                         │     │                              │
│  ✓ Learn patterns here  │     │  ✓ Use in production        │
│  ✓ Study source code    │     │  ✓ Packaged & tested        │
│  ✓ Experiment locally   │     │  ✓ Ready to deploy          │
└─────────────────────────┘     └──────────────────────────────┘
```

**Key Point:** Study components here → Build your own provider → Or use [terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider) in production.

---

## Your First Component: The `length` Function

Let's learn by studying a real component from source code to usage.

### Step 1: Understand What It Does

The `length` function counts items in a collection (list or map).

**Terraform usage:**
```terraform
locals {
  items = ["apple", "banana", "cherry"]
  count = provider::pyvider::length(local.items)  # Returns: 3
}
```

### Step 2: Read the Source Code

**File:** `src/pyvider/components/functions/collection_functions.py`

```python
from pyvider.hub import register_function

@register_function(
    name="length",
    summary="Returns the number of items in a collection."
)
def length(collection: list | dict | None) -> int | None:
    """Calculate the length of a list or map."""
    if collection is None:
        return None
    return len(collection)
```

**Key Learning Points:**

1. **The decorator pattern** - `@register_function()` registers this with Pyvider
2. **Type hints** - Shows what inputs/outputs are expected
3. **Null handling** - Returns `None` for `None` inputs (Terraform pattern)
4. **Simple implementation** - Uses Python's built-in `len()`

### Step 3: Study the Examples

Navigate to: `examples/function/length/`

You'll find multiple example files showing progressively complex usage:

**`basic.tf`** - Simple usage:
```terraform
locals {
  items = ["apple", "banana", "cherry"]
  count = provider::pyvider::length(local.items)  # 3
}
```

**`comprehensive.tf`** - Advanced patterns:
```terraform
locals {
  # Works with lists
  list_length = provider::pyvider::length(["a", "b", "c"])  # 3

  # Works with maps
  map_length = provider::pyvider::length({
    host = "localhost"
    port = 8080
  })  # 2

  # Handles null
  null_length = provider::pyvider::length(null)  # null
}
```

### Step 4: Run It Locally (Optional)

If you want to test the function:

```bash
cd examples/function/length
terraform init
terraform plan
```

This uses the development version of pyvider-components to see the function in action.

---

## Exploring Components by Category

Now that you understand the learning process, explore components by category:

### 🔢 Start with Functions (Easiest)

Functions are the simplest components - they take inputs and return outputs with no side effects.

**Beginner-friendly functions:**

- **`add`** - Add two numbers (`src/pyvider/components/functions/numeric_functions.py:12`)
- **`upper`** - Convert string to uppercase
- **`length`** - Count items in a collection

**Why start here?** Functions are pure Python with no state management complexity.

**Study path:**
1. Read source code in `src/pyvider/components/functions/`
2. Check examples in `examples/function/{name}/`
3. Notice the `@register_function()` decorator pattern
4. See how type hints define the Terraform schema

### 📥 Progress to Data Sources (Intermediate)

Data sources read external information into Terraform.

**Learning progression:**

1. **`pyvider_env_variables`** - Read environment variables (simple read)
2. **`pyvider_file_info`** - Get file metadata (filesystem interaction)
3. **`pyvider_http_api`** - Make HTTP requests (external API)
4. **`pyvider_lens_jq`** - Transform data with JQ (complex processing)

**New concepts to learn:**

- Schema definition with `@data_source()` decorator
- The `Read` method pattern
- Attribute types (string, number, map, list)
- Computed vs required attributes

**Example source:** `src/pyvider/components/data_sources/env_variables.py`

### 📦 Master Resources (Advanced)

Resources manage infrastructure with full lifecycle (create, read, update, delete).

**Learning progression:**

1. **`pyvider_file_content`** - Manage file contents (CRUD operations)
2. **`pyvider_local_directory`** - Create directories (simpler lifecycle)
3. **`pyvider_timed_token`** - Time-based resource (state management)

**New concepts:**

- Full CRUD methods: `Create`, `Read`, `Update`, `Delete`
- State management and drift detection
- Resource IDs and identity
- Private state (internal tracking)

**Example source:** `src/pyvider/components/resources/file_content.py`

---

## Component Complexity Levels

As you explore, components roughly fall into these complexity tiers:

### Tier 1: Foundation Patterns
**Learn the basics** (1-2 hours)

- Simple functions: `add`, `upper`, `lower`
- Basic data sources: `pyvider_env_variables`
- Single-file resources: `pyvider_file_content`

### Tier 2: Real-World Patterns
**Production-ready patterns** (3-4 hours)

- Collection functions: `length`, `contains`, `lookup`
- External data: `pyvider_http_api`, `pyvider_file_info`
- Stateful resources: `pyvider_local_directory`

### Tier 3: Advanced Techniques
**Complex scenarios** (4-6 hours)

- Data transformation: `lens_jq`, nested processing
- State management: `pyvider_private_state_verifier`
- Error handling and validation patterns

---

## Understanding the Code Structure

All components follow consistent patterns:

### Directory Layout

```
pyvider-components/
├── src/pyvider/components/
│   ├── functions/          # Function implementations
│   │   ├── numeric_functions.py
│   │   ├── string_manipulation.py
│   │   └── collection_functions.py
│   ├── data_sources/       # Data source implementations
│   │   ├── env_variables.py
│   │   └── http_api.py
│   └── resources/          # Resource implementations
│       ├── file_content.py
│       └── local_directory.py
├── examples/               # Terraform usage examples
│   ├── function/{name}/    # One directory per function
│   ├── data_source/{name}/ # One directory per data source
│   └── resource/{name}/    # One directory per resource
└── docs/                   # Documentation you're reading
```

### The Decorator Pattern

All components use decorators for registration:

**Functions:**
```python
@register_function(name="add", summary="Adds two numbers")
def add(a: int, b: int) -> int:
    return a + b
```

**Data Sources:**
```python
@data_source(name="pyvider_env_variables")
class EnvVariables:
    def Read(self, ctx, req):
        # Implementation
```

**Resources:**
```python
@resource(name="pyvider_file_content")
class FileContent:
    def Create(self, ctx, req):
        # Create logic

    def Read(self, ctx, req):
        # Read logic

    def Update(self, ctx, req):
        # Update logic

    def Delete(self, ctx, req):
        # Delete logic
```

---

## Example File Naming Convention

When you explore `examples/`, you'll find consistent file naming:

| File | Purpose |
|------|---------|
| `basic.tf` | Simplest usage example |
| `advanced.tf` | More complex scenarios |
| `comprehensive.tf` | Full feature demonstration |
| `provider.tf` | Provider configuration |
| `{scenario}.tf` | Specific use case (e.g., `filtering.tf`) |

**Learning tip:** Always start with `basic.tf`, then progress to `advanced.tf` and `comprehensive.tf`.

---

## Learning Paths by Goal

### Goal: Build a Custom Terraform Provider

**Path:** Study the full component lifecycle

1. Start with functions to understand registration
2. Move to data sources to learn read patterns
3. Master resources for full CRUD operations
4. Review the Pyvider framework docs for architecture

**Time:** 2-3 weeks of study

### Goal: Understand Terraform Provider Internals

**Path:** Focus on protocol communication

1. Study how schemas are defined (type hints → Terraform types)
2. Examine request/response patterns in data sources
3. See state management in resources
4. Look at error handling across components

**Time:** 1 week of focused study

### Goal: Contribute to terraform-provider-pyvider

**Path:** Understand production patterns

1. Study existing production components
2. Review test components for patterns (`*_test` data sources/resources)
3. Understand the distinction between example and production code
4. Check terraform-provider-pyvider for packaging patterns

**Time:** 3-5 days

---

## Test Components

Several components are marked as **test-only** - they demonstrate specific patterns:

**Test Data Sources:**

- `pyvider_mixed_map_test` - Mixed type handling
- `pyvider_nested_resource_test` - Nested structures
- `pyvider_simple_map_test` - Simple map patterns
- `pyvider_structured_object_test` - Complex object schemas

**Test Resources:**

- `pyvider_private_state_verifier` - Private state management
- `pyvider_warning_example` - Warning/diagnostic patterns

**Why study these?** They isolate specific patterns you'll need in real providers.

---

## Common Questions

### Can I use these components in production?

**Short answer:** Use [terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider) instead.

**Long answer:** pyvider-components is for learning. The production provider packages these components with proper testing, versioning, and distribution. If you're building your own provider, use these as templates.

### Can I copy code from here?

**Yes!** That's the point. All code is Apache 2.0 licensed. Copy, adapt, and use in your own providers.

### How do I run the examples?

See the [How-To Guide: Studying Components](how-to/study-components.md) for detailed instructions on running examples locally.

### What if I find a bug?

Since this is example code, report it! But remember the goal is educational clarity, not production robustness.

### Where's the API documentation?

Reference docs for each component are in:

- [Functions Reference](functions/) - All 25 provider functions
- [Data Sources Reference](data-sources/) - 10 data sources
- [Resources Reference](resources/) - 7 resources

---

## Next Steps

Now that you understand the basics:

### 1. Pick a Learning Path

Choose based on your goal:

- **New to Pyvider?** → Start with functions
- **Building a provider?** → Study data sources, then resources
- **Contributing?** → Review test components and production patterns

### 2. Study Components in Depth

Follow this process for each component:

1. Read the source code in `src/`
2. Study examples in `examples/`
3. Run examples locally (optional)
4. Adapt patterns for your use case

**See:** [How-To Guide: Studying Components](how-to/study-components.md)

### 3. Explore the Pyvider Ecosystem

Pyvider-components is part of a larger ecosystem:

- **[Pyvider](https://github.com/provide-io/pyvider)** - Core framework
- **[terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider)** - Production provider
- **[provide-foundation](https://docs.provide.io)** - Python foundations

**See:** [Ecosystem Overview](https://docs.provide.io/provide-foundation/ecosystem/)

### 4. Build Your Own Component

Ready to try? Start with a simple function:

1. Copy the pattern from `src/pyvider/components/functions/numeric_functions.py`
2. Modify for your use case
3. Create example Terraform files
4. Test with terraform-provider-pyvider

---

## Additional Resources

**Documentation:**

- [How-To: Study Components](how-to/study-components.md) - Detailed study process
- [Functions Reference](functions/) - All provider functions
- [Data Sources Reference](data-sources/) - All data sources
- [Resources Reference](resources/) - All resources

**Source Code:**

- [GitHub Repository](https://github.com/provide-io/pyvider-components)
- [Pyvider Framework](https://github.com/provide-io/pyvider)

**Community:**

- [Ecosystem Overview](https://docs.provide.io/provide-foundation/ecosystem/)
- [Provider Documentation](https://github.com/provide-io/terraform-provider-pyvider)

---

**Happy Learning!** 🎓

You're now ready to explore 100+ working component examples. Start with a simple function and work your way up to complex resources.

Remember: This is reference material for learning. Take your time, study the patterns, and build your own amazing Terraform providers.
