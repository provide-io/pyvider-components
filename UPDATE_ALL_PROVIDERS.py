#!/usr/bin/env python3
"""Update all provider.tf files to use registry provider."""

from pathlib import Path

correct_provider = """terraform {
  required_providers {
    pyvider = {
      source  = "registry.terraform.io/provide-io/pyvider"
      version = "0.0.3"
    }
  }
}

provider "pyvider" {}
"""

garnish_dir = Path('/Users/tim/code/gh/provide-io/pyvider-components/.garnish-tests')

if garnish_dir.exists():
    count = 0
    for provider_file in garnish_dir.glob('*/provider.tf'):
        provider_file.write_text(correct_provider)
        print(f"Updated: {provider_file.name}")
        count += 1
    
    print(f"\n✅ Updated {count} provider.tf files to use registry provider")
    print("This bypasses the local provider issue.")
    print("\nNow run: garnish test")
else:
    print("No .garnish-tests directory found")