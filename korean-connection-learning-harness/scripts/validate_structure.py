#!/usr/bin/env python3
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'references' / 'agent_registry.toml'

REQUIRED_FILES = [
    'AGENTS.md', 'README.md', '.gitignore',
    '_workspace/README.md', '_workspace/00_source_audit.md',
    '_workspace/01_conversational_runtime_audit.md', '_workspace/templates/run_handoff_template.md',
    'domain/01_identity/brand_positioning.md', 'domain/01_identity/customer_promise.md',
    'domain/02_learning_model/pedagogy_principles.md', 'domain/02_learning_model/grammar_progression.md',
    'domain/02_learning_model/vocabulary_progression.md', 'domain/02_learning_model/conversation_skill_progression.md',
    'domain/02_learning_model/mastery_definition.md',
    'domain/03_curriculum/situation_map.md', 'domain/03_curriculum/module_map.md',
    'domain/03_curriculum/sequence_rules.md', 'domain/03_curriculum/spiral_review_rules.md',
    'domain/04_lesson_system/lesson_contract.md', 'domain/04_lesson_system/practice_ladder.md',
    'domain/04_lesson_system/culture_usage_rules.md', 'domain/04_lesson_system/student_experience_rules.md',
    'domain/04_lesson_system/mission_and_followup.md', 'domain/04_lesson_system/homework_and_retention.md',
    'domain/05_learner_state/learner_model.schema.md', 'domain/05_learner_state/grammar_mastery.schema.md',
    'domain/05_learner_state/conversation_mastery.schema.md', 'domain/05_learner_state/mission_history.schema.md',
    'domain/05_learner_state/lesson_result.schema.md',
    'domain/06_research/insight_promotion_rules.md', 'domain/06_research/evidence_levels.md',
    'domain/07_governance/privacy.md', 'domain/07_governance/approval_rules.md',
    'domain/07_governance/source_priority.md',
    'references/agent_registry.toml', 'references/agent_responsibility_matrix.md',
    'references/runtime_workflows.md', 'references/artifact_dependency_map.md',
    'references/human_approval_gates.md', 'references/conversational_teacher_loop.md',
    'references/conversation_state_machine.md',
    'scripts/structured_artifacts.py', 'scripts/validate_semantic_contracts.py',
    'scripts/validate_golden_run.py', 'scripts/render_golden_assessment.py',
    'scripts/validate_conversational_runtime.py',
    'tests/test_conversational_guards.py', 'tests/test_golden_run.py',
    '_workspace/02_semantic_validation_audit.md',
]

REQUIRED_DIRS = [
    '.codex/agents', '.agents/skills', 'contracts', 'contracts/conversation',
    'tests/fixtures', 'tests/fixtures/conversation', 'tests/fixtures/golden/conversational_cafe',
    'tests/acceptance', 'tests/acceptance/conversation', '_workspace/templates', '_workspace/runs',
]

BASE_SKILLS = [
    'kc-learner-state-analysis', 'kc-learning-progression-planning', 'kc-lesson-architecture',
    'kc-practice-design', 'kc-student-experience-design', 'kc-learning-followup',
    'kc-assessment-review', 'kc-research-synthesis', 'kc-domain-curation', 'kc-privacy-audit',
    'korean-connection-orchestrator',
]

FRONT_STAGE_SKILLS = [
    'kc-lesson-intake', 'kc-lesson-resume', 'kc-lesson-turn', 'kc-lesson-unknown',
    'kc-lesson-scope-lock', 'kc-post-lesson-reflection', 'kc-next-lesson-decision',
]

BASE_ACCEPTANCE = [
    'trial', 'making_friends', 'daily_life_transfer', 'creator_korean',
    'student_experience_design', 'post_lesson_followup', 'research_promotion', 'privacy_failure',
]

CONVERSATION_ACCEPTANCE = [
    'bare_lesson_intake', 'rich_non_linear_entry', 'unknown_to_recommendation',
    'lesson_scope_lock', 'build_blocked_without_lock', 'teacher_override_advance',
    'post_lesson_reflection', 'next_lesson_teacher_decision', 'resume_requires_run_dir',
    'continue_does_not_bypass_gate',
]


def fail(messages: list[str]) -> None:
    print('FAIL: structure validation failed')
    for message in messages:
        print(f'- {message}')
    sys.exit(1)


def main() -> None:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f'missing required file: {rel}')
    for rel in REQUIRED_DIRS:
        if not (ROOT / rel).is_dir():
            failures.append(f'missing required directory: {rel}')

    if REGISTRY.is_file():
        data = tomllib.loads(REGISTRY.read_text(encoding='utf-8'))
        entries = data.get('agents', [])
        names = [entry.get('name') for entry in entries]
        if len(names) != len(set(names)):
            failures.append('agent registry contains duplicate names')
        for entry in entries:
            if entry.get('status') != 'approved':
                continue
            name = entry.get('name')
            if entry.get('required') is True and not (ROOT / '.codex' / 'agents' / f'{name}.toml').is_file():
                failures.append(f'missing required registered agent: {name}')

    for skill in BASE_SKILLS + FRONT_STAGE_SKILLS:
        if not (ROOT / '.agents' / 'skills' / skill / 'SKILL.md').is_file():
            failures.append(f'missing required skill: {skill}')

    for scenario in BASE_ACCEPTANCE:
        if not (ROOT / 'tests' / 'acceptance' / f'{scenario}.md').is_file():
            failures.append(f'missing acceptance scenario: {scenario}')
    for scenario in CONVERSATION_ACCEPTANCE:
        if not (ROOT / 'tests' / 'acceptance' / 'conversation' / f'{scenario}.md').is_file():
            failures.append(f'missing conversation acceptance scenario: {scenario}')

    nested_git = [path for path in ROOT.rglob('.git') if path.is_dir()]
    if nested_git:
        failures.append('nested git repository detected')
    if (ROOT / '.codex' / 'skills').exists():
        failures.append('project skills must live under .agents/skills, not .codex/skills')

    if failures:
        fail(failures)
    print('PASS: structure is complete')


if __name__ == '__main__':
    main()
