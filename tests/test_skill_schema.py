import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / '.agents' / 'skills' / 'harness'
UPSTREAM_SHA = 'cceac68ea1d0ad198ef4b7b906cd238375836387'
ACTIVE_PORTED = [
    SKILL_DIR / 'SKILL.md',
    SKILL_DIR / 'references' / 'agent-design-patterns.md',
    SKILL_DIR / 'references' / 'orchestrator-template.md',
    SKILL_DIR / 'references' / 'team-examples.md',
    SKILL_DIR / 'references' / 'skill-writing-guide.md',
    SKILL_DIR / 'references' / 'skill-testing-guide.md',
    SKILL_DIR / 'references' / 'qa-agent-guide.md',
]
BANNED = [
    '.claude/agents', '.claude/skills', 'CLAUDE.md', '.claude-plugin',
    'TeamCreate', 'SendMessage', 'TaskCreate', 'TeamDelete',
    'CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS', 'model: "opus"',
]


def parse_limited_frontmatter(path: Path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise AssertionError('SKILL.md must start with frontmatter')
    end = text.find('\n---\n', 4)
    if end == -1:
        raise AssertionError('SKILL.md frontmatter must close with ---')
    fields = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ':' not in line:
            raise AssertionError(f'unsupported frontmatter line: {line}')
        key, value = line.split(':', 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


class SkillSchemaTests(unittest.TestCase):
    def test_skill_frontmatter_has_name_and_description(self):
        fields = parse_limited_frontmatter(SKILL_DIR / 'SKILL.md')
        self.assertEqual(fields.get('name'), 'harness')
        self.assertTrue(fields.get('description'))

    def test_runtime_references_are_inside_skill_directory(self):
        skill = (SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('docs/harness/', skill)
        refs = re.findall(r'`(references/[^`]+)`', skill)
        self.assertGreaterEqual(len(refs), 6)
        for ref in refs:
            target = (SKILL_DIR / ref).resolve()
            self.assertTrue(str(target).startswith(str(SKILL_DIR.resolve())))
            self.assertTrue(target.exists(), f'missing referenced file: {ref}')

    def test_no_codex_skills_mirror(self):
        self.assertFalse((ROOT / '.codex' / 'skills').exists())

    def test_active_ports_have_prominent_modification_notice(self):
        for path in ACTIVE_PORTED:
            with self.subTest(path=path):
                text = path.read_text(encoding='utf-8')
                head = '\n'.join(text.splitlines()[:20])
                self.assertIn('MODIFICATION NOTICE', head)
                self.assertIn('https://github.com/revfactory/harness', head)
                self.assertIn(UPSTREAM_SHA, head)
                self.assertIn('ChanneulPark HarnessMaker', head)
                self.assertRegex(head, r'Codex[- ]native|Codex port')

    def test_canonical_docs_do_not_contain_legacy_runtime_tokens(self):
        areas = [ROOT / 'AGENTS.md', SKILL_DIR, ROOT / '.codex' / 'agents', ROOT / 'docs' / 'harness']
        for area in areas:
            paths = [area] if area.is_file() else list(area.rglob('*'))
            for path in paths:
                if not path.is_file():
                    continue
                text = path.read_text(encoding='utf-8')
                for token in BANNED:
                    self.assertNotIn(token, text, f'{token} found in {path}')

    def test_required_runtime_references_exist_and_are_nonempty(self):
        required = [
            'agent-design-patterns.md', 'orchestrator-template.md', 'team-examples.md',
            'skill-writing-guide.md', 'skill-testing-guide.md', 'qa-agent-guide.md',
        ]
        for name in required:
            path = SKILL_DIR / 'references' / name
            with self.subTest(name=name):
                self.assertTrue(path.exists())
                self.assertGreater(len(path.read_text(encoding='utf-8').strip()), 500)


if __name__ == '__main__':
    unittest.main()
