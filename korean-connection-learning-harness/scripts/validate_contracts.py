#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / 'contracts'
CONVERSATION_DIR = CONTRACT_DIR / 'conversation'

BASE_CONTRACTS = [
    'lesson_request', 'learner_context_snapshot', 'learner_state_delta', 'progression_plan',
    'lesson_blueprint', 'practice_plan', 'student_deck_spec', 'design_manifest', 'lesson_result',
    'material_manifest', 'weekly_learning_pack', 'homework_plan', 'quizlet_plan',
    'follow_up_message', 'next_lesson_check', 'assessment_report', 'privacy_report',
    'research_insight_proposal', 'domain_update_proposal', 'approval_state',
]

CONVERSATION_CONTRACTS = [
    'lesson_intake_state', 'teacher_decision_card', 'lesson_scope_lock',
    'post_lesson_teacher_card', 'next_lesson_decision_lock',
]

REQUIRED_SECTIONS = ['## Purpose', '## Producer', '## Consumers', '## Required Fields', '## Validation']


def validate_contract(path: Path, failures: list[str]) -> None:
    if not path.is_file():
        failures.append(f'missing contract: {path.relative_to(ROOT)}')
        return
    text = path.read_text(encoding='utf-8')
    if not text.startswith('# Contract: '):
        failures.append(f'{path.relative_to(ROOT)} must start with Contract heading')
    for section in REQUIRED_SECTIONS:
        if section not in text:
            failures.append(f'{path.relative_to(ROOT)} missing {section}')
    if '```yaml' not in text:
        failures.append(f'{path.relative_to(ROOT)} missing yaml field block')


def fail(failures: list[str]) -> None:
    print('FAIL: contract validation failed')
    for failure in failures:
        print(f'- {failure}')
    sys.exit(1)


def main() -> None:
    failures: list[str] = []
    for name in BASE_CONTRACTS:
        validate_contract(CONTRACT_DIR / f'{name}.md', failures)
    for name in CONVERSATION_CONTRACTS:
        validate_contract(CONVERSATION_DIR / f'{name}.md', failures)

    actual_base = sorted(path.stem for path in CONTRACT_DIR.glob('*.md'))
    extra_base = sorted(set(actual_base) - set(BASE_CONTRACTS))
    if extra_base:
        failures.append('unexpected base contracts: ' + ', '.join(extra_base))
    actual_conversation = sorted(path.stem for path in CONVERSATION_DIR.glob('*.md'))
    extra_conversation = sorted(set(actual_conversation) - set(CONVERSATION_CONTRACTS))
    if extra_conversation:
        failures.append('unexpected conversation contracts: ' + ', '.join(extra_conversation))

    lock_text = (CONVERSATION_DIR / 'lesson_scope_lock.md').read_text(encoding='utf-8')
    for term in ['approved_by_teacher', 'approval_evidence', 'unresolved_blockers', 'revision', 'supersedes']:
        if term not in lock_text:
            failures.append(f'lesson_scope_lock missing {term}')
    post_text = (CONVERSATION_DIR / 'post_lesson_teacher_card.md').read_text(encoding='utf-8')
    if 'homework_approved' not in post_text:
        failures.append('post_lesson_teacher_card missing homework approval')
    next_text = (CONVERSATION_DIR / 'next_lesson_decision_lock.md').read_text(encoding='utf-8')
    for treatment in ['explicit_review', 'retrieval', 'carrier', 'transfer', 'defer']:
        if treatment not in next_text:
            failures.append(f'next_lesson_decision_lock missing {treatment}')

    if failures:
        fail(failures)
    print('PASS: contracts are complete')


if __name__ == '__main__':
    main()
