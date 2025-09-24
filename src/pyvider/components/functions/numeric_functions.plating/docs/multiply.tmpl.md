---
page_title: "Function: multiply"
description: |-
  Multiplies two numbers with intelligent integer conversion and null-safe handling
---

# multiply (Function)

> Performs multiplication of two numeric values with null-safe handling and automatic type optimization

The `multiply` function multiplies two numbers (integers or floats) and returns the result. It handles null values gracefully and automatically converts floating-point results to integers when they represent whole numbers.

## When to Use This

- **Scaling calculations**: Scale values by multipliers or factors
- **Resource sizing**: Calculate total capacity based on unit size
- **Area calculations**: Compute areas, volumes, or dimensions
- **Cost calculations**: Calculate total costs based on unit prices
- **Percentage calculations**: Apply percentage multipliers

**Anti-patterns (when NOT to use):**
- Complex mathematical operations (use multiple function calls)
- String repetition (use appropriate string functions)
- List/array operations (use collection functions)
- Boolean logic (use conditional expressions)

## Quick Start

```terraform
# Simple multiplication
locals {
  total_storage = provider::pyvider::multiply(10, 5)  # Returns: 50
}

# Scaling with variables
variable "instances" {
  default = 4
}

variable "cpu_per_instance" {
  default = 2
}

locals {
  total_cpu = provider::pyvider::multiply(var.instances, var.cpu_per_instance)  # Returns: 8
}
```

## Examples

### Basic Usage

```terraform
# Basic multiplication operations
locals {
  basic_operations = {
    integers = provider::pyvider::multiply(6, 7)              # 42
    floats = provider::pyvider::multiply(3.5, 2.0)            # 7.0 (becomes 7)
    mixed = provider::pyvider::multiply(4, 2.5)               # 10.0 (becomes 10)
    decimals = provider::pyvider::multiply(3.14, 2)           # 6.28
    zero = provider::pyvider::multiply(100, 0)                # 0
    negative = provider::pyvider::multiply(-5, 3)             # -15
    both_negative = provider::pyvider::multiply(-4, -6)       # 24
  }

  # Percentage calculations
  percentage_examples = {
    twenty_percent = provider::pyvider::multiply(100, 0.2)    # 20.0 (becomes 20)
    tax_calculation = provider::pyvider::multiply(500, 1.08)  # 540.0 (becomes 540)
    discount = provider::pyvider::multiply(200, 0.85)         # 170.0 (becomes 170)
    compound_growth = provider::pyvider::multiply(1000, 1.05) # 1050.0 (becomes 1050)
  }
}

# Unit conversions
locals {
  conversions = {
    gb_to_mb = provider::pyvider::multiply(16, 1024)          # 16384 (GB to MB)
    hours_to_minutes = provider::pyvider::multiply(2.5, 60)   # 150.0 (becomes 150)
    days_to_seconds = provider::pyvider::multiply(1, 86400)   # 86400
    meters_to_feet = provider::pyvider::multiply(100, 3.28084) # 328.084
  }
}

output "basic_examples" {
  value = {
    operations = local.basic_operations
    percentages = local.percentage_examples
    conversions = local.conversions
  }
}
```

### Infrastructure Scaling

```terraform
# Instance scaling calculations
variable "environments" {
  type = map(object({
    instance_count = number
    cpu_per_instance = number
    memory_per_instance = number
    storage_per_instance = number
    cost_per_hour = number
  }))
  default = {
    development = {
      instance_count = 2
      cpu_per_instance = 2
      memory_per_instance = 4
      storage_per_instance = 20
      cost_per_hour = 0.05
    }
    staging = {
      instance_count = 3
      cpu_per_instance = 4
      memory_per_instance = 8
      storage_per_instance = 50
      cost_per_hour = 0.10
    }
    production = {
      instance_count = 10
      cpu_per_instance = 8
      memory_per_instance = 16
      storage_per_instance = 100
      cost_per_hour = 0.20
    }
  }
}

# Calculate total resources for each environment
locals {
  environment_resources = {
    for env_name, env_config in var.environments :
    env_name => {
      total_cpu = provider::pyvider::multiply(env_config.instance_count, env_config.cpu_per_instance)
      total_memory = provider::pyvider::multiply(env_config.instance_count, env_config.memory_per_instance)
      total_storage = provider::pyvider::multiply(env_config.instance_count, env_config.storage_per_instance)
      hourly_cost = provider::pyvider::multiply(env_config.instance_count, env_config.cost_per_hour)
      daily_cost = provider::pyvider::multiply(
        provider::pyvider::multiply(env_config.instance_count, env_config.cost_per_hour),
        24
      )
      monthly_cost = provider::pyvider::multiply(
        provider::pyvider::multiply(env_config.instance_count, env_config.cost_per_hour),
        730  # Average hours per month
      )
    }
  }

  # Calculate total across all environments
  total_resources = {
    total_cpu = sum([for env in local.environment_resources : env.total_cpu])
    total_memory = sum([for env in local.environment_resources : env.total_memory])
    total_storage = sum([for env in local.environment_resources : env.total_storage])
    total_monthly_cost = sum([for env in local.environment_resources : env.monthly_cost])
  }
}

# Kubernetes scaling calculations
variable "workloads" {
  type = list(object({
    name = string
    replicas = number
    cpu_request = number
    memory_request = number
    cpu_limit = number
    memory_limit = number
  }))
  default = [
    {
      name = "web-app"
      replicas = 5
      cpu_request = 0.5
      memory_request = 512
      cpu_limit = 1.0
      memory_limit = 1024
    },
    {
      name = "background-worker"
      replicas = 3
      cpu_request = 0.25
      memory_request = 256
      cpu_limit = 0.5
      memory_limit = 512
    },
    {
      name = "database"
      replicas = 1
      cpu_request = 2.0
      memory_request = 4096
      cpu_limit = 4.0
      memory_limit = 8192
    }
  ]
}

locals {
  workload_resources = {
    for workload in var.workloads :
    workload.name => {
      total_cpu_requests = provider::pyvider::multiply(workload.replicas, workload.cpu_request)
      total_memory_requests = provider::pyvider::multiply(workload.replicas, workload.memory_request)
      total_cpu_limits = provider::pyvider::multiply(workload.replicas, workload.cpu_limit)
      total_memory_limits = provider::pyvider::multiply(workload.replicas, workload.memory_limit)

      # Calculate resource efficiency ratios
      cpu_efficiency = provider::pyvider::multiply(
        provider::pyvider::divide(workload.cpu_request, workload.cpu_limit),
        100
      )
      memory_efficiency = provider::pyvider::multiply(
        provider::pyvider::divide(workload.memory_request, workload.memory_limit),
        100
      )
    }
  }
}

output "infrastructure_scaling" {
  value = {
    environment_resources = local.environment_resources
    total_resources = local.total_resources
    workload_resources = local.workload_resources
  }
}
```

### Cost Calculations and Budgeting

```terraform
# Project cost calculation
variable "project_phases" {
  type = list(object({
    phase_name = string
    duration_weeks = number
    team_size = number
    hourly_rate = number
    hours_per_week = number
    infrastructure_cost_per_week = number
    tool_licenses_per_person = number
  }))
  default = [
    {
      phase_name = "Planning & Design"
      duration_weeks = 4
      team_size = 3
      hourly_rate = 100
      hours_per_week = 40
      infrastructure_cost_per_week = 200
      tool_licenses_per_person = 50
    },
    {
      phase_name = "Development"
      duration_weeks = 12
      team_size = 8
      hourly_rate = 95
      hours_per_week = 40
      infrastructure_cost_per_week = 800
      tool_licenses_per_person = 50
    },
    {
      phase_name = "Testing & QA"
      duration_weeks = 6
      team_size = 4
      hourly_rate = 90
      hours_per_week = 40
      infrastructure_cost_per_week = 400
      tool_licenses_per_person = 50
    },
    {
      phase_name = "Deployment"
      duration_weeks = 2
      team_size = 2
      hourly_rate = 110
      hours_per_week = 50
      infrastructure_cost_per_week = 1000
      tool_licenses_per_person = 50
    }
  ]
}

locals {
  phase_costs = {
    for phase in var.project_phases :
    phase.phase_name => {
      # Labor costs
      weekly_labor_hours = provider::pyvider::multiply(phase.team_size, phase.hours_per_week)
      weekly_labor_cost = provider::pyvider::multiply(local.phase_costs[phase.phase_name].weekly_labor_hours, phase.hourly_rate)
      total_labor_cost = provider::pyvider::multiply(local.phase_costs[phase.phase_name].weekly_labor_cost, phase.duration_weeks)

      # Infrastructure costs
      total_infrastructure_cost = provider::pyvider::multiply(phase.infrastructure_cost_per_week, phase.duration_weeks)

      # Tool licensing costs
      weekly_tool_cost = provider::pyvider::multiply(phase.team_size, phase.tool_licenses_per_person)
      total_tool_cost = provider::pyvider::multiply(local.phase_costs[phase.phase_name].weekly_tool_cost, phase.duration_weeks)

      # Phase totals
      total_phase_cost = sum([
        local.phase_costs[phase.phase_name].total_labor_cost,
        local.phase_costs[phase.phase_name].total_infrastructure_cost,
        local.phase_costs[phase.phase_name].total_tool_cost
      ])

      # Metrics
      cost_per_person_week = provider::pyvider::divide(local.phase_costs[phase.phase_name].total_phase_cost, provider::pyvider::multiply(phase.team_size, phase.duration_weeks))
    }
  }

  # Project totals
  total_project_cost = sum([for phase_name, costs in local.phase_costs : costs.total_phase_cost])

  # Add contingency and profit margins
  contingency_multiplier = 1.15  # 15% contingency
  profit_multiplier = 1.25       # 25% profit margin

  project_estimate = {
    base_cost = local.total_project_cost
    with_contingency = provider::pyvider::multiply(local.total_project_cost, contingency_multiplier)
    final_quote = provider::pyvider::multiply(local.total_project_cost, provider::pyvider::multiply(contingency_multiplier, profit_multiplier))
  }
}

# SaaS pricing calculations
variable "subscription_tiers" {
  type = map(object({
    monthly_base_price = number
    included_users = number
    additional_user_price = number
    included_storage_gb = number
    additional_storage_price_per_gb = number
    transaction_limit = number
    overage_price_per_transaction = number
  }))
  default = {
    starter = {
      monthly_base_price = 29
      included_users = 5
      additional_user_price = 8
      included_storage_gb = 10
      additional_storage_price_per_gb = 2
      transaction_limit = 1000
      overage_price_per_transaction = 0.01
    }
    professional = {
      monthly_base_price = 99
      included_users = 25
      additional_user_price = 6
      included_storage_gb = 100
      additional_storage_price_per_gb = 1.5
      transaction_limit = 10000
      overage_price_per_transaction = 0.008
    }
    enterprise = {
      monthly_base_price = 299
      included_users = 100
      additional_user_price = 4
      included_storage_gb = 1000
      additional_storage_price_per_gb = 1
      transaction_limit = 100000
      overage_price_per_transaction = 0.005
    }
  }
}

variable "customer_usage" {
  type = object({
    tier = string
    users = number
    storage_gb = number
    monthly_transactions = number
  })
  default = {
    tier = "professional"
    users = 35
    storage_gb = 150
    monthly_transactions = 15000
  }
}

locals {
  tier_config = var.subscription_tiers[var.customer_usage.tier]

  customer_billing = {
    # Base subscription cost
    base_cost = local.tier_config.monthly_base_price

    # Additional user costs
    extra_users = max(0, var.customer_usage.users - local.tier_config.included_users)
    user_overage_cost = provider::pyvider::multiply(local.customer_billing.extra_users, local.tier_config.additional_user_price)

    # Storage overage costs
    extra_storage = max(0, var.customer_usage.storage_gb - local.tier_config.included_storage_gb)
    storage_overage_cost = provider::pyvider::multiply(local.customer_billing.extra_storage, local.tier_config.additional_storage_price_per_gb)

    # Transaction overage costs
    extra_transactions = max(0, var.customer_usage.monthly_transactions - local.tier_config.transaction_limit)
    transaction_overage_cost = provider::pyvider::multiply(local.customer_billing.extra_transactions, local.tier_config.overage_price_per_transaction)

    # Total monthly bill
    total_monthly_cost = sum([
      local.customer_billing.base_cost,
      local.customer_billing.user_overage_cost,
      local.customer_billing.storage_overage_cost,
      local.customer_billing.transaction_overage_cost
    ])

    # Annual calculations with discounts
    annual_base = provider::pyvider::multiply(local.customer_billing.total_monthly_cost, 12)
    annual_discount_rate = 0.1  # 10% annual discount
    annual_with_discount = provider::pyvider::multiply(local.customer_billing.annual_base, 0.9)
  }
}

output "cost_calculations" {
  value = {
    phase_costs = local.phase_costs
    project_estimate = local.project_estimate
    customer_billing = local.customer_billing
  }
}
```

### Performance and Capacity Planning

```terraform
# Database capacity planning
variable "database_config" {
  type = object({
    records_per_day = number
    average_record_size_bytes = number
    retention_days = number
    replication_factor = number
    index_overhead_multiplier = number
    compression_ratio = number
  })
  default = {
    records_per_day = 100000
    average_record_size_bytes = 512
    retention_days = 365
    replication_factor = 3
    index_overhead_multiplier = 1.3
    compression_ratio = 0.4
  }
}

locals {
  database_capacity = {
    # Raw data calculations
    daily_data_bytes = provider::pyvider::multiply(var.database_config.records_per_day, var.database_config.average_record_size_bytes)
    retention_data_bytes = provider::pyvider::multiply(local.database_capacity.daily_data_bytes, var.database_config.retention_days)

    # Storage with overhead and compression
    data_with_indexes = provider::pyvider::multiply(local.database_capacity.retention_data_bytes, var.database_config.index_overhead_multiplier)
    compressed_data = provider::pyvider::multiply(local.database_capacity.data_with_indexes, var.database_config.compression_ratio)
    replicated_data = provider::pyvider::multiply(local.database_capacity.compressed_data, var.database_config.replication_factor)

    # Convert to human-readable units
    storage_gb = provider::pyvider::divide(local.database_capacity.replicated_data, 1073741824)  # bytes to GB
    storage_tb = provider::pyvider::divide(local.database_capacity.storage_gb, 1024)

    # Growth projections (20% annual growth)
    growth_multiplier = 1.2
    year_1_storage_tb = provider::pyvider::multiply(local.database_capacity.storage_tb, local.database_capacity.growth_multiplier)
    year_2_storage_tb = provider::pyvider::multiply(local.database_capacity.year_1_storage_tb, local.database_capacity.growth_multiplier)
    year_3_storage_tb = provider::pyvider::multiply(local.database_capacity.year_2_storage_tb, local.database_capacity.growth_multiplier)
  }
}

# CDN bandwidth calculations
variable "cdn_usage" {
  type = object({
    unique_visitors_per_day = number
    pages_per_visitor = number
    average_page_size_mb = number
    static_assets_multiplier = number
    peak_traffic_multiplier = number
    geographic_regions = number
  })
  default = {
    unique_visitors_per_day = 50000
    pages_per_visitor = 3
    average_page_size_mb = 2.5
    static_assets_multiplier = 4
    peak_traffic_multiplier = 8
    geographic_regions = 5
  }
}

locals {
  cdn_bandwidth = {
    # Basic traffic calculations
    daily_page_views = provider::pyvider::multiply(var.cdn_usage.unique_visitors_per_day, var.cdn_usage.pages_per_visitor)
    daily_data_mb = provider::pyvider::multiply(local.cdn_bandwidth.daily_page_views, var.cdn_usage.average_page_size_mb)
    daily_with_assets = provider::pyvider::multiply(local.cdn_bandwidth.daily_data_mb, var.cdn_usage.static_assets_multiplier)

    # Peak traffic requirements
    peak_hourly_mb = provider::pyvider::multiply(provider::pyvider::divide(local.cdn_bandwidth.daily_with_assets, 24), var.cdn_usage.peak_traffic_multiplier)
    peak_bandwidth_mbps = provider::pyvider::divide(local.cdn_bandwidth.peak_hourly_mb, 3600)  # MB/hour to MB/second

    # Regional distribution
    per_region_peak_mbps = provider::pyvider::divide(local.cdn_bandwidth.peak_bandwidth_mbps, var.cdn_usage.geographic_regions)

    # Monthly totals
    monthly_data_gb = provider::pyvider::multiply(provider::pyvider::divide(local.cdn_bandwidth.daily_with_assets, 1024), 30)

    # Cost estimates (example pricing: $0.08 per GB)
    monthly_bandwidth_cost = provider::pyvider::multiply(local.cdn_bandwidth.monthly_data_gb, 0.08)
  }
}

output "performance_planning" {
  value = {
    database_capacity = local.database_capacity
    cdn_bandwidth = local.cdn_bandwidth
  }
}
```

### Null Handling and Edge Cases

```terraform
# Null and edge case handling
variable "test_inputs" {
  type = object({
    valid_number = number
    zero_value = number
    negative_value = number
    null_value = number
    large_number = number
  })
  default = {
    valid_number = 42
    zero_value = 0
    negative_value = -10
    null_value = null
    large_number = 999999999
  }
}

locals {
  null_handling_examples = {
    # Valid operations
    valid_multiply = provider::pyvider::multiply(var.test_inputs.valid_number, 2)        # 84
    zero_multiply = provider::pyvider::multiply(var.test_inputs.zero_value, 100)         # 0
    negative_multiply = provider::pyvider::multiply(var.test_inputs.negative_value, 3)   # -30
    large_multiply = provider::pyvider::multiply(var.test_inputs.large_number, 2)        # 1999999998

    # Null handling
    null_first = provider::pyvider::multiply(var.test_inputs.null_value, 5)              # null
    null_second = provider::pyvider::multiply(10, var.test_inputs.null_value)            # null
    both_null = provider::pyvider::multiply(var.test_inputs.null_value, var.test_inputs.null_value) # null

    # Conditional multiplication with null checks
    safe_multiply = var.test_inputs.null_value != null && var.test_inputs.valid_number != null ?
                   provider::pyvider::multiply(var.test_inputs.null_value, var.test_inputs.valid_number) :
                   0

    # Default value when null
    multiply_with_default = provider::pyvider::multiply(
      coalesce(var.test_inputs.null_value, 1),  # Use 1 if null
      var.test_inputs.valid_number
    )
  }

  # Resource calculations with null safety
  resource_multipliers = {
    cpu_scaling = var.test_inputs.valid_number != null ? provider::pyvider::multiply(var.test_inputs.valid_number, 2) : 2
    memory_scaling = var.test_inputs.null_value != null ? provider::pyvider::multiply(var.test_inputs.null_value, 4) : 8
    storage_scaling = coalesce(
      var.test_inputs.null_value != null ? provider::pyvider::multiply(var.test_inputs.null_value, 10) : null,
      100  # default 100GB if calculation results in null
    )
  }

  # Validation patterns
  validated_operations = {
    for key, value in var.test_inputs :
    key => {
      original_value = value
      is_valid = value != null
      multiplied_by_2 = value != null ? provider::pyvider::multiply(value, 2) : null
      multiplied_safe = coalesce(
        value != null ? provider::pyvider::multiply(value, 2) : null,
        0  # default to 0 if null
      )
    }
  }
}

output "null_handling" {
  value = {
    examples = local.null_handling_examples
    resource_multipliers = local.resource_multipliers
    validated_operations = local.validated_operations
  }
}
```

## Signature

`multiply(a: number, b: number) -> number`

## Arguments

- **`a`** (number, required) - The first number to multiply. Can be an integer or float. Returns `null` if this value is `null`.
- **`b`** (number, required) - The second number to multiply. Can be an integer or float. Returns `null` if this value is `null`.

## Return Value

Returns the product of `a` and `b` as a number. The return type is automatically optimized:
- If the result is a whole number (e.g., `6.0`), returns an integer (`6`)
- If the result has decimal places (e.g., `6.75`), returns a float (`6.75`)
- Returns `null` if either input is `null`

## Common Patterns

### Resource Capacity
```terraform
variable "nodes" {
  type    = number
  default = 3
}

variable "cores_per_node" {
  type    = number
  default = 8
}

locals {
  total_cores = provider::pyvider::multiply(var.nodes, var.cores_per_node)
}

resource "pyvider_file_content" "capacity_report" {
  filename = "/tmp/capacity.txt"
  content  = "Total CPU cores: ${local.total_cores}"
}
```

### Cost Estimation
```terraform
variable "unit_price" {
  type = number
}

variable "quantity" {
  type = number
}

locals {
  total_cost = provider::pyvider::multiply(var.unit_price, var.quantity)
}
```

## Related Functions

- [`add`](./add.md) - Add two numbers
- [`subtract`](./subtract.md) - Subtract two numbers
- [`divide`](./divide.md) - Divide two numbers
- [`round`](./round.md) - Round the result to specific precision
