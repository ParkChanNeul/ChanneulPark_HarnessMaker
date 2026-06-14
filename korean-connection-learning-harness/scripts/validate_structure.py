#!/usr/bin/env python3
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    ".gitignore",
    "_workspace/README.md",
    "_workspace/00_source_audit.md",
    "_workspace/templates/run_handoff_template.md",
    "domain/01_identity/brand_positioning.md",
    "domain/01_identity/customer_promise.md",
    "domain/02_learning_model/pedagogy_principles.md",
    "domain/02_learning_model/grammar_progression.md",
    "domain/02_learning_model/vocabulary_progression.md",
    "domain/02_learning_model/conversation_skill_progression.md",
    "domain/02_learning_model/mastery_definition.md",
    "domain/03_curriculum/situation_map.md",
    "domain/03_curriculum/module_map.md",
    "domain/03_curriculum/sequence_rules.md",
    "domain/03_curriculum/spiral_review_rules.md",
    "domain/04_lesson_system/lesson_contract.md",
    "domain/04_lesson_system/practice_ladder.md",
    "domain/04_lesson_system/culture_usage_rules.md",
    "domain/04_lesson_system/student_experience_rules.md",
    "domain/04_lesson_system/mission_and_followup.md",
    "domain/04_lesson_system/homework_and_retention.md",
    "domain/05_learner_state/learner_model.schema.md",
    "domain/05_learner_state/grammar_mastery.schema.md",
    "domain/05_learner_state/conversation_mastery.schema.md",
    "domain/05_learner_state/mission_history.schema.md",
    "domain/05_learner_state/lesson_result.schema.md",
    "domain/06_research/insight_promotion_rules.md",
    "domain/06_research/evidence_levels.md",
    "domain/07_governance/privacy.md",
    "domain/07_governance/approval_rules.md",
    "domain/07_governance/source_priority.md",
    "references/agent_responsibility_matrix.md",
    "references/runtime_workflows.md",
    "references/artifact_dependency_map.md",
    "references/human_approval_gates.md",
]

REQUIRED_DIRS = [
    ".codex/agents",
    ".agents/skills",
    "contracts",
    "tests/fixtures",
    "tests/acceptance",
    "_workspace/templates",
    "_workspace/runs",
]

EXPECTED_AGENTS = [
    "kc_learner_state_analyst",
    "kc_learning_progression_planner",
    "kc_lesson_architect",
    "kc_practice_designer",
    "kc_student_experience_designer",
    "kc_learning_followup_teacher",
    "kc_assessment_reviewer",
    "kc_research_synthesizer",
    "kc_domain_curator",
    "kc_privacy_auditor",
]

EXPECTED_SKILLS = [
    "kc-learner-state-analysis",
    "kc-learning-progression-planning",
    "kc-lesson-architecture",
    "kc-practice-design",
    "kc-student-experience-design",
    "kc-learning-followup",
    "kc-assessment-review",
    "kc-research-synthesis",
    "kc-domain-curation",
    "kc-privacy-audit",
    "korean-connection-orchestrator",
]

EXPECTED_ACCEPTANCE = [
    "trial",
    "making_friends",
    "daily_life_transfer",
    "creator_korean",
    "student_experience_design",
    "post_lesson_followup",
    "research_promotion",
    "privacy_failure",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    missing += [path for path in REQUIRED_DIRS if not (ROOT / path).is_dir()]

    for agent in EXPECTED_AGENTS:
        path = ROOT / ".codex" / "agents" / f"{agent}.toml"
        if not path.is_file():
            missing.append(str(path.relative_to(ROOT)))

    for skill in EXPECTED_SKILLS:
        path = ROOT / ".agents" / "skills" / skill / "SKILL.md"
        if not path.is_file():
            missing.append(str(path.relative_to(ROOT)))

    for scenario in EXPECTED_ACCEPTANCE:
        path = ROOT / "tests" / "acceptance" / f"{scenario}.md"
        if not path.is_file():
            missing.append(str(path.relative_to(ROOT)))

    if missing:
        fail("missing required paths:\n" + "\n".join(f"- {path}" for path in missing))

    nested_git = [path for path in ROOT.rglob(".git") if path.is_dir()]
    if nested_git:
        fail("nested git repository detected:\n" + "\n".join(str(path) for path in nested_git))

    forbidden_dir = ROOT / ".codex" / "skills"
    if forbidden_dir.exists():
        fail("project skills must live under .agents/skills, not .codex/skills")

    print("PASS: structure is complete")


if __name__ == "__main__":
    main()
