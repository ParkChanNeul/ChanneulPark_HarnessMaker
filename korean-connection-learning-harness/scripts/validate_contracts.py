#!/usr/bin/env python3
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts"

EXPECTED_CONTRACTS = [
    "lesson_request",
    "learner_context_snapshot",
    "learner_state_delta",
    "progression_plan",
    "lesson_blueprint",
    "practice_plan",
    "student_deck_spec",
    "design_manifest",
    "lesson_result",
    "material_manifest",
    "weekly_learning_pack",
    "homework_plan",
    "quizlet_plan",
    "follow_up_message",
    "next_lesson_check",
    "assessment_report",
    "privacy_report",
    "research_insight_proposal",
    "domain_update_proposal",
    "approval_state",
]

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Producer",
    "## Consumers",
    "## Required Fields",
    "## Validation",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    failures: list[str] = []

    for name in EXPECTED_CONTRACTS:
        path = CONTRACT_DIR / f"{name}.md"
        if not path.is_file():
            failures.append(f"missing contract: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("# Contract: "):
            failures.append(f"{path.relative_to(ROOT)} must start with '# Contract: '")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                failures.append(f"{path.relative_to(ROOT)} missing {section}")
        if "```yaml" not in text:
            failures.append(f"{path.relative_to(ROOT)} missing yaml field block")

    actual = sorted(path.stem for path in CONTRACT_DIR.glob("*.md"))
    extra = sorted(set(actual) - set(EXPECTED_CONTRACTS))
    if extra:
        failures.append("unexpected contracts: " + ", ".join(extra))

    if failures:
        fail("\n".join(f"- {failure}" for failure in failures))

    print("PASS: contracts are complete")


if __name__ == "__main__":
    main()
