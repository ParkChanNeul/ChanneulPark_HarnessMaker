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

    def test_golden_uses_canonical_target_and_situation_structures(self) -> None:
        lock = extract_structured_block(
            GOLDEN / "00_conversation" / "lesson_scope_lock.md"
        )
        progression = extract_structured_block(GOLDEN / "02_progression_plan.md")
        blueprint = extract_structured_block(GOLDEN / "03_lesson_blueprint.md")
        result = extract_structured_block(GOLDEN / "06_lesson_result.md")

        self.assertIn("language_targets", lock)
        self.assertIn("situation_scope", lock["lesson"])
        self.assertIn("language_targets", progression)
        self.assertIn("situation_scope", progression)
        self.assertIn("language_targets", blueprint)
        self.assertIn("situation_scope", blueprint)
        self.assertIn("language_targets", result)

    def test_transfer_target_requires_surface_evidence(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)

        def remove_surface_evidence(data: dict) -> None:
            transfer_task = data["practice_ladder"]["transfer"][0]
            transfer_task["targets"] = ["grammar_request_verb_eo_juseyo"]
            transfer_task["prompt"] = "다른 방식으로 요청하기"
            transfer_task["examples"] = []

        self.mutate(root, "04_practice_plan.md", remove_surface_evidence)
        self.assert_has_error(
            validate_golden_run(root),
            "transfer target surface evidence",
        )

    def test_transfer_target_rejects_noun_request_only(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)

        def replace_with_noun_request(data: dict) -> None:
            transfer_task = data["practice_ladder"]["transfer"][0]
            transfer_task["prompt"] = "아메리카노 주세요."
            transfer_task["examples"] = ["라테 주세요.", "물 주세요."]

        self.mutate(root, "04_practice_plan.md", replace_with_noun_request)
        self.assert_has_error(
            validate_golden_run(root),
            "transfer target surface evidence",
        )

    def test_task_level_language_target_shape_is_validated(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)

        def add_duplicate_and_type(data: dict) -> None:
            targets = data["practice_ladder"]["transfer"][0]["language_targets"]
            targets[0]["target_type"] = "grammar_construction"
            targets.append(
                {
                    "target_ref": "grammar_request_verb_eo_juseyo",
                    "treatment": "review",
                }
            )

        self.mutate(root, "04_practice_plan.md", add_duplicate_and_type)
        errors = validate_golden_run(root)
        self.assert_has_error(errors, "unexpected fields target_type")
        self.assert_has_error(errors, "cannot have multiple treatments")

    def test_missing_relative_reference_fails(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "10_weekly_learning_pack.md",
            lambda data: data.update({"homework_ref": "missing_homework.md"}),
        )
        self.assert_has_error(validate_golden_run(root), "missing_homework.md")

    def test_scope_lock_and_progression_language_target_mismatch_fails(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "02_progression_plan.md",
            lambda data: data["language_targets"][0].update(
                {"target_ref": "different_target"}
            ),
        )
        self.assert_has_error(validate_golden_run(root), "language targets")

    def test_unregistered_canonical_target_fails(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "00_conversation/lesson_scope_lock.md",
            lambda data: data["language_targets"][0].update(
                {"target_ref": "unknown_canonical_target"}
            ),
        )
        self.assert_has_error(validate_golden_run(root), "unregistered target_ref")

    def test_legacy_target_id_in_new_artifact_fails(self) -> None:
        temp, root = self.golden_copy()
        self.addCleanup(temp.cleanup)
        self.mutate(
            root,
            "00_conversation/lesson_scope_lock.md",
            lambda data: data["language_targets"][0].update(
                {"target_ref": "request_juseyo"}
            ),
        )
        self.assert_has_error(validate_golden_run(root), "legacy target_ref")

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
