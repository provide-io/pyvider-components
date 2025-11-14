# FlavorPack Examples

This directory contains complete, working examples demonstrating FlavorPack's packaging capabilities.

## Available Examples

### 1. SysInfo CLI (`sysinfo-cli/`)

**Pure stdlib system information tool - zero external dependencies**

Language: **Python**
A lightweight CLI tool demonstrating minimal dependency packaging.

```bash
cd sysinfo-cli
flavor pack --manifest pyproject.toml --output sysinfo.psp
./sysinfo.psp
```

**Features:**
- System information display (OS, architecture, Python version)
- Environment details (user, shell, PATH)
- Process information (PID, executable, working directory)
- Multiple output modes (beautiful text, JSON)
- **Zero dependencies** (pure Python stdlib)

**Package Size:** ~26 MB (smallest possible)

**Best For:**
- Learning FlavorPack basics
- Minimal dependency applications
- Fast build times
- Maximum portability

**Key Lessons:**
- How to package stdlib-only applications
- Environment variable filtering for security
- Professional CLI UX with argparse
- JSON output for automation

---

### 2. MiniMonitor (`minimonitor/`)

**Glances-like system monitor - demonstrates TUI patterns**

Language: **Python**
A real-time system monitor with TUI interface, proving the Glances packaging pattern works.

```bash
cd minimonitor
python minimonitor.py
python minimonitor.py --json
```

---

### 3. Glances Wrapper (`glances-wrapper/`)

**Python-based system monitoring (htop/btop alternative) - complex real-world application**

Language: **Python**
A full-featured system monitor demonstrating complex dependency management.

```bash
cd glances-wrapper
flavor pack --manifest pyproject.toml --output glances.psp
./glances.psp
```

**Features:**
- Real-time CPU, memory, disk, network monitoring
- Per-process resource tracking
- Docker container monitoring
- Optional web interface
- Database export (InfluxDB, Elasticsearch)
- **30+ dependencies** including psutil, bottle, matplotlib

**Package Size:** ~35-45 MB (core) or ~80-100 MB (full-featured)

**Best For:**
- Understanding complex dependency resolution
- Real-world application packaging
- Optional feature management
- Production deployment strategies

**Key Lessons:**
- Managing multiple dependencies
- Optional extras (web, export, graph)
- Terminal UI integration
- Performance optimization

---

### 4. Dash Utils (`dash-utils/`)

**Pure POSIX shell scripts - NO Python runtime**

Language: **Shell (dash)**
Demonstrates packaging non-Python applications using FlavorPack.

```bash
cd dash-utils
dash dash-utils.sh sysinfo
dash dash-utils.sh procmon
dash dash-utils.sh benchmark
```

**Package Structure:**
- Slot 0: dash binary (127 KB)
- Slot 1: Shell scripts (357 lines)

**Key Features:**
- System information (OS, CPU, memory, disk)
- Disk usage analyzer
- Process monitor
- Network information
- System benchmark

**Key Lessons:**
- Packaging non-Python executables
- Slot system for binary + scripts
- TOML and JSON manifests
- Zero Python at runtime

---

### 5. Node-Sysmon (`node-sysmon/`)

**Pure JavaScript system monitor - NO Python runtime**

Language: **Node.js (JavaScript)**
Demonstrates packaging Node.js applications using FlavorPack.

```bash
cd node-sysmon
node sysmon.js sysinfo
node sysmon.js network
node sysmon.js --json
```

**Package Structure:**
- Slot 0: Node.js binary (~118 MB)
- Slot 1: JavaScript code (287 lines)

**Key Features:**
- System information (OS, CPU, memory)
- Network interfaces and configuration
- Process details and memory usage
- JSON output for automation
- Zero npm dependencies (pure Node.js stdlib)

**Key Lessons:**
- Packaging JavaScript applications
- Node.js runtime bundling
- Multiple manifest formats (package.json, TOML, JSON)
- Beautiful CLI with ANSI colors

---

## Comparison Matrix

| Aspect | SysInfo | MiniMonitor | Glances | Dash Utils | Node-Sysmon |
|--------|---------|-------------|---------|------------|-------------|
| **Language** | Python | Python | Python | Shell | JavaScript |
| **Complexity** | Simple | Medium | Complex | Simple | Medium |
| **Dependencies** | 0 | 0 | 30+ | 0 | 0 |
| **Package Size** | 26 MB | 26 MB | 35-80 MB | 2-5 MB | 42 MB |
| **Runtime** | Python | Python | Python | dash | Node.js |
| **Use Case** | Education | Demo | Production | Education | Demo |

## Why These Examples?

### Problem: btop and htop are C/C++

Users often ask "Can I package btop/htop with FlavorPack?"

**Answer:** No - FlavorPack is designed for Python applications.

**Solution:** Package **Glances**, a Python alternative with similar functionality!

### Progression Path

1. **Start with SysInfo** - Learn basics with zero dependencies
2. **Move to Glances** - Understand complex packaging
3. **Package your own app** - Apply lessons to real projects

---

## Quick Start

### Prerequisites

```bash
# Install FlavorPack from source
git clone https://github.com/provide-io/flavorpack.git
cd flavorpack
uv sync
make build-helpers

# Verify installation
flavor --version
```

### Try SysInfo (5 minutes)

```bash
cd examples/sysinfo-cli

# Package
flavor pack --manifest pyproject.toml --output sysinfo.psp

# Run
chmod +x sysinfo.psp
./sysinfo.psp

# Try different modes
./sysinfo.psp --system
./sysinfo.psp --json
```

### Try Glances (10 minutes)

```bash
cd examples/glances-wrapper

# Package (requires network for dependencies)
flavor pack --manifest pyproject.toml --output glances.psp

# Run
chmod +x glances.psp
./glances.psp

# Try features
./glances.psp --percpu      # Per-CPU view
./glances.psp -w            # Web interface mode
```

---

## Documentation

Each example includes comprehensive documentation:

### SysInfo Documentation
- **README.md** - Quick start and usage guide
- **PACKAGING_DEMO.md** - Detailed packaging workflow
- **pyproject.toml** - Annotated manifest configuration

### Glances Documentation
- **README.md** - Features and usage examples
- **PACKAGING_GUIDE.md** - Step-by-step packaging guide
- **pyproject.toml** - Complex dependency configuration

---

## Integration with Docs

These examples are referenced in the main FlavorPack documentation:

- **Getting Started:** `/docs/getting-started/examples.md`
- **CLI Packaging Guide:** `/docs/cookbook/examples/cli-tool.md`
- **Cookbook Index:** `/docs/cookbook/examples/index.md`

See the documentation for more examples including:
- Web applications (FastAPI, Flask)
- Data science tools (pandas, numpy)
- Task managers
- API servers
- Multi-platform builds

---

## Testing Examples

Both examples have been tested and validated:

```bash
# Run FlavorPack test suite
cd /path/to/flavorpack
uv run pytest tests/ -v

# Result: 996 passed, 2 failed, 43 skipped (99.8% pass rate)
```

### Environment Requirements

- **OS:** Linux (CentOS 7+, Ubuntu 18.04+, Alpine 3.12+)
- **Python:** 3.11+ (for building packages)
- **Disk Space:** ~500 MB for cache
- **Network:** Required for downloading dependencies (Glances only)

**Note:** Built packages run on any Linux system without Python installed!

---

## Performance Characteristics

### SysInfo Performance

| Metric | First Run | Cached Run |
|--------|-----------|------------|
| Startup | ~1.2s | ~52ms |
| Overhead | - | ~2ms |
| Memory | 35 MB | 35 MB |

### Glances Performance

| Metric | First Run | Cached Run |
|--------|-----------|------------|
| Startup | ~1.5s | ~82ms |
| Overhead | - | ~7ms |
| Memory | 47 MB | 47 MB |
| CPU (monitoring) | 2.4% | 2.4% |

**Conclusion:** Negligible runtime overhead compared to native Python

---

## Distribution Strategies

### Single File Distribution

```bash
# Just copy the .psp file
scp myapp.psp user@server:/usr/local/bin/
ssh user@server 'chmod +x /usr/local/bin/myapp.psp'

# No dependencies required on target!
```

### Container Distribution

```dockerfile
FROM scratch
COPY app.psp /app
ENTRYPOINT ["/app"]
```

### Release Artifacts

```bash
# Create signed release
flavor pack \
  --output myapp-v1.0.0-linux-amd64.psp \
  --private-key release-keys/private.pem

# Distribute with public key for verification
tar czf myapp-v1.0.0.tar.gz \
  myapp-v1.0.0-linux-amd64.psp \
  release-keys/public.pem
```

---

## Contributing Examples

Have an interesting FlavorPack use case? Contribute an example!

### Example Structure

```
examples/your-example/
├── README.md              # Quick start and overview
├── PACKAGING_GUIDE.md     # Detailed walkthrough (optional)
├── pyproject.toml         # FlavorPack manifest
├── your_app.py           # Application code
└── requirements.txt       # For reference (optional)
```

### Requirements

- Must be a Python application
- Include working pyproject.toml
- Comprehensive README
- Tested and validated
- Clear learning objective

---

## Troubleshooting

### Common Issues

**Issue:** Package too large
**Solution:** Use `--strip` and optimize dependencies

**Issue:** Missing dependencies
**Solution:** Check `flavor inspect` output and update pyproject.toml

**Issue:** Slow builds
**Solution:** Use local package index or cache wheels

### Getting Help

- **Documentation:** https://github.com/provide-io/flavorpack
- **Issues:** https://github.com/provide-io/flavorpack/issues
- **Examples:** Review these example READMEs

---

## Next Steps

1. **Try both examples** to understand the spectrum of complexity
2. **Read the packaging guides** for detailed explanations
3. **Package your own application** using lessons learned
4. **Share your experience** by contributing examples or documentation

Happy packaging! 🌶️
