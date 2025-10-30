#!/usr/bin/env python3
"""
Fix variable name conflicts in .plating template files.
Adds prefixes to local variables and outputs based on the filename to ensure uniqueness.
"""

import os
import re
from pathlib import Path

SRC_DIR = Path("/Users/tim/code/gh/provide-io/pyvider-components/src/pyvider/components")

def find_plating_examples():
    """Find all .plating/examples directories."""
    plating_dirs = []
    for root, dirs, files in os.walk(SRC_DIR):
        if root.endswith("/.plating/examples") or "/.plating/examples/" in root:
            plating_dirs.append(Path(root))
    return plating_dirs

def get_local_vars(content):
    """Extract local variable names from a terraform file."""
    locals_pattern = r'locals\s*\{([^}]*)\}'
    local_vars = set()

    for match in re.finditer(locals_pattern, content, re.DOTALL):
        block = match.group(1)
        # Find variable definitions
        for var_match in re.finditer(r'^\s*(\w+)\s*=', block, re.MULTILINE):
            local_vars.add(var_match.group(1))

    return local_vars

def get_output_names(content):
    """Extract output names from a terraform file."""
    output_pattern = r'output\s+"(\w+)"'
    outputs = set()

    for match in re.finditer(output_pattern, content):
        outputs.add(match.group(1))

    return outputs

def rename_variables_in_content(content, old_name, new_name):
    """Rename a variable throughout the content."""
    # Rename in locals block definitions
    content = re.sub(
        r'(locals\s*\{[^}]*\b)' + re.escape(old_name) + r'(\s*=)',
        r'\1' + new_name + r'\2',
        content,
        flags=re.DOTALL
    )

    # Rename in local references
    content = re.sub(
        r'\blocal\.' + re.escape(old_name) + r'\b',
        f'local.{new_name}',
        content
    )

    # Rename in output blocks
    content = re.sub(
        r'(output\s+")\w+(")',
        r'\1' + new_name + r'\2',
        content
    )

    return content

def fix_example_directory(examples_dir):
    """Fix variable conflicts in an examples directory."""
    tf_files = list(examples_dir.glob("*.tf"))

    # Skip if only provider.tf or single example
    non_provider_files = [f for f in tf_files if f.name not in ["provider.tf", "example.tf"]]

    if len(non_provider_files) <= 1:
        return

    print(f"\nFixing: {examples_dir}")

    # Collect all variable names from all files
    all_vars = {}
    for tf_file in non_provider_files:
        content = tf_file.read_text()
        local_vars = get_local_vars(content)
        outputs = get_output_names(content)
        all_vars[tf_file] = {"locals": local_vars, "outputs": outputs}

    # Find conflicts
    local_counts = {}
    output_counts = {}

    for tf_file, vars_info in all_vars.items():
        for var in vars_info["locals"]:
            local_counts[var] = local_counts.get(var, 0) + 1
        for out in vars_info["outputs"]:
            output_counts[out] = output_counts.get(out, 0) + 1

    conflicts = {var for var, count in local_counts.items() if count > 1}
    output_conflicts = {var for var, count in output_counts.items() if count > 1}

    if not conflicts and not output_conflicts:
        print("  No conflicts found")
        return

    print(f"  Found {len(conflicts)} local conflicts, {len(output_conflicts)} output conflicts")

    # Fix each file
    for tf_file in non_provider_files:
        content = tf_file.read_text()
        modified = False

        # Get prefix from filename (e.g., "basic.tf" -> "basic_")
        prefix = tf_file.stem + "_"

        # Rename conflicting locals
        for var in all_vars[tf_file]["locals"]:
            if var in conflicts:
                new_name = prefix + var
                content = rename_variables_in_content(content, var, new_name)
                modified = True
                print(f"    {tf_file.name}: {var} -> {new_name}")

        # Rename conflicting outputs
        for out in all_vars[tf_file]["outputs"]:
            if out in output_conflicts:
                new_name = prefix + out
                # Rename output
                content = re.sub(
                    r'output\s+"' + re.escape(out) + r'"',
                    f'output "{new_name}"',
                    content
                )
                modified = True
                print(f"    {tf_file.name}: output {out} -> {new_name}")

        if modified:
            tf_file.write_text(content)

def main():
    print("Finding .plating/examples directories...")
    plating_dirs = find_plating_examples()
    print(f"Found {len(plating_dirs)} directories")

    for examples_dir in plating_dirs:
        fix_example_directory(examples_dir)

    print("\n✅ Variable conflict fixing complete!")
    print("\nNow regenerate examples with:")
    print("  plating plate --generate-examples --examples-dir examples --component-type function --component-type data_source --component-type resource")

if __name__ == "__main__":
    main()
