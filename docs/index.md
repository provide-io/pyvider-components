---
page_title: "Pyvider Components"
description: |-
  Learning and reference library for Pyvider framework components
---

# Pyvider Components

**A learning and reference library** containing 100+ example components for the [Pyvider framework](https://github.com/provide-io/pyvider).

!!! tip "This is a Learning Library"
    Pyvider-components is designed for **studying and learning** how to build Terraform providers. It's not meant for direct production use. For production, see [terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider).

## Quick Links

- 📚 **[Getting Started Guide](getting-started.md)** - New to pyvider-components? Start here!
- 🔍 **[How to Study Components](how-to/study-components.md)** - Learn the study process
- 💾 **[Source Code](https://github.com/provide-io/pyvider-components)** - Browse the repository
- 🚀 **[Production Provider](https://github.com/provide-io/terraform-provider-pyvider)** - Use in production

## What's Inside

This repository contains **100+ working examples** organized in three categories:

### 📦 Resources (7 total)

Manage infrastructure with full lifecycle (create, read, update, delete):

- [`pyvider_file_content`](./resources/file_content.md) - Manage file contents
- [`pyvider_local_directory`](./resources/local_directory.md) - Create and manage directories
- [`pyvider_timed_token`](./resources/timed_token.md) - Time-based resource (test component)

[View all resources →](resources/)

### 📥 Data Sources (10 total)

Read external data into Terraform:

- [`pyvider_env_variables`](./data-sources/env_variables.md) - Access environment variables
- [`pyvider_file_info`](./data-sources/file_info.md) - Get file/directory metadata
- [`pyvider_http_api`](./data-sources/http_api.md) - Make HTTP requests
- [`pyvider_lens_jq`](./data-sources/lens_jq.md) - Transform data with JQ
- [`pyvider_nested_data_processor`](./data-sources/nested_data_processor.md) - Process nested data
- [`pyvider_provider_config_reader`](./data-sources/provider_config_reader.md) - Read provider config

[View all data sources →](data-sources/)

### 🔢 Functions (25 total)

Transform and compute values - the simplest components to start learning:

**Numeric:** [`add`](./functions/add.md) · [`subtract`](./functions/subtract.md) · [`multiply`](./functions/multiply.md) · [`divide`](./functions/divide.md) · [`min`](./functions/min.md) · [`max`](./functions/max.md) · [`sum`](./functions/sum.md) · [`round`](./functions/round.md)

**String:** [`upper`](./functions/upper.md) · [`lower`](./functions/lower.md) · [`split`](./functions/split.md) · [`join`](./functions/join.md) · [`replace`](./functions/replace.md) · [`format`](./functions/format.md) · [`truncate`](./functions/truncate.md) · [`format_size`](./functions/format_size.md) · [`pluralize`](./functions/pluralize.md) · [`to_snake_case`](./functions/to_snake_case.md) · [`to_kebab_case`](./functions/to_kebab_case.md) · [`to_camel_case`](./functions/to_camel_case.md)

**Collection:** [`length`](./functions/length.md) · [`contains`](./functions/contains.md) · [`lookup`](./functions/lookup.md)

**Type Conversion:** [`tostring`](./functions/tostring.md)

**Transformation:** [`lens_jq`](./functions/lens_jq.md)

[View all functions →](functions/)

---

## Test Components

Several components demonstrate specific patterns in isolation - perfect for understanding advanced concepts:

**Test Resources:** [`pyvider_private_state_verifier`](./resources/private_state_verifier.md) · [`pyvider_warning_example`](./resources/warning_example.md)

**Test Data Sources:** [`pyvider_mixed_map_test`](./data-sources/mixed_map_test.md) · [`pyvider_nested_resource_test`](./data-sources/nested_resource_test.md) · [`pyvider_simple_map_test`](./data-sources/simple_map_test.md) · [`pyvider_structured_object_test`](./data-sources/structured_object_test.md)

---

## How to Use This Library

### 1. Start with Getting Started

New to pyvider-components? Begin with the [Getting Started Guide](getting-started.md) to:

- Understand the library's purpose
- Learn the three component types
- Study your first component
- Find your learning path

### 2. Study Components

Follow the systematic process in [How to Study Components](how-to/study-components.md):

1. **Identify** - Choose a component to study
2. **Source** - Read the implementation
3. **Schema** - Understand the Terraform interface
4. **Examples** - Study usage patterns
5. **Adapt** - Apply to your own work

### 3. Explore Examples

Each component has working Terraform examples in the [`examples/`](https://github.com/provide-io/pyvider-components/tree/main/examples) directory:

- `basic.tf` - Simple usage
- `advanced.tf` - Complex scenarios
- `comprehensive.tf` - Full features

### 4. Build Your Own

Use these components as templates for your own Terraform providers:

- Copy the patterns (Apache 2.0 licensed)
- Adapt for your use case
- Reference the [Pyvider framework docs](https://github.com/provide-io/pyvider)

---

## Learning Paths

### For Beginners

**Goal:** Understand basic provider development

1. Study simple functions (`add`, `upper`, `length`)
2. Review basic data sources (`pyvider_env_variables`)
3. Explore simple resources (`pyvider_file_content`)

**Time:** 1-2 weeks

### For Provider Developers

**Goal:** Build production-ready providers

1. Master all component types
2. Study test components for patterns
3. Review error handling and validation
4. Understand state management

**Time:** 3-4 weeks

### For Contributors

**Goal:** Contribute to terraform-provider-pyvider

1. Study existing production components
2. Understand packaging patterns
3. Review terraform-provider-pyvider codebase
4. Follow contribution guidelines

**Time:** 1 week

---

## Related Projects

Pyvider-components is part of the provide.io ecosystem:

- **[Pyvider](https://github.com/provide-io/pyvider)** - Core framework for building Terraform providers
- **[terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider)** - Production provider (use this in Terraform)
- **[provide-foundation](https://docs.provide.io)** - Python foundations and utilities
- **[Ecosystem Overview](https://docs.provide.io/provide-foundation/ecosystem/)** - How all projects fit together

---

## Ready to Learn?

👉 **[Start with the Getting Started Guide →](getting-started.md)**

Or jump directly to:

- [How to Study Components](how-to/study-components.md)
- [View Functions Reference](functions/)
- [View Data Sources Reference](data-sources/)
- [View Resources Reference](resources/)
- [Browse Source Code](https://github.com/provide-io/pyvider-components)
