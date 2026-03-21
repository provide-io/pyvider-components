#!/usr/bin/env python
"""Memray stress test for environment variables data source filtering logic."""

import os
import re

os.environ["PLUGIN_LOG_LEVEL"] = "ERROR"

# Set up mock environment variables for filtering
for i in range(100):
    os.environ[f"MYAPP_VAR_{i}"] = f"value_{i}"
    os.environ[f"OTHER_VAR_{i}"] = f"other_{i}"
    os.environ[f"TEST_PREFIX_{i}"] = f"test_{i}"


def stress_key_filtering() -> None:
    """Simulate key-list filtering logic from EnvVariablesDataSource.read()."""
    source_vars = os.environ.copy()
    keys_list = [f"MYAPP_VAR_{i}" for i in range(50)]

    for _ in range(5_000):
        filtered = {}
        for key in keys_list:
            value = source_vars.get(key)
            if value is not None:
                if value:  # exclude_empty=True
                    filtered[key] = value


def stress_prefix_filtering() -> None:
    """Simulate prefix filtering logic from EnvVariablesDataSource.read()."""
    source_vars = os.environ.copy()
    prefix = "MYAPP_"

    for _ in range(5_000):
        filtered = {}
        for key, value in source_vars.items():
            if key.startswith(prefix):
                if value:  # exclude_empty=True
                    filtered[key] = value


def stress_regex_filtering() -> None:
    """Simulate regex filtering logic from EnvVariablesDataSource.read()."""
    source_vars = os.environ.copy()
    compiled_regex = re.compile(r"TEST_PREFIX_\d+")

    for _ in range(5_000):
        filtered = {}
        for key, value in source_vars.items():
            if compiled_regex.match(key):
                if value:  # exclude_empty=True
                    filtered[key] = value


def main() -> None:
    stress_key_filtering()
    stress_prefix_filtering()
    stress_regex_filtering()
    print("Env datasource stress test complete.")


if __name__ == "__main__":
    main()
