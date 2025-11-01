# How to Study Components

This guide provides a practical, step-by-step process for studying pyvider-components as reference material for learning provider development patterns.

## Prerequisites

- Basic Python knowledge
- Basic Terraform knowledge
- Familiarity with the [Getting Started guide](../getting-started.md)

---

## The Five-Step Study Process

Follow this process for any component you want to learn from:

```
1. Identify     → Find a component to study
2. Source       → Read the implementation code
3. Schema       → Understand the Terraform interface
4. Examples     → Study usage patterns
5. Adapt        → Apply to your own work
```

---

## Step 1: Identify a Component to Study

### Choose by Learning Goal

**Learning functions?** Start with numeric functions:

```bash
cd src/pyvider/components/functions
ls -l numeric_functions.py string_manipulation.py collection_functions.py
```

**Learning data sources?** Start simple:

```bash
cd src/pyvider/components/data_sources
ls -l env_variables.py file_info.py
```

**Learning resources?** Pick by complexity:

```bash
cd src/pyvider/components/resources
ls -l file_content.py local_directory.py
```

### Browse Available Components

**List all functions:**
```bash
grep -r "@register_function" src/pyvider/components/functions/
```

**List all data sources:**
```bash
grep -r "@data_source" src/pyvider/components/data_sources/
```

**List all resources:**
```bash
grep -r "@resource" src/pyvider/components/resources/
```

---

## Step 2: Read the Source Code

### Start with the Decorator

Every component begins with a registration decorator. Find it first.

**Example: The `upper` function**

```python
# File: src/pyvider/components/functions/string_manipulation.py

@register_function(
    name="upper",
    summary="Converts a string to uppercase."
)
def upper(s: str | None) -> str | None:
    """Convert string to uppercase."""
    if s is None:
        return None
    return s.upper()
```

### Identify Key Elements

Look for these in every component:

| Element | What to Notice |
|---------|----------------|
| **Decorator** | `@register_function`, `@data_source`, or `@resource` |
| **Name** | How it's called in Terraform |
| **Parameters** | Type hints define Terraform schema |
| **Return type** | What Terraform receives back |
| **Null handling** | How `None` values are managed |
| **Error handling** | `FunctionError`, `raise`, validation |

### Understand Type Mapping

Python types map to Terraform types:

```python
# Python Type         → Terraform Type
str                  → string
int                  → number
float                → number
bool                 → bool
list[str]            → list(string)
dict[str, any]       → map(any)
Type | None          → optional attribute
```

**Example:**
```python
def add(a: int | float | None, b: int | float | None) -> int | float | None:
    # Terraform sees: function that accepts two optional numbers, returns optional number
```

---

## Step 3: Understand the Terraform Interface

### For Functions

Functions have simple signatures:

```python
@register_function(
    name="length",                            # Terraform: provider::pyvider::length()
    summary="Returns the number of items.",   # Help text
    param_descriptions={                      # Parameter docs
        "collection": "The collection to measure"
    }
)
def length(collection: list | dict | None) -> int | None:
    # Implementation
```

**Terraform usage:**
```terraform
locals {
  count = provider::pyvider::length(["a", "b", "c"])  # 3
}
```

### For Data Sources

Data sources define schemas and a `Read` method:

```python
@data_source(name="pyvider_env_variables")
class EnvVariables:
    # Schema defined via type hints or explicit schema
    keys: list[str]          # Input: required
    values: dict[str, str]   # Output: computed

    def Read(self, ctx, req):
        # Read external data
        # Populate values
        return response
```

**Key concepts:**

- **Input attributes** - What user provides in Terraform
- **Computed attributes** - What provider returns after reading
- **The `Read` method** - Where data fetching happens

### For Resources

Resources have full CRUD lifecycle:

```python
@resource(name="pyvider_file_content")
class FileContent:
    # Schema
    filename: str     # Required
    content: str      # Required
    content_hash: str # Computed

    def Create(self, ctx, req):
        # Create the resource
        return response

    def Read(self, ctx, req):
        # Read current state
        return response

    def Update(self, ctx, req):
        # Update the resource
        return response

    def Delete(self, ctx, req):
        # Delete the resource
        return response
```

**Key concepts:**

- **CRUD methods** - Create, Read, Update, Delete
- **State management** - Tracking resource state
- **ID assignment** - Unique identifier for each resource
- **Drift detection** - `Read` checks if external state changed

---

## Step 4: Study Usage Examples

### Navigate to Examples Directory

Every component has an `examples/` directory:

```
examples/
├── function/{component_name}/
├── data_source/{component_name}/
└── resource/{component_name}/
```

### Example File Patterns

Components typically have:

| File | Content |
|------|---------|
| `provider.tf` | Provider configuration |
| `basic.tf` | Simplest usage |
| `advanced.tf` | Complex scenarios |
| `comprehensive.tf` | Full feature showcase |
| `{scenario}.tf` | Specific use cases |

### Study Progression

**Always follow this order:**

1. **`basic.tf`** - Understand fundamental usage
2. **`advanced.tf`** - See additional patterns
3. **`comprehensive.tf`** - Full feature exploration
4. **Scenario files** - Specific use cases

**Example: Studying `pyvider_http_api`**

```bash
cd examples/data_source/http_api/

# Start simple
cat basic.tf

# Progress to advanced
cat advanced.tf
cat comprehensive.tf

# Explore scenarios
cat error_handling.tf
cat authentication.tf
```

### Run Examples Locally (Optional)

To see components in action:

```bash
# Navigate to example directory
cd examples/function/add/

# Initialize Terraform
terraform init

# See the plan
terraform plan

# Apply (if safe)
terraform apply
```

**Note:** Examples use the local development provider. Make sure you've set up the development environment:

```bash
# From repository root
uv sync --all-groups
source .venv/bin/activate
```

---

## Step 5: Adapt Patterns to Your Work

### Extract Reusable Patterns

As you study, note these patterns:

#### Pattern: Null-Safe Operations

```python
def safe_operation(value: str | None) -> str | None:
    if value is None:
        return None
    return value.upper()  # Your operation here
```

**When to use:** Functions that should gracefully handle null values.

#### Pattern: Error Handling

```python
from pyvider.exceptions import FunctionError

def validated_operation(value: int) -> int:
    if value < 0:
        raise FunctionError("Value must be non-negative")
    return value * 2
```

**When to use:** Input validation and error reporting.

#### Pattern: Type Coercion

```python
def flexible_input(number: int | float | None) -> int | None:
    if number is None:
        return None
    result = calculate(number)
    # Return int if whole number, float otherwise
    return int(result) if isinstance(result, float) and result.is_integer() else result
```

**When to use:** Making Terraform outputs cleaner.

#### Pattern: Schema with Computed Values

```python
@data_source(name="my_data_source")
class MyDataSource:
    # Required inputs
    input_param: str

    # Computed outputs
    result: str
    metadata: dict[str, str]

    def Read(self, ctx, req):
        # Fetch data based on input_param
        # Populate result and metadata
        return response
```

**When to use:** Data sources that fetch external information.

#### Pattern: State Management

```python
@resource(name="my_resource")
class MyResource:
    def Create(self, ctx, req):
        # Create resource
        # Set ID
        response.id = generate_id()
        return response

    def Read(self, ctx, req):
        # Check if resource still exists
        # Update state if changed
        return response
```

**When to use:** Resources that manage external state.

### Copy and Modify

The code is Apache 2.0 licensed - copy freely:

```bash
# Copy a function as starting point
cp src/pyvider/components/functions/string_manipulation.py \
   ~/my-provider/src/my_provider/functions/custom_strings.py

# Modify for your needs
# - Change decorator name
# - Update implementation
# - Adjust type hints
```

### Create Your Own Component

Use this template workflow:

1. **Choose a similar component** as starting point
2. **Copy the file** to your provider project
3. **Rename** the decorator and function/class
4. **Modify implementation** for your use case
5. **Create examples** in your project
6. **Test** with terraform-provider-pyvider or your own provider

---

## Understanding Component Architecture

### Functions Layer

```
Your Terraform Config
        ↓
provider::pyvider::function_name(args)
        ↓
@register_function decorator
        ↓
Your Python function
        ↓
Return value → Terraform
```

### Data Sources Layer

```
Your Terraform Config
        ↓
data "pyvider_source" "name" { }
        ↓
@data_source decorator
        ↓
Read() method called
        ↓
Computed attributes populated
        ↓
State returned to Terraform
```

### Resources Layer

```
Your Terraform Config (resource block)
        ↓
terraform apply
        ↓
@resource decorator
        ↓
Create/Read/Update/Delete methods
        ↓
State management
        ↓
Resource ID and state → Terraform
```

---

## Common Study Patterns

### Pattern: Progressive Complexity

Study components in this order within each type:

**Functions:**
1. `add` - Basic arithmetic
2. `upper` - String manipulation
3. `length` - Collection operations
4. `lens_jq` - Complex transformations

**Data Sources:**
1. `pyvider_env_variables` - Simple read
2. `pyvider_file_info` - Filesystem interaction
3. `pyvider_http_api` - External API
4. `pyvider_nested_data_processor` - Complex structures

**Resources:**
1. `pyvider_file_content` - Basic CRUD
2. `pyvider_local_directory` - Simpler lifecycle
3. `pyvider_timed_token` - Time-based logic

### Pattern: Compare Similar Components

Compare components that solve similar problems:

**String manipulation:**
```bash
# Study these together
src/pyvider/components/functions/string_manipulation.py
# Functions: upper, lower, split, join, replace
```

**Numeric operations:**
```bash
# Study these together
src/pyvider/components/functions/numeric_functions.py
# Functions: add, subtract, multiply, divide, sum, min, max
```

**Data transformation:**
```bash
# Compare these approaches
data_sources/lens_jq.py          # JQ-based transformation
data_sources/nested_data_processor.py  # Nested structure handling
```

### Pattern: Trace Dependencies

Follow imports to understand framework integration:

```python
from pyvider.hub import register_function        # Function registration
from pyvider.exceptions import FunctionError     # Error types
from pyvider_rpcplugin import DataSource         # Base classes
from pyvider_rpcplugin import Resource           # Resource base
```

**Trace these to understand:**

- How registration works
- What base classes provide
- Error handling patterns
- Framework conventions

---

## Testing Your Understanding

### Can You Answer These?

After studying a component, verify your understanding:

**For Functions:**
- [ ] What does the function do?
- [ ] What are the input types?
- [ ] What does it return?
- [ ] How does it handle null values?
- [ ] How is it called in Terraform?

**For Data Sources:**
- [ ] What external data does it read?
- [ ] What are the required inputs?
- [ ] What attributes are computed?
- [ ] How does the `Read` method work?
- [ ] What errors can it produce?

**For Resources:**
- [ ] What does the resource manage?
- [ ] What's the create/update/delete logic?
- [ ] How is the resource ID assigned?
- [ ] How does it detect drift?
- [ ] What happens on errors?

### Build a Mental Model

Create your own diagram of how the component works:

```
Input → Validation → Processing → Output
  ↓         ↓            ↓          ↓
Type?    Rules?      Logic?    Format?
```

---

## Advanced Study Techniques

### Technique: Code Annotation

As you read source code, annotate it:

```python
@register_function(name="add", summary="Adds two numbers.")
# ^ Decorator registers this function with Pyvider
def add(a: int | float | None, b: int | float | None) -> int | float | None:
    # ^ Type hints define Terraform schema: two optional numbers → optional number
    if a is None or b is None:
        # ^ Terraform null handling - null inputs = null output
        return None
    try:
        result = a + b
        # ^ Core logic - simple Python addition
        return (
            int(result) if isinstance(result, float) and result.is_integer() else result
        )
        # ^ Type coercion - return int when possible for cleaner Terraform output
    except TypeError as e:
        raise FunctionError(f"Invalid argument types for addition: {e}") from e
        # ^ Error handling - convert Python errors to Terraform diagnostics
```

### Technique: Example Matrix

Create a matrix of component capabilities:

| Component | Null Safe | Error Handling | Complex Types | External I/O |
|-----------|-----------|----------------|---------------|--------------|
| `add` | ✓ | ✓ | ✗ | ✗ |
| `lens_jq` | ✓ | ✓ | ✓ | ✗ |
| `http_api` | ✓ | ✓ | ✓ | ✓ |

### Technique: Pattern Extraction

Build a personal pattern library:

```markdown
# My Pattern Library

## Pattern: Variadic Arguments
Source: src/pyvider/components/functions/numeric_functions.py:100
Use case: Optional parameters in Terraform functions

## Pattern: Private State
Source: src/pyvider/components/resources/private_state_verifier.py
Use case: Internal resource tracking
```

---

## Troubleshooting Study Issues

### Issue: Can't Find the Source Code

**Problem:** Looking for component implementation
**Solution:** Use grep to locate:

```bash
grep -r "register_function.*add" src/
grep -r "data_source.*env_variables" src/
grep -r "resource.*file_content" src/
```

### Issue: Example Won't Run

**Problem:** `terraform init` fails
**Solution:** Check provider installation:

```bash
# Ensure development environment is set up
cd /path/to/pyvider-components
uv sync --all-groups
source .venv/bin/activate

# Ensure provider is built (if using locally)
# See terraform-provider-pyvider docs
```

### Issue: Don't Understand the Pattern

**Problem:** Code is confusing
**Solution:** Study progression:

1. Start with simpler component in same category
2. Read framework documentation (pyvider, pyvider-rpcplugin)
3. Compare with similar components
4. Check test components for isolated patterns

---

## Next Steps

### Keep Learning

- **Study different component types** - Build complete mental model
- **Compare implementations** - See multiple approaches to similar problems
- **Read framework docs** - Understand the underlying Pyvider architecture
- **Build your own** - Apply patterns in your own provider

### Contribute

Once you understand the patterns:

- **Report issues** - Found a bug or unclear example? Report it
- **Suggest improvements** - Better patterns? Share them
- **Build on these** - Create your own provider using these patterns

### Resources

- [Getting Started Guide](../getting-started.md) - Introduction to pyvider-components
- [Pyvider Framework](https://github.com/provide-io/pyvider) - Core framework documentation
- [Production Provider](https://github.com/provide-io/terraform-provider-pyvider) - See production packaging
- [Ecosystem Overview](https://docs.provide.io/provide-foundation/ecosystem/) - How projects relate

---

**Happy Studying!** 🔍

This process will help you systematically learn from 100+ component examples. Take your time, study thoroughly, and apply these patterns to build amazing Terraform providers.
