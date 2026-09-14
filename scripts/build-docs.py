#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Materialize shared Foundry scaffolding and build the documentation strictly."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Prepare ignored shared files, then build the authored MkDocs site."""
    try:
        from provide.foundry.config import extract_base_mkdocs
    except ModuleNotFoundError:
        print(
            "provide-foundry is unavailable; install the locked docs dependency group",
            file=sys.stderr,
        )
        return 1

    inherited_config = extract_base_mkdocs(ROOT)
    if not inherited_config.is_file():
        print(f"Foundry did not materialize {inherited_config}", file=sys.stderr)
        return 1

    subprocess.run(["mkdocs", "build", "--strict"], cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
