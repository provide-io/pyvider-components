---
page_title: "Function: subtract"
description: |-
  Subtracts one number from another with intelligent integer conversion
---

# subtract (Function)

> Performs subtraction of two numeric values with null-safe handling and automatic type optimization

The `subtract` function subtracts the second number from the first number and returns the result. It handles null values gracefully and automatically converts floating-point results to integers when they represent whole numbers.

## When to Use This

- **Arithmetic calculations**: Perform basic subtraction in Terraform configurations
- **Countdown operations**: Subtract values from counters or timers
- **Resource calculations**: Compute remaining capacity or quota
- **Configuration math**: Calculate derived configuration values
- **Budget calculations**: Calculate remaining budget or costs

**Anti-patterns (when NOT to use):**
- Complex mathematical operations (use multiple function calls)
- String operations (use string functions)
- List/array operations (use collection functions)
- Boolean logic (use conditional expressions)

## Quick Start

```terraform
# Simple subtraction
locals {
  remaining_quota = provider::pyvider::subtract(100, 25)  # Returns: 75
}

# Subtracting with variables
variable "total_budget" {
  default = 1000
}

variable "spent_amount" {
  default = 250
}

locals {
  remaining_budget = provider::pyvider::subtract(var.total_budget, var.spent_amount)  # Returns: 750
}
```

## Examples

### Basic Usage

```terraform
# Simple numeric subtraction
locals {
  basic_examples = {
    simple_subtract = provider::pyvider::subtract(100, 25)        # 75
    decimal_result = provider::pyvider::subtract(10.5, 3.2)      # 7.3
    integer_from_decimal = provider::pyvider::subtract(10.0, 5)  # 5 (auto-converted to integer)
    negative_result = provider::pyvider::subtract(5, 10)         # -5
    zero_result = provider::pyvider::subtract(42, 42)            # 0
  }

  # Working with variables
  total_budget = 1000
  spent_amount = 350
  remaining = provider::pyvider::subtract(local.total_budget, local.spent_amount)  # 650

  # Chaining operations
  base_value = 100
  first_deduction = provider::pyvider::subtract(local.base_value, 20)   # 80
  final_result = provider::pyvider::subtract(local.first_deduction, 15) # 65
}

# Edge cases and type handling
locals {
  edge_cases = {
    large_numbers = provider::pyvider::subtract(1000000, 999999)     # 1
    small_decimals = provider::pyvider::subtract(0.1, 0.05)         # 0.05
    mixed_types = provider::pyvider::subtract(10, 3.5)              # 6.5
    null_handling = provider::pyvider::subtract(null, 5)            # null
    null_second = provider::pyvider::subtract(10, null)             # null
  }
}

output "basic_subtraction" {
  value = {
    examples = local.basic_examples
    remaining_budget = local.remaining
    chained_result = local.final_result
    edge_cases = local.edge_cases
  }
}
```

### Budget and Cost Management

```terraform
# Project budget tracking
variable "project_budgets" {
  type = map(object({
    allocated_budget = number
    expenses = list(object({
      description = string
      amount = number
      category = string
    }))
  }))
  default = {
    web_development = {
      allocated_budget = 50000
      expenses = [
        { description = "Frontend Development", amount = 15000, category = "development" },
        { description = "Backend API", amount = 12000, category = "development" },
        { description = "Database Setup", amount = 3000, category = "infrastructure" },
        { description = "Testing & QA", amount = 8000, category = "quality" }
      ]
    }
    marketing_campaign = {
      allocated_budget = 25000
      expenses = [
        { description = "Social Media Ads", amount = 8000, category = "advertising" },
        { description = "Content Creation", amount = 5000, category = "content" },
        { description = "Analytics Tools", amount = 2000, category = "tools" }
      ]
    }
  }
}

# Calculate remaining budgets and spending analysis
locals {
  budget_analysis = {
    for project_name, project in var.project_budgets :
    project_name => {
      allocated = project.allocated_budget
      total_spent = sum([for expense in project.expenses : expense.amount])
      remaining = provider::pyvider::subtract(
        project.allocated_budget,
        sum([for expense in project.expenses : expense.amount])
      )

      # Calculate percentage spent
      percent_spent = round(
        (sum([for expense in project.expenses : expense.amount]) / project.allocated_budget) * 100,
        2
      )

      # Budget status
      is_over_budget = sum([for expense in project.expenses : expense.amount]) > project.allocated_budget
      budget_variance = provider::pyvider::subtract(
        sum([for expense in project.expenses : expense.amount]),
        project.allocated_budget
      )

      # Category breakdown
      category_spending = {
        for category in distinct([for expense in project.expenses : expense.category]) :
        category => {
          spent = sum([
            for expense in project.expenses :
            expense.category == category ? expense.amount : 0
          ])
          # Calculate what's left if we assume equal budget allocation
          category_budget = project.allocated_budget / length(distinct([for expense in project.expenses : expense.category]))
          category_remaining = provider::pyvider::subtract(
            category_budget,
            sum([for expense in project.expenses : expense.category == category ? expense.amount : 0])
          )
        }
      }
    }
  }

  # Overall financial summary
  financial_summary = {
    total_allocated = sum([for project in var.project_budgets : project.allocated_budget])
    total_spent = sum([
      for project in var.project_budgets :
      sum([for expense in project.expenses : expense.amount])
    ])
    total_remaining = provider::pyvider::subtract(
      sum([for project in var.project_budgets : project.allocated_budget]),
      sum([for project in var.project_budgets : sum([for expense in project.expenses : expense.amount])])
    )
  }
}

output "budget_management" {
  value = {
    project_analysis = local.budget_analysis
    financial_summary = local.financial_summary
  }
}
```

### Resource Capacity Planning

```terraform
# Infrastructure capacity management
variable "server_resources" {
  type = map(object({
    total_cpu_cores = number
    total_memory_gb = number
    total_storage_gb = number
    allocated_resources = list(object({
      service_name = string
      cpu_cores = number
      memory_gb = number
      storage_gb = number
    }))
  }))
  default = {
    production_cluster = {
      total_cpu_cores = 64
      total_memory_gb = 256
      total_storage_gb = 2000
      allocated_resources = [
        { service_name = "web-app", cpu_cores = 16, memory_gb = 64, storage_gb = 200 },
        { service_name = "api-service", cpu_cores = 12, memory_gb = 48, storage_gb = 150 },
        { service_name = "database", cpu_cores = 20, memory_gb = 96, storage_gb = 800 },
        { service_name = "cache-redis", cpu_cores = 4, memory_gb = 16, storage_gb = 50 }
      ]
    }
    staging_cluster = {
      total_cpu_cores = 32
      total_memory_gb = 128
      total_storage_gb = 1000
      allocated_resources = [
        { service_name = "web-app-staging", cpu_cores = 4, memory_gb = 16, storage_gb = 100 },
        { service_name = "api-staging", cpu_cores = 4, memory_gb = 16, storage_gb = 100 }
      ]
    }
  }
}

# Calculate available resources
locals {
  resource_availability = {
    for cluster_name, cluster in var.server_resources :
    cluster_name => {
      # Calculate total allocated resources
      total_allocated_cpu = sum([for service in cluster.allocated_resources : service.cpu_cores])
      total_allocated_memory = sum([for service in cluster.allocated_resources : service.memory_gb])
      total_allocated_storage = sum([for service in cluster.allocated_resources : service.storage_gb])

      # Calculate remaining capacity
      available_cpu = provider::pyvider::subtract(cluster.total_cpu_cores, sum([for service in cluster.allocated_resources : service.cpu_cores]))
      available_memory = provider::pyvider::subtract(cluster.total_memory_gb, sum([for service in cluster.allocated_resources : service.memory_gb]))
      available_storage = provider::pyvider::subtract(cluster.total_storage_gb, sum([for service in cluster.allocated_resources : service.storage_gb]))

      # Calculate utilization percentages
      cpu_utilization = round((sum([for service in cluster.allocated_resources : service.cpu_cores]) / cluster.total_cpu_cores) * 100, 1)
      memory_utilization = round((sum([for service in cluster.allocated_resources : service.memory_gb]) / cluster.total_memory_gb) * 100, 1)
      storage_utilization = round((sum([for service in cluster.allocated_resources : service.storage_gb]) / cluster.total_storage_gb) * 100, 1)

      # Capacity warnings
      cpu_warning = sum([for service in cluster.allocated_resources : service.cpu_cores]) > (cluster.total_cpu_cores * 0.8)
      memory_warning = sum([for service in cluster.allocated_resources : service.memory_gb]) > (cluster.total_memory_gb * 0.8)
      storage_warning = sum([for service in cluster.allocated_resources : service.storage_gb]) > (cluster.total_storage_gb * 0.8)

      # Can accommodate new service estimation
      estimated_new_service = {
        cpu_cores = 8
        memory_gb = 32
        storage_gb = 200
      }

      can_fit_new_service = (
        local.resource_availability[cluster_name].available_cpu >= local.resource_availability[cluster_name].estimated_new_service.cpu_cores &&
        local.resource_availability[cluster_name].available_memory >= local.resource_availability[cluster_name].estimated_new_service.memory_gb &&
        local.resource_availability[cluster_name].available_storage >= local.resource_availability[cluster_name].estimated_new_service.storage_gb
      )
    }
  }
}

output "capacity_planning" {
  value = local.resource_availability
}
```

### Countdown and Timer Operations

```terraform
# Event countdown management
variable "scheduled_events" {
  type = list(object({
    event_name = string
    total_duration_hours = number
    elapsed_hours = number
    priority = string
  }))
  default = [
    {
      event_name = "Product Launch"
      total_duration_hours = 720  # 30 days
      elapsed_hours = 480         # 20 days
      priority = "high"
    },
    {
      event_name = "Security Audit"
      total_duration_hours = 168  # 7 days
      elapsed_hours = 72          # 3 days
      priority = "medium"
    },
    {
      event_name = "Server Maintenance"
      total_duration_hours = 24   # 1 day
      elapsed_hours = 6           # 6 hours
      priority = "low"
    }
  ]
}

# Calculate remaining time and urgency
locals {
  event_status = {
    for event in var.scheduled_events :
    event.event_name => {
      total_hours = event.total_duration_hours
      elapsed_hours = event.elapsed_hours
      remaining_hours = provider::pyvider::subtract(event.total_duration_hours, event.elapsed_hours)

      # Convert to more readable formats
      remaining_days = provider::pyvider::subtract(event.total_duration_hours, event.elapsed_hours) / 24
      completion_percentage = round((event.elapsed_hours / event.total_duration_hours) * 100, 1)

      # Urgency calculations
      is_urgent = provider::pyvider::subtract(event.total_duration_hours, event.elapsed_hours) <= 48  # Less than 2 days
      is_overdue = event.elapsed_hours > event.total_duration_hours
      overdue_hours = event.elapsed_hours > event.total_duration_hours ? provider::pyvider::subtract(event.elapsed_hours, event.total_duration_hours) : 0

      priority = event.priority

      # Status classification
      status = (
        event.elapsed_hours > event.total_duration_hours ? "overdue" :
        provider::pyvider::subtract(event.total_duration_hours, event.elapsed_hours) <= 24 ? "critical" :
        provider::pyvider::subtract(event.total_duration_hours, event.elapsed_hours) <= 72 ? "urgent" :
        "on_track"
      )
    }
  }

  # Summary statistics
  countdown_summary = {
    total_events = length(var.scheduled_events)
    urgent_events = length([
      for event in var.scheduled_events : event.event_name
      if provider::pyvider::subtract(event.total_duration_hours, event.elapsed_hours) <= 48
    ])
    overdue_events = length([
      for event in var.scheduled_events : event.event_name
      if event.elapsed_hours > event.total_duration_hours
    ])
    on_track_events = length([
      for event in var.scheduled_events : event.event_name
      if event.elapsed_hours <= event.total_duration_hours && provider::pyvider::subtract(event.total_duration_hours, event.elapsed_hours) > 48
    ])
  }
}

output "countdown_management" {
  value = {
    event_details = local.event_status
    summary = local.countdown_summary
  }
}
```

### Inventory and Stock Management

```terraform
# Inventory tracking
variable "inventory_items" {
  type = map(object({
    initial_stock = number
    transactions = list(object({
      type = string  # "sale", "return", "adjustment"
      quantity = number
      date = string
    }))
    reorder_point = number
    max_stock = number
  }))
  default = {
    laptop_computers = {
      initial_stock = 100
      transactions = [
        { type = "sale", quantity = 15, date = "2024-01-15" },
        { type = "sale", quantity = 8, date = "2024-01-16" },
        { type = "return", quantity = 2, date = "2024-01-17" },
        { type = "sale", quantity = 12, date = "2024-01-18" }
      ]
      reorder_point = 20
      max_stock = 150
    }
    monitors = {
      initial_stock = 75
      transactions = [
        { type = "sale", quantity = 10, date = "2024-01-15" },
        { type = "adjustment", quantity = -3, date = "2024-01-16" },  # damaged items
        { type = "sale", quantity = 5, date = "2024-01-17" }
      ]
      reorder_point = 15
      max_stock = 100
    }
  }
}

# Calculate current inventory levels
locals {
  inventory_status = {
    for item_name, item in var.inventory_items :
    item_name => {
      starting_inventory = item.initial_stock

      # Calculate total outbound (sales + adjustments)
      total_sales = sum([
        for transaction in item.transactions :
        transaction.type == "sale" ? transaction.quantity : 0
      ])

      total_adjustments = sum([
        for transaction in item.transactions :
        transaction.type == "adjustment" ? transaction.quantity : 0
      ])

      total_returns = sum([
        for transaction in item.transactions :
        transaction.type == "return" ? transaction.quantity : 0
      ])

      # Calculate net outbound
      net_outbound = local.inventory_status[item_name].total_sales + local.inventory_status[item_name].total_adjustments - local.inventory_status[item_name].total_returns

      # Current stock level
      current_stock = provider::pyvider::subtract(item.initial_stock, local.inventory_status[item_name].net_outbound)

      # Stock analysis
      needs_reorder = local.inventory_status[item_name].current_stock <= item.reorder_point
      space_available = provider::pyvider::subtract(item.max_stock, local.inventory_status[item_name].current_stock)
      suggested_reorder_quantity = item.needs_reorder ? provider::pyvider::subtract(item.max_stock, local.inventory_status[item_name].current_stock) : 0

      # Stock turnover metrics
      stock_turnover_rate = item.initial_stock > 0 ? round((local.inventory_status[item_name].total_sales / item.initial_stock) * 100, 1) : 0

      # Status indicators
      stock_status = (
        local.inventory_status[item_name].current_stock <= 0 ? "out_of_stock" :
        local.inventory_status[item_name].current_stock <= item.reorder_point ? "low_stock" :
        local.inventory_status[item_name].current_stock >= item.max_stock * 0.9 ? "overstocked" :
        "normal"
      )
    }
  }

  # Inventory summary
  inventory_summary = {
    total_items = length(var.inventory_items)
    items_needing_reorder = length([
      for item_name, analysis in local.inventory_status : item_name
      if analysis.needs_reorder
    ])
    out_of_stock_items = length([
      for item_name, analysis in local.inventory_status : item_name
      if analysis.current_stock <= 0
    ])
    overstocked_items = length([
      for item_name, analysis in local.inventory_status : item_name
      if analysis.stock_status == "overstocked"
    ])
  }
}

output "inventory_management" {
  value = {
    item_status = local.inventory_status
    summary = local.inventory_summary
  }
}

## Signature

`subtract(a: number, b: number) -> number`

## Arguments

- **`a`** (number, required) - The number to subtract from (minuend). Can be an integer or float. Returns `null` if this value is `null`.
- **`b`** (number, required) - The number to subtract (subtrahend). Can be an integer or float. Returns `null` if this value is `null`.

## Return Value

Returns the difference of `a - b` as a number. The return type is automatically optimized:
- If the result is a whole number (e.g., `5.0`), returns an integer (`5`)
- If the result has decimal places (e.g., `5.7`), returns a float (`5.7`)
- Returns `null` if either input is `null`

## Related Functions

- [`add`](./add.md) - Add two numbers
- [`multiply`](./multiply.md) - Multiply two numbers
- [`divide`](./divide.md) - Divide two numbers
- [`max`](./max.md) - Find maximum value (useful for ensuring non-negative results)
- [`round`](./round.md) - Round the result to specific precision
