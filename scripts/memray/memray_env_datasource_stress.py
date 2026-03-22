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
            if value is not None and value:  # exclude_empty=True
                filtered[key] = value


def stress_prefix_filtering() -> None:
    """Simulate prefix filtering logic from EnvVariablesDataSource.read()."""
    source_vars = os.environ.copy()
    prefix = "MYAPP_"
    _startswith = str.startswith

    for _ in range(5_000):
        filtered = {}
        for key, value in source_vars.items():
            if _startswith(key, prefix) and value:  # exclude_empty=True
                filtered[key] = value


def stress_regex_filtering() -> None:
    """Simulate regex filtering logic from EnvVariablesDataSource.read()."""
    source_vars = os.environ.copy()
    regex_str = r"TEST_PREFIX_\d+"
    compiled_regex = re.compile(regex_str)
    # Mirror production code: extract literal prefix for fast pre-filtering
    _regex_special = frozenset(r"\[](){}*+?.|^$")
    prefix_chars: list[str] = []
    for ch in regex_str:
        if ch in _regex_special:
            break
        prefix_chars.append(ch)
    literal_pfx = "".join(prefix_chars)
    _match = compiled_regex.match

    for _ in range(5_000):
        filtered = {}
        for key, value in source_vars.items():
            if literal_pfx and not key.startswith(literal_pfx):
                continue
            if _match(key) and value:  # exclude_empty=True
                filtered[key] = value


def main() -> None:
    stress_key_filtering()
    stress_prefix_filtering()
    stress_regex_filtering()
    print("Env datasource stress test complete.")


if __name__ == "__main__":
    main()
