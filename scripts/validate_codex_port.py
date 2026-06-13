#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit('Python 3.11+ is required. Use python3.11 if python3 is older.')

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / '.agents' / 'skills' / 'harness'
SHA = 'cceac68ea1d0ad198ef4b7b906cd238375836387'
BANNED = [
    '.claude/agents', '.claude/skills', 'CLAUDE.md', '.claude-plugin',
    'TeamCreate', 'SendMessage', 'TaskCreate', 'TeamDelete',
    'CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS', 'model: "opus"',
]
CANONICAL_AREAS = [ROOT / 'AGENTS.md', SKILL_DIR, ROOT / '.codex' / 'agents', ROOT / 'docs' / 'harness']
REQUIRED = [
    'AGENTS.md', 'README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md',
    '.agents/skills/harness/SKILL.md',
    '.agents/skills/harness/references/agent-design-patterns.md',
    '.agents/skills/harness/references/orchestrator-template.md',
    '.agents/skills/harness/references/team-examples.md',
    '.agents/skills/harness/references/skill-writing-guide.md',
    '.agents/skills/harness/references/skill-testing-guide.md',
    '.agents/skills/harness/references/qa-agent-guide.md',
    '.agents/skills/harness/references/artifact-contract.md',
    '.agents/skills/harness/references/handoff-protocol.md',
    '.codex/agents/discovery_analyst.toml',
    '.codex/agents/architecture_designer.toml',
    '.codex/agents/skill_designer.toml',
    '.codex/agents/qa_reviewer.toml',
    '.codex/config.toml.example',
    'docs/harness/architecture-patterns.json',
    'docs/harness/agent-contracts.toml',
    'docs/upstream/provenance.md',
    'docs/upstream/port-checklist.json',
    'scripts/install_harness.py',
]


def error(errors, rule, path, message, line=None, token=None):
    loc = str(path.relative_to(ROOT)) if path.exists() or path.is_absolute() else str(path)
    details = f'{rule}: {loc}'
    if line is not None:
        details += f':{line}'
    if token:
        details += f' token={token!r}'
    details += f' - {message}'
    errors.append(details)


def parse_frontmatter(path: Path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return None
    end = text.find('\n---\n', 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ':' not in line:
            return None
        key, value = line.split(':', 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def iter_text_files(area: Path):
    if area.is_file():
        yield area
    elif area.exists():
        for path in area.rglob('*'):
            if path.is_file():
                yield path


def validate_required(errors):
    for rel in REQUIRED:
        path = ROOT / rel
        if not path.exists():
            error(errors, 'required-file', path, 'missing required file')
    if (ROOT / '.codex' / 'skills').exists():
        error(errors, 'no-codex-skills', ROOT / '.codex' / 'skills', 'unexpected .codex/skills mirror exists')
    if (ROOT / '.codex').exists() and not (ROOT / '.codex').is_dir():
        error(errors, 'codex-dir', ROOT / '.codex', '.codex must be a directory in source repository')
    for path in ROOT.rglob('.harnessmaker-install.json'):
        if '.git' not in path.parts:
            error(errors, 'source-manifest', path, 'install manifest must not be committed in source tree')


def validate_skill(errors):
    skill = SKILL_DIR / 'SKILL.md'
    fields = parse_frontmatter(skill) if skill.exists() else None
    if not fields:
        error(errors, 'skill-frontmatter', skill, 'frontmatter is missing or unsupported')
    else:
        for key in ['name', 'description']:
            if not fields.get(key):
                error(errors, 'skill-frontmatter', skill, f'missing {key}')
    if skill.exists():
        text = skill.read_text(encoding='utf-8')
        if 'docs/harness/' in text:
            error(errors, 'skill-self-contained', skill, 'runtime skill references docs/harness outside installed skill')
        for match in re.findall(r'`(references/[^`]+)`', text):
            target = (SKILL_DIR / match).resolve(strict=False)
            if os.path.commonpath([str(SKILL_DIR.resolve()), str(target)]) != str(SKILL_DIR.resolve()):
                error(errors, 'reference-link', skill, f'link escapes skill dir: {match}')
            if not target.exists():
                error(errors, 'reference-link', skill, f'missing reference: {match}')


def validate_notices_and_banned(errors):
    active = [
        SKILL_DIR / 'SKILL.md',
        SKILL_DIR / 'references' / 'agent-design-patterns.md',
        SKILL_DIR / 'references' / 'orchestrator-template.md',
        SKILL_DIR / 'references' / 'team-examples.md',
        SKILL_DIR / 'references' / 'skill-writing-guide.md',
        SKILL_DIR / 'references' / 'skill-testing-guide.md',
        SKILL_DIR / 'references' / 'qa-agent-guide.md',
    ]
    for path in active:
        if not path.exists():
            continue
        head = '\n'.join(path.read_text(encoding='utf-8').splitlines()[:20])
        for required in ['MODIFICATION NOTICE', 'https://github.com/revfactory/harness', SHA, 'ChanneulPark HarnessMaker']:
            if required not in head:
                error(errors, 'modification-notice', path, f'missing {required}')
    for area in CANONICAL_AREAS:
        for path in iter_text_files(area):
            try:
                lines = path.read_text(encoding='utf-8').splitlines()
            except UnicodeDecodeError:
                continue
            for idx, line in enumerate(lines, start=1):
                for token in BANNED:
                    if token in line:
                        error(errors, 'legacy-runtime-token', path, 'legacy runtime token is not allowed in canonical area', idx, token)
                if '/Volumes/' in line or '/Users/channeulpark/' in line:
                    error(errors, 'local-absolute-path', path, 'local absolute path is not allowed in runtime/source docs', idx)


def validate_agents(errors):
    agent_dir = ROOT / '.codex' / 'agents'
    names = []
    for path in sorted(agent_dir.glob('*.toml')):
        try:
            data = tomllib.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            error(errors, 'agent-toml', path, f'TOML parse failed: {exc}')
            continue
        for key in ['name', 'description', 'developer_instructions']:
            if not data.get(key):
                error(errors, 'agent-field', path, f'missing {key}')
        if data.get('name') != path.stem:
            error(errors, 'agent-name', path, 'name must match filename stem')
        if data.get('sandbox_mode') != 'read-only':
            error(errors, 'agent-sandbox', path, 'sandbox_mode must be read-only')
        if 'model' in data:
            error(errors, 'agent-model', path, 'model must not be hard-coded')
        names.append(data.get('name'))
    if len(names) != len(set(names)):
        error(errors, 'agent-duplicate', agent_dir, 'duplicate agent name')


def validate_contracts(errors):
    contract = ROOT / 'docs' / 'harness' / 'agent-contracts.toml'
    if not contract.exists():
        return
    data = tomllib.loads(contract.read_text(encoding='utf-8'))
    agents = data.get('agents', [])
    names = [a.get('name') for a in agents]
    toml_names = {p.stem for p in (ROOT / '.codex' / 'agents').glob('*.toml')}
    if set(names) != toml_names:
        error(errors, 'agent-contract', contract, 'contract agent names must match TOML agent files')
    produced = {}
    for agent in agents:
        for output in agent.get('produces', []):
            if output in produced:
                error(errors, 'agent-contract', contract, f'duplicate producer for {output}')
            produced[output] = agent.get('name')
    for agent in agents:
        for dep in agent.get('reads', []):
            if dep not in produced:
                error(errors, 'agent-contract', contract, f'unknown dependency {dep}')


def validate_registry_and_port_checklist(errors):
    registry = ROOT / 'docs' / 'harness' / 'architecture-patterns.json'
    if registry.exists():
        data = json.loads(registry.read_text(encoding='utf-8'))
        if len(data.get('patterns', [])) != 6:
            error(errors, 'architecture-registry', registry, 'must contain six upstream patterns')
    checklist = ROOT / 'docs' / 'upstream' / 'port-checklist.json'
    if checklist.exists():
        data = json.loads(checklist.read_text(encoding='utf-8'))
        for source, spec in data.items():
            target = ROOT / spec['target']
            if not target.exists():
                error(errors, 'port-checklist', target, f'missing target for {source}')
                continue
            text = target.read_text(encoding='utf-8').lower()
            for concept in spec.get('required_concepts', []):
                if concept.lower() not in text:
                    error(errors, 'port-checklist', target, f'missing concept {concept}')
            for heading in spec.get('required_headings', []):
                if heading.lower() not in text:
                    error(errors, 'port-checklist', target, f'missing heading {heading}')


def validate_installer_help(errors):
    result = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'install_harness.py'), '--help'], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        error(errors, 'installer-help', ROOT / 'scripts' / 'install_harness.py', result.stderr.strip())


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_skill(errors)
    validate_notices_and_banned(errors)
    validate_agents(errors)
    validate_contracts(errors)
    validate_registry_and_port_checklist(errors)
    validate_installer_help(errors)
    if errors:
        print('Codex port validation failed:')
        for item in errors:
            print(f'- {item}')
        return 1
    print('Codex port validation passed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
