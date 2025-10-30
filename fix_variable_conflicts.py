#!/usr/bin/env python3
"""
Add file-based prefixes to ALL variables in .plating template files.
This ensures complete uniqueness across all .tf files in the same directory.
Each file's variables get prefixed with the filename (e.g., basic.tf → basic_*).
"""

import os
import re
from pathlib import Path

SRC_DIR = Path("/Users/tim/code/gh/provide-io/pyvider-components/src/pyvider/components")

def find_plating_examples():
    """Find all .plating/examples directories."""
    plating_dirs = []
    for root, dirs, files in os.walk(SRC_DIR):
        if root.endswith(".plating/examples"):
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

    # Count total variables to process
    total_locals = sum(len(vars_info["locals"]) for vars_info in all_vars.values())
    total_outputs = sum(len(vars_info["outputs"]) for vars_info in all_vars.values())

    if total_locals == 0 and total_outputs == 0:
        print("  No variables found")
        return

    print(f"  Processing {total_locals} local variables, {total_outputs} outputs")

    # Fix each file
    for tf_file in non_provider_files:
        content = tf_file.read_text()
        modified = False

        # Get prefix from filename (e.g., "basic.tf" -> "basic_")
        prefix = tf_file.stem + "_"

        # Rename all locals with file prefix
        for var in all_vars[tf_file]["locals"]:
            new_name = prefix + var
            content = rename_variables_in_content(content, var, new_name)
            modified = True
            print(f"    {tf_file.name}: {var} -> {new_name}")

        # Rename all outputs with file prefix
        for out in all_vars[tf_file]["outputs"]:
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

    print("\n✅ Variable prefixing complete! All variables now have file-based prefixes.")
    print("\nNow regenerate examples with:")
    print("  plating plate --generate-examples --examples-dir examples --component-type function --component-type data_source --component-type resource")

if __name__ == "__main__":
    main()
