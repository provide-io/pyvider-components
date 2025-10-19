# Pyvider Components Examples Guide

This guide defines standards for writing example Terraform configurations for Pyvider components.

## Example Types

### Basic Examples (`basic.tf`)

**Purpose**: "Hello World" level demonstration of core functionality

**Characteristics**:
- **Length**: 30-80 lines maximum
- **Examples**: 2-4 simple demonstrations
- **Inline data**: < 10 lines per data structure
- **Resources**: 1-3 simple resources/data sources
- **Outputs**: 1-2 outputs showing key attributes
- **Complexity**: Minimal logic, no complex conditionals

**Good basic.tf example**:
```hcl
# Basic file creation
resource "pyvider_file_content" "readme" {
  filename = "/tmp/readme.txt"
  content  = "Hello from Pyvider!"
}

output "file_details" {
  value = {
    filename = pyvider_file_content.readme.filename
    exists   = pyvider_file_content.readme.exists
  }
}
```

**Bad basic.tf example**:
- 300+ lines
- Complex nested data structures
- Multiple file_content resources with 50+ line JSON configs
- Complex validation logic
- Advanced HCL features (for expressions, conditional logic)

### Advanced Examples (`advanced.tf`, `example.tf`)

**Purpose**: Production-like patterns and realistic use cases

**Characteristics**:
- **Length**: 100-200 lines maximum
- **Examples**: Multiple coordinated resources
- **Patterns**: Realistic workflows and orchestration
- **Data**: Can reference external files if needed
- **Complexity**: Moderate logic, practical error handling

**Appropriate for advanced.tf**:
- Multi-service orchestration
- Complex configuration management
- Integration with multiple systems
- Token rotation strategies
- Real-world API integrations

### Complex Examples (`complex.tf`, `api_processing.tf`, etc.)

**Purpose**: Edge cases, advanced patterns, comprehensive demonstrations

**Characteristics**:
- **Length**: 200-300 lines maximum (avoid exceeding)
- **Inline data**: Keep under 50 lines per block
- **Use cases**: Advanced JQ transformations, complex data processing
- **Patterns**: Sophisticated workflows, advanced features

**Guidelines**:
- If inline data exceeds 50 lines, consider extracting to a separate file
- Document why complexity is necessary
- Keep focused on specific advanced use case

## Data Structure Guidelines

### Inline JSON/YAML

**Basic examples**:
```hcl
# Good: Small, focused data (6 lines)
user = {
  name  = "Alice"
  email = "alice@example.com"
  age   = 30
}
```

**Advanced examples**:
```hcl
# Acceptable: Moderate data for realistic scenarios (20 lines)
config = {
  database = {
    host = "db.example.com"
    port = 5432
    ssl  = true
    connections = [
      { name = "primary", pool_size = 20 },
      { name = "replica", pool_size = 10 }
    ]
  }
  cache = {
    host = "redis.local"
    port = 6379
  }
}
```

**Complex examples**:
```hcl
# Maximum: Large data structures (40-50 lines)
# Beyond this, extract to external file or simplify
```

## Common Mistakes to Avoid

### 1. Over-engineered Basic Examples

❌ **Bad**:
- 330-line basic.tf with 4+ massive locals blocks
- Complex validation logic in basic examples
- Advanced HCL features (for expressions, regex, conditionals)
- Multiple file_content resources generating complex configs

✅ **Good**:
- 50-line basic.tf with 2-3 simple examples
- Direct demonstration of core functionality
- Minimal logic and straightforward usage

### 2. Massive Inline Data

❌ **Bad**:
```hcl
# 80-line log_entries array in basic.tf
log_entries = [
  { timestamp = "...", level = "INFO", message = "...", ... },
  { timestamp = "...", level = "DEBUG", message = "...", ... },
  # ... 30 more entries
]
```

✅ **Good**:
```hcl
# 5-line focused data
log_entries = [
  { timestamp = "2024-01-15T10:30:15Z", level = "INFO", message = "App started" },
  { timestamp = "2024-01-15T10:31:20Z", level = "ERROR", message = "Query failed" }
]
```

### 3. "Example" Files That Are Actually Advanced

❌ **Bad**: `example.tf` with 376 lines of complex patterns
✅ **Good**: Rename to `advanced.tf` and ensure it demonstrates realistic scenarios

## Example File Naming

- `basic.tf` - Always required, demonstrates core functionality
- `advanced.tf` - Optional, realistic production patterns
- `<use_case>.tf` - Specific scenario (e.g., `api_integration.tf`, `cicd.tf`)
- `complex.tf` - Advanced features, edge cases

## Testing Considerations

Examples should:
- ✅ Pass `terraform validate`
- ✅ Run successfully with `terraform plan/apply`
- ✅ Complete within reasonable time (< 30 seconds for basic.tf)
- ✅ Not rely on external services when possible
- ✅ Clean up resources (avoid /tmp pollution)

## Real-World Example Comparison

### Before (Bloated)

**functions/lens_jq/basic.tf - 330 lines**:
- 4 massive locals blocks
- user_data (25 lines), api_response (80 lines), app_config (40 lines), log_entries (40 lines)
- 4 file_content resources
- Complex JQ queries on large datasets

### After (Simplified)

**functions/lens_jq/basic.tf - 77 lines**:
- 4 focused locals blocks
- user_data (8 lines), colors (4 lines), config (10 lines), users (6 lines)
- 1 output
- Simple JQ queries demonstrating core functionality

**Improvement**: 76% reduction in lines, much more approachable for new users

## Summary

**Basic examples** = "How do I get started?"
**Advanced examples** = "How do I use this in production?"
**Complex examples** = "How do I handle edge cases?"

Keep basic examples truly basic, and users will have a better experience learning Pyvider.
