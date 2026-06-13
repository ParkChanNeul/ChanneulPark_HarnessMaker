import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / 'docs' / 'harness' / 'agent-contracts.toml'
AGENT_DIR = ROOT / '.codex' / 'agents'


class AgentContractsTests(unittest.TestCase):
    def test_contract_matches_agent_files_and_has_acyclic_dependencies(self):
        data = tomllib.loads(CONTRACT.read_text(encoding='utf-8'))
        agents = data.get('agents', [])
        names = [a['name'] for a in agents]
        self.assertEqual(set(names), {p.stem for p in AGENT_DIR.glob('*.toml')})
        self.assertEqual(len(names), len(set(names)))
        produced = {}
        for agent in agents:
            self.assertEqual(agent.get('mode'), 'read-only')
            for output in agent.get('produces', []):
                self.assertNotIn(output, produced)
                produced[output] = agent['name']
        for agent in agents:
            for dep in agent.get('reads', []):
                self.assertIn(dep, produced)
                self.assertNotEqual(produced[dep], agent['name'])
        graph = {a['name']: {produced[d] for d in a.get('reads', []) if d in produced} for a in agents}
        visiting, visited = set(), set()
        def visit(node):
            if node in visiting:
                self.fail(f'cycle detected at {node}')
            if node in visited:
                return
            visiting.add(node)
            for dep in graph[node]:
                visit(dep)
            visiting.remove(node)
            visited.add(node)
        for name in names:
            visit(name)


if __name__ == '__main__':
    unittest.main()
