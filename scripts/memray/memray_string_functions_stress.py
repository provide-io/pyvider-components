#!/usr/bin/env python
"""Memray stress test for string manipulation and type conversion functions."""

import os

os.environ["PLUGIN_LOG_LEVEL"] = "ERROR"

from pyvider.components.functions.string_manipulation import (
    format_str,
    join,
    lower,
    replace,
    split,
    upper,
)
from pyvider.components.functions.type_conversion_functions import tostring


def main() -> None:
    # 10K calls to tostring with varied types
    for i in range(10_000):
        mod = i % 6
        if mod == 0:
            tostring(True)
        elif mod == 1:
            tostring(False)
        elif mod == 2:
            tostring(i)
        elif mod == 3:
            tostring(3.14159 * i)
        elif mod == 4:
            tostring(f"string_{i}")
        else:
            tostring(None)

    # 10K calls to format_str with templates and value lists
    for i in range(10_000):
        format_str("Hello {}, you are {} years old", [f"user_{i}", str(i % 100)])

    # 5K calls to upper
    for i in range(5_000):
        upper(f"hello world {i}")

    # 5K calls to lower
    for i in range(5_000):
        lower(f"HELLO WORLD {i}")

    # 5K calls to join
    for i in range(5_000):
        join(", ", [f"item_{j}" for j in range(i % 5 + 1)])

    # 5K calls to split
    for i in range(5_000):
        split(",", f"a,b,c,d,e,{i}")

    # 5K calls to replace
    for i in range(5_000):
        replace(f"hello world {i} hello", "hello", "hi")

    print("String functions stress test complete.")


if __name__ == "__main__":
    main()
