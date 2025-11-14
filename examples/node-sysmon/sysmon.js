#!/usr/bin/env node
/**
 * Node System Monitor - Pure JavaScript CLI
 * Demonstrates FlavorPack packaging of Node.js applications
 *
 * No external dependencies - pure Node.js stdlib!
 */

const os = require('os');
const fs = require('fs');
const path = require('path');

const VERSION = '1.0.0';

// ANSI colors
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
};

function formatBytes(bytes) {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }

  return `${size.toFixed(1)} ${units[unitIndex]}`;
}

function formatUptime(seconds) {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);

  const parts = [];
  if (days > 0) parts.push(`${days}d`);
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);

  return parts.join(' ') || '0m';
}

function showBanner() {
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║            NODE.JS SYSTEM MONITOR                        ║');
  console.log('║         Packaged with FlavorPack (PSPF/2025)             ║');
  console.log('╚══════════════════════════════════════════════════════════╝');
  console.log('');
}

function showSystemInfo() {
  showBanner();

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`${colors.cyan}Operating System${colors.reset}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`  Platform:     ${os.platform()}`);
  console.log(`  Type:         ${os.type()}`);
  console.log(`  Release:      ${os.release()}`);
  console.log(`  Architecture: ${os.arch()}`);
  console.log(`  Hostname:     ${os.hostname()}`);
  console.log('');

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`${colors.cyan}CPU Information${colors.reset}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  const cpus = os.cpus();
  console.log(`  Model:  ${cpus[0].model}`);
  console.log(`  Cores:  ${cpus.length}`);
  console.log(`  Speed:  ${cpus[0].speed} MHz`);
  console.log('');

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`${colors.cyan}Memory${colors.reset}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  const totalMem = os.totalmem();
  const freeMem = os.freemem();
  const usedMem = totalMem - freeMem;
  const usedPercent = ((usedMem / totalMem) * 100).toFixed(1);

  console.log(`  Total:     ${formatBytes(totalMem)}`);
  console.log(`  Used:      ${formatBytes(usedMem)} (${usedPercent}%)`);
  console.log(`  Free:      ${formatBytes(freeMem)}`);

  // Progress bar
  const barWidth = 40;
  const filled = Math.floor(barWidth * usedPercent / 100);
  const bar = '█'.repeat(filled) + '░'.repeat(barWidth - filled);
  console.log(`  [${bar}]`);
  console.log('');

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`${colors.cyan}System Status${colors.reset}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`  Uptime:    ${formatUptime(os.uptime())}`);
  const loadAvg = os.loadavg();
  console.log(`  Load Avg:  ${loadAvg[0].toFixed(2)}, ${loadAvg[1].toFixed(2)}, ${loadAvg[2].toFixed(2)}`);
  console.log('');

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`${colors.cyan}Node.js Runtime${colors.reset}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`  Node.js:   ${process.version}`);
  console.log(`  V8:        ${process.versions.v8}`);
  console.log(`  Process:   Pure JavaScript - no Python required!`);
  console.log('');
}

function showNetworkInfo() {
  showBanner();

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`${colors.cyan}Network Interfaces${colors.reset}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  const interfaces = os.networkInterfaces();
  for (const [name, addrs] of Object.entries(interfaces)) {
    console.log(`\n  ${colors.bright}${name}${colors.reset}`);
    addrs.forEach(addr => {
      if (addr.family === 'IPv4') {
        console.log(`    IPv4: ${addr.address}`);
        console.log(`    MAC:  ${addr.mac}`);
      } else if (addr.family === 'IPv6' && !addr.address.startsWith('fe80')) {
        console.log(`    IPv6: ${addr.address}`);
      }
    });
  }
  console.log('');
}

function showProcessInfo() {
  showBanner();

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`${colors.cyan}Process Information${colors.reset}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  const mem = process.memoryUsage();
  console.log(`  Process ID:    ${process.pid}`);
  console.log(`  Parent PID:    ${process.ppid}`);
  console.log(`  Working Dir:   ${process.cwd()}`);
  console.log(`  Executable:    ${process.execPath}`);
  console.log(`  Node Version:  ${process.version}`);
  console.log('');

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`${colors.cyan}Memory Usage${colors.reset}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`  RSS:           ${formatBytes(mem.rss)}`);
  console.log(`  Heap Total:    ${formatBytes(mem.heapTotal)}`);
  console.log(`  Heap Used:     ${formatBytes(mem.heapUsed)}`);
  console.log(`  External:      ${formatBytes(mem.external)}`);
  console.log('');
}

function showJSON() {
  const data = {
    timestamp: new Date().toISOString(),
    system: {
      platform: os.platform(),
      type: os.type(),
      release: os.release(),
      arch: os.arch(),
      hostname: os.hostname(),
      uptime: os.uptime(),
    },
    cpu: {
      model: os.cpus()[0].model,
      cores: os.cpus().length,
      speed: os.cpus()[0].speed,
    },
    memory: {
      total: os.totalmem(),
      free: os.freemem(),
      used: os.totalmem() - os.freemem(),
    },
    process: {
      pid: process.pid,
      ppid: process.ppid,
      version: process.version,
      cwd: process.cwd(),
    },
    loadAverage: os.loadavg(),
  };

  console.log(JSON.stringify(data, null, 2));
}

function showHelp() {
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║            NODE.JS SYSTEM MONITOR                        ║');
  console.log('║         Packaged with FlavorPack (PSPF/2025)             ║');
  console.log('╚══════════════════════════════════════════════════════════╝');
  console.log('');
  console.log('Usage: node-sysmon [command] [options]');
  console.log('');
  console.log('Commands:');
  console.log('  sysinfo     Show system information (default)');
  console.log('  network     Show network interfaces');
  console.log('  process     Show process information');
  console.log('  json        Output all data as JSON');
  console.log('  help        Show this help message');
  console.log('  version     Show version');
  console.log('');
  console.log('Options:');
  console.log('  --json      Output as JSON (can combine with any command)');
  console.log('');
  console.log('Examples:');
  console.log('  node-sysmon');
  console.log('  node-sysmon sysinfo');
  console.log('  node-sysmon network');
  console.log('  node-sysmon --json');
  console.log('');
  console.log('This is a pure Node.js package - no Python required!');
  console.log('All code is pure JavaScript using Node.js standard library.');
  console.log('');
  console.log('Packaged using FlavorPack PSPF/2025 format.');
}

// Main CLI logic
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'sysinfo';
  const hasJsonFlag = args.includes('--json');

  if (hasJsonFlag) {
    showJSON();
    return;
  }

  switch (command) {
    case 'sysinfo':
    case 'sys':
      showSystemInfo();
      break;

    case 'network':
    case 'net':
      showNetworkInfo();
      break;

    case 'process':
    case 'proc':
      showProcessInfo();
      break;

    case 'json':
      showJSON();
      break;

    case 'version':
    case '--version':
    case '-v':
      console.log(`node-sysmon version ${VERSION}`);
      console.log(`Node.js ${process.version}`);
      console.log('Packaged with FlavorPack PSPF/2025');
      break;

    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;

    default:
      console.error(`Unknown command: ${command}`);
      console.error('Run "node-sysmon help" for usage information');
      process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { main };
