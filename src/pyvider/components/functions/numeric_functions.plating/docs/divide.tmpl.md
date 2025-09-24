---
page_title: "Function: divide"
description: |-
  Divides two numbers with division-by-zero protection and intelligent type conversion
---

# divide (Function)

> Performs division of two numeric values with null-safe handling, division-by-zero protection, and automatic type optimization

The `divide` function divides the first number by the second number and returns the result. It includes division-by-zero protection, handles null values gracefully, and automatically converts floating-point results to integers when they represent whole numbers.

## When to Use This

- **Rate calculations**: Calculate rates, ratios, or averages
- **Resource allocation**: Distribute resources evenly
- **Percentage calculations**: Convert values to percentages
- **Unit conversions**: Convert between different units
- **Performance metrics**: Calculate per-unit metrics

**Anti-patterns (when NOT to use):**
- Division by potentially zero values without error handling
- Complex mathematical operations (use multiple function calls)
- Integer division when you need exact integer results (check result type)
- String operations (use string functions)

## Quick Start

```terraform
# Simple division
locals {
  average = provider::pyvider::divide(100, 4)  # Returns: 25
}

# Rate calculation
variable "total_requests" {
  default = 1000
}

variable "time_period" {
  default = 60  # seconds
}

locals {
  requests_per_second = provider::pyvider::divide(var.total_requests, var.time_period)  # Returns: 16.67
}
```

## Examples

### Basic Usage

```terraform
# Basic division operations
locals {
  basic_operations = {
    integers = provider::pyvider::divide(20, 4)           # 5
    floats = provider::pyvider::divide(15.0, 3.0)         # 5.0 (becomes 5)
    mixed = provider::pyvider::divide(10, 3.0)            # 3.33333...
    decimal_result = provider::pyvider::divide(22, 7)     # 3.14285...
    negative = provider::pyvider::divide(-15, 3)          # -5
    both_negative = provider::pyvider::divide(-20, -4)    # 5
    fraction = provider::pyvider::divide(1, 8)            # 0.125
  }

  # Percentage calculations
  percentage_examples = {
    convert_to_percent = provider::pyvider::divide(85, 100)      # 0.85 (85%)
    success_rate = provider::pyvider::divide(450, 500)          # 0.9 (90%)
    utilization = provider::pyvider::divide(1800, 2400)         # 0.75 (75%)
    efficiency = provider::pyvider::divide(240, 300)            # 0.8 (80%)
  }

  # Unit conversions
  conversions = {
    mb_to_gb = provider::pyvider::divide(2048, 1024)            # 2 (MB to GB)
    seconds_to_minutes = provider::pyvider::divide(300, 60)     # 5
    bytes_to_kb = provider::pyvider::divide(8192, 1024)         # 8
    milliseconds_to_seconds = provider::pyvider::divide(5500, 1000) # 5.5
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

### Performance and Rate Calculations

```terraform
# System performance metrics
variable "system_metrics" {
  type = map(object({
    total_requests = number
    time_period_seconds = number
    total_bytes_transferred = number
    error_count = number
    response_time_total_ms = number
  }))
  default = {
    web_server = {
      total_requests = 50000
      time_period_seconds = 3600  # 1 hour
      total_bytes_transferred = 2147483648  # 2GB
      error_count = 250
      response_time_total_ms = 125000
    }
    api_gateway = {
      total_requests = 25000
      time_period_seconds = 1800  # 30 minutes
      total_bytes_transferred = 524288000  # 500MB
      error_count = 75
      response_time_total_ms = 50000
    }
    database = {
      total_requests = 100000
      time_period_seconds = 7200  # 2 hours
      total_bytes_transferred = 1073741824  # 1GB
      error_count = 10
      response_time_total_ms = 200000
    }
  }
}

locals {
  performance_metrics = {
    for service_name, metrics in var.system_metrics :
    service_name => {
      # Request rates
      requests_per_second = provider::pyvider::divide(metrics.total_requests, metrics.time_period_seconds)
      requests_per_minute = provider::pyvider::multiply(
        provider::pyvider::divide(metrics.total_requests, metrics.time_period_seconds),
        60
      )

      # Data transfer rates
      bytes_per_second = provider::pyvider::divide(metrics.total_bytes_transferred, metrics.time_period_seconds)
      mb_per_second = provider::pyvider::divide(
        provider::pyvider::divide(metrics.total_bytes_transferred, 1048576),  # bytes to MB
        metrics.time_period_seconds
      )

      # Error rates
      error_percentage = provider::pyvider::multiply(
        provider::pyvider::divide(metrics.error_count, metrics.total_requests),
        100
      )
      errors_per_minute = provider::pyvider::multiply(
        provider::pyvider::divide(metrics.error_count, metrics.time_period_seconds),
        60
      )

      # Response time metrics
      average_response_time_ms = provider::pyvider::divide(metrics.response_time_total_ms, metrics.total_requests)
      average_response_time_seconds = provider::pyvider::divide(
        local.performance_metrics[service_name].average_response_time_ms,
        1000
      )

      # Efficiency metrics
      successful_requests = provider::pyvider::subtract(metrics.total_requests, metrics.error_count)
      success_rate = provider::pyvider::multiply(
        provider::pyvider::divide(local.performance_metrics[service_name].successful_requests, metrics.total_requests),
        100
      )
    }
  }

  # Comparative analysis
  performance_comparison = {
    highest_rps = max([for service, metrics in local.performance_metrics : metrics.requests_per_second])
    lowest_error_rate = min([for service, metrics in local.performance_metrics : metrics.error_percentage])
    average_success_rate = provider::pyvider::divide(
      sum([for service, metrics in local.performance_metrics : metrics.success_rate]),
      length(local.performance_metrics)
    )
  }
}

# SLA compliance calculations
variable "sla_targets" {
  type = object({
    max_response_time_ms = number
    min_uptime_percentage = number
    max_error_rate_percentage = number
    min_throughput_rps = number
  })
  default = {
    max_response_time_ms = 500
    min_uptime_percentage = 99.9
    max_error_rate_percentage = 0.1
    min_throughput_rps = 100
  }
}

locals {
  sla_compliance = {
    for service_name, metrics in local.performance_metrics :
    service_name => {
      response_time_compliance = metrics.average_response_time_ms <= var.sla_targets.max_response_time_ms
      error_rate_compliance = metrics.error_percentage <= var.sla_targets.max_error_rate_percentage
      throughput_compliance = metrics.requests_per_second >= var.sla_targets.min_throughput_rps
      uptime_compliance = metrics.success_rate >= var.sla_targets.min_uptime_percentage

      # Overall compliance score (0-100)
      compliance_score = provider::pyvider::multiply(
        provider::pyvider::divide(
          length([
            for check in [
              local.sla_compliance[service_name].response_time_compliance,
              local.sla_compliance[service_name].error_rate_compliance,
              local.sla_compliance[service_name].throughput_compliance,
              local.sla_compliance[service_name].uptime_compliance
            ] : check if check == true
          ]),
          4  # total number of checks
        ),
        100
      )
    }
  }
}

output "performance_calculations" {
  value = {
    metrics = local.performance_metrics
    comparison = local.performance_comparison
    sla_compliance = local.sla_compliance
  }
}
```

### Resource Allocation and Distribution

```terraform
# Budget allocation across teams/projects
variable "budget_allocation" {
  type = object({
    total_annual_budget = number
    departments = map(object({
      headcount = number
      priority_weight = number
      base_allocation_percentage = number
    }))
  })
  default = {
    total_annual_budget = 2500000
    departments = {
      engineering = {
        headcount = 25
        priority_weight = 0.4
        base_allocation_percentage = 45
      }
      product = {
        headcount = 8
        priority_weight = 0.25
        base_allocation_percentage = 20
      }
      marketing = {
        headcount = 12
        priority_weight = 0.2
        base_allocation_percentage = 18
      }
      operations = {
        headcount = 6
        priority_weight = 0.15
        base_allocation_percentage = 17
      }
    }
  }
}

locals {
  budget_distribution = {
    total_headcount = sum([for dept, config in var.budget_allocation.departments : config.headcount])

    # Base allocation by percentage
    base_allocations = {
      for dept_name, dept_config in var.budget_allocation.departments :
      dept_name => {
        base_amount = provider::pyvider::multiply(
          var.budget_allocation.total_annual_budget,
          provider::pyvider::divide(dept_config.base_allocation_percentage, 100)
        )
        per_person_base = provider::pyvider::divide(
          local.budget_distribution.base_allocations[dept_name].base_amount,
          dept_config.headcount
        )
      }
    }

    # Per-capita allocation
    per_capita_allocations = {
      for dept_name, dept_config in var.budget_allocation.departments :
      dept_name => {
        per_capita_amount = provider::pyvider::divide(
          var.budget_allocation.total_annual_budget,
          local.budget_distribution.total_headcount
        )
        total_per_capita = provider::pyvider::multiply(
          local.budget_distribution.per_capita_allocations[dept_name].per_capita_amount,
          dept_config.headcount
        )
      }
    }

    # Weighted allocation
    total_weight = sum([for dept, config in var.budget_allocation.departments : config.priority_weight])
    weighted_allocations = {
      for dept_name, dept_config in var.budget_allocation.departments :
      dept_name => {
        weight_percentage = provider::pyvider::divide(dept_config.priority_weight, local.budget_distribution.total_weight)
        weighted_amount = provider::pyvider::multiply(
          var.budget_allocation.total_annual_budget,
          local.budget_distribution.weighted_allocations[dept_name].weight_percentage
        )
        per_person_weighted = provider::pyvider::divide(
          local.budget_distribution.weighted_allocations[dept_name].weighted_amount,
          dept_config.headcount
        )
      }
    }

    # Quarterly breakdowns
    quarterly_allocations = {
      for dept_name, dept_config in var.budget_allocation.departments :
      dept_name => {
        q1_budget = provider::pyvider::divide(local.budget_distribution.base_allocations[dept_name].base_amount, 4)
        q2_budget = provider::pyvider::divide(local.budget_distribution.base_allocations[dept_name].base_amount, 4)
        q3_budget = provider::pyvider::divide(local.budget_distribution.base_allocations[dept_name].base_amount, 4)
        q4_budget = provider::pyvider::divide(local.budget_distribution.base_allocations[dept_name].base_amount, 4)
        monthly_budget = provider::pyvider::divide(local.budget_distribution.base_allocations[dept_name].base_amount, 12)
      }
    }
  }
}

# Infrastructure resource distribution
variable "infrastructure_resources" {
  type = object({
    total_vcpus = number
    total_memory_gb = number
    total_storage_gb = number
    environments = map(object({
      priority = number
      min_vcpus = number
      min_memory_gb = number
      min_storage_gb = number
      scaling_factor = number
    }))
  })
  default = {
    total_vcpus = 256
    total_memory_gb = 1024
    total_storage_gb = 10240
    environments = {
      production = {
        priority = 1
        min_vcpus = 64
        min_memory_gb = 256
        min_storage_gb = 4096
        scaling_factor = 0.5
      }
      staging = {
        priority = 2
        min_vcpus = 16
        min_memory_gb = 64
        min_storage_gb = 1024
        scaling_factor = 0.25
      }
      development = {
        priority = 3
        min_vcpus = 8
        min_memory_gb = 32
        min_storage_gb = 512
        scaling_factor = 0.15
      }
      testing = {
        priority = 4
        min_vcpus = 4
        min_memory_gb = 16
        min_storage_gb = 256
        scaling_factor = 0.1
      }
    }
  }
}

locals {
  infrastructure_distribution = {
    # Calculate remaining resources after minimums
    total_min_vcpus = sum([for env, config in var.infrastructure_resources.environments : config.min_vcpus])
    total_min_memory = sum([for env, config in var.infrastructure_resources.environments : config.min_memory_gb])
    total_min_storage = sum([for env, config in var.infrastructure_resources.environments : config.min_storage_gb])

    remaining_vcpus = provider::pyvider::subtract(var.infrastructure_resources.total_vcpus, local.infrastructure_distribution.total_min_vcpus)
    remaining_memory = provider::pyvider::subtract(var.infrastructure_resources.total_memory_gb, local.infrastructure_distribution.total_min_memory)
    remaining_storage = provider::pyvider::subtract(var.infrastructure_resources.total_storage_gb, local.infrastructure_distribution.total_min_storage)

    # Distribute remaining resources by scaling factor
    total_scaling_factor = sum([for env, config in var.infrastructure_resources.environments : config.scaling_factor])

    environment_allocations = {
      for env_name, env_config in var.infrastructure_resources.environments :
      env_name => {
        # Base allocation (minimum guaranteed)
        base_vcpus = env_config.min_vcpus
        base_memory_gb = env_config.min_memory_gb
        base_storage_gb = env_config.min_storage_gb

        # Additional allocation from remaining pool
        scaling_weight = provider::pyvider::divide(env_config.scaling_factor, local.infrastructure_distribution.total_scaling_factor)
        additional_vcpus = provider::pyvider::multiply(local.infrastructure_distribution.remaining_vcpus, local.infrastructure_distribution.environment_allocations[env_name].scaling_weight)
        additional_memory_gb = provider::pyvider::multiply(local.infrastructure_distribution.remaining_memory, local.infrastructure_distribution.environment_allocations[env_name].scaling_weight)
        additional_storage_gb = provider::pyvider::multiply(local.infrastructure_distribution.remaining_storage, local.infrastructure_distribution.environment_allocations[env_name].scaling_weight)

        # Total allocation
        total_vcpus = provider::pyvider::add(env_config.min_vcpus, local.infrastructure_distribution.environment_allocations[env_name].additional_vcpus)
        total_memory_gb = provider::pyvider::add(env_config.min_memory_gb, local.infrastructure_distribution.environment_allocations[env_name].additional_memory_gb)
        total_storage_gb = provider::pyvider::add(env_config.min_storage_gb, local.infrastructure_distribution.environment_allocations[env_name].additional_storage_gb)

        # Resource ratios
        vcpu_percentage = provider::pyvider::multiply(
          provider::pyvider::divide(local.infrastructure_distribution.environment_allocations[env_name].total_vcpus, var.infrastructure_resources.total_vcpus),
          100
        )
        memory_percentage = provider::pyvider::multiply(
          provider::pyvider::divide(local.infrastructure_distribution.environment_allocations[env_name].total_memory_gb, var.infrastructure_resources.total_memory_gb),
          100
        )
        storage_percentage = provider::pyvider::multiply(
          provider::pyvider::divide(local.infrastructure_distribution.environment_allocations[env_name].total_storage_gb, var.infrastructure_resources.total_storage_gb),
          100
        )
      }
    }
  }
}

output "resource_distribution" {
  value = {
    budget_distribution = local.budget_distribution
    infrastructure_distribution = local.infrastructure_distribution
  }
}
```

### Ratio and Proportion Analysis

```terraform
# Financial ratio analysis
variable "company_financials" {
  type = object({
    revenue = number
    cost_of_goods_sold = number
    operating_expenses = number
    total_assets = number
    current_assets = number
    current_liabilities = number
    total_debt = number
    shareholders_equity = number
    shares_outstanding = number
  })
  default = {
    revenue = 5000000
    cost_of_goods_sold = 2000000
    operating_expenses = 1800000
    total_assets = 8000000
    current_assets = 2500000
    current_liabilities = 1200000
    total_debt = 2800000
    shareholders_equity = 5200000
    shares_outstanding = 100000
  }
}

locals {
  financial_ratios = {
    # Profitability ratios
    gross_profit = provider::pyvider::subtract(var.company_financials.revenue, var.company_financials.cost_of_goods_sold)
    gross_margin = provider::pyvider::multiply(
      provider::pyvider::divide(local.financial_ratios.gross_profit, var.company_financials.revenue),
      100
    )

    operating_income = provider::pyvider::subtract(local.financial_ratios.gross_profit, var.company_financials.operating_expenses)
    operating_margin = provider::pyvider::multiply(
      provider::pyvider::divide(local.financial_ratios.operating_income, var.company_financials.revenue),
      100
    )

    # Liquidity ratios
    current_ratio = provider::pyvider::divide(var.company_financials.current_assets, var.company_financials.current_liabilities)

    # Leverage ratios
    debt_to_equity = provider::pyvider::divide(var.company_financials.total_debt, var.company_financials.shareholders_equity)
    debt_to_assets = provider::pyvider::multiply(
      provider::pyvider::divide(var.company_financials.total_debt, var.company_financials.total_assets),
      100
    )

    # Efficiency ratios
    asset_turnover = provider::pyvider::divide(var.company_financials.revenue, var.company_financials.total_assets)

    # Per-share metrics
    earnings_per_share = provider::pyvider::divide(local.financial_ratios.operating_income, var.company_financials.shares_outstanding)
    book_value_per_share = provider::pyvider::divide(var.company_financials.shareholders_equity, var.company_financials.shares_outstanding)
  }

  # Benchmark comparisons (industry averages)
  industry_benchmarks = {
    target_gross_margin = 60
    target_operating_margin = 25
    target_current_ratio = 2.0
    target_debt_to_equity = 0.4
    target_asset_turnover = 1.2
  }

  performance_vs_benchmark = {
    gross_margin_vs_target = provider::pyvider::divide(local.financial_ratios.gross_margin, local.industry_benchmarks.target_gross_margin)
    operating_margin_vs_target = provider::pyvider::divide(local.financial_ratios.operating_margin, local.industry_benchmarks.target_operating_margin)
    current_ratio_vs_target = provider::pyvider::divide(local.financial_ratios.current_ratio, local.industry_benchmarks.target_current_ratio)
    debt_to_equity_vs_target = provider::pyvider::divide(local.financial_ratios.debt_to_equity, local.industry_benchmarks.target_debt_to_equity)
    asset_turnover_vs_target = provider::pyvider::divide(local.financial_ratios.asset_turnover, local.industry_benchmarks.target_asset_turnover)
  }
}

output "ratio_analysis" {
  value = {
    financial_ratios = local.financial_ratios
    benchmark_comparison = local.performance_vs_benchmark
  }
}
```

### Error Handling and Edge Cases

```terraform
# Safe division patterns with comprehensive error handling
variable "division_test_cases" {
  type = map(object({
    dividend = number
    divisor = number
    expected_error = bool
  }))
  default = {
    normal_division = {
      dividend = 100
      divisor = 4
      expected_error = false
    }
    zero_divisor = {
      dividend = 50
      divisor = 0
      expected_error = true
    }
    null_dividend = {
      dividend = null
      divisor = 5
      expected_error = false  # null handling, not error
    }
    null_divisor = {
      dividend = 10
      divisor = null
      expected_error = false  # null handling, not error
    }
    negative_numbers = {
      dividend = -15
      divisor = -3
      expected_error = false
    }
    small_divisor = {
      dividend = 1
      divisor = 0.001
      expected_error = false
    }
  }
}

locals {
  safe_division_results = {
    for test_name, test_case in var.division_test_cases :
    test_name => {
      # Check for valid inputs
      dividend_valid = test_case.dividend != null
      divisor_valid = test_case.divisor != null && test_case.divisor != 0

      # Safe division with multiple fallback strategies
      result = local.safe_division_results[test_name].dividend_valid && local.safe_division_results[test_name].divisor_valid ?
               provider::pyvider::divide(test_case.dividend, test_case.divisor) :
               null

      # Alternative with default value
      result_with_default = coalesce(local.safe_division_results[test_name].result, 0)

      # Validation flags
      has_null_inputs = test_case.dividend == null || test_case.divisor == null
      has_zero_divisor = test_case.divisor == 0
      is_safe_operation = local.safe_division_results[test_name].dividend_valid && local.safe_division_results[test_name].divisor_valid

      # Error prediction vs actual
      predicted_error = test_case.expected_error
      actual_has_issue = local.safe_division_results[test_name].has_null_inputs || local.safe_division_results[test_name].has_zero_divisor
    }
  }

  # Resource allocation with safe division
  resource_calculations = {
    cpu_per_instance = var.total_cpu != null && var.instance_count != null && var.instance_count > 0 ?
                      provider::pyvider::divide(var.total_cpu, var.instance_count) :
                      1  # minimum 1 CPU per instance

    memory_per_instance = var.total_memory != null && var.instance_count != null && var.instance_count > 0 ?
                         provider::pyvider::divide(var.total_memory, var.instance_count) :
                         512  # minimum 512MB per instance

    storage_per_instance = var.total_storage != null && var.instance_count != null && var.instance_count > 0 ?
                          provider::pyvider::divide(var.total_storage, var.instance_count) :
                          20  # minimum 20GB per instance

    # Utilization calculations with bounds checking
    cpu_utilization_percent = var.used_cpu != null && var.total_cpu != null && var.total_cpu > 0 ?
                             min(100, provider::pyvider::multiply(
                               provider::pyvider::divide(var.used_cpu, var.total_cpu),
                               100
                             )) :
                             0

    # Cost efficiency metrics
    cost_per_user = var.total_cost != null && var.active_users != null && var.active_users > 0 ?
                   provider::pyvider::divide(var.total_cost, var.active_users) :
                   null  # Cannot calculate without active users

    cost_per_transaction = var.total_cost != null && var.transaction_count != null && var.transaction_count > 0 ?
                          provider::pyvider::divide(var.total_cost, var.transaction_count) :
                          null  # Cannot calculate without transactions
  }

  # Validation and alerting
  division_warnings = {
    for calc_name, calc_result in local.resource_calculations :
    calc_name => {
      has_null_result = calc_result == null
      is_below_threshold = calc_result != null && calc_result < 1
      requires_attention = local.division_warnings[calc_name].has_null_result || local.division_warnings[calc_name].is_below_threshold

      warning_message = local.division_warnings[calc_name].requires_attention ?
                       "Division result for ${calc_name} requires attention: ${coalesce(tostring(calc_result), "null")}" :
                       "OK"
    }
  }
}

# Variables for resource calculations (would be defined elsewhere)
variable "total_cpu" {
  type = number
  default = null
}

variable "instance_count" {
  type = number
  default = null
}

variable "total_memory" {
  type = number
  default = null
}

variable "total_storage" {
  type = number
  default = null
}

variable "used_cpu" {
  type = number
  default = null
}

variable "total_cost" {
  type = number
  default = null
}

variable "active_users" {
  type = number
  default = null
}

variable "transaction_count" {
  type = number
  default = null
}

output "error_handling" {
  value = {
    test_results = local.safe_division_results
    resource_calculations = local.resource_calculations
    warnings = local.division_warnings
  }
}
```

## Signature

`divide(a: number, b: number) -> number`

## Arguments

- **`a`** (number, required) - The dividend (number to be divided). Can be an integer or float. Returns `null` if this value is `null`.
- **`b`** (number, required) - The divisor (number to divide by). Can be an integer or float. Returns `null` if this value is `null`. **Cannot be zero** - will raise an error.

## Return Value

Returns the quotient of `a / b` as a number. The return type is automatically optimized:
- If the result is a whole number (e.g., `4.0`), returns an integer (`4`)
- If the result has decimal places (e.g., `4.75`), returns a float (`4.75`)
- Returns `null` if either input is `null`
- **Raises an error** if the divisor (`b`) is zero

## Error Handling

### Division by Zero
```terraform
# This will cause an error
locals {
  # Error: Division by zero
  # bad_result = provider::pyvider::divide(10, 0)
}

# Safe division with check
variable "divisor" {
  type = number
}

locals {
  safe_result = var.divisor != 0 ? provider::pyvider::divide(100, var.divisor) : null
}
```

### Null Safety
```terraform
locals {
  # These all return null
  result1 = provider::pyvider::divide(null, 5)     # null
  result2 = provider::pyvider::divide(10, null)    # null
  result3 = provider::pyvider::divide(null, null)  # null
}
```

## Common Patterns

### Average Calculation
```terraform
variable "total_value" {
  type = number
}

variable "count" {
  type = number
}

locals {
  average = var.count > 0 ? provider::pyvider::divide(var.total_value, var.count) : 0
}

resource "pyvider_file_content" "stats" {
  filename = "/tmp/average.txt"
  content  = "Average value: ${local.average}"
}
```

### Resource Per Unit
```terraform
variable "total_memory_gb" {
  type = number
}

variable "instance_count" {
  type = number
}

locals {
  memory_per_instance = var.instance_count > 0 ? provider::pyvider::divide(var.total_memory_gb, var.instance_count) : 0
}
```

## Best Practices

### 1. Always Check for Zero Division
```terraform
variable "numerator" {
  type = number
}

variable "denominator" {
  type = number
  validation {
    condition     = var.denominator != 0
    error_message = "Denominator cannot be zero."
  }
}

locals {
  result = provider::pyvider::divide(var.numerator, var.denominator)
}
```

### 2. Handle Edge Cases
```terraform
locals {
  safe_division = var.total > 0 && var.count > 0 ? provider::pyvider::divide(var.total, var.count) : 0
}
```

## Related Functions

- [`add`](./add.md) - Add two numbers
- [`subtract`](./subtract.md) - Subtract two numbers
- [`multiply`](./multiply.md) - Multiply two numbers
- [`round`](./round.md) - Round division results to specific precision
