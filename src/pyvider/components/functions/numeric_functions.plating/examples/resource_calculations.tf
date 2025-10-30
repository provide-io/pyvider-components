# Infrastructure resource calculations

# Calculate EC2 instance costs
locals {
  instance_type_hourly_cost = {
    "t2.micro"  = 0.0116
    "t2.small"  = 0.023
    "t2.medium" = 0.0464
    "m5.large"  = 0.096
    "m5.xlarge" = 0.192
  }

  instances = [
    { type = "t2.micro", hours = 730 },
    { type = "m5.large", hours = 730 },
    { type = "t2.small", hours = 365 }
  ]

  # Calculate monthly costs
  monthly_costs = [
    for inst in local.instances :
    provider::pyvider::multiply(
      local.instance_type_hourly_cost[inst.type],
      inst.hours
    )
  ]

  total_monthly_cost = provider::pyvider::sum(local.monthly_costs)
  average_instance_cost = provider::pyvider::divide(local.total_monthly_cost, length(local.instances))
}

# Storage capacity planning
locals {
  volume_sizes_gb = [100, 250, 500, 1000]

  total_storage = provider::pyvider::sum(local.volume_sizes_gb)
  largest_volume = provider::pyvider::max(local.volume_sizes_gb)
  smallest_volume = provider::pyvider::min(local.volume_sizes_gb)

  # Calculate percentage of total
  largest_percentage = provider::pyvider::multiply(
    provider::pyvider::divide(local.largest_volume, local.total_storage),
    100
  )
}

# Auto-scaling calculations
locals {
  current_instances = 3
  target_cpu_percent = 70
  current_cpu_percent = 85

  # Calculate scaling factor
  scale_factor = provider::pyvider::divide(current_cpu_percent, target_cpu_percent)

  # Round up desired instances
  desired_instances = provider::pyvider::round(
    provider::pyvider::multiply(local.current_instances, local.scale_factor),
    0
  )

  # Ensure within min/max bounds
  min_instances = 2
  max_instances = 10

  final_instance_count = provider::pyvider::min([
    provider::pyvider::max([local.desired_instances, local.min_instances]),
    local.max_instances
  ])
}

output "resource_calculations" {
  value = {
    cost_analysis = {
      total_monthly = local.total_monthly_cost
      average_per_instance = local.average_instance_cost
      individual_costs = local.monthly_costs
    }
    storage_analysis = {
      total_gb = local.total_storage
      largest_volume = local.largest_volume
      smallest_volume = local.smallest_volume
      largest_percentage = local.largest_percentage
    }
    autoscaling = {
      current = local.current_instances
      desired = local.desired_instances
      final = local.final_instance_count
      scale_factor = local.scale_factor
    }
  }
}
