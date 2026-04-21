#!/usr/bin/env python
"""Memray stress test for collection manipulation functions."""

import os

os.environ["PLUGIN_LOG_LEVEL"] = "ERROR"

from pyvider.components.functions.collection_functions import contains, length, lookup


def main() -> None:
    # 20K calls to lookup with varying map sizes and keys
    small_map = {"a": 1, "b": 2, "c": 3}
    medium_map = {f"key_{i}": i for i in range(50)}
    large_map = {f"key_{i}": f"value_{i}" for i in range(200)}

    for i in range(20_000):
        mod = i % 4
        if mod == 0:
            lookup(small_map, "a")
        elif mod == 1:
            lookup(medium_map, f"key_{i % 50}")
        elif mod == 2:
            lookup(large_map, f"key_{i % 200}")
        else:
            # Not-found with default
            lookup(small_map, "missing", f"default_{i}")

    # 10K calls to length with lists, dicts, strings
    for i in range(10_000):
        mod = i % 3
        if mod == 0:
            length([1, 2, 3, 4, 5])
        elif mod == 1:
            length({"a": 1, "b": 2})
        else:
            length(f"hello world {i}")

    # 10K calls to contains with lists and strings
    test_list = list(range(100))
    for i in range(10_000):
        mod = i % 2
        if mod == 0:
            contains(test_list, i % 100)
        else:
            contains(test_list, i + 1000)  # Not found

    print("Collection functions stress test complete.")


if __name__ == "__main__":
    main()
