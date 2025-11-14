# Glances Portable - System Monitoring with FlavorPack

This example demonstrates packaging **Glances**, a popular Python-based system monitoring tool, as a portable PSPF package.

## About Glances

**Glances** is a cross-platform monitoring tool written in Python that provides:
- CPU, memory, disk, and network monitoring
- Per-process resource usage
- Docker container monitoring
- Sensor monitoring (temperature, fans)
- Web interface mode
- Export to various databases (InfluxDB, Elasticsearch, etc.)

**Why Glances?**
- Pure Python (unlike htop/btop which are C/C++)
- Rich feature set similar to htop/btop
- Active development and maintenance
- Extensive plugin ecosystem

## Packaging

### Basic Package (TUI only)

```bash
# Package with core dependencies only
cd examples/glances-wrapper
flavor pack --manifest pyproject.toml --output glances.psp

# The resulting package includes:
# - Glances TUI application
# - psutil for system metrics
# - All Python dependencies
# - Package size: ~35-45 MB
```

### Full-Featured Package

```bash
# Package with web interface and export features
flavor pack \
  --manifest pyproject.toml \
  --output glances-full.psp \
  --extras web,export,graph

# Additional features:
# - Built-in web server (access via browser)
# - Export to time-series databases
# - Graph generation with matplotlib
# - Package size: ~80-100 MB
```

## Usage

### Basic Monitoring

```bash
# Run glances in default mode
./glances.psp

# Run in minimal mode
./glances.psp -1

# Run in per-CPU mode
./glances.psp --percpu

# Refresh every 5 seconds
./glances.psp -t 5
```

### Web Server Mode

```bash
# Start web interface on port 61208
./glances.psp -w

# Custom port
./glances.psp -w --port 8080

# Access in browser: http://localhost:61208
```

### Remote Monitoring

```bash
# Server mode (listen for clients)
./glances.psp -s

# Client mode (connect to server)
./glances.psp -c <server-ip>
```

### Export to Databases

```bash
# Export to InfluxDB
./glances.psp --export influxdb

# Export to Elasticsearch
./glances.psp --export elasticsearch

# Export to CSV
./glances.psp --export csv --export-csv-file /tmp/glances.csv
```

## Configuration

Glances can be configured via `~/.config/glances/glances.conf`:

```ini
[global]
check_update=false
refresh=2

[cpu]
user_careful=50
user_warning=70
user_critical=90

[memory]
careful=50
warning=70
critical=90
```

## Distribution

### Single Executable

```bash
# Rename for convenience
mv glances.psp /usr/local/bin/glances
chmod +x /usr/local/bin/glances

# Now available system-wide
glances
```

### Docker Integration

```dockerfile
FROM scratch
COPY glances.psp /glances
ENTRYPOINT ["/glances"]
CMD ["-w"]
EXPOSE 61208
```

```bash
docker build -t glances-portable .
docker run -p 61208:61208 glances-portable
```

## Comparison with Native Glances

### Before FlavorPack (Traditional Install)

```bash
# Requires Python installation
sudo apt install python3 python3-pip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install glances and dependencies
pip install glances[web,export]

# Must activate venv every time
source venv/bin/activate
glances
```

**Issues:**
- ❌ Requires Python and pip
- ❌ Virtual environment management
- ❌ Dependency conflicts with system packages
- ❌ Different versions across machines
- ❌ Complex deployment

### After FlavorPack (Portable Package)

```bash
# Download single file
./glances.psp
```

**Benefits:**
- ✅ No Python installation required
- ✅ No virtual environment needed
- ✅ Consistent version everywhere
- ✅ Single file distribution
- ✅ Zero configuration
- ✅ Cryptographically signed

## Performance

**Package Size:**
- Core TUI: ~35-45 MB
- With web interface: ~50-60 MB
- Full featured: ~80-100 MB

**Runtime Performance:**
- First run: ~1.5s (extraction to cache)
- Subsequent runs: ~80-100ms startup
- Runtime overhead: <3ms (negligible)
- Monitoring accuracy: Identical to native

**Cache Location:** `~/.cache/flavor/glances-portable/`

## Advanced Features

### Custom Plugins

You can package custom Glances plugins:

```python
# custom_plugin.py
from glances.plugins.plugin.model import GlancesPluginModel

class Plugin(GlancesPluginModel):
    def update(self):
        # Your monitoring logic
        pass
```

Update `pyproject.toml`:
```toml
[tool.flavor.slots.plugins]
id = 3
path = "plugins/"
extract_to = "{workenv}/lib/python3.11/site-packages/glances/plugins"
lifecycle = "cached"
operations = "tar.gz"
```

### Pre-configured Setup

Include default configuration in package:

```toml
[tool.flavor.slots.config]
id = 4
path = "glances.conf"
extract_to = "{home}/.config/glances/glances.conf"
lifecycle = "persistent"
operations = "identity"
```

## Security Considerations

**Environment Isolation:**
- Only essential variables passed through
- No access to sensitive environment variables
- Sandboxed execution environment

**Integrity:**
- Cryptographic signature verification
- Tamper detection via Ed25519
- Reproducible builds

**Network Access:**
- Web mode only opens local ports
- Export features require explicit configuration
- No automatic external connections

## Troubleshooting

### Terminal Not Detected

```bash
# Ensure TERM is set
export TERM=xterm-256color
./glances.psp
```

### Sensors Not Working

```bash
# Install lm-sensors on host (required for hardware sensors)
sudo apt install lm-sensors
sudo sensors-detect

# Then run glances
./glances.psp --enable-plugin sensors
```

### High CPU Usage

```bash
# Increase refresh interval
./glances.psp -t 5  # 5 second refresh

# Disable heavy plugins
./glances.psp --disable-plugin docker,gpu
```

## Why This Example Matters

This demonstrates FlavorPack's ability to package **complex, dependency-heavy Python applications**:

1. **Real-world application** - Not a toy example
2. **Multiple dependencies** - psutil, bottle, influxdb-client, etc.
3. **System integration** - Requires terminal access, sensors, proc filesystem
4. **Optional features** - Web server, database exports, plugins
5. **Cross-platform** - Works on any Linux distribution

Compare to native package managers:
- **apt/yum:** Tied to distribution, outdated versions
- **pip:** Requires Python, virtual environments, conflicts
- **snap/flatpak:** Large overhead, complex runtimes
- **FlavorPack:** Single file, no runtime, signed, portable

## Related Examples

- **[SysInfo CLI](../sysinfo-cli/)** - Pure stdlib monitoring (lightweight)
- **Glances Wrapper** - Full-featured monitoring (this example)
- See also: [CLI Tool Packaging Guide](../../docs/cookbook/examples/cli-tool.md)

## Resources

- **Glances Project:** https://github.com/nicolargo/glances
- **Documentation:** https://glances.readthedocs.io/
- **FlavorPack Docs:** https://github.com/provide-io/flavorpack
