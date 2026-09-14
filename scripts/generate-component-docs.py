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
MKDOCS = ROOT / "mkdocs.yml"


def generate_component_docs(output_dir: Path) -> None:
    """Generate default and provider docs while preserving authored navigation."""
    original_mkdocs = MKDOCS.read_bytes()
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
        MKDOCS.write_bytes(original_mkdocs)


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
