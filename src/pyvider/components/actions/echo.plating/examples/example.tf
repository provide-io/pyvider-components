action "pyvider_echo" "example" {
  config {
    # Configuration options here
  }
}

# Actions run as a side effect of an apply, triggered from a resource:
#
#   lifecycle {
#     action_trigger {
#       events  = [after_create]
#       actions = [action.pyvider_echo.example]
#     }
#   }
