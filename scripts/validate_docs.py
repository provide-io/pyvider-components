#!/usr/bin/env python3
"""Simple script to validate Terraform provider documentation."""

import re
import sys
from pathlib import Path


def validate_frontmatter(file_path: Path) -> tuple[bool, str]:
    """Validate frontmatter in a markdown file."""
    content = file_path.read_text()

    # Check if starts with ---
    if not content.startswith("---\n"):
        return False, "Missing frontmatter opening ---"

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False, "Missing frontmatter closing ---"

    frontmatter = parts[1]

    # Check for required fields
    has_page_title = "page_title:" in frontmatter
    has_description = "description:" in frontmatter
    has_subcategory = "subcategory:" in frontmatter

    # Extract subcategory value
    subcategory_match = re.search(r'subcategory:\s*["\']([^"\']+)["\']', frontmatter)
    subcategory = subcategory_match.group(1) if subcategory_match else None

    issues = []
    if not has_page_title:
        issues.append("Missing page_title")
    if not has_description:
        issues.append("Missing description")
    if not has_subcategory:
        issues.append("Missing subcategory")
    elif subcategory not in ["Utilities", "Lens", "Test Mode"]:
        issues.append(f"Invalid subcategory: {subcategory}")

    if issues:
        return False, ", ".join(issues)

    return True, subcategory


def main() -> None:
    docs_dir = Path("/Users/tim/code/gh/provide-io/pyvider-components/docs")

    if not docs_dir.exists():
        print(f"❌ Documentation directory not found: {docs_dir}")
        sys.exit(1)

    print("🔍 Validating Terraform Provider Documentation\n")

    # Find all markdown files
    md_files = []
    for subdir in ["resources", "data-sources", "functions"]:
        subdir_path = docs_dir / subdir
        if subdir_path.exists():
            md_files.extend(subdir_path.glob("*.md"))

    if not md_files:
        print("❌ No markdown files found")
        sys.exit(1)

    print(f"Found {len(md_files)} documentation files\n")

    # Validate each file
    valid_count = 0
    invalid_count = 0
    categories = {"Utilities": [], "Lens": [], "Test Mode": []}

    for file_path in sorted(md_files):
        is_valid, result = validate_frontmatter(file_path)

        if is_valid:
            valid_count += 1
            categories[result].append(file_path.name)
            print(f"✅ {file_path.relative_to(docs_dir)}: {result}")
        else:
            invalid_count += 1
            print(f"❌ {file_path.relative_to(docs_dir)}: {result}")

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"Summary: {valid_count} valid, {invalid_count} invalid\n")

    print("📊 Components by Category:")
    for category, files in sorted(categories.items()):
        if files:
            print(f"\n  {category} ({len(files)}):")
            for file in sorted(files):
                print(f"    • {file}")

    print(f"\n{'=' * 60}")

    if invalid_count > 0:
        print("\n❌ Validation failed")
        sys.exit(1)
    else:
        print("\n✅ All documentation files are valid!")
        print("\n💡 Your documentation is ready for the Terraform Registry!")
        print("   The registry will display components grouped by these categories.")
        sys.exit(0)


if __name__ == "__main__":
    main()
