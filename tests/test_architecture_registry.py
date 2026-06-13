import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'docs' / 'harness' / 'architecture-patterns.json'


class ArchitectureRegistryTests(unittest.TestCase):
    def test_registry_has_upstream_patterns(self):
        data = json.loads(REGISTRY.read_text(encoding='utf-8'))
        self.assertEqual(data.get('schema_version'), 1)
        patterns = data.get('patterns', [])
        self.assertEqual(len(patterns), 6)
        ids = [p['id'] for p in patterns]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {'pipeline', 'fan-out-fan-in', 'expert-pool', 'producer-reviewer', 'supervisor', 'hierarchical-delegation'})
        for pattern in patterns:
            self.assertTrue(pattern.get('name'))
            self.assertTrue(pattern.get('codex_usage'))


if __name__ == '__main__':
    unittest.main()
