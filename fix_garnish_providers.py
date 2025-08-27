#!/usr/bin/env python3
"""Fix all provider.tf files in .garnish-tests to use registry provider."""

import os
from pathlib import Path
import subprocess

def fix_provider_tf(file_path):
    """Fix a single provider.tf file."""
    correct_content = """terraform {
  required_providers {
    pyvider = {
      source  = "registry.terraform.io/provide-io/pyvider"
      version = "0.0.3"
    }
  }
}

provider "pyvider" {
  # Provider configuration for tests
}
"""
    with open(file_path, 'w') as f:
        f.write(correct_content)
    print(f"Fixed: {file_path}")

def test_example(test_dir):
    """Test a single example."""
    os.chdir(test_dir)
    
    # Clean
    for item in ['.terraform', '.terraform.lock.hcl']:
        subprocess.run(['rm', '-rf', item], capture_output=True)
    
    # Init
    result = subprocess.run(['terraform', 'init'], capture_output=True, text=True)
    if result.returncode != 0:
        return False, "init failed"
    
    # Plan
    result = subprocess.run(['terraform', 'plan'], capture_output=True, text=True)
    if result.returncode != 0:
        return False, "plan failed"
    
    return True, "PASS"

def main():
    base_dir = Path('/Users/tim/code/gh/provide-io/pyvider-components')
    garnish_dir = base_dir / '.garnish-tests'
    
    if not garnish_dir.exists():
        print("No .garnish-tests directory found")
        return
    
    print("Fixing all provider.tf files...")
    print("-" * 50)
    
    # Fix all provider.tf files
    count = 0
    for provider_file in garnish_dir.glob('*/provider.tf'):
        fix_provider_tf(provider_file)
        count += 1
    
    print(f"\nFixed {count} provider.tf files")
    
    # Test a few examples
    print("\nTesting examples...")
    print("-" * 50)
    
    os.environ['PYVIDER_PRIVATE_STATE_SHARED_SECRET'] = 'test-secret'
    
    test_cases = [
        'function_add_test',
        'resource_local_directory_test',
        'data_source_env_variables_test',
        'resource_timed_token_test'
    ]
    
    for test_name in test_cases:
        test_path = garnish_dir / test_name
        if test_path.exists():
            success, msg = test_example(str(test_path))
            status = "✅ PASS" if success else f"❌ {msg}"
            print(f"{test_name}: {status}")
    
    print("\n" + "=" * 50)
    print("✅ All provider.tf files have been fixed!")
    print("The tests should now work when you run: garnish test")
    print("=" * 50)

if __name__ == '__main__':
    main()