from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
GOLDEN = ROOT / "tests" / "fixtures" / "golden" / "conversational_cafe"
sys.path.insert(0, str(SCRIPTS))

from structured_artifacts import extract_structured_block  # noqa: E402
from validate_golden_run import validate_golden_run  # noqa: E402


FENCE_RE = re.compile(r"```(?:yaml|json)\s*\n.*?\n```", re.DOTALL)


def write_payload(path: Path, data: dict) -> None:
    text = path.read_text(encoding="utf-8")
    block = "```yaml\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```"
    updated, count = FENCE_RE.subn(block, text, count=1)
    if count != 1:
        raise AssertionError(f"structured fence not found in {path}")
    path.write_text(updated, encoding="utf-8")


class GoldenRunTests(unittest.TestCase):
    def golden_copy(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        target = Path(temp.name) / "conversational_cafe"
        shutil.copytree(GOLDEN, target)
        return temp, target

    def mutate(self, root: Path, rel: str, callback) -> None:
        path = root / rel
        data = extract_structured_block(path)
        callback(data)
        write_payload(path, data)

    def assert_has_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}, got {errors!r}",
        )

    def test_current_golden_cafe_run_passes(self) -> None:
        self.assertEqual(validate_golden_run(GOLDEN), [])

    def test_missing_relative_reference_fails(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "10_weekly_learning_pack.md",
            lambda data: data.update({"homework_ref": "missing_homework.md"}),
        )
        self.assert_has_error(validate_golden_run(root), "missing_homework.md")

    def test_scope_lock_and_progression_new_grammar_mismatch_fails(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "02_progression_plan.md",
            lambda data: data.update({"new_target_candidates": ["different_target"]}),
        )
        self.assert_has_error(validate_golden_run(root), "new grammar")

    def test_progression_and_blueprint_vocabulary_mismatch_fails(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)

        def change(data: dict) -> None:
            data["vocabulary_scope"]["productive_core_count"] = 5
            data["vocabulary_scope"]["receptive_support_count"] = 5

        self.mutate(root, "03_lesson_blueprint.md", change)
        self.assert_has_error(validate_golden_run(root), "vocabulary scope")

    def test_slide_count_mismatch_fails(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "05_student_deck_spec.md",
            lambda data: data.update({"slide_count_target": 11}),
        )
        self.assert_has_error(validate_golden_run(root), "slide_count_target")

    def test_homework_only_rejects_next_lesson_check(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)

        def change(data: dict) -> None:
            data["followup_scope"] = "homework_only"
            data["source_next_lesson_decision_lock"] = None

        self.mutate(root, "10_weekly_learning_pack.md", change)
        self.assert_has_error(validate_golden_run(root), "homework_only")

    def test_full_followup_requires_next_lesson_lock(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "10_weekly_learning_pack.md",
            lambda data: data.update({"source_next_lesson_decision_lock": None}),
        )
        self.assert_has_error(validate_golden_run(root), "full_followup")

    def test_valid_homework_only_passes(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)

        def change_pack(data: dict) -> None:
            data["followup_scope"] = "homework_only"
            data["source_next_lesson_decision_lock"] = None
            data["next_lesson_check_ref"] = None

        self.mutate(root, "10_weekly_learning_pack.md", change_pack)
        for rel in [
            "07_homework_plan.md",
            "08_quizlet_plan.md",
            "09_follow_up_message.md",
        ]:
            self.mutate(
                root,
                rel,
                lambda data: data.update({"followup_scope": "homework_only"}),
            )
        (root / "10_next_lesson_check.md").unlink()
        (root / "00_conversation" / "next_lesson_decision_lock.md").unlink()
        assessment = root / "11_assessment_report.md"
        assessment.unlink()
        self.assertEqual(validate_golden_run(root, check_assessment=False), [])

    def test_full_followup_with_valid_lock_passes(self) -> None:
        self.assertEqual(validate_golden_run(GOLDEN), [])

    def test_assessment_report_must_match_computed_result(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "11_assessment_report.md",
            lambda data: data.update({"overall_status": "blocked"}),
        )
        self.assert_has_error(validate_golden_run(root), "assessment report")


if __name__ == "__main__":
    unittest.main()
