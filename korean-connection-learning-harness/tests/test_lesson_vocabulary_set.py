from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_semantic_contracts  # noqa: E402


CANONICAL_TARGET_IDS = {
    "chunk_request_noun_juseyo",
    "interaction_confirm_and_answer",
}


def valid_scope_lock() -> dict:
    return {
        "lesson_scope_lock_id": "lock-001",
        "language_targets": [
            {
                "target_ref": "chunk_request_noun_juseyo",
                "treatment": "new",
            },
            {
                "target_ref": "interaction_confirm_and_answer",
                "treatment": "practice",
            },
        ],
        "vocabulary_scope": {
            "in_class_new_item_count": 2,
        },
    }


def vocabulary_item(
    item_id: str,
    role: str,
    *,
    target_refs: list[str] | None = None,
) -> dict:
    return {
        "item_id": item_id,
        "surface_form": "아메리카노",
        "item_type": "word",
        "gloss_en": "Americano",
        "role": role,
        "collocations": [],
        "example_ko": "아메리카노 주세요.",
        "example_en": "Please give me an Americano.",
        "production_prompt": "원하는 음료를 주문하세요.",
        "target_refs": target_refs or ["chunk_request_noun_juseyo"],
        "situation_refs": ["cafe_ordering"],
        "notes": "",
    }


def valid_proposed_set() -> dict:
    return {
        "lesson_vocabulary_set_id": "vocab-set-001",
        "revision": 1,
        "supersedes": None,
        "selection_status": "proposed",
        "selection_mode": "manual",
        "lesson_scope_lock_ref": None,
        "target_pack": "cafe_core",
        "approved_by_teacher": False,
        "approval_evidence": "",
        "counts": {
            "review": 1,
            "productive_core": 1,
            "receptive_support": 1,
            "homework_expansion": 1,
        },
        "items": [
            vocabulary_item("review-001", "review"),
            vocabulary_item("core-001", "productive_core"),
            vocabulary_item(
                "support-001",
                "receptive_support",
                target_refs=["interaction_confirm_and_answer"],
            ),
            vocabulary_item("homework-001", "homework_expansion"),
        ],
        "created_artifact_refs": [],
    }


def valid_locked_set() -> dict:
    data = valid_proposed_set()
    data["selection_status"] = "locked"
    data["lesson_scope_lock_ref"] = "lock-001"
    data["approved_by_teacher"] = True
    data["approval_evidence"] = "이 단어 구성으로 진행합니다."
    return data


class LessonVocabularySetTests(unittest.TestCase):
    def assert_has_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}, got {errors!r}",
        )

    def validate(self, data: dict, scope_lock: dict | None = None) -> list[str]:
        return validate_semantic_contracts.validate_lesson_vocabulary_set(
            data,
            scope_lock or valid_scope_lock(),
            CANONICAL_TARGET_IDS,
        )

    def test_validator_is_available(self) -> None:
        self.assertTrue(
            hasattr(
                validate_semantic_contracts,
                "validate_lesson_vocabulary_set",
            )
        )

    def test_valid_proposed_set_passes_without_teacher_approval(self) -> None:
        self.assertEqual(self.validate(valid_proposed_set()), [])

    def test_valid_locked_set_passes(self) -> None:
        self.assertEqual(self.validate(valid_locked_set()), [])

    def test_duplicate_item_id_fails(self) -> None:
        data = valid_proposed_set()
        data["items"][1]["item_id"] = data["items"][0]["item_id"]
        self.assert_has_error(self.validate(data), "item_id values must be unique")

    def test_role_count_mismatch_fails(self) -> None:
        data = valid_proposed_set()
        data["counts"]["productive_core"] = 2
        self.assert_has_error(self.validate(data), "productive_core role count")

    def test_new_item_count_mismatch_fails(self) -> None:
        scope_lock = valid_scope_lock()
        scope_lock["vocabulary_scope"]["in_class_new_item_count"] = 3
        self.assert_has_error(
            self.validate(valid_proposed_set(), scope_lock),
            "in_class_new_item_count",
        )

    def test_locked_set_requires_teacher_approval(self) -> None:
        data = valid_locked_set()
        data["approved_by_teacher"] = False
        self.assert_has_error(self.validate(data), "approved_by_teacher")

    def test_locked_set_requires_approval_evidence(self) -> None:
        data = valid_locked_set()
        data["approval_evidence"] = ""
        self.assert_has_error(self.validate(data), "approval_evidence")

    def test_unknown_target_ref_fails(self) -> None:
        data = valid_proposed_set()
        data["items"][0]["target_refs"] = ["unknown_target"]
        self.assert_has_error(self.validate(data), "unknown target_ref")

    def test_locked_set_requires_matching_scope_lock_ref(self) -> None:
        data = valid_locked_set()
        data["lesson_scope_lock_ref"] = "missing-lock"
        self.assert_has_error(self.validate(data), "lesson_scope_lock_ref")

    def test_required_item_identity_fields_must_be_non_empty(self) -> None:
        for field in ["surface_form", "role", "item_type"]:
            with self.subTest(field=field):
                data = valid_proposed_set()
                data["items"][0][field] = ""
                self.assert_has_error(self.validate(data), field)


if __name__ == "__main__":
    unittest.main()
