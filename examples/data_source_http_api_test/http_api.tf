# Simple GET request
data "pyvider_http_api" "get_request" {
  url    = "https://httpbin.org/get"
  method = "GET"
  headers = {
    "User-Agent" = "Pyvider/1.0"
  }
  timeout = 10
}

# POST request with body
data "pyvider_http_api" "post_request" {
  url    = "https://httpbin.org/post"
  method = "POST"
  body   = jsonencode({
    message = "Hello from Pyvider"
    test    = true
  })
  headers = {
    "Content-Type" = "application/json"
    "User-Agent"   = "Pyvider/1.0"
  }
  timeout = 10
}

output "get_response" {
  description = "GET request response details"
  value = {
    status_code      = data.pyvider_http_api.get_request.status_code
    content_type     = data.pyvider_http_api.get_request.content_type
    response_time_ms = data.pyvider_http_api.get_request.response_time_ms
    header_count     = data.pyvider_http_api.get_request.header_count
  }
}

output "get_response_body" {
  description = "Parsed GET response body"
  value       = jsondecode(data.pyvider_http_api.get_request.response_body)
}

output "post_response" {
  description = "POST request response details"
  value = {
    status_code = data.pyvider_http_api.post_request.status_code
    body_echo   = jsondecode(data.pyvider_http_api.post_request.response_body).json
  }
}
