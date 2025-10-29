# JQ transformation function examples

# Example 1: Basic JSON data extraction
locals {
  adv_user_data = {
    name = "John Doe"
    age  = 30
    email = "john.doe@example.com"
    address = {
      street = "123 Main St"
      city   = "Anytown"
      state  = "CA"
      zip    = "12345"
    }
    hobbies = ["reading", "hiking", "coding"]
  }

  # Extract specific fields
  adv_user_name = provider::pyvider::lens_jq(local.adv_user_data, ".name")
  adv_user_city = provider::pyvider::lens_jq(local.adv_user_data, ".address.city")
  adv_hobby_count = provider::pyvider::lens_jq(local.adv_user_data, ".hobbies | length")
}

# Example 2: Array manipulation and filtering
locals {
  adv_employees = [
    {
      id = 1
      name = "Alice Smith"
      department = "Engineering"
      salary = 95000
      skills = ["Python", "Go", "Docker"]
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
  adv_engineers = provider::pyvider::lens_jq(
    local.adv_employees,
    "[.[] | select(.department == \"Engineering\")]"
  )

  adv_high_earners = provider::pyvider::lens_jq(
    local.adv_employees,
    "[.[] | select(.salary > 80000) | {name, salary}]"
  )

  adv_all_skills = provider::pyvider::lens_jq(
    local.adv_employees,
    "[.[].skills[]] | unique"
  )

  adv_avg_salary = provider::pyvider::lens_jq(
    local.adv_employees,
    "[.[].salary] | add / length"
  )
}

# Example 3: Complex data transformation
locals {
  adv_api_response = {
    status = "success"
    data = {
      users = [
        {
          id = "user1"
          profile = {
            firstName = "John"
            lastName = "Doe"
            settings = {
              theme = "dark"
              notifications = true
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
  adv_user_summaries = provider::pyvider::lens_jq(
    local.adv_api_response,
    ".data.users | map({id, full_name: (.profile.firstName + \" \" + .profile.lastName), theme: .profile.settings.theme, total_likes: [.posts[].likes] | add, post_count: (.posts | length)})"
  )

  adv_dark_theme_users = provider::pyvider::lens_jq(
    local.adv_api_response,
    ".data.users | map(select(.profile.settings.theme == \"dark\")) | map(.profile.firstName)"
  )

  adv_popular_posts = provider::pyvider::lens_jq(
    local.adv_api_response,
    ".data.users[].posts[] | select(.likes > 10) | .title"
  )
}

output "lens_jq_examples_results" {
  description = "Results from various JQ transformation examples"
  value = {
    basic_operations = {
      user_name = local.adv_user_name
      user_city = local.adv_user_city
      hobby_count = local.adv_hobby_count
    }

    array_processing = {
      engineers_found = length(local.adv_engineers)
      high_earners_found = length(local.adv_high_earners)
      unique_skills_count = length(local.adv_all_skills)
      average_salary = local.adv_avg_salary
    }

    complex_data = {
      user_summaries_count = length(local.adv_user_summaries)
      dark_theme_users = local.adv_dark_theme_users
      popular_posts_found = length(local.adv_popular_posts)
    }
  }
}
