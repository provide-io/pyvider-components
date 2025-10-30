# Statistical aggregations and analysis

locals {
  response_times_ms = [45, 52, 48, 51, 150, 47, 49, 53, 46, 50]

  # Basic statistics
  total_time = provider::pyvider::sum(local.response_times_ms)
  count = length(local.response_times_ms)
  average = provider::pyvider::divide(local.total_time, local.count)

  # Find outliers
  min_time = provider::pyvider::min(local.response_times_ms)
  max_time = provider::pyvider::max(local.response_times_ms)
  range = provider::pyvider::subtract(local.max_time, local.min_time)

  # Performance analysis
  acceptable_threshold = 100
  slow_requests = [for t in local.response_times_ms : t if t > local.acceptable_threshold]
  performance_score = provider::pyvider::multiply(
    provider::pyvider::divide(
      provider::pyvider::subtract(local.count, length(local.slow_requests)),
      local.count
    ),
    100
  )
}

# Budget allocation example
locals {
  department_budgets = [50000, 75000, 100000, 125000, 80000]

  total_budget = provider::pyvider::sum(local.department_budgets)
  average_budget = provider::pyvider::divide(local.total_budget, length(local.department_budgets))

  # Calculate percentages
  budget_percentages = [
    for budget in local.department_budgets :
    provider::pyvider::round(
      provider::pyvider::multiply(
        provider::pyvider::divide(budget, local.total_budget),
        100
      ),
      2
    )
  ]
}

output "aggregation_results" {
  value = {
    performance_metrics = {
      average_response = local.average
      min_response = local.min_time
      max_response = local.max_time
      range = local.range
      slow_count = length(local.slow_requests)
      performance_score = local.performance_score
    }
    budget_analysis = {
      total = local.total_budget
      average = local.average_budget
      percentages = local.budget_percentages
    }
  }
}
