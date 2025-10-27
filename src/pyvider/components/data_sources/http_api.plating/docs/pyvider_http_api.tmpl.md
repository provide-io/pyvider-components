---
page_title: "Data Source: pyvider_http_api"
description: |-
  Make HTTP requests from Terraform and capture the response.
---

# pyvider_http_api (Data Source)

Issue an HTTP request and reuse the response inside Terraform plans. Supports custom methods, headers, and timeouts.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Notes

- `method` defaults to `GET`; supply `POST`, `PUT`, `PATCH`, `DELETE`, etc. as needed.
- Set `headers`, `body`, and `timeout` to match the target API.
- Response fields like `status_code`, `response_body`, and `response_headers` are always populated when the call succeeds.
- Request failures surface as Terraform errors with details from the provider.
