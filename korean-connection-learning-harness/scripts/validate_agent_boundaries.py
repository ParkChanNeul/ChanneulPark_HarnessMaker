#!/usr/bin/env python3
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / '.codex' / 'agents'
SKILL_DIR = ROOT / '.agents' / 'skills'
REGISTRY = ROOT / 'references' / 'agent_registry.toml'


def fail(failures: list[str]) -> None:
    print('FAIL: agent boundary validation failed')
    for failure in failures:
        print(f'- {failure}')
    sys.exit(1)


def main() -> None:
    failures: list[str] = []
    data = tomllib.loads(REGISTRY.read_text(encoding='utf-8'))
    entries = data.get('agents', [])
    registry = {entry.get('name'): entry for entry in entries}
    if None in registry:
        failures.append('agent registry entry missing name')
    if len(registry) != len(entries):
        failures.append('agent registry contains duplicate names')

    actual = {path.stem for path in AGENT_DIR.glob('*.toml')}
    approved = {name for name, entry in registry.items() if entry.get('status') == 'approved'}
    required = {name for name, entry in registry.items() if entry.get('status') == 'approved' and entry.get('required') is True}

    missing = sorted(required - actual)
    unregistered = sorted(actual - approved)
    if missing:
        failures.append('missing required registered agents: ' + ', '.join(missing))
    if unregistered:
        failures.append('unregistered or unapproved agents: ' + ', '.join(unregistered))

    for path in sorted(AGENT_DIR.glob('*.toml')):
        agent = tomllib.loads(path.read_text(encoding='utf-8'))
        if agent.get('name') != path.stem:
            failures.append(f'{path.relative_to(ROOT)} name must match filename stem')
        for field in ['name', 'description', 'sandbox_mode', 'developer_instructions']:
            if field not in agent:
                failures.append(f'{path.relative_to(ROOT)} missing {field}')
        if agent.get('sandbox_mode') != 'read-only':
            failures.append(f'{path.relative_to(ROOT)} must be read-only')
        if 'model' in agent:
            failures.append(f'{path.relative_to(ROOT)} must not hardcode model')
        entry = registry.get(path.stem, {})
        skill = entry.get('skill')
        instructions = agent.get('developer_instructions', '')
        if not skill:
            failures.append(f'{path.relative_to(ROOT)} missing registry skill mapping')
        elif skill not in instructions:
            failures.append(f'{path.relative_to(ROOT)} does not reference skill {skill}')
        elif not (SKILL_DIR / skill / 'SKILL.md').is_file():
            failures.append(f'missing skill for {path.stem}: {skill}')
        if 'Do not write final files' not in instructions and 'Do not write target files' not in instructions:
            failures.append(f'{path.relative_to(ROOT)} must state parent-owned final writes')

    forbidden = {
        'korean_connection_orchestrator', 'kc_lesson_intake', 'kc_lesson_resume',
        'kc_lesson_turn', 'kc_lesson_unknown', 'kc_lesson_scope_lock',
        'kc_post_lesson_reflection', 'kc_next_lesson_decision',
    }
    found_forbidden = sorted(actual & forbidden)
    if found_forbidden:
        failures.append('front-stage or orchestrator agent TOML is forbidden: ' + ', '.join(found_forbidden))

    if failures:
        fail(failures)
    print('PASS: agent boundaries are valid')


if __name__ == '__main__':
    main()
