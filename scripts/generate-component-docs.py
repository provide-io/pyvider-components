#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Generate all published component documentation with Plating."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def generate_component_docs(output_dir: Path) -> None:
    """Generate default and provider docs while preserving authored navigation."""
    output_dir = output_dir.resolve()
    navigation_target = output_dir.parent / "mkdocs.yml"
    navigation_existed = navigation_target.exists()
    original_navigation = navigation_target.read_bytes() if navigation_existed else None
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(["plating", "plate", "--output-dir", str(output_dir)], cwd=ROOT, check=True)
        subprocess.run(
            [
                "plating",
                "plate",
                "--output-dir",
                str(output_dir),
                "--component-type",
                "provider",
            ],
            cwd=ROOT,
            check=True,
        )
    finally:
        if navigation_existed:
            assert original_navigation is not None
            navigation_target.write_bytes(original_navigation)
        else:
            navigation_target.unlink(missing_ok=True)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the command-line interface."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        metavar="PATH",
        type=Path,
        help="directory that retains generated docs; omit to generate in a disposable temporary directory",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the supported component documentation workflow."""
    args = parse_args(argv)
    if args.output_dir is not None:
        generate_component_docs(args.output_dir.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix="pyvider-component-docs-") as temporary_dir:
            generate_component_docs(Path(temporary_dir) / "docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
