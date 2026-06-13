import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class InstallManifestTests(unittest.TestCase):
    def test_manifest_is_not_committed_in_source_tree(self):
        found = [p for p in ROOT.rglob('.harnessmaker-install.json') if '.git' not in p.parts]
        self.assertEqual(found, [])

    def test_project_install_creates_manifest_after_files(self):
        from scripts.install_harness import install
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            result = install(scope='project', target=target, repo_root=ROOT)
            self.assertTrue(result.ok)
            manifest = target / '.agents' / 'skills' / 'harness' / '.harnessmaker-install.json'
            self.assertTrue(manifest.exists())
            data = json.loads(manifest.read_text(encoding='utf-8'))
            self.assertIn('skill', data['components'])
            self.assertIn('.agents/skills/harness/SKILL.md', data['installed_files'])
            self.assertTrue((target / '.agents' / 'skills' / 'harness' / 'SKILL.md').exists())

    def test_skill_to_agent_component_addition_is_valid(self):
        from scripts.install_harness import install
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            self.assertTrue(install(scope='project', target=target, repo_root=ROOT).ok)
            second = install(scope='project', target=target, repo_root=ROOT, with_agent_templates=True)
            self.assertTrue(second.ok)
            data = json.loads((target / '.agents' / 'skills' / 'harness' / '.harnessmaker-install.json').read_text(encoding='utf-8'))
            self.assertIn('agent-templates', data['components'])
            self.assertIn('config-example', data['components'])
            self.assertTrue((target / '.codex' / 'agents' / 'qa_reviewer.toml').exists())


if __name__ == '__main__':
    unittest.main()
