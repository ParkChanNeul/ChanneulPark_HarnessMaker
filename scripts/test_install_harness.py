#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit('Python 3.11+ is required. Use python3.11 if python3 is older.')

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / 'scripts' / 'install_harness.py'


def run(args, env=None):
    return subprocess.run([sys.executable, str(INSTALLER), *args], cwd=ROOT, env=env, text=True, capture_output=True)


def main() -> int:
    checks = []
    checks.append(('help', run(['--help'])))
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / 'target'
        target.mkdir()
        checks.append(('dry-run', run(['--scope', 'project', '--target', str(target), '--with-agent-templates', '--dry-run'])))
        checks.append(('project-install', run(['--scope', 'project', '--target', str(target), '--with-agent-templates'])))
        if not (target / '.agents' / 'skills' / 'harness' / '.harnessmaker-install.json').exists():
            print('manifest was not created', file=sys.stderr)
            return 1
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / 'home'
        home.mkdir()
        env = {**os.environ, 'HOME': str(home)}
        checks.append(('user-install', run(['--scope', 'user', '--with-agent-templates'], env=env)))
        if not (home / '.codex' / 'harnessmaker.config.toml.example').exists():
            print('user config example was not created at harnessmaker-specific path', file=sys.stderr)
            return 1
    failed = [(name, result) for name, result in checks if result.returncode != 0]
    if failed:
        for name, result in failed:
            print(f'{name} failed', file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
        return 1
    print('install harness smoke tests passed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
