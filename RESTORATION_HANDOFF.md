# Documentation Restoration Handoff Document

## Executive Summary

This document provides a detailed specification for restoring comprehensive documentation to 34 `.tmpl.md` files that were simplified between commit `dce87e4838f4f0bebdfb3cfe83101173bf37f92c` (last good version) and current HEAD.

**Restoration Philosophy**: Pyvider is a showcase project demonstrating Terraform provider framework capabilities. Documentation should focus on **what components can do**, not production troubleshooting or anti-patterns.

---

## Source and Target

- **Source Commit**: `dce87e4838f4f0bebdfb3cfe83101173bf37f92c`
- **Target**: Current HEAD
- **Files Affected**: 34 `.tmpl.md` files across data_sources, resources, and functions

---

## Content Restoration Strategy

### What to RESTORE from Old Documentation

1. **Comprehensive Descriptions** (2-4 paragraphs)
   - Explain what the component does
   - Highlight key capabilities
   - Explain the value proposition
   - Focus on feature showcase, not limitations

2. **Use Case / Capabilities Lists**
   - Extract the positive bullet points from "When to Use This" sections
   - Reframe as "Capabilities" or "Use Cases"
   - Remove anti-pattern content
   - Show what the component **can do**

3. **Cross-References to Examples**
   - Link to existing example files in the examples/ directory
   - Reference: `basic.tf`, `advanced.tf`, `comprehensive.tf`
   - For functions with granular examples, reference per-function `.tf` files
   - Add brief descriptions of what each example demonstrates

4. **Informational Reference Tables**
   - Permission format tables (for file operations)
   - Unit conversion charts (for functions like format_size)
   - Other reference information that showcases capabilities

5. **Related Components Section**
   - Cross-reference related pyvider components
   - Show how components work together
   - Demonstrate the breadth of the framework

### What to EXCLUDE (Do Not Restore)

1. **"Anti-patterns" sections** - These describe what NOT to do (constraints/limitations)
2. **"Common Issues & Solutions" sections** - Production troubleshooting content
3. **"Best Practices" sections** - Operational guidance for production users
4. **Error handling examples** - Production-oriented content
5. **Troubleshooting commands** - Not relevant for showcase

### What to KEEP from New Template

1. **Template structure**:
   - Page title and subcategory metadata
   - `{{ example("example") }}` placeholders for dynamic examples
   - `{{ schema() }}` placeholders for auto-generated schemas
   - Basic import instructions

2. **Dynamic content generation approach**
   - Keep Jinja2 template variables
   - Keep schema auto-generation
   - Keep example file inclusion mechanism

---

## File-by-File Restoration Specification

### Data Sources (6 files)

#### 1. `data_sources/env_variables.plating/docs/pyvider_env_variables.tmpl.md`

**Current State**: 403 bytes (minimal template)
**Old State**: 4,743 bytes (comprehensive docs)
**Content Reduction**: 91.5%

**What to Restore**:
- Comprehensive description explaining environment variable data source capabilities
- Capabilities list showing use cases:
  - Configuration management
  - Secret injection
  - Environment-aware deployment
  - Build-time configuration
  - Feature flagging
- Cross-references to examples:
  - `examples/basic.tf` - Simple environment variable reads
  - `examples/advanced.tf` - Complex environment configurations
  - `examples/comprehensive.tf` - Full-featured example
- Related components: Link to other configuration-related components

**Skip**:
- Anti-patterns section
- Common issues/troubleshooting

---

#### 2. `data_sources/file_info.plating/docs/pyvider_file_info.tmpl.md`

**Current State**: 388 bytes (minimal template)
**Old State**: 5,280 bytes (comprehensive docs)
**Content Reduction**: 92.7%

**What to Restore**:
- Comprehensive description of file information gathering capabilities
- Capabilities list:
  - Conditional resource creation based on file existence
  - File system validation
  - Deployment checks
  - Backup verification
  - Permission auditing
- Permission format reference table (from old docs)
- Cross-references to examples:
  - `examples/basic.tf` - Basic file info queries
  - `examples/advanced.tf` - Advanced file system inspection
  - `examples/comprehensive.tf` - Complete file info example
- Related components: `pyvider_file_content`, `pyvider_local_directory`

**Skip**:
- Anti-patterns
- Common issues (symlink handling, path errors)

---

#### 3. `data_sources/http_api.plating/docs/pyvider_http_api.tmpl.md`

**Current State**: 389 bytes (minimal template)
**Old State**: 7,891 bytes (comprehensive docs)
**Content Reduction**: 95.1%

**What to Restore**:
- Comprehensive description of HTTP API data source capabilities
- Capabilities list:
  - RESTful API integration
  - Dynamic data fetching
  - Authentication support (headers, tokens)
  - Response transformation with jq
  - Multi-API orchestration
- Cross-references to examples:
  - `examples/basic.tf` - Simple GET requests
  - `examples/advanced.tf` - Authentication and headers
  - `examples/comprehensive.tf` - Full API integration
- Related components: `pyvider_lens_jq` for response transformation

**Skip**:
- Anti-patterns
- Error handling troubleshooting

---

#### 4. `data_sources/lens_jq.plating/docs/pyvider_lens_jq.tmpl.md`

**Current State**: 391 bytes (minimal template)
**Old State**: 8,234 bytes (comprehensive docs)
**Content Reduction**: 95.3%

**What to Restore**:
- Comprehensive description of lens transformation capabilities
- Capabilities list:
  - Complex data structure transformation
  - JSON querying with jq syntax
  - Data extraction and filtering
  - Nested data manipulation
  - API response processing
- jq syntax reference examples (from old docs)
- Cross-references to examples:
  - `examples/basic.tf` - Simple jq transformations
  - `examples/advanced.tf` - Complex queries
  - `examples/lens_jq.tf` - Lens-specific examples
  - `examples/comprehensive.tf` - Full transformation pipeline
- Related components: `pyvider_http_api` for API integration

**Skip**:
- Anti-patterns
- jq troubleshooting

---

#### 5. `data_sources/provider_config_reader.plating/docs/pyvider_provider_config_reader.tmpl.md`

**Current State**: 418 bytes (minimal template)
**Old State**: 4,892 bytes (comprehensive docs)
**Content Reduction**: 91.5%

**What to Restore**:
- Comprehensive description of provider configuration reading capabilities
- Capabilities list:
  - Provider configuration inspection
  - Multi-provider setup validation
  - Configuration discovery
  - Dynamic provider configuration
- Cross-references to examples:
  - `examples/basic.tf` - Reading provider config
  - `examples/advanced.tf` - Multi-provider scenarios
  - `examples/comprehensive.tf` - Full config inspection
- Related components: Other provider management components

**Skip**:
- Anti-patterns
- Configuration error troubleshooting

---

#### 6. `data_sources/terraform_data_reader.plating/docs/pyvider_terraform_data_reader.tmpl.md`

**Current State**: 414 bytes (minimal template)
**Old State**: 5,123 bytes (comprehensive docs)
**Content Reduction**: 91.9%

**What to Restore**:
- Comprehensive description of Terraform data reading capabilities
- Capabilities list:
  - State file inspection
  - Resource data access
  - Cross-stack data sharing
  - Dynamic configuration based on existing resources
- Cross-references to examples:
  - `examples/basic.tf` - Simple data reads
  - `examples/advanced.tf` - Cross-stack scenarios
  - `examples/comprehensive.tf` - Full data reader example
- Related components: `pyvider_provider_config_reader`

**Skip**:
- Anti-patterns
- State file troubleshooting

---

### Resources (7 files)

#### 1. `resources/file_content.plating/docs/pyvider_file_content.tmpl.md`

**Current State**: 398 bytes (minimal template)
**Old State**: 6,847 bytes (comprehensive docs)
**Content Reduction**: 94.2%

**What to Restore**:
- Comprehensive description of file content management capabilities
- Capabilities list:
  - Configuration file creation and management
  - Template rendering
  - Atomic file operations
  - Content tracking with automatic hashing
  - Dynamic file generation
- Cross-references to examples:
  - `examples/example.tf` - Basic file creation
  - `examples/advanced.tf` - Advanced file management
  - `examples/lifecycle.tf` - Lifecycle management examples
- Related components: `pyvider_local_directory`, `pyvider_file_info`

**Skip**:
- Anti-patterns (large binary files, temporary files)
- Permission error troubleshooting

---

#### 2. `resources/local_directory.plating/docs/pyvider_local_directory.tmpl.md`

**Current State**: 399 bytes (minimal template)
**Old State**: 5,280 bytes (comprehensive docs)
**Content Reduction**: 92.4%

**What to Restore**:
- Comprehensive description of directory management capabilities
- Capabilities list:
  - Project structure creation
  - Dynamic directory hierarchies
  - Permission management
  - Workspace setup
  - File count monitoring
- Permission format reference table (from old docs)
- Cross-references to examples:
  - `examples/example.tf` - Basic directory creation
  - `examples/basic.tf` - Simple directory management
  - `examples/project_structure.tf` - Project scaffolding
  - `examples/permissions.tf` - Permission examples
- Related components: `pyvider_file_content`, `pyvider_file_info`

**Skip**:
- Anti-patterns
- Permission error troubleshooting

---

#### 3. `resources/private_state_verifier.plating/docs/pyvider_private_state_verifier.tmpl.md`

**Current State**: 428 bytes (minimal template)
**Old State**: 13,476 bytes (comprehensive docs)
**Content Reduction**: 96.8%

**What to Restore**:
- Comprehensive description of private state encryption/verification capabilities
- Capabilities list:
  - Encrypted state management
  - State verification and validation
  - Compliance testing
  - Security verification
  - Tamper detection
  - Secret management
- Encryption mechanism explanation (showcase the security features)
- Cross-references to examples:
  - `examples/example.tf` - Basic private state usage
  - `examples/basic.tf` - Simple encryption
  - `examples/comprehensive.tf` - Full encryption/verification
  - `examples/provider_alias.tf` - Multi-provider scenarios
- Related components: Other security-related components

**Skip**:
- Anti-patterns
- Encryption key troubleshooting

---

#### 4. `resources/provider_config_reader.plating/docs/pyvider_provider_config.tmpl.md`

**Current State**: 410 bytes (minimal template)
**Old State**: 5,234 bytes (comprehensive docs)
**Content Reduction**: 92.2%

**What to Restore**:
- Comprehensive description of provider configuration resource capabilities
- Capabilities list:
  - Provider configuration management
  - Dynamic provider setup
  - Configuration validation
  - Multi-provider orchestration
- Cross-references to examples:
  - `examples/example.tf` - Basic provider config
  - Available example files
- Related components: `pyvider_provider_config_reader` (data source)

**Skip**:
- Anti-patterns
- Configuration error troubleshooting

---

#### 5. `resources/simple_resource.plating/docs/pyvider_simple_resource.tmpl.md`

**Current State**: 397 bytes (minimal template)
**Old State**: 4,123 bytes (comprehensive docs)
**Content Reduction**: 90.4%

**What to Restore**:
- Comprehensive description of simple resource capabilities (example/template resource)
- Capabilities list:
  - Basic CRUD operations demonstration
  - Resource lifecycle management
  - State management example
  - Template for custom resources
- Cross-references to examples:
  - `examples/example.tf` - Basic usage
  - Available example files
- Related components: Other resource examples

**Skip**:
- Anti-patterns
- Troubleshooting

---

#### 6. `resources/timed_token.plating/docs/pyvider_timed_token.tmpl.md`

**Current State**: 395 bytes (minimal template)
**Old State**: 7,892 bytes (comprehensive docs)
**Content Reduction**: 95.0%

**What to Restore**:
- Comprehensive description of timed token capabilities
- Capabilities list:
  - Time-based token generation
  - Token expiration management
  - API authentication token creation
  - Rotating credentials
  - Webhook authentication
  - Multi-service token orchestration
- Token lifecycle explanation
- Cross-references to examples:
  - `examples/example.tf` - Basic token creation
  - `examples/basic.tf` - Simple token usage
  - `examples/comprehensive.tf` - Full token lifecycle
- Related components: Authentication-related components

**Skip**:
- Anti-patterns
- Token expiration troubleshooting

---

#### 7. `resources/warning_example.plating/docs/pyvider_warning_example.tmpl.md`

**Current State**: 393 bytes (minimal template)
**Old State**: 12,192 bytes (comprehensive docs)
**Content Reduction**: 96.8%

**What to Restore**:
- Comprehensive description of warning/diagnostic capabilities
- Capabilities list:
  - Terraform warning generation
  - Diagnostic message demonstration
  - Warning severity levels
  - User feedback mechanisms
  - Example resource for testing warnings
- Cross-references to examples:
  - `examples/example.tf` - Warning examples
  - Available example files
- Related components: Other diagnostic/testing components

**Skip**:
- Anti-patterns
- Troubleshooting

---

### Functions (21 files)

#### Collection Functions (3 files)

##### 1. `functions/collection_functions.plating/docs/contains.tmpl.md`

**Current State**: 341 bytes (minimal template)
**Old State**: 8,234 bytes (comprehensive docs)
**Content Reduction**: 95.9%

**What to Restore**:
- Comprehensive description of contains() function capabilities
- Capabilities list:
  - List membership testing
  - Value existence checking
  - Conditional logic support
  - Validation workflows
- Function signature and return value specification
- Cross-references to examples:
  - `examples/example.tf` - Basic contains usage
  - `examples/basic.tf` - Simple examples
  - `examples/contains.tf` - Specific contains examples
  - `examples/advanced.tf` - Advanced patterns
  - `examples/comprehensive.tf` - Complete examples
- Related functions: `length()`, `lookup()`

**Skip**:
- Anti-patterns
- Empty list error handling

---

##### 2. `functions/collection_functions.plating/docs/length.tmpl.md`

**Current State**: 338 bytes (minimal template)
**Old State**: 7,456 bytes (comprehensive docs)
**Content Reduction**: 95.5%

**What to Restore**:
- Comprehensive description of length() function capabilities
- Capabilities list:
  - Collection size determination
  - String length calculation
  - Conditional resource creation
  - Validation and constraints
  - Iteration control
- Function signature and return value specification
- Cross-references to examples:
  - `examples/example.tf` - Basic length usage
  - `examples/basic.tf` - Simple examples
  - `examples/length.tf` - Specific length examples
  - `examples/advanced.tf` - Advanced patterns
  - `examples/comprehensive.tf` - Complete examples
- Related functions: `contains()`, `lookup()`

**Skip**:
- Anti-patterns
- Error handling

---

##### 3. `functions/collection_functions.plating/docs/lookup.tmpl.md`

**Current State**: 338 bytes (minimal template)
**Old State**: 9,123 bytes (comprehensive docs)
**Content Reduction**: 96.3%

**What to Restore**:
- Comprehensive description of lookup() function capabilities
- Capabilities list:
  - Map/object value retrieval
  - Default value support
  - Dynamic configuration lookup
  - Safe key access
  - Configuration management
- Function signature and return value specification
- Cross-references to examples:
  - `examples/example.tf` - Basic lookup usage
  - `examples/basic.tf` - Simple examples
  - `examples/lookup.tf` - Specific lookup examples
  - `examples/advanced.tf` - Advanced patterns
  - `examples/comprehensive.tf` - Complete examples
- Related functions: `contains()`, `length()`

**Skip**:
- Anti-patterns
- Missing key error handling

---

#### Numeric Functions (8 files)

##### 1. `functions/numeric_functions.plating/docs/add.tmpl.md`

**Current State**: 331 bytes (minimal template)
**Old State**: 6,789 bytes (comprehensive docs)
**Content Reduction**: 95.1%

**What to Restore**:
- Comprehensive description of add() function capabilities
- Capabilities list:
  - Numeric addition
  - Resource calculation
  - Cost estimation
  - Capacity planning
  - Metric aggregation
- Function signature and return value specification
- Cross-references to examples:
  - `examples/example.tf` - Basic addition
  - `examples/basic.tf` - Simple examples
  - `examples/add.tf` - Specific add examples
  - `examples/resource_calculations.tf` - Real-world calculations
  - `examples/comprehensive.tf` - Complete examples
- Related functions: `subtract()`, `multiply()`, `sum()`

**Skip**:
- Anti-patterns
- Type error handling

---

##### 2-8. Similar structure for: `subtract.tmpl.md`, `multiply.tmpl.md`, `divide.tmpl.md`, `sum.tmpl.md`, `min.tmpl.md`, `max.tmpl.md`, `round.tmpl.md`

**Follow same pattern as add.tmpl.md**:
- Comprehensive description
- Capabilities list (tailored to each function)
- Function signature and return value
- Cross-references to examples (including function-specific .tf files)
- Related functions

**max.tmpl.md specific notes**:
- **Old State**: 15,851 bytes (97.8% reduction)
- Capabilities list should include: capacity planning, performance optimization, scaling decisions, budget planning, quality metrics
- Cross-reference to: `examples/max.tf`, `examples/aggregations.tf`, `examples/resource_calculations.tf`

---

#### String Manipulation Functions (9 files)

##### 1. `functions/string_manipulation.plating/docs/format_size.tmpl.md`

**Current State**: 434 bytes (minimal template)
**Old State**: 15,430 bytes (comprehensive docs)
**Content Reduction**: 97.2%

**What to Restore**:
- Comprehensive description of format_size() function capabilities
- Capabilities list:
  - File size display in human-readable format
  - Storage reports
  - Bandwidth monitoring
  - Memory usage display
  - Progress indicators
- Unit conversion reference table (bytes, KB, MB, GB, TB)
- Function signature and return value specification
- Cross-references to examples:
  - `examples/example.tf` - Basic size formatting
  - `examples/basic.tf` - Simple examples
  - `examples/format_size.tf` - Specific format_size examples
  - `examples/comprehensive.tf` - Complete examples
- Related functions: `format()`, `tostring()`

**Skip**:
- Anti-patterns (when exact bytes are needed, binary units)
- Error handling

---

##### 2. `functions/string_manipulation.plating/docs/format.tmpl.md`

**Current State**: 352 bytes (minimal template)
**Old State**: 10,234 bytes (comprehensive docs)
**Content Reduction**: 96.6%

**What to Restore**:
- Comprehensive description of format() function capabilities
- Capabilities list:
  - String templating
  - Dynamic message generation
  - Formatted output creation
  - Variable interpolation
  - Report generation
- Format specifier reference (if present in old docs)
- Function signature and return value specification
- Cross-references to examples:
  - `examples/example.tf` - Basic formatting
  - `examples/basic.tf` - Simple examples
  - `examples/format.tf` - Specific format examples
  - `examples/comprehensive.tf` - Complete examples
- Related functions: `format_size()`, `join()`, `replace()`

**Skip**:
- Anti-patterns
- Format string error handling

---

##### 3-9. Similar structure for: `join.tmpl.md`, `split.tmpl.md`, `lower.tmpl.md`, `upper.tmpl.md`, `replace.tmpl.md`, `pluralize.tmpl.md`, `truncate.tmpl.md`, `to_camel_case.tmpl.md`, `to_kebab_case.tmpl.md`, `to_snake_case.tmpl.md`

**Follow same pattern**:
- Comprehensive description
- Capabilities list (tailored to each function)
- Function signature and return value
- Cross-references to examples (including function-specific .tf files like `join.tf`, `split.tf`, etc.)
- Related functions

**Special notes**:

**truncate.tmpl.md**:
- **Old State**: 13,387 bytes (96.9% reduction)
- Include ellipsis handling explanation
- Cross-reference to truncate-specific examples

**Case conversion functions** (`to_camel_case.tmpl.md`, `to_kebab_case.tmpl.md`, `to_snake_case.tmpl.md`):
- Capabilities should include: API field mapping, CSS class generation, database naming, URL slug generation, environment variable creation
- Cross-reference to case conversion examples in `examples/` directory

---

#### Type Conversion Functions (1 file)

##### 1. `functions/type_conversion_functions.plating/docs/tostring.tmpl.md`

**Current State**: 348 bytes (minimal template)
**Old State**: 7,234 bytes (comprehensive docs)
**Content Reduction**: 95.2%

**What to Restore**:
- Comprehensive description of tostring() function capabilities
- Capabilities list:
  - Type coercion to string
  - Number formatting
  - Boolean conversion
  - Output generation
  - String concatenation preparation
- Function signature and return value specification
- Cross-references to examples:
  - `examples/example.tf` - Basic type conversion
  - `examples/basic.tf` - Simple examples
  - `examples/tostring.tf` - Specific tostring examples
  - `examples/comprehensive.tf` - Complete examples
- Related functions: `format()`, string manipulation functions

**Skip**:
- Anti-patterns
- Type conversion error handling

---

## Implementation Guidelines

### General Approach for Each File

1. **Extract from old commit** (`dce87e4838f4f0bebdfb3cfe83101173bf37f92c`):
   ```bash
   git show dce87e4838f4f0bebdfb3cfe83101173bf37f92c:path/to/file.tmpl.md
   ```

2. **Identify sections to preserve**:
   - Comprehensive description paragraphs
   - Use case/capability bullet points (from "When to Use This")
   - Reference tables (permissions, units, etc.)
   - Related components lists

3. **Identify sections to skip**:
   - "Anti-patterns" sections
   - "Common Issues & Solutions" sections
   - Error handling examples
   - Troubleshooting commands

4. **Merge with current template**:
   - Keep current frontmatter (page_title, subcategory, description)
   - Keep `{{ example() }}` placeholders
   - Keep `{{ schema() }}` placeholders
   - Add restored content as additional sections

5. **Add example cross-references**:
   - Check what example files exist in current `examples/` directory
   - Add links to each with brief descriptions
   - Format as:
     ```markdown
     ## Examples

     - **[example.tf](examples/example.tf)** - Basic usage
     - **[basic.tf](examples/basic.tf)** - Simple scenarios
     - **[advanced.tf](examples/advanced.tf)** - Advanced patterns
     - **[comprehensive.tf](examples/comprehensive.tf)** - Complete example
     ```

6. **Add related components section**:
   - Extract from old docs
   - Format as:
     ```markdown
     ## Related Components

     - **pyvider_component_name** - Description of relationship
     - **pyvider_another_component** - Description of relationship
     ```

### Template Structure (Target Format)

```markdown
---
page_title: "Type: component_name"
subcategory: "Category"
description: |-
  Brief one-line description
---

# component_name (Type)

[2-4 paragraph comprehensive description of what this component does,
highlighting key capabilities and the value it provides. Focus on
showcasing features, not limitations.]

## Capabilities

This component enables you to:

- **Capability 1**: Description showing what it can do
- **Capability 2**: Description showing what it can do
- **Capability 3**: Description showing what it can do
- **Capability 4**: Description showing what it can do

## Example Usage

{{ example("example") }}

## Examples

Explore these examples to see the component in action:

- **[example.tf](examples/example.tf)** - Basic usage pattern
- **[basic.tf](examples/basic.tf)** - Simple scenarios
- **[advanced.tf](examples/advanced.tf)** - Advanced patterns
- **[comprehensive.tf](examples/comprehensive.tf)** - Full-featured example
- **[specific_feature.tf](examples/specific_feature.tf)** - Specific feature demonstration

## Argument Reference

{{ schema() }}

[Optional: Reference tables if relevant, e.g., permission formats, unit conversions]

## Related Components

- **pyvider_related_component** - How it relates
- **pyvider_another_component** - How it relates

## Import

[For resources only]

```bash
terraform import component_name.example <id>
```
```

### Quality Checklist

For each restored file, verify:

- [ ] Comprehensive description is present (2-4 paragraphs)
- [ ] Capabilities list focuses on what the component **can do**
- [ ] No anti-pattern content included
- [ ] No troubleshooting/error handling content included
- [ ] Example cross-references include all available examples
- [ ] Example cross-references have brief descriptions
- [ ] Related components section is present (if applicable)
- [ ] Reference tables included (if applicable)
- [ ] Template placeholders (`{{ example() }}`, `{{ schema() }}`) preserved
- [ ] Markdown formatting is clean and consistent

---

## File Inventory

### Data Sources (6 files)
1. `src/pyvider/components/data_sources/env_variables.plating/docs/pyvider_env_variables.tmpl.md`
2. `src/pyvider/components/data_sources/file_info.plating/docs/pyvider_file_info.tmpl.md`
3. `src/pyvider/components/data_sources/http_api.plating/docs/pyvider_http_api.tmpl.md`
4. `src/pyvider/components/data_sources/lens_jq.plating/docs/pyvider_lens_jq.tmpl.md`
5. `src/pyvider/components/data_sources/provider_config_reader.plating/docs/pyvider_provider_config_reader.tmpl.md`
6. `src/pyvider/components/data_sources/terraform_data_reader.plating/docs/pyvider_terraform_data_reader.tmpl.md`

### Resources (7 files)
1. `src/pyvider/components/resources/file_content.plating/docs/pyvider_file_content.tmpl.md`
2. `src/pyvider/components/resources/local_directory.plating/docs/pyvider_local_directory.tmpl.md`
3. `src/pyvider/components/resources/private_state_verifier.plating/docs/pyvider_private_state_verifier.tmpl.md`
4. `src/pyvider/components/resources/provider_config_reader.plating/docs/pyvider_provider_config.tmpl.md`
5. `src/pyvider/components/resources/simple_resource.plating/docs/pyvider_simple_resource.tmpl.md`
6. `src/pyvider/components/resources/timed_token.plating/docs/pyvider_timed_token.tmpl.md`
7. `src/pyvider/components/resources/warning_example.plating/docs/pyvider_warning_example.tmpl.md`

### Functions - Collection (3 files)
1. `src/pyvider/components/functions/collection_functions.plating/docs/contains.tmpl.md`
2. `src/pyvider/components/functions/collection_functions.plating/docs/length.tmpl.md`
3. `src/pyvider/components/functions/collection_functions.plating/docs/lookup.tmpl.md`

### Functions - Numeric (8 files)
1. `src/pyvider/components/functions/numeric_functions.plating/docs/add.tmpl.md`
2. `src/pyvider/components/functions/numeric_functions.plating/docs/divide.tmpl.md`
3. `src/pyvider/components/functions/numeric_functions.plating/docs/max.tmpl.md`
4. `src/pyvider/components/functions/numeric_functions.plating/docs/min.tmpl.md`
5. `src/pyvider/components/functions/numeric_functions.plating/docs/multiply.tmpl.md`
6. `src/pyvider/components/functions/numeric_functions.plating/docs/round.tmpl.md`
7. `src/pyvider/components/functions/numeric_functions.plating/docs/subtract.tmpl.md`
8. `src/pyvider/components/functions/numeric_functions.plating/docs/sum.tmpl.md`

### Functions - String Manipulation (9 files)
1. `src/pyvider/components/functions/string_manipulation.plating/docs/format.tmpl.md`
2. `src/pyvider/components/functions/string_manipulation.plating/docs/format_size.tmpl.md`
3. `src/pyvider/components/functions/string_manipulation.plating/docs/join.tmpl.md`
4. `src/pyvider/components/functions/string_manipulation.plating/docs/lower.tmpl.md`
5. `src/pyvider/components/functions/string_manipulation.plating/docs/pluralize.tmpl.md`
6. `src/pyvider/components/functions/string_manipulation.plating/docs/replace.tmpl.md`
7. `src/pyvider/components/functions/string_manipulation.plating/docs/split.tmpl.md`
8. `src/pyvider/components/functions/string_manipulation.plating/docs/to_camel_case.tmpl.md`
9. `src/pyvider/components/functions/string_manipulation.plating/docs/to_kebab_case.tmpl.md`
10. `src/pyvider/components/functions/string_manipulation.plating/docs/to_snake_case.tmpl.md`
11. `src/pyvider/components/functions/string_manipulation.plating/docs/truncate.tmpl.md`
12. `src/pyvider/components/functions/string_manipulation.plating/docs/upper.tmpl.md`

### Functions - Type Conversion (1 file)
1. `src/pyvider/components/functions/type_conversion_functions.plating/docs/tostring.tmpl.md`

**Total: 34 files**

---

## Example Restoration Workflow

### Step 1: Extract old content
```bash
git show dce87e4838f4f0bebdfb3cfe83101173bf37f92c:src/pyvider/components/data_sources/file_info.plating/docs/pyvider_file_info.tmpl.md > /tmp/old_file_info.md
```

### Step 2: Read current content
```bash
cat src/pyvider/components/data_sources/file_info.plating/docs/pyvider_file_info.tmpl.md
```

### Step 3: Identify sections to restore
From `/tmp/old_file_info.md`:
- Extract comprehensive description (paragraphs 1-3)
- Extract "When to Use This" bullets (skip anti-patterns)
- Extract permission format table
- Extract "Related Components" section

### Step 4: Check available examples
```bash
ls src/pyvider/components/data_sources/file_info.plating/examples/
```

### Step 5: Merge and update
- Keep current frontmatter
- Add comprehensive description
- Add capabilities section (from "When to Use This", excluding anti-patterns)
- Keep `{{ example("example") }}`
- Add examples section with cross-references
- Keep `{{ schema() }}`
- Add permission format table
- Add related components section

### Step 6: Verify quality
- Check against quality checklist
- Ensure no troubleshooting content included
- Ensure showcase focus maintained

---

## Success Criteria

The restoration is complete when:

1. **All 34 files** have been updated with comprehensive documentation
2. **Each file** includes:
   - Comprehensive description (2-4 paragraphs)
   - Capabilities/use cases section (positive focus only)
   - Example cross-references with descriptions
   - Related components section (where applicable)
   - Reference tables (where applicable)
   - Template placeholders preserved
3. **No files** include:
   - Anti-patterns sections
   - Troubleshooting content
   - Error handling examples
   - Production-oriented guidance
4. **Documentation** maintains a showcase focus, highlighting what pyvider can do
5. **All links** to examples are valid and accurate

---

## Notes

- **Priority**: All 34 files are equally important
- **Order**: Can be done in any order, but grouping by type (data sources, resources, functions) may be more efficient
- **Testing**: After restoration, verify that plating/documentation generation still works correctly
- **Consistency**: Maintain consistent structure and tone across all files
- **Showcase focus**: Always emphasize capabilities and features, not limitations or troubleshooting

---

## Contact

For questions about this restoration:
- Review original commit: `dce87e4838f4f0bebdfb3cfe83101173bf37f92c`
- Check current simplified versions in HEAD
- Refer to this handoff document for guidance
