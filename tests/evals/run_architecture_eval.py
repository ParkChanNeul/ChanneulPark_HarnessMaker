#!/usr/bin/env python3
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class CodexArchitectureEval(unittest.TestCase):
    def test_codex_cli_architecture_eval(self):
        if shutil.which('codex') is None:
            raise unittest.SkipTest('Codex CLI is not installed')
        fixture = ROOT / 'tests' / 'fixtures' / 'simple-single-agent' / 'request.md'
        prompt = fixture.read_text(encoding='utf-8') + '\n\nReturn JSON with a pattern field.'
        result = subprocess.run(['codex', 'exec', '--skip-git-repo-check', prompt], cwd=ROOT, text=True, capture_output=True, timeout=120)
        if result.returncode != 0 and ('auth' in result.stderr.lower() or 'login' in result.stderr.lower()):
            raise unittest.SkipTest('Codex CLI is not authenticated')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('pattern', result.stdout.lower())


if __name__ == '__main__':
    unittest.main()
