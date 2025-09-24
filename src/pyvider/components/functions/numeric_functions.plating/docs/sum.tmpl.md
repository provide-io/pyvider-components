---
page_title: "Function: sum"
description: |-
  Calculates the sum of all numbers in a list with intelligent type conversion
---

# sum (Function)

> Calculates the sum of all numeric values in a list with null-safe handling and automatic type optimization

The `sum` function adds all numbers in a list and returns the total. It handles null values gracefully and automatically converts floating-point results to integers when they represent whole numbers.

## When to Use This

- **Aggregate calculations**: Sum multiple values from lists or collections
- **Total calculations**: Calculate totals for costs, quantities, or metrics
- **Accumulation**: Add up values from dynamic lists
- **Budget summation**: Total multiple budget items
- **Resource totals**: Sum resource allocations or usage

**Anti-patterns (when NOT to use):**
- Empty lists without validation (will return 0)
- Non-numeric data (ensure list contains only numbers)
- Single value addition (use `add` for two values)

## Quick Start

```terraform
# Simple sum
locals {
  numbers = [10, 20, 30, 40]
  total = provider::pyvider::sum(local.numbers)  # Returns: 100
}

# Sum with variables
variable "costs" {
  default = [150.50, 75.25, 200.00]
}

locals {
  total_cost = provider::pyvider::sum(var.costs)  # Returns: 425.75
}
```

## Examples

### Basic Usage

```terraform
# Basic sum operations
locals {
  basic_examples = {
    integers = provider::pyvider::sum([1, 2, 3, 4, 5])              # 15
    floats = provider::pyvider::sum([1.5, 2.5, 3.0])               # 7.0 (becomes 7)
    mixed = provider::pyvider::sum([10, 15.5, 20, 4.5])            # 50.0 (becomes 50)
    negative = provider::pyvider::sum([-5, 10, -3, 8])             # 10
    empty_list = provider::pyvider::sum([])                         # 0
    single_value = provider::pyvider::sum([42])                     # 42
    large_numbers = provider::pyvider::sum([1000000, 2000000, 3000000]) # 6000000
  }

  # Different list sizes
  list_size_examples = {
    two_items = provider::pyvider::sum([25, 75])                    # 100
    many_items = provider::pyvider::sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) # 55
    decimal_precision = provider::pyvider::sum([0.1, 0.2, 0.3])    # 0.6
  }

  # Percentage and ratio sums
  percentage_sums = {
    percentages = provider::pyvider::sum([0.25, 0.35, 0.40])       # 1.0 (becomes 1)
    ratios = provider::pyvider::sum([0.33, 0.33, 0.34])            # 1.0 (becomes 1)
    weights = provider::pyvider::sum([0.5, 0.3, 0.15, 0.05])       # 1.0 (becomes 1)
  }
}

output "basic_examples" {
  value = {
    basic = local.basic_examples
    list_sizes = local.list_size_examples
    percentages = local.percentage_sums
  }
}
```

### Financial and Cost Analysis

```terraform
# Project cost aggregation
variable "project_costs" {
  type = map(object({
    development = list(number)
    infrastructure = list(number)
    marketing = list(number)
    operations = list(number)
  }))
  default = {
    q1_2024 = {
      development = [45000, 52000, 48000]    # Monthly development costs
      infrastructure = [8000, 9500, 12000]   # Monthly infrastructure costs
      marketing = [15000, 18000, 22000]      # Monthly marketing costs
      operations = [25000, 26000, 24000]     # Monthly operations costs
    }
    q2_2024 = {
      development = [55000, 58000, 60000]
      infrastructure = [13000, 14500, 16000]
      marketing = [28000, 32000, 35000]
      operations = [27000, 28500, 29000]
    }
  }
}

locals {
  quarterly_totals = {
    for quarter, costs in var.project_costs :
    quarter => {
      development_total = provider::pyvider::sum(costs.development)
      infrastructure_total = provider::pyvider::sum(costs.infrastructure)
      marketing_total = provider::pyvider::sum(costs.marketing)
      operations_total = provider::pyvider::sum(costs.operations)

      # Department totals
      total_by_department = {
        development = local.quarterly_totals[quarter].development_total
        infrastructure = local.quarterly_totals[quarter].infrastructure_total
        marketing = local.quarterly_totals[quarter].marketing_total
        operations = local.quarterly_totals[quarter].operations_total
      }

      # Overall quarterly total
      quarterly_total = provider::pyvider::sum([
        local.quarterly_totals[quarter].development_total,
        local.quarterly_totals[quarter].infrastructure_total,
        local.quarterly_totals[quarter].marketing_total,
        local.quarterly_totals[quarter].operations_total
      ])

      # Monthly averages
      monthly_averages = {
        development = provider::pyvider::divide(local.quarterly_totals[quarter].development_total, 3)
        infrastructure = provider::pyvider::divide(local.quarterly_totals[quarter].infrastructure_total, 3)
        marketing = provider::pyvider::divide(local.quarterly_totals[quarter].marketing_total, 3)
        operations = provider::pyvider::divide(local.quarterly_totals[quarter].operations_total, 3)
      }
    }
  }

  # Annual aggregations
  annual_summary = {
    total_development = provider::pyvider::sum([
      for quarter, totals in local.quarterly_totals : totals.development_total
    ])
    total_infrastructure = provider::pyvider::sum([
      for quarter, totals in local.quarterly_totals : totals.infrastructure_total
    ])
    total_marketing = provider::pyvider::sum([
      for quarter, totals in local.quarterly_totals : totals.marketing_total
    ])
    total_operations = provider::pyvider::sum([
      for quarter, totals in local.quarterly_totals : totals.operations_total
    ])

    grand_total = provider::pyvider::sum([
      local.annual_summary.total_development,
      local.annual_summary.total_infrastructure,
      local.annual_summary.total_marketing,
      local.annual_summary.total_operations
    ])

    # Department percentages of total
    department_percentages = {
      development = provider::pyvider::multiply(
        provider::pyvider::divide(local.annual_summary.total_development, local.annual_summary.grand_total),
        100
      )
      infrastructure = provider::pyvider::multiply(
        provider::pyvider::divide(local.annual_summary.total_infrastructure, local.annual_summary.grand_total),
        100
      )
      marketing = provider::pyvider::multiply(
        provider::pyvider::divide(local.annual_summary.total_marketing, local.annual_summary.grand_total),
        100
      )
      operations = provider::pyvider::multiply(
        provider::pyvider::divide(local.annual_summary.total_operations, local.annual_summary.grand_total),
        100
      )
    }
  }
}

# Budget variance analysis
variable "budget_vs_actual" {
  type = map(object({
    budgeted = list(number)
    actual = list(number)
  }))
  default = {
    development = {
      budgeted = [50000, 50000, 50000, 55000, 55000, 55000]
      actual = [45000, 52000, 48000, 55000, 58000, 60000]
    }
    marketing = {
      budgeted = [20000, 20000, 25000, 30000, 30000, 30000]
      actual = [15000, 18000, 22000, 28000, 32000, 35000]
    }
  }
}

locals {
  budget_analysis = {
    for department, budget_data in var.budget_vs_actual :
    department => {
      total_budgeted = provider::pyvider::sum(budget_data.budgeted)
      total_actual = provider::pyvider::sum(budget_data.actual)
      variance = provider::pyvider::subtract(local.budget_analysis[department].total_actual, local.budget_analysis[department].total_budgeted)
      variance_percentage = provider::pyvider::multiply(
        provider::pyvider::divide(local.budget_analysis[department].variance, local.budget_analysis[department].total_budgeted),
        100
      )
      is_over_budget = local.budget_analysis[department].variance > 0
      is_under_budget = local.budget_analysis[department].variance < 0

      # Monthly variance details
      monthly_variances = [
        for i in range(length(budget_data.budgeted)) :
        provider::pyvider::subtract(budget_data.actual[i], budget_data.budgeted[i])
      ]
      total_monthly_variance = provider::pyvider::sum(local.budget_analysis[department].monthly_variances)
    }
  }
}

output "cost_calculations" {
  value = {
    quarterly_totals = local.quarterly_totals
    annual_summary = local.annual_summary
    budget_analysis = local.budget_analysis
  }
}
```

### Infrastructure Resource Aggregation

```terraform
# Multi-environment resource totaling
variable "environment_resources" {
  type = map(map(object({
    instances = list(number)     # CPU cores per instance
    memory_gb = list(number)     # Memory GB per instance
    storage_gb = list(number)    # Storage GB per instance
    network_mbps = list(number)  # Network bandwidth per instance
  })))
  default = {
    production = {
      web_servers = {
        instances = [4, 4, 8, 8, 8]        # 5 web servers
        memory_gb = [16, 16, 32, 32, 32]   # Memory per server
        storage_gb = [100, 100, 200, 200, 200] # Storage per server
        network_mbps = [1000, 1000, 1000, 1000, 1000]
      }
      databases = {
        instances = [8, 16]                 # 2 database servers
        memory_gb = [64, 128]
        storage_gb = [500, 1000]
        network_mbps = [10000, 10000]
      }
      cache_servers = {
        instances = [2, 2, 2]               # 3 cache servers
        memory_gb = [8, 8, 8]
        storage_gb = [50, 50, 50]
        network_mbps = [1000, 1000, 1000]
      }
    }
    staging = {
      web_servers = {
        instances = [2, 2]
        memory_gb = [8, 8]
        storage_gb = [50, 50]
        network_mbps = [100, 100]
      }
      databases = {
        instances = [4]
        memory_gb = [32]
        storage_gb = [200]
        network_mbps = [1000]
      }
    }
  }
}

locals {
  environment_totals = {
    for env_name, env_resources in var.environment_resources :
    env_name => {
      service_totals = {
        for service_name, service_resources in env_resources :
        service_name => {
          total_cpu = provider::pyvider::sum(service_resources.instances)
          total_memory_gb = provider::pyvider::sum(service_resources.memory_gb)
          total_storage_gb = provider::pyvider::sum(service_resources.storage_gb)
          total_network_mbps = provider::pyvider::sum(service_resources.network_mbps)
          instance_count = length(service_resources.instances)

          # Average per instance
          avg_cpu_per_instance = provider::pyvider::divide(
            local.environment_totals[env_name].service_totals[service_name].total_cpu,
            local.environment_totals[env_name].service_totals[service_name].instance_count
          )
          avg_memory_per_instance = provider::pyvider::divide(
            local.environment_totals[env_name].service_totals[service_name].total_memory_gb,
            local.environment_totals[env_name].service_totals[service_name].instance_count
          )
        }
      }

      # Environment-wide totals
      env_total_cpu = provider::pyvider::sum([
        for service_name, totals in local.environment_totals[env_name].service_totals : totals.total_cpu
      ])
      env_total_memory_gb = provider::pyvider::sum([
        for service_name, totals in local.environment_totals[env_name].service_totals : totals.total_memory_gb
      ])
      env_total_storage_gb = provider::pyvider::sum([
        for service_name, totals in local.environment_totals[env_name].service_totals : totals.total_storage_gb
      ])
      env_total_network_mbps = provider::pyvider::sum([
        for service_name, totals in local.environment_totals[env_name].service_totals : totals.total_network_mbps
      ])
      env_total_instances = provider::pyvider::sum([
        for service_name, totals in local.environment_totals[env_name].service_totals : totals.instance_count
      ])
    }
  }

  # Global infrastructure summary
  global_infrastructure_totals = {
    total_cpu_across_all_envs = provider::pyvider::sum([
      for env_name, env_totals in local.environment_totals : env_totals.env_total_cpu
    ])
    total_memory_gb_across_all_envs = provider::pyvider::sum([
      for env_name, env_totals in local.environment_totals : env_totals.env_total_memory_gb
    ])
    total_storage_gb_across_all_envs = provider::pyvider::sum([
      for env_name, env_totals in local.environment_totals : env_totals.env_total_storage_gb
    ])
    total_network_mbps_across_all_envs = provider::pyvider::sum([
      for env_name, env_totals in local.environment_totals : env_totals.env_total_network_mbps
    ])
    total_instances_across_all_envs = provider::pyvider::sum([
      for env_name, env_totals in local.environment_totals : env_totals.env_total_instances
    ])

    # Resource distribution by environment
    environment_resource_percentages = {
      for env_name, env_totals in local.environment_totals :
      env_name => {
        cpu_percentage = provider::pyvider::multiply(
          provider::pyvider::divide(env_totals.env_total_cpu, local.global_infrastructure_totals.total_cpu_across_all_envs),
          100
        )
        memory_percentage = provider::pyvider::multiply(
          provider::pyvider::divide(env_totals.env_total_memory_gb, local.global_infrastructure_totals.total_memory_gb_across_all_envs),
          100
        )
        storage_percentage = provider::pyvider::multiply(
          provider::pyvider::divide(env_totals.env_total_storage_gb, local.global_infrastructure_totals.total_storage_gb_across_all_envs),
          100
        )
      }
    }
  }
}

output "resource_totals" {
  value = {
    environment_totals = local.environment_totals
    global_totals = local.global_infrastructure_totals
  }
}
```

### Performance Metrics Aggregation

```terraform
# Application performance monitoring aggregation
variable "application_metrics" {
  type = map(object({
    response_times_ms = list(number)
    error_counts = list(number)
    request_counts = list(number)
    cpu_usage_percent = list(number)
    memory_usage_mb = list(number)
  }))
  default = {
    api_service = {
      response_times_ms = [120, 145, 98, 156, 134, 187, 142, 165, 99, 178]
      error_counts = [2, 5, 1, 8, 3, 12, 4, 7, 1, 9]
      request_counts = [1500, 1750, 1200, 1800, 1650, 2000, 1400, 1900, 1300, 1850]
      cpu_usage_percent = [65, 72, 58, 78, 69, 85, 62, 79, 61, 82]
      memory_usage_mb = [512, 568, 489, 612, 545, 698, 502, 634, 478, 656]
    }
    web_frontend = {
      response_times_ms = [45, 52, 38, 61, 48, 67, 42, 58, 39, 64]
      error_counts = [1, 2, 0, 4, 1, 6, 2, 3, 0, 5]
      request_counts = [5000, 5500, 4800, 6200, 5300, 6800, 4900, 6100, 4700, 6500]
      cpu_usage_percent = [35, 42, 28, 48, 38, 55, 32, 46, 29, 52]
      memory_usage_mb = [256, 289, 234, 321, 267, 354, 245, 312, 228, 343]
    }
    background_worker = {
      response_times_ms = [2500, 2800, 2200, 3100, 2650, 3400, 2300, 2900, 2100, 3200]
      error_counts = [0, 1, 0, 2, 1, 3, 0, 1, 0, 2]
      request_counts = [50, 60, 45, 68, 55, 75, 48, 62, 42, 70]
      cpu_usage_percent = [15, 18, 12, 22, 16, 25, 13, 20, 11, 24]
      memory_usage_mb = [128, 145, 118, 162, 134, 178, 125, 156, 115, 171]
    }
  }
}

locals {
  application_summaries = {
    for app_name, metrics in var.application_metrics :
    app_name => {
      # Total metrics
      total_response_time_ms = provider::pyvider::sum(metrics.response_times_ms)
      total_errors = provider::pyvider::sum(metrics.error_counts)
      total_requests = provider::pyvider::sum(metrics.request_counts)
      total_cpu_usage = provider::pyvider::sum(metrics.cpu_usage_percent)
      total_memory_usage_mb = provider::pyvider::sum(metrics.memory_usage_mb)

      # Average metrics
      avg_response_time_ms = provider::pyvider::divide(
        local.application_summaries[app_name].total_response_time_ms,
        length(metrics.response_times_ms)
      )
      avg_cpu_usage_percent = provider::pyvider::divide(
        local.application_summaries[app_name].total_cpu_usage,
        length(metrics.cpu_usage_percent)
      )
      avg_memory_usage_mb = provider::pyvider::divide(
        local.application_summaries[app_name].total_memory_usage_mb,
        length(metrics.memory_usage_mb)
      )

      # Error rate calculation
      error_rate_percent = provider::pyvider::multiply(
        provider::pyvider::divide(local.application_summaries[app_name].total_errors, local.application_summaries[app_name].total_requests),
        100
      )

      # Performance scoring (lower is better for response times and errors)
      performance_score = provider::pyvider::divide(
        provider::pyvider::sum([
          local.application_summaries[app_name].avg_response_time_ms,
          local.application_summaries[app_name].total_errors,
          local.application_summaries[app_name].avg_cpu_usage_percent
        ]),
        3
      )
    }
  }

  # Cross-application aggregations
  system_wide_metrics = {
    total_system_errors = provider::pyvider::sum([
      for app_name, summary in local.application_summaries : summary.total_errors
    ])
    total_system_requests = provider::pyvider::sum([
      for app_name, summary in local.application_summaries : summary.total_requests
    ])
    total_system_memory_mb = provider::pyvider::sum([
      for app_name, summary in local.application_summaries : summary.total_memory_usage_mb
    ])

    # System-wide averages
    system_avg_response_time = provider::pyvider::divide(
      provider::pyvider::sum([
        for app_name, summary in local.application_summaries : summary.total_response_time_ms
      ]),
      provider::pyvider::sum([
        for app_name, metrics in var.application_metrics : length(metrics.response_times_ms)
      ])
    )

    system_error_rate = provider::pyvider::multiply(
      provider::pyvider::divide(local.system_wide_metrics.total_system_errors, local.system_wide_metrics.total_system_requests),
      100
    )
  }
}

output "performance_aggregation" {
  value = {
    application_summaries = local.application_summaries
    system_metrics = local.system_wide_metrics
  }
}
```

### Dynamic List Aggregation and Conditional Sums

```terraform
# Dynamic cost calculation based on conditions
variable "service_usage" {
  type = map(object({
    base_cost = number
    usage_hours = list(number)
    hourly_rates = list(number)
    discount_eligible = bool
    environment_tier = string
  }))
  default = {
    compute_service = {
      base_cost = 50
      usage_hours = [24, 18, 32, 28, 22, 30, 26]  # Daily hours for a week
      hourly_rates = [0.10, 0.10, 0.15, 0.12, 0.10, 0.15, 0.12]  # Varying rates
      discount_eligible = true
      environment_tier = "production"
    }
    storage_service = {
      base_cost = 25
      usage_hours = [24, 24, 24, 24, 24, 24, 24]  # Always on
      hourly_rates = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
      discount_eligible = false
      environment_tier = "production"
    }
    network_service = {
      base_cost = 15
      usage_hours = [8, 12, 6, 14, 10, 16, 9]    # Variable usage
      hourly_rates = [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
      discount_eligible = true
      environment_tier = "development"
    }
  }
}

locals {
  service_costs = {
    for service_name, usage in var.service_usage :
    service_name => {
      # Calculate hourly costs for each day
      daily_costs = [
        for i in range(length(usage.usage_hours)) :
        provider::pyvider::multiply(usage.usage_hours[i], usage.hourly_rates[i])
      ]

      # Sum up all variable costs
      total_variable_cost = provider::pyvider::sum(local.service_costs[service_name].daily_costs)
      total_usage_hours = provider::pyvider::sum(usage.usage_hours)

      # Apply discounts conditionally
      discount_rate = usage.discount_eligible && usage.environment_tier == "production" ? 0.1 : 0
      discount_amount = provider::pyvider::multiply(local.service_costs[service_name].total_variable_cost, local.service_costs[service_name].discount_rate)

      # Final calculations
      total_before_discount = provider::pyvider::add(usage.base_cost, local.service_costs[service_name].total_variable_cost)
      total_after_discount = provider::pyvider::subtract(local.service_costs[service_name].total_before_discount, local.service_costs[service_name].discount_amount)

      # Metrics
      average_hourly_rate = provider::pyvider::divide(
        provider::pyvider::sum(usage.hourly_rates),
        length(usage.hourly_rates)
      )
      cost_per_hour = provider::pyvider::divide(local.service_costs[service_name].total_after_discount, local.service_costs[service_name].total_usage_hours)
    }
  }

  # Service tier aggregations
  tier_summaries = {
    production_services = {
      service_names = [for name, usage in var.service_usage : name if usage.environment_tier == "production"]
      total_cost = provider::pyvider::sum([
        for name, costs in local.service_costs : costs.total_after_discount
        if var.service_usage[name].environment_tier == "production"
      ])
      total_usage_hours = provider::pyvider::sum([
        for name, costs in local.service_costs : costs.total_usage_hours
        if var.service_usage[name].environment_tier == "production"
      ])
    }

    development_services = {
      service_names = [for name, usage in var.service_usage : name if usage.environment_tier == "development"]
      total_cost = provider::pyvider::sum([
        for name, costs in local.service_costs : costs.total_after_discount
        if var.service_usage[name].environment_tier == "development"
      ])
      total_usage_hours = provider::pyvider::sum([
        for name, costs in local.service_costs : costs.total_usage_hours
        if var.service_usage[name].environment_tier == "development"
      ])
    }
  }

  # Overall totals
  grand_totals = {
    all_services_cost = provider::pyvider::sum([
      for service_name, costs in local.service_costs : costs.total_after_discount
    ])
    all_services_usage_hours = provider::pyvider::sum([
      for service_name, costs in local.service_costs : costs.total_usage_hours
    ])
    all_discounts_applied = provider::pyvider::sum([
      for service_name, costs in local.service_costs : costs.discount_amount
    ])

    # Cost distribution
    production_cost_percentage = provider::pyvider::multiply(
      provider::pyvider::divide(local.tier_summaries.production_services.total_cost, local.grand_totals.all_services_cost),
      100
    )
    development_cost_percentage = provider::pyvider::multiply(
      provider::pyvider::divide(local.tier_summaries.development_services.total_cost, local.grand_totals.all_services_cost),
      100
    )
  }
}

output "dynamic_calculations" {
  value = {
    service_costs = local.service_costs
    tier_summaries = local.tier_summaries
    grand_totals = local.grand_totals
  }
}
```

## Signature

`sum(numbers: list[number]) -> number`

## Arguments

- **`numbers`** (list[number], required) - A list of numbers to sum. Can contain integers and floats. Returns `null` if the list is `null`. Returns `0` for empty lists.

## Return Value

Returns the sum of all numbers in the list as a number. The return type is automatically optimized:
- If the result is a whole number (e.g., `15.0`), returns an integer (`15`)
- If the result has decimal places (e.g., `15.75`), returns a float (`15.75`)
- Returns `null` if the input list is `null`
- Returns `0` for empty lists

## Common Patterns

### Budget Totaling
```terraform
variable "monthly_costs" {
  type = list(number)
  default = [1200.00, 800.50, 450.25, 300.00]
}

locals {
  total_monthly_budget = provider::pyvider::sum(var.monthly_costs)
}

resource "pyvider_file_content" "budget_summary" {
  filename = "/tmp/budget.txt"
  content  = "Total monthly budget: $${local.total_monthly_budget}"
}
```

### Resource Aggregation
```terraform
variable "server_cpu_cores" {
  type = list(number)
  default = [4, 8, 16, 2]
}

locals {
  total_cpu_capacity = provider::pyvider::sum(var.server_cpu_cores)
}
```

### Dynamic Calculation
```terraform
locals {
  usage_metrics = [
    var.app1_cpu_usage,
    var.app2_cpu_usage,
    var.app3_cpu_usage
  ]
  total_cpu_usage = provider::pyvider::sum(local.usage_metrics)
}
```

## Best Practices

### 1. Validate List Contents
```terraform
variable "values" {
  type = list(number)
  validation {
    condition     = length(var.values) > 0
    error_message = "Values list cannot be empty."
  }
}

locals {
  total = provider::pyvider::sum(var.values)
}
```

### 2. Handle Null Lists
```terraform
locals {
  safe_total = var.optional_values != null ? provider::pyvider::sum(var.optional_values) : 0
}
```

## Related Functions

- [`add`](./add.md) - Add two numbers
- [`max`](./max.md) - Find maximum value in a list
- [`min`](./min.md) - Find minimum value in a list
- [`round`](./round.md) - Round the result to specific precision
