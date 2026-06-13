import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests' / 'fixtures'
REGISTRY = ROOT / 'docs' / 'harness' / 'architecture-patterns.json'


class ArchitectureFixtureTests(unittest.TestCase):
    def test_fixtures_are_schema_consistent(self):
        allowed = {p['id'] for p in json.loads(REGISTRY.read_text(encoding='utf-8'))['patterns']}
        cases = ['simple-single-agent', 'parallel-research', 'hierarchical-build']
        for case in cases:
            base = FIXTURES / case
            with self.subTest(case=case):
                for name in ['request.md', 'expected-architecture.json', 'expected-files.txt', 'expected-validation.json']:
                    self.assertTrue((base / name).exists(), f'missing {name}')
                arch = json.loads((base / 'expected-architecture.json').read_text(encoding='utf-8'))
                self.assertIn(arch['pattern'], allowed)
                self.assertIsInstance(arch.get('rationale'), str)
                files = [line for line in (base / 'expected-files.txt').read_text(encoding='utf-8').splitlines() if line.strip()]
                self.assertTrue(files)
                self.assertTrue(all(not line.startswith('/') for line in files))
                validation = json.loads((base / 'expected-validation.json').read_text(encoding='utf-8'))
                self.assertIn('expected_pass', validation)
                self.assertIn('checks', validation)


if __name__ == '__main__':
    unittest.main()
