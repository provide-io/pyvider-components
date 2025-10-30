# Basic numeric function examples

# Addition examples
locals {
  comp_simple_add = provider::pyvider::add(5, 3)      # Returns: 8
  comp_float_add = provider::pyvider::add(2.5, 1.5)   # Returns: 4
  comp_mixed_add = provider::pyvider::add(10, 2.3)    # Returns: 12.3
}

# Subtraction examples
locals {
  comp_simple_subtract = provider::pyvider::subtract(10, 4)    # Returns: 6
  comp_float_subtract = provider::pyvider::subtract(5.5, 2.1)  # Returns: 3.4
  comp_negative_result = provider::pyvider::subtract(3, 7)     # Returns: -4
}

# Multiplication examples
locals {
  comp_simple_multiply = provider::pyvider::multiply(4, 3)     # Returns: 12
  comp_float_multiply = provider::pyvider::multiply(2.5, 4)    # Returns: 10
  comp_zero_multiply = provider::pyvider::multiply(5, 0)       # Returns: 0
}

# Division examples
locals {
  comp_simple_divide = provider::pyvider::divide(12, 3)        # Returns: 4
  comp_float_divide = provider::pyvider::divide(10, 3)         # Returns: 3.333...
  comp_precise_divide = provider::pyvider::divide(15, 3)       # Returns: 5
}

# List operations
locals {
  comp_numbers = [10, 5, 8, 2, 15]

  comp_list_sum = provider::pyvider::sum(local.comp_numbers)         # Returns: 40
  comp_list_min = provider::pyvider::min(local.comp_numbers)         # Returns: 2
  comp_list_max = provider::pyvider::max(local.comp_numbers)         # Returns: 15
}

# Rounding examples
locals {
  comp_round_to_int = provider::pyvider::round(3.7, 0)         # Returns: 4
  comp_round_to_decimal = provider::pyvider::round(3.14159, 2) # Returns: 3.14
  comp_round_negative = provider::pyvider::round(-2.6, 0)      # Returns: -3
}

# Output results for verification
output "numeric_examples" {
  value = {
    addition = {
      simple = local.comp_simple_add
      float = local.comp_float_add
      mixed = local.comp_mixed_add
    }
    subtraction = {
      simple = local.comp_simple_subtract
      float = local.comp_float_subtract
      negative = local.comp_negative_result
    }
    multiplication = {
      simple = local.comp_simple_multiply
      float = local.comp_float_multiply
      zero = local.comp_zero_multiply
    }
    division = {
      simple = local.comp_simple_divide
      float = local.comp_float_divide
      precise = local.comp_precise_divide
    }
    list_operations = {
      sum = local.comp_list_sum
      min = local.comp_list_min
      max = local.comp_list_max
    }
    rounding = {
      to_int = local.comp_round_to_int
      to_decimal = local.comp_round_to_decimal
      negative = local.comp_round_negative
    }
  }
}