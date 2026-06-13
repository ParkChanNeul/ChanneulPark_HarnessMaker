import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / '.codex' / 'agents'


class AgentSchemaTests(unittest.TestCase):
    def test_agent_toml_files_parse_and_match_filename(self):
        expected = {'discovery_analyst', 'architecture_designer', 'skill_designer', 'qa_reviewer'}
        paths = sorted(AGENT_DIR.glob('*.toml'))
        self.assertEqual({p.stem for p in paths}, expected)
        names = []
        for path in paths:
            data = tomllib.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(data.get('name'), path.stem)
            self.assertTrue(data.get('description'))
            self.assertTrue(data.get('developer_instructions'))
            self.assertEqual(data.get('sandbox_mode'), 'read-only')
            self.assertNotIn('model', data)
            self.assertIn('Do not modify', data['developer_instructions'])
            names.append(data['name'])
        self.assertEqual(len(names), len(set(names)))


if __name__ == '__main__':
    unittest.main()
