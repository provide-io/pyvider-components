# JQ transformation function examples

# Example 1: Basic JSON data extraction
locals {
  advanced_user_data = {
    advanced_name = "John Doe"
    advanced_age  = 30
    advanced_email = "john.doe@example.com"
    advanced_address = {
      advanced_street = "123 Main St"
      advanced_city   = "Anytown"
      advanced_state  = "CA"
      advanced_zip    = "12345"
    }
    hobbies = ["reading", "hiking", "coding"]
  }

  # Extract specific fields
  user_name = provider::pyvider::lens_jq(local.advanced_user_data, ".name")
  user_city = provider::pyvider::lens_jq(local.advanced_user_data, ".address.city")
  hobby_count = provider::pyvider::lens_jq(local.advanced_user_data, ".hobbies | length")
}

# Example 2: Array manipulation and filtering
locals {
  advanced_employees = [
    {
      advanced_id = 1
      advanced_name = "Alice Smith"
      advanced_department = "Engineering"
      advanced_salary = 95000
      advanced_skills = ["Python", "Go", "Docker"]
    },
    {
      id = 2
      name = "Bob Johnson"
      department = "Marketing"
      salary = 75000
      skills = ["SEO", "Analytics", "Content"]
    },
    {
      id = 3
      name = "Carol Davis"
      department = "Engineering"
      salary = 105000
      skills = ["JavaScript", "React", "Node.js"]
    }
  ]

  # Filter and transform arrays
  engineers = provider::pyvider::lens_jq(
    local.advanced_employees,
    '[.[] | select(.department == "Engineering")]'
  )

  high_earners = provider::pyvider::lens_jq(
    local.advanced_employees,
    '[.[] | select(.salary > 80000) | {name, salary}]'
  )

  all_skills = provider::pyvider::lens_jq(
    local.advanced_employees,
    '[.[].skills[]] | unique'
  )

  avg_salary = provider::pyvider::lens_jq(
    local.advanced_employees,
    '[.[].salary] | add / length'
  )
}

# Example 3: Complex data transformation
locals {
  advanced_api_response = {
    advanced_status = "success"
    advanced_data = {
      advanced_users = [
        {
          advanced_id = "user1"
          advanced_profile = {
            advanced_firstName = "John"
            advanced_lastName = "Doe"
            advanced_settings = {
              advanced_theme = "dark"
              advanced_notifications = true
            }
          }
          posts = [
            { title = "Hello World", likes = 5 },
            { title = "JQ is Awesome", likes = 12 }
          ]
        },
        {
          id = "user2"
          profile = {
            firstName = "Jane"
            lastName = "Smith"
            settings = {
              theme = "light"
              notifications = false
            }
          }
          posts = [
            { title = "Getting Started", likes = 8 },
            { title = "Advanced Tips", likes = 15 }
          ]
        }
      ]
    }
  }

  # Complex transformations
  user_summaries = provider::pyvider::lens_jq(
    local.advanced_api_response,
    '.data.users | map({
      id,
      full_name: (.profile.firstName + " " + .profile.lastName),
      theme: .profile.settings.theme,
      total_likes: [.posts[].likes] | add,
      post_count: (.posts | length)
    })'
  )

  dark_theme_users = provider::pyvider::lens_jq(
    local.advanced_api_response,
    '.data.users | map(select(.profile.settings.theme == "dark")) | map(.profile.firstName)'
  )

  popular_posts = provider::pyvider::lens_jq(
    local.advanced_api_response,
    '.data.users[].posts[] | select(.likes > 10) | .title'
  )
}

output "advanced_user_data" {
  description = "Results from various JQ transformation examples"
  value = {
    basic_operations = {
      user_name = local.user_name
      user_city = local.user_city
      hobby_count = local.hobby_count
    }

    array_processing = {
      engineers_found = length(local.engineers)
      high_earners_found = length(local.high_earners)
      unique_skills_count = length(local.all_skills)
      average_salary = local.avg_salary
    }

    complex_data = {
      user_summaries_count = length(local.user_summaries)
      dark_theme_users = local.dark_theme_users
      popular_posts_found = length(local.popular_posts)
    }
  }
}
