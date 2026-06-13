import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / 'scripts' / 'install_harness.py'


class InstallerBehaviorTests(unittest.TestCase):
    def run_cli(self, args, env=None):
        return subprocess.run([sys.executable, str(INSTALLER), *args], cwd=ROOT, env=env, text=True, capture_output=True)

    def test_help_succeeds(self):
        result = self.run_cli(['--help'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--scope', result.stdout)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            result = self.run_cli(['--scope', 'project', '--target', str(target), '--with-agent-templates', '--dry-run'])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((target / '.agents').exists())
            self.assertIn('DRY RUN', result.stdout)

    def test_user_scope_uses_temp_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / 'home'
            home.mkdir()
            env = {**os.environ, 'HOME': str(home)}
            result = self.run_cli(['--scope', 'user', '--with-agent-templates'], env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / '.agents' / 'skills' / 'harness' / 'SKILL.md').exists())
            self.assertTrue((home / '.codex' / 'agents' / 'discovery_analyst.toml').exists())
            self.assertTrue((home / '.codex' / 'harnessmaker.config.toml.example').exists())

    def test_unmanaged_same_name_file_fails_even_with_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            dest = target / '.agents' / 'skills' / 'harness'
            dest.mkdir(parents=True)
            (dest / 'SKILL.md').write_text('user file\n', encoding='utf-8')
            result = self.run_cli(['--scope', 'project', '--target', str(target), '--force'])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('unmanaged', result.stderr.lower())

    def test_codex_file_collision_only_when_agents_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            (target / '.codex').write_text('legacy file\n', encoding='utf-8')
            base = self.run_cli(['--scope', 'project', '--target', str(target)])
            self.assertEqual(base.returncode, 0, base.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            (target / '.codex').write_text('legacy file\n', encoding='utf-8')
            agents = self.run_cli(['--scope', 'project', '--target', str(target), '--with-agent-templates'])
            self.assertNotEqual(agents.returncode, 0)
            self.assertIn('.codex', agents.stderr)


if __name__ == '__main__':
    unittest.main()
