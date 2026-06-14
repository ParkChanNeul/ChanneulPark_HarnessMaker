#!/usr/bin/env python3
from pathlib import Path
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / ".codex" / "agents"
SKILL_DIR = ROOT / ".agents" / "skills"

EXPECTED_AGENT_SKILLS = {
    "kc_learner_state_analyst": "kc-learner-state-analysis",
    "kc_learning_progression_planner": "kc-learning-progression-planning",
    "kc_lesson_architect": "kc-lesson-architecture",
    "kc_practice_designer": "kc-practice-design",
    "kc_student_experience_designer": "kc-student-experience-design",
    "kc_learning_followup_teacher": "kc-learning-followup",
    "kc_assessment_reviewer": "kc-assessment-review",
    "kc_research_synthesizer": "kc-research-synthesis",
    "kc_domain_curator": "kc-domain-curation",
    "kc_privacy_auditor": "kc-privacy-audit",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    failures: list[str] = []
    agent_files = sorted(AGENT_DIR.glob("*.toml"))

    actual_agents = {path.stem for path in agent_files}
    missing = sorted(set(EXPECTED_AGENT_SKILLS) - actual_agents)
    extra = sorted(actual_agents - set(EXPECTED_AGENT_SKILLS))
    if missing:
        failures.append("missing agents: " + ", ".join(missing))
    if extra:
        failures.append("unexpected agents: " + ", ".join(extra))

    for path in agent_files:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        name = data.get("name")
        if name != path.stem:
            failures.append(f"{path.relative_to(ROOT)} name must match filename stem")
        for field in ["name", "description", "sandbox_mode", "developer_instructions"]:
            if field not in data:
                failures.append(f"{path.relative_to(ROOT)} missing {field}")
        if data.get("sandbox_mode") != "read-only":
            failures.append(f"{path.relative_to(ROOT)} must be read-only")
        if "model" in data:
            failures.append(f"{path.relative_to(ROOT)} must not hardcode model")
        skill = EXPECTED_AGENT_SKILLS.get(path.stem)
        instructions = data.get("developer_instructions", "")
        if skill and skill not in instructions:
            failures.append(f"{path.relative_to(ROOT)} does not reference skill {skill}")
        if skill and not (SKILL_DIR / skill / "SKILL.md").is_file():
            failures.append(f"missing skill for {path.stem}: {skill}")
        if "Do not write final files" not in instructions and "Do not write target files" not in instructions:
            failures.append(f"{path.relative_to(ROOT)} must state parent-owned final writes")

    orchestrator_agent = AGENT_DIR / "korean_connection_orchestrator.toml"
    if orchestrator_agent.exists():
        failures.append("do not create a separate orchestrator agent TOML")

    if failures:
        fail("\n".join(f"- {failure}" for failure in failures))

    print("PASS: agent boundaries are valid")


if __name__ == "__main__":
    main()
