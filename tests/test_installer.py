import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
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

    def test_manifest_replace_failure_restores_managed_file(self):
        from scripts import install_harness

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            first = install_harness.install(scope='project', target=target, repo_root=ROOT)
            self.assertTrue(first.ok, first.messages)

            managed = target / '.agents' / 'skills' / 'harness' / 'SKILL.md'
            edited_text = managed.read_text(encoding='utf-8') + '\nmanaged local edit\n'
            managed.write_text(edited_text, encoding='utf-8')

            with mock.patch.object(install_harness.os, 'replace', side_effect=OSError('forced manifest failure')):
                result = install_harness.install(scope='project', target=target, repo_root=ROOT, force=True)

            self.assertFalse(result.ok)
            self.assertIn('rollback attempted', '\n'.join(result.messages))
            self.assertEqual(managed.read_text(encoding='utf-8'), edited_text)

    def test_copy_failure_restores_prior_managed_files_and_removes_created_files(self):
        from scripts import install_harness

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            first = install_harness.install(scope='project', target=target, repo_root=ROOT, with_agent_templates=True)
            self.assertTrue(first.ok, first.messages)

            managed_skill = target / '.agents' / 'skills' / 'harness' / 'SKILL.md'
            managed_agent = target / '.codex' / 'agents' / 'qa_reviewer.toml'
            skill_edit = managed_skill.read_text(encoding='utf-8') + '\nmanaged skill edit\n'
            agent_edit = managed_agent.read_text(encoding='utf-8') + '\n# managed agent edit\n'
            managed_skill.write_text(skill_edit, encoding='utf-8')
            managed_agent.write_text(agent_edit, encoding='utf-8')

            real_copy2 = install_harness.shutil.copy2
            def failing_copy(src, dst, *args, **kwargs):
                dst_path = Path(dst)
                if dst_path.resolve(strict=False) == managed_agent.resolve(strict=False):
                    raise OSError('forced copy failure')
                return real_copy2(src, dst, *args, **kwargs)

            with mock.patch.object(install_harness.shutil, 'copy2', side_effect=failing_copy):
                result = install_harness.install(scope='project', target=target, repo_root=ROOT, with_agent_templates=True, force=True)

            self.assertFalse(result.ok)
            self.assertEqual(managed_skill.read_text(encoding='utf-8'), skill_edit)
            self.assertEqual(managed_agent.read_text(encoding='utf-8'), agent_edit)

    def test_force_preserves_unmanaged_agent_file(self):
        from scripts.install_harness import install

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            self.assertTrue(install(scope='project', target=target, repo_root=ROOT, with_agent_templates=True).ok)

            unmanaged = target / '.codex' / 'agents' / 'user_agent.toml'
            unmanaged.write_text('name = "user_agent"\n', encoding='utf-8')
            managed = target / '.codex' / 'agents' / 'qa_reviewer.toml'
            managed.write_text(managed.read_text(encoding='utf-8') + '\n# changed managed file\n', encoding='utf-8')

            result = install(scope='project', target=target, repo_root=ROOT, with_agent_templates=True, force=True)

            self.assertTrue(result.ok, result.messages)
            self.assertTrue(unmanaged.exists())
            self.assertEqual(unmanaged.read_text(encoding='utf-8'), 'name = "user_agent"\n')


if __name__ == '__main__':
    unittest.main()
