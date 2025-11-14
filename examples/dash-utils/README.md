# Dash Utils - Non-Python Packaging Demo

This example demonstrates FlavorPack's ability to package **non-Python applications** using the PSPF/2025 format.

## What This Proves

**FlavorPack is NOT Python-only!** The PSPF format is language-agnostic:

- ✅ Package ANY executable (dash, ruby, rust, go, etc.)
- ✅ Use slot system for binaries + data
- ✅ NO Python runtime required at execution
- ✅ Use Go/Rust builders directly (no Python builder)

## Package Contents

**Slot 0: Runtime** - dash binary (~125 KB)
- Static or dynamic dash executable
- POSIX-compliant shell interpreter
- Minimal resource usage

**Slot 1: Application Code** - Shell scripts (~10 KB)
- `dash-utils.sh` - Main dispatcher
- `utils/sysinfo.sh` - System information
- `utils/diskusage.sh` - Disk usage analyzer
- `utils/procmon.sh` - Process monitor
- `utils/netinfo.sh` - Network information
- `utils/benchmark.sh` - Simple benchmark

**Total Package Size:** ~150-300 KB (vs 26+ MB for Python apps!)

## Features

All utilities are pure POSIX shell scripts:

```bash
./dash-utils.psp sysinfo     # System information
./dash-utils.psp diskusage   # Disk usage statistics
./dash-utils.psp procmon     # Process monitoring
./dash-utils.psp netinfo     # Network information
./dash-utils.psp benchmark   # System benchmark
```

## Building the Package

### Option 1: Using Python Builder (pyproject.toml)

```bash
# Python is only used during BUILD, not execution!
flavor pack --manifest pyproject.toml --output dash-utils.psp
```

### Option 2: Using Go/Rust Builder (manifest.json)

```bash
# Use native builder directly - NO Python involved!
flavor-rs-builder-linux_amd64 --manifest manifest.json --output dash-utils.psp
# OR
flavor-go-builder-linux_amd64 --manifest manifest.json --output dash-utils.psp
```

### Option 3: Direct Builder Invocation

```bash
# Call Rust builder directly with JSON manifest
dist/bin/flavor-rs-builder-linux_amd64 \
  --manifest manifest.json \
  --output dash-utils.psp \
  --sign-deterministic dash-utils-v1
```

## Running the Package

```bash
# Make executable
chmod +x dash-utils.psp

# Run commands
./dash-utils.psp help
./dash-utils.psp sysinfo
./dash-utils.psp procmon 10
```

**Output:**
```
╔══════════════════════════════════════════════════════════╗
║                  SYSTEM INFORMATION                      ║
╚══════════════════════════════════════════════════════════╝

Operating System
  Distribution: Ubuntu
  Version:      24.04.3 LTS (Noble Numbat)
  Architecture: x86_64
  Hostname:     runsc

CPU
  Model:  unknown
  Cores:  16

Memory
  Total:     13312 MB
  Available: 12988 MB

Shell: dash (Debian Almquist Shell)
Script: Pure POSIX sh - no Python required!
```

## Verifying the Package

```bash
# Inspect package structure
flavor inspect dash-utils.psp

# Extract to examine contents
flavor extract dash-utils.psp --output-dir /tmp/dash-extracted

# Check workenv cache (after running)
ls -lah ~/.cache/flavor/dash-utils/
# Should see:
#   bin/dash        (Slot 0 - dash binary)
#   scripts/        (Slot 1 - shell scripts)
```

## Architecture

```
dash-utils.psp (PSPF/2025 package)
├── Native Launcher (Go/Rust binary ~2-5 MB)
├── Metadata Block (~1 KB)
├── Slot 0: dash binary (~125 KB gzip compressed)
├── Slot 1: Shell scripts (~10 KB tar.gz)
└── Signature (Ed25519)

On first run:
1. Launcher extracts to ~/.cache/flavor/dash-utils/
2. Slot 0 → {workenv}/bin/dash
3. Slot 1 → {workenv}/scripts/
4. Executes: {workenv}/bin/dash {workenv}/scripts/dash-utils.sh

Subsequent runs:
1. Launcher validates cache checksums
2. Directly executes cached binary (~2ms overhead)
```

## Why This Matters

### Traditional Packaging Problems

**Problem:** Distributing shell scripts
- ❌ Needs tar.gz + README explaining where to extract
- ❌ No version verification
- ❌ No integrity checks
- ❌ Difficult to update
- ❌ Manual PATH setup required

**Solution:** FlavorPack PSPF package
- ✅ Single executable file
- ✅ Cryptographic signing (Ed25519)
- ✅ Automatic extraction to cache
- ✅ Version management built-in
- ✅ Just run it - no installation!

### Language-Agnostic Packaging

FlavorPack can package:
- ✅ **Shell scripts** (dash, bash, zsh)
- ✅ **Ruby applications** (ruby interpreter + gems)
- ✅ **Node.js apps** (node binary + packages)
- ✅ **Go binaries** (static executables)
- ✅ **Rust binaries** (static executables)
- ✅ **Any executable + data files**

The PSPF format doesn't care about the language - it just packages:
1. Runtime/interpreter (slot 0)
2. Application code/data (slot 1+)
3. Execution configuration

## Comparison

| Aspect | Traditional | FlavorPack PSPF |
|--------|-------------|-----------------|
| **Files** | Many (10-100s) | One (.psp) |
| **Installation** | Manual extraction | Automatic |
| **Updates** | Manual download | Single file replacement |
| **Integrity** | MD5/SHA checksums | Ed25519 signature |
| **Dependencies** | User installs | Bundled in package |
| **Size** | Variable | 150-300 KB (this example) |
| **Portability** | Requires compatible shell | Self-contained |

## Performance

**Package Size:**
- dash binary: ~125 KB
- Shell scripts: ~10 KB
- Metadata: ~1 KB
- Launcher: ~2-5 MB
- **Total:** ~2.2-5.2 MB (mostly launcher)

**Execution Performance:**
- First run: ~500ms (extraction)
- Cached runs: ~5-10ms (native dash overhead)
- Script execution: Identical to native
- Memory: 1-2 MB (dash process only)

## Manifest Formats

FlavorPack supports multiple manifest formats:

### TOML (pyproject.toml)
```toml
[tool.flavor]
package_name = "dash-utils"
entry_point = "package_dash:main"

[tool.flavor.execution]
command = "{workenv}/bin/dash"
args = ["{workenv}/scripts/dash-utils.sh"]
```

### JSON (manifest.json)
```json
{
  "package": {"name": "dash-utils"},
  "execution": {
    "command": "{workenv}/bin/dash",
    "args": ["{workenv}/scripts/dash-utils.sh"]
  }
}
```

### YAML (manifest.yaml)
```yaml
package:
  name: dash-utils
execution:
  command: "{workenv}/bin/dash"
  args:
    - "{workenv}/scripts/dash-utils.sh"
```

## Extending to Other Languages

### Ruby Example

```json
{
  "package": {"name": "ruby-cli"},
  "execution": {
    "command": "{workenv}/bin/ruby",
    "args": ["{workenv}/app/main.rb"]
  },
  "slots": [
    {"id": 0, "path": "bin/ruby"},
    {"id": 1, "path": "app/"},
    {"id": 2, "path": "vendor/gems/"}
  ]
}
```

### Node.js Example

```json
{
  "package": {"name": "node-cli"},
  "execution": {
    "command": "{workenv}/bin/node",
    "args": ["{workenv}/app/index.js"]
  },
  "slots": [
    {"id": 0, "path": "bin/node"},
    {"id": 1, "path": "app/"},
    {"id": 2, "path": "node_modules/"}
  ]
}
```

## Next Steps

1. **Try the package:** Run the utilities and explore the cache
2. **Inspect the workenv:** See how slots are extracted
3. **Create your own:** Package a Ruby/Node/Go app
4. **Use pretaster:** Validate across builder/launcher combinations

## Resources

- **FlavorPack:** https://github.com/provide-io/flavorpack
- **PSPF Spec:** `docs/reference/spec/FEP-0001-core-format-and-operation-chains.md`
- **Slot System:** `docs/reference/spec/SLOT_DESCRIPTOR_SPECIFICATION.md`
- **Examples:** `examples/` directory

---

**Key Takeaway:** FlavorPack is a **universal packaging system** for executable applications, not just Python. The PSPF format works with ANY language that produces executables and data files!
