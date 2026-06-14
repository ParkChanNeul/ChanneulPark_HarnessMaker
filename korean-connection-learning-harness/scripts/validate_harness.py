#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

MODES = [
    "build_lesson",
    "render_materials",
    "post_lesson_followup",
    "review_outputs",
    "research_to_domain",
    "audit_domain",
    "partial_rerun",
]

CORE_TERMS = [
    "Situation-led",
    "Culture-explained",
    "Grammar-tracked",
    "Practice-repeated",
    "Mastery-verified",
]

LEGACY_PRIVATE_PATTERNS = [
    r"\bBritish\b",
    r"\bBlack\b",
    r"\bTikTok\b",
    r"\b20\s?yo\b",
    r"\b20-year\b",
    r"\b1M\+?\b",
    r"\b\d+\s*(?:M|million)\+?\s+followers\b",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def run_script(script_name: str) -> None:
    script = ROOT / "scripts" / script_name
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        fail(f"{script_name} failed:\n{result.stdout}")
    print(result.stdout.strip())


def scan_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix in {".md", ".toml", ".py", ".txt"}
    ]


def main() -> None:
    run_script("validate_structure.py")
    run_script("validate_contracts.py")
    run_script("validate_agent_boundaries.py")

    orchestrator = ROOT / ".agents" / "skills" / "korean-connection-orchestrator" / "SKILL.md"
    orchestrator_text = orchestrator.read_text(encoding="utf-8")
    failures: list[str] = []

    for mode in MODES:
        if mode not in orchestrator_text:
            failures.append(f"orchestrator missing mode {mode}")

    combined = "\n".join(
        [
            (ROOT / "README.md").read_text(encoding="utf-8"),
            orchestrator_text,
            (ROOT / "domain" / "02_learning_model" / "pedagogy_principles.md").read_text(encoding="utf-8"),
        ]
    )
    for term in CORE_TERMS:
        if term not in combined:
            failures.append(f"missing core term {term}")

    agents = (ROOT / "references" / "agent_responsibility_matrix.md").read_text(encoding="utf-8")
    for agent in [
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
    ]:
        if agent not in agents:
            failures.append(f"responsibility matrix missing {agent}")

    for path in scan_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in LEGACY_PRIVATE_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                failures.append(f"legacy private pattern {pattern!r} found in {path.relative_to(ROOT)}")

    if failures:
        fail("\n".join(f"- {failure}" for failure in failures))

    print("PASS: harness validates end to end")


if __name__ == "__main__":
    main()
