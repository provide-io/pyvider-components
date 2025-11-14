# SysInfo - System Information CLI Tool

A beautiful system information tool packaged as a single executable using FlavorPack (PSPF/2025).

## Features

- **Zero Installation**: Just download and run - no dependencies required
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Self-Contained**: Everything bundled in a single `.psp` executable
- **Secure**: Cryptographically signed with Ed25519 signatures
- **Fast**: Cached work environment for instant startup

## Usage

```bash
# Show all information
./sysinfo.psp

# Show only system details
./sysinfo.psp --system

# Show only environment details
./sysinfo.psp --env

# Show only process details
./sysinfo.psp --process

# Output as JSON
./sysinfo.psp --json
```

## Packaging with FlavorPack

This tool demonstrates FlavorPack's capability to package Python CLI tools into single executables:

```bash
# Generate signing keys (optional for demo)
flavor keygen --output keys/

# Build the package
flavor pack --manifest pyproject.toml --output sysinfo.psp

# Verify the package
flavor verify sysinfo.psp

# Inspect the package structure
flavor inspect sysinfo.psp

# Run it!
./sysinfo.psp
```

## Package Structure (PSPF/2025)

```
sysinfo.psp (Single Executable)
├── Native Launcher (Go/Rust compiled, 2-5 MB)
├── Metadata (GZIP JSON, ~10 KB)
├── Slot Table (64 bytes per slot)
├── Slot 0: UV binary (tool, gzip compressed)
├── Slot 1: Python runtime (tar.gz, ~45 MB)
├── Slot 2: Application wheels (tar.gz)
└── Index Block (8 KB, with Ed25519 signature)
```

## Benefits of PSPF Packaging

1. **Single File**: Distribute one file instead of many
2. **No Dependencies**: Users don't need Python installed
3. **Verified Integrity**: Ed25519 signatures prevent tampering
4. **Smart Caching**: Fast subsequent runs (~2ms overhead)
5. **Reproducible**: Deterministic builds ensure consistency

## About FlavorPack

FlavorPack implements the Progressive Secure Package Format (PSPF/2025), a polyglot packaging system for creating self-contained Python executables.

Learn more: https://github.com/provide-io/flavorpack
