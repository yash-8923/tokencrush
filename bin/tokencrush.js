#!/usr/bin/env node
const { execSync, spawnSync } = require('child_process');

function hasCmd(cmd) {
  try { spawnSync(cmd, ['--version'], { encoding: 'utf8' }); return true; } catch { return false; }
}

// Install uv if missing
if (!hasCmd('uv')) {
  console.log('Installing uv...');
  try {
    execSync('pip install uv --quiet', { stdio: 'inherit' });
  } catch {
    console.error('✗ Could not install uv. Install manually: https://docs.astral.sh/uv');
    process.exit(1);
  }
}

console.log('Installing tokencrush...');
execSync('uv pip install tokencrush --system --quiet', { stdio: 'inherit' });

const args = process.argv.slice(2);
const cmd = args.length ? args.join(' ') : 'init';

try {
  execSync(`python -m tokencrush ${cmd}`, { stdio: 'inherit' });
} catch (e) {
  process.exit(e.status || 1);
}
