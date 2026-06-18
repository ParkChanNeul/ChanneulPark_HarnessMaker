#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]

FRONT_STAGE_SKILLS = [
    'kc-lesson-intake',
    'kc-lesson-resume',
    'kc-lesson-turn',
    'kc-lesson-unknown',
    'kc-lesson-scope-lock',
    'kc-post-lesson-reflection',
    'kc-next-lesson-decision',
]

CONVERSATION_CONTRACTS = [
    'lesson_intake_state',
    'teacher_decision_card',
    'lesson_scope_lock',
    'post_lesson_teacher_card',
    'next_lesson_decision_lock',
]

EXECUTION_MODES = [
    'build_lesson',
    'render_materials',
    'post_lesson_followup',
    'review_outputs',
    'research_to_domain',
    'audit_domain',
    'partial_rerun',
]

CONVERSATION_SCENARIOS = [
    'bare_lesson_intake',
    'rich_non_linear_entry',
    'unknown_to_recommendation',
    'lesson_scope_lock',
    'build_blocked_without_lock',
    'teacher_override_advance',
    'post_lesson_reflection',
    'next_lesson_teacher_decision',
    'resume_requires_run_dir',
    'continue_does_not_bypass_gate',
]

HANDOFF_FIELDS = [
    'Recommended Next Skill:',
    'Why:',
    'Ready To Continue:',
    'Need Teacher Confirmation:',
    'Requires run_dir:',
    'Blocking Conditions:',
    'Suggested Prompt:',
]

GOLDEN_FILES = [
    '00_conversation/lesson_intake_state.md',
    '00_conversation/teacher_decision_card.md',
    '00_conversation/lesson_scope_lock.md',
    '00_conversation/post_lesson_teacher_card.md',
    '00_conversation/next_lesson_decision_lock.md',
    '01_learner_context_snapshot.md',
    '02_progression_plan.md',
    '03_lesson_blueprint.md',
    '04_practice_plan.md',
    '05_student_deck_spec.md',
    '06_lesson_result.md',
    '07_homework_plan.md',
    '08_quizlet_plan.md',
    '09_follow_up_message.md',
    '10_weekly_learning_pack.md',
    '10_next_lesson_check.md',
    '11_assessment_report.md',
]

SEMANTIC_RUNTIME_FILES = [
    'scripts/structured_artifacts.py',
    'scripts/validate_semantic_contracts.py',
    'scripts/validate_golden_run.py',
    'scripts/render_golden_assessment.py',
    'tests/test_conversational_guards.py',
    'tests/test_golden_run.py',
]

PRIVATE_PATTERNS = [
    r'legal_name\s*:',
    r'@[A-Za-z0-9_]{3,}',
    r'\b\d{3}-\d{3,4}-\d{4}\b',
]


def fail(messages: list[str]) -> None:
    print('FAIL: conversational runtime validation failed')
    for message in messages:
        print(f'- {message}')
    sys.exit(1)


def text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def main() -> None:
    failures: list[str] = []
    skill_root = ROOT / '.agents' / 'skills'
    contract_root = ROOT / 'contracts' / 'conversation'
    orchestrator = skill_root / 'korean-connection-orchestrator' / 'SKILL.md'
    orchestrator_text = text(orchestrator)

    for skill in FRONT_STAGE_SKILLS:
        path = skill_root / skill / 'SKILL.md'
        if not path.is_file():
            failures.append(f'missing front-stage skill: {path.relative_to(ROOT)}')
            continue
        content = text(path)
        if not content.startswith('---\n') or f'name: {skill}' not in content:
            failures.append(f'invalid skill frontmatter: {path.relative_to(ROOT)}')
        if '## Next Skill Handoff' not in content:
            failures.append(f'missing Next Skill Handoff: {path.relative_to(ROOT)}')
        for field in HANDOFF_FIELDS:
            if field not in content:
                failures.append(f'{path.relative_to(ROOT)} missing handoff field {field}')

    for contract in CONVERSATION_CONTRACTS:
        path = contract_root / f'{contract}.md'
        if not path.is_file():
            failures.append(f'missing conversation contract: {path.relative_to(ROOT)}')
            continue
        content = text(path)
        for section in ['## Purpose', '## Producer', '## Consumers', '## Required Fields', '## Validation']:
            if section not in content:
                failures.append(f'{path.relative_to(ROOT)} missing {section}')
        if '```yaml' not in content:
            failures.append(f'{path.relative_to(ROOT)} missing yaml block')

    if '## Front-Stage Conversational Routing' not in orchestrator_text:
        failures.append('orchestrator missing separate front-stage conversational routing')
    if '## Execution Modes' not in orchestrator_text:
        failures.append('orchestrator missing execution modes heading')
    for mode in EXECUTION_MODES:
        if f'### `{mode}`' not in orchestrator_text:
            failures.append(f'orchestrator missing execution mode {mode}')
    for route in ['lesson_intake', 'lesson_resume', 'lesson_turn', 'lesson_unknown', 'lesson_scope_lock', 'post_lesson_reflection', 'next_lesson_decision']:
        if route not in orchestrator_text:
            failures.append(f'orchestrator missing front-stage route {route}')
        if f'### `{route}`' in orchestrator_text:
            failures.append(f'front-stage route must not be declared as execution mode: {route}')

    required_orchestrator_terms = [
        'BLOCKED: approved lesson_scope_lock is required',
        'homework_only',
        'full_followup',
        'next_lesson_decision_lock',
        'Non-linear Entry',
        'run_dir',
        'continue does not approve',
        'advisory mode',
    ]
    for term in required_orchestrator_terms:
        if term not in orchestrator_text:
            failures.append(f'orchestrator missing rule: {term}')

    registry = ROOT / 'references' / 'agent_registry.toml'
    if not registry.is_file():
        failures.append('missing approved agent registry')
    else:
        data = tomllib.loads(text(registry))
        if data.get('schema_version') != 1:
            failures.append('agent registry schema_version must be 1')
        entries = data.get('agents', [])
        names = [entry.get('name') for entry in entries]
        if len(names) != len(set(names)):
            failures.append('agent registry contains duplicate names')
        required = {entry.get('name') for entry in entries if entry.get('required') is True and entry.get('status') == 'approved'}
        if not required:
            failures.append('agent registry must declare at least one required approved agent')
        for name in required:
            if not (ROOT / '.codex' / 'agents' / f'{name}.toml').is_file():
                failures.append(f'missing required registered agent file: {name}')

    for scenario in CONVERSATION_SCENARIOS:
        acceptance = ROOT / 'tests' / 'acceptance' / 'conversation' / f'{scenario}.md'
        fixture = ROOT / 'tests' / 'fixtures' / 'conversation' / f'{scenario}.md'
        if not acceptance.is_file():
            failures.append(f'missing acceptance scenario: {acceptance.relative_to(ROOT)}')
        if not fixture.is_file():
            failures.append(f'missing conversation fixture: {fixture.relative_to(ROOT)}')

    for rel in SEMANTIC_RUNTIME_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f'missing semantic runtime file: {rel}')

    golden = ROOT / 'tests' / 'fixtures' / 'golden' / 'conversational_cafe'
    for rel in GOLDEN_FILES:
        path = golden / rel
        if not path.is_file():
            failures.append(f'missing golden artifact: {path.relative_to(ROOT)}')

    scope_contract = contract_root / 'lesson_scope_lock.md'
    if scope_contract.is_file():
        content = text(scope_contract)
        for term in [
            'approved_by_teacher',
            'approval_evidence',
            'unresolved_blockers',
            'vocabulary_scope',
            'in_class_new_item_count',
            'productive_core_count',
            'receptive_support_count',
            'homework_expansion_count',
        ]:
            if term not in content:
                failures.append(f'lesson_scope_lock missing field {term}')

    next_contract = contract_root / 'next_lesson_decision_lock.md'
    if next_contract.is_file():
        content = text(next_contract)
        for term in ['explicit_review', 'retrieval', 'carrier', 'transfer', 'defer']:
            if term not in content:
                failures.append(f'next_lesson_decision_lock missing treatment {term}')

    all_text_files = [p for p in ROOT.rglob('*') if p.is_file() and p.suffix in {'.md', '.toml', '.py', '.txt'} and '.git' not in p.parts]
    for path in all_text_files:
        content = text(path)
        for pattern in PRIVATE_PATTERNS:
            if re.search(pattern, content, flags=re.IGNORECASE):
                failures.append(f'possible private data pattern {pattern!r} in {path.relative_to(ROOT)}')

    nested_git = [path for path in ROOT.rglob('.git') if path.is_dir()]
    if nested_git:
        failures.append('nested git repository detected')

    if failures:
        fail(failures)
    print('PASS: conversational runtime is valid')


if __name__ == '__main__':
    main()
