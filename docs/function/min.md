---
page_title: "Function: min"
description: |-
  Finds the minimum value in a list of numbers with error handling for empty lists
---

# min (Function)

> Finds the smallest numeric value in a list with null-safe handling and empty list validation

The `min` function finds and returns the smallest number from a list of numbers. It requires at least one number in the list and handles null values gracefully.

## When to Use This

- **Threshold calculations**: Find minimum acceptable values
- **Resource optimization**: Find lowest resource usage or cost
- **Performance metrics**: Identify best performance values
- **Capacity planning**: Find minimum requirements
- **Quality assurance**: Identify minimum quality metrics

**Anti-patterns (when NOT to use):**
- Empty lists (will cause an error)
- Single-value comparisons (just use the value directly)
- Non-numeric data (ensure list contains only numbers)

## Quick Start

```terraform
# Simple minimum
locals {
  prices = [19.99, 15.50, 22.00, 12.75]
  lowest_price = provider::pyvider::min(local.prices)  # Returns: 12.75
}

# Resource minimum
variable "cpu_requirements" {
  default = [2, 4, 1, 8]
}

locals {
  min_cpu_needed = provider::pyvider::min(var.cpu_requirements)  # Returns: 1
}
```

## Examples

### Basic Usage

```terraform
# Simple minimum value finding
locals {
  basic_examples = {
    prices = [19.99, 15.50, 22.00, 12.75, 18.25]
    lowest_price = provider::pyvider::min(local.basic_examples.prices)  # 12.75

    scores = [85, 92, 78, 95, 88]
    minimum_score = provider::pyvider::min(local.basic_examples.scores)  # 78

    temperatures = [-5, 12, 8, -2, 15, 3]
    lowest_temp = provider::pyvider::min(local.basic_examples.temperatures)  # -5

    response_times = [250.5, 180.2, 320.8, 195.1, 275.6]
    fastest_response = provider::pyvider::min(local.basic_examples.response_times)  # 180.2
  }

  # Working with variables
  cpu_usage_samples = [45, 62, 38, 71, 55, 42, 68]
  min_cpu_usage = provider::pyvider::min(local.cpu_usage_samples)  # 38

  # Mixed integer and float values
  mixed_values = [10, 7.5, 12, 9.2, 8]
  minimum_mixed = provider::pyvider::min(local.mixed_values)  # 7.5

  # Single value list
  single_value = [42]
  single_min = provider::pyvider::min(local.single_value)  # 42
}

# Error prevention with validation
variable "user_ratings" {
  type = list(number)
  default = []
}

locals {
  # Safe minimum calculation with empty list check
  has_ratings = length(var.user_ratings) > 0
  min_rating = local.has_ratings ? provider::pyvider::min(var.user_ratings) : null

  # Conditional minimum with fallback
  default_values = [1, 2, 3]
  safe_minimum = length(var.user_ratings) > 0 ?
    provider::pyvider::min(var.user_ratings) :
    provider::pyvider::min(local.default_values)
}

output "basic_min_examples" {
  value = {
    examples = local.basic_examples
    min_cpu = local.min_cpu_usage
    mixed_minimum = local.minimum_mixed
    safe_handling = {
      has_data = local.has_ratings
      minimum = local.min_rating
      fallback_minimum = local.safe_minimum
    }
  }
}
```

### Resource Capacity Planning

```terraform
# Server resource optimization
variable "server_configurations" {
  type = list(object({
    server_type = string
    cpu_cores = number
    memory_gb = number
    storage_gb = number
    cost_per_hour = number
  }))
  default = [
    {
      server_type = "micro"
      cpu_cores = 1
      memory_gb = 2
      storage_gb = 20
      cost_per_hour = 0.012
    },
    {
      server_type = "small"
      cpu_cores = 2
      memory_gb = 4
      storage_gb = 40
      cost_per_hour = 0.024
    },
    {
      server_type = "medium"
      cpu_cores = 4
      memory_gb = 8
      storage_gb = 80
      cost_per_hour = 0.048
    },
    {
      server_type = "large"
      cpu_cores = 8
      memory_gb = 16
      storage_gb = 160
      cost_per_hour = 0.096
    }
  ]
}

# Find minimum resource requirements
locals {
  resource_analysis = {
    # Extract individual resource lists
    cpu_options = [for config in var.server_configurations : config.cpu_cores]
    memory_options = [for config in var.server_configurations : config.memory_gb]
    storage_options = [for config in var.server_configurations : config.storage_gb]
    cost_options = [for config in var.server_configurations : config.cost_per_hour]

    # Find minimum values for each resource type
    min_cpu = provider::pyvider::min(local.resource_analysis.cpu_options)         # 1
    min_memory = provider::pyvider::min(local.resource_analysis.memory_options)   # 2
    min_storage = provider::pyvider::min(local.resource_analysis.storage_options) # 20
    min_cost = provider::pyvider::min(local.resource_analysis.cost_options)       # 0.012

    # Find most cost-effective configuration
    cheapest_server = [
      for config in var.server_configurations : config
      if config.cost_per_hour == local.resource_analysis.min_cost
    ][0]

    # Calculate resource efficiency (performance per dollar)
    efficiency_scores = [
      for config in var.server_configurations : {
        server_type = config.server_type
        cpu_per_dollar = config.cpu_cores / config.cost_per_hour
        memory_per_dollar = config.memory_gb / config.cost_per_hour
        storage_per_dollar = config.storage_gb / config.cost_per_hour
        overall_score = (config.cpu_cores + config.memory_gb + config.storage_gb) / config.cost_per_hour
      }
    ]

    # Find minimum efficiency scores
    cpu_efficiency_scores = [for score in local.resource_analysis.efficiency_scores : score.cpu_per_dollar]
    min_cpu_efficiency = provider::pyvider::min(local.resource_analysis.cpu_efficiency_scores)

    memory_efficiency_scores = [for score in local.resource_analysis.efficiency_scores : score.memory_per_dollar]
    min_memory_efficiency = provider::pyvider::min(local.resource_analysis.memory_efficiency_scores)
  }

  # Workload-specific minimum requirements
  workload_requirements = [
    { name = "web-frontend", min_cpu = 2, min_memory = 4, min_storage = 20 },
    { name = "api-backend", min_cpu = 4, min_memory = 8, min_storage = 40 },
    { name = "database", min_cpu = 8, min_memory = 16, min_storage = 100 },
    { name = "cache", min_cpu = 2, min_memory = 8, min_storage = 20 }
  ]

  workload_analysis = {
    for workload in local.workload_requirements :
    workload.name => {
      # Find servers that meet minimum requirements
      suitable_servers = [
        for config in var.server_configurations : config
        if config.cpu_cores >= workload.min_cpu &&
           config.memory_gb >= workload.min_memory &&
           config.storage_gb >= workload.min_storage
      ]

      # Find minimum cost among suitable servers
      suitable_costs = [for server in local.workload_analysis[workload.name].suitable_servers : server.cost_per_hour]
      min_suitable_cost = length(local.workload_analysis[workload.name].suitable_costs) > 0 ?
        provider::pyvider::min(local.workload_analysis[workload.name].suitable_costs) : null

      # Get the cheapest suitable server
      cheapest_suitable = length(local.workload_analysis[workload.name].suitable_servers) > 0 ? [
        for server in local.workload_analysis[workload.name].suitable_servers : server
        if server.cost_per_hour == local.workload_analysis[workload.name].min_suitable_cost
      ][0] : null

      can_be_hosted = length(local.workload_analysis[workload.name].suitable_servers) > 0
    }
  }
}

output "resource_planning" {
  value = {
    resource_minimums = local.resource_analysis
    workload_optimization = local.workload_analysis
  }
}
```

### Performance Threshold Management

```terraform
# Service performance monitoring
variable "service_metrics" {
  type = map(object({
    response_times_ms = list(number)
    error_rates_percent = list(number)
    cpu_usage_samples = list(number)
    memory_usage_samples = list(number)
    throughput_rps = list(number)
  }))
  default = {
    api_service = {
      response_times_ms = [120, 95, 140, 88, 105, 130, 92, 115]
      error_rates_percent = [0.2, 0.1, 0.3, 0.15, 0.08, 0.25, 0.12, 0.18]
      cpu_usage_samples = [45, 52, 38, 61, 48, 55, 42, 50]
      memory_usage_samples = [65, 72, 58, 78, 62, 69, 60, 66]
      throughput_rps = [850, 920, 780, 1050, 890, 960, 820, 910]
    }
    database = {
      response_times_ms = [25, 18, 32, 22, 28, 20, 35, 24]
      error_rates_percent = [0.05, 0.02, 0.08, 0.03, 0.06, 0.04, 0.07, 0.02]
      cpu_usage_samples = [30, 28, 35, 32, 29, 33, 31, 27]
      memory_usage_samples = [82, 85, 79, 87, 80, 84, 81, 83]
      throughput_rps = [1200, 1350, 1100, 1280, 1320, 1180, 1250, 1380]
    }
    cache_service = {
      response_times_ms = [5, 3, 7, 4, 6, 2, 8, 5]
      error_rates_percent = [0.01, 0.0, 0.02, 0.01, 0.0, 0.01, 0.02, 0.0]
      cpu_usage_samples = [15, 18, 12, 22, 16, 20, 14, 19]
      memory_usage_samples = [45, 48, 42, 52, 44, 50, 43, 47]
      throughput_rps = [2800, 3100, 2600, 2950, 3050, 2750, 2900, 3200]
    }
  }
}

# Analyze performance minimums and thresholds
locals {
  performance_analysis = {
    for service_name, metrics in var.service_metrics :
    service_name => {
      # Find minimum (best) performance values
      min_response_time = provider::pyvider::min(metrics.response_times_ms)
      min_error_rate = provider::pyvider::min(metrics.error_rates_percent)
      min_cpu_usage = provider::pyvider::min(metrics.cpu_usage_samples)
      min_memory_usage = provider::pyvider::min(metrics.memory_usage_samples)
      min_throughput = provider::pyvider::min(metrics.throughput_rps)

      # Calculate baseline performance (minimum values represent best performance)
      performance_baselines = {
        best_response_time = local.performance_analysis[service_name].min_response_time
        lowest_error_rate = local.performance_analysis[service_name].min_error_rate
        lowest_cpu_usage = local.performance_analysis[service_name].min_cpu_usage
        lowest_memory_usage = local.performance_analysis[service_name].min_memory_usage
        minimum_throughput = local.performance_analysis[service_name].min_throughput
      }

      # Performance improvement potential
      current_avg_response = sum(metrics.response_times_ms) / length(metrics.response_times_ms)
      improvement_potential = local.performance_analysis[service_name].current_avg_response - local.performance_analysis[service_name].min_response_time

      # SLA compliance (assuming SLAs are set at 150% of minimum observed values)
      sla_thresholds = {
        max_response_time = local.performance_analysis[service_name].min_response_time * 1.5
        max_error_rate = local.performance_analysis[service_name].min_error_rate + 0.1
        max_cpu_usage = local.performance_analysis[service_name].min_cpu_usage + 20
        max_memory_usage = local.performance_analysis[service_name].min_memory_usage + 15
      }

      # Check SLA violations
      response_time_violations = length([
        for rt in metrics.response_times_ms : rt
        if rt > local.performance_analysis[service_name].sla_thresholds.max_response_time
      ])

      error_rate_violations = length([
        for er in metrics.error_rates_percent : er
        if er > local.performance_analysis[service_name].sla_thresholds.max_error_rate
      ])

      # Performance stability score (lower variation from minimum is better)
      response_time_variance = [
        for rt in metrics.response_times_ms :
        abs(rt - local.performance_analysis[service_name].min_response_time)
      ]
      min_variance = provider::pyvider::min(local.performance_analysis[service_name].response_time_variance)
      avg_variance = sum(local.performance_analysis[service_name].response_time_variance) / length(local.performance_analysis[service_name].response_time_variance)

      stability_score = local.performance_analysis[service_name].min_variance == 0 ? 100 :
        round((1 - (local.performance_analysis[service_name].avg_variance / local.performance_analysis[service_name].min_response_time)) * 100, 1)
    }
  }

  # System-wide performance summary
  system_performance = {
    # Find service with best (minimum) response times
    all_min_response_times = [for service_name, analysis in local.performance_analysis : analysis.min_response_time]
    best_response_time_overall = provider::pyvider::min(local.system_performance.all_min_response_times)

    # Find service with lowest error rates
    all_min_error_rates = [for service_name, analysis in local.performance_analysis : analysis.min_error_rate]
    best_error_rate_overall = provider::pyvider::min(local.system_performance.all_min_error_rates)

    # Find most efficient resource usage
    all_min_cpu_usage = [for service_name, analysis in local.performance_analysis : analysis.min_cpu_usage]
    lowest_cpu_usage_overall = provider::pyvider::min(local.system_performance.all_min_cpu_usage)

    all_min_memory_usage = [for service_name, analysis in local.performance_analysis : analysis.min_memory_usage]
    lowest_memory_usage_overall = provider::pyvider::min(local.system_performance.all_min_memory_usage)

    # Performance leaders (services achieving system minimums)
    response_time_leader = [
      for service_name, analysis in local.performance_analysis : service_name
      if analysis.min_response_time == local.system_performance.best_response_time_overall
    ][0]

    error_rate_leader = [
      for service_name, analysis in local.performance_analysis : service_name
      if analysis.min_error_rate == local.system_performance.best_error_rate_overall
    ][0]
  }
}

output "performance_thresholds" {
  value = {
    service_analysis = local.performance_analysis
    system_summary = local.system_performance
  }
}
```

### Cost Optimization Analysis

```terraform
# Multi-cloud cost comparison
variable "cloud_pricing" {
  type = map(object({
    compute_instances = list(object({
      type = string
      vcpus = number
      memory_gb = number
      hourly_cost = number
    }))
    storage_costs_per_gb = list(number)
    network_costs_per_gb = list(number)
  }))
  default = {
    aws = {
      compute_instances = [
        { type = "t3.micro", vcpus = 2, memory_gb = 1, hourly_cost = 0.0104 },
        { type = "t3.small", vcpus = 2, memory_gb = 2, hourly_cost = 0.0208 },
        { type = "t3.medium", vcpus = 2, memory_gb = 4, hourly_cost = 0.0416 },
        { type = "m5.large", vcpus = 2, memory_gb = 8, hourly_cost = 0.096 }
      ]
      storage_costs_per_gb = [0.10, 0.045, 0.125]  # Different storage types
      network_costs_per_gb = [0.09, 0.085, 0.05]  # Different data transfer types
    }
    azure = {
      compute_instances = [
        { type = "B1s", vcpus = 1, memory_gb = 1, hourly_cost = 0.0104 },
        { type = "B1ms", vcpus = 1, memory_gb = 2, hourly_cost = 0.0208 },
        { type = "B2s", vcpus = 2, memory_gb = 4, hourly_cost = 0.0416 },
        { type = "D2s_v3", vcpus = 2, memory_gb = 8, hourly_cost = 0.088 }
      ]
      storage_costs_per_gb = [0.095, 0.05, 0.12]
      network_costs_per_gb = [0.087, 0.08, 0.05]
    }
    gcp = {
      compute_instances = [
        { type = "f1-micro", vcpus = 1, memory_gb = 0.6, hourly_cost = 0.0076 },
        { type = "g1-small", vcpus = 1, memory_gb = 1.7, hourly_cost = 0.027 },
        { type = "n1-standard-1", vcpus = 1, memory_gb = 3.75, hourly_cost = 0.0475 },
        { type = "n1-standard-2", vcpus = 2, memory_gb = 7.5, hourly_cost = 0.095 }
      ]
      storage_costs_per_gb = [0.08, 0.04, 0.10]
      network_costs_per_gb = [0.085, 0.08, 0.045]
    }
  }
}

# Find minimum costs across all cloud providers
locals {
  cost_optimization = {
    # Extract all compute costs for comparison
    all_compute_costs = flatten([
      for provider, pricing in var.cloud_pricing : [
        for instance in pricing.compute_instances : {
          provider = provider
          instance_type = instance.type
          vcpus = instance.vcpus
          memory_gb = instance.memory_gb
          hourly_cost = instance.hourly_cost
          cost_per_vcpu = instance.hourly_cost / instance.vcpus
          cost_per_gb_memory = instance.hourly_cost / instance.memory_gb
        }
      ]
    ])

    # Find absolute minimums
    all_hourly_costs = [for instance in local.cost_optimization.all_compute_costs : instance.hourly_cost]
    min_hourly_cost = provider::pyvider::min(local.cost_optimization.all_hourly_costs)

    all_vcpu_costs = [for instance in local.cost_optimization.all_compute_costs : instance.cost_per_vcpu]
    min_cost_per_vcpu = provider::pyvider::min(local.cost_optimization.all_vcpu_costs)

    all_memory_costs = [for instance in local.cost_optimization.all_compute_costs : instance.cost_per_gb_memory]
    min_cost_per_gb_memory = provider::pyvider::min(local.cost_optimization.all_memory_costs)

    # Find cheapest options
    cheapest_overall = [
      for instance in local.cost_optimization.all_compute_costs : instance
      if instance.hourly_cost == local.cost_optimization.min_hourly_cost
    ][0]

    most_vcpu_efficient = [
      for instance in local.cost_optimization.all_compute_costs : instance
      if instance.cost_per_vcpu == local.cost_optimization.min_cost_per_vcpu
    ][0]

    most_memory_efficient = [
      for instance in local.cost_optimization.all_compute_costs : instance
      if instance.cost_per_gb_memory == local.cost_optimization.min_cost_per_gb_memory
    ][0]

    # Storage cost analysis
    storage_analysis = {
      for provider, pricing in var.cloud_pricing :
      provider => {
        min_storage_cost = provider::pyvider::min(pricing.storage_costs_per_gb)
        min_network_cost = provider::pyvider::min(pricing.network_costs_per_gb)
        total_min_cost = local.cost_optimization.storage_analysis[provider].min_storage_cost +
                        local.cost_optimization.storage_analysis[provider].min_network_cost
      }
    }

    # Find globally cheapest storage and network
    all_storage_costs = flatten([for provider, pricing in var.cloud_pricing : pricing.storage_costs_per_gb])
    min_storage_cost_global = provider::pyvider::min(local.cost_optimization.all_storage_costs)

    all_network_costs = flatten([for provider, pricing in var.cloud_pricing : pricing.network_costs_per_gb])
    min_network_cost_global = provider::pyvider::min(local.cost_optimization.all_network_costs)

    # Provider-specific minimums
    provider_minimums = {
      for provider, pricing in var.cloud_pricing :
      provider => {
        compute_costs = [for instance in pricing.compute_instances : instance.hourly_cost]
        min_compute_cost = provider::pyvider::min(local.cost_optimization.provider_minimums[provider].compute_costs)

        min_storage_cost = provider::pyvider::min(pricing.storage_costs_per_gb)
        min_network_cost = provider::pyvider::min(pricing.network_costs_per_gb)

        cheapest_compute_instance = [
          for instance in pricing.compute_instances : instance
          if instance.hourly_cost == local.cost_optimization.provider_minimums[provider].min_compute_cost
        ][0]
      }
    }

    # Cost savings analysis
    cost_savings = {
      # Potential savings by choosing cheapest options
      hourly_savings_vs_average = local.cost_optimization.min_hourly_cost - (
        sum(local.cost_optimization.all_hourly_costs) / length(local.cost_optimization.all_hourly_costs)
      )

      # Monthly and annual projections
      monthly_savings = local.cost_optimization.cost_savings.hourly_savings_vs_average * 24 * 30
      annual_savings = local.cost_optimization.cost_savings.monthly_savings * 12

      storage_savings_per_tb = (local.cost_optimization.min_storage_cost_global * 1000) -
        ((sum(local.cost_optimization.all_storage_costs) / length(local.cost_optimization.all_storage_costs)) * 1000)
    }
  }
}

output "cost_optimization" {
  value = local.cost_optimization
}

## Signature

`min(numbers: list[number]) -> number`

## Arguments

- **`numbers`** (list[number], required) - A list of numbers to find the minimum from. Must contain at least one number. Returns `null` if the list is `null`. **Raises an error** if the list is empty.

## Return Value

Returns the smallest number from the list. Preserves the original type (integer or float) of the minimum value.
- Returns `null` if the input list is `null`
- **Raises an error** if the list is empty

## Error Handling

```terraform
# This will cause an error
locals {
  # Error: min() requires at least one number
  # bad_result = provider::pyvider::min([])
}

# Safe usage with validation
variable "values" {
  type = list(number)
}

locals {
  minimum = length(var.values) > 0 ? provider::pyvider::min(var.values) : null
}
```

## Related Functions

- [`max`](./max.md) - Find maximum value in a list
- [`sum`](./sum.md) - Calculate sum of all values in a list