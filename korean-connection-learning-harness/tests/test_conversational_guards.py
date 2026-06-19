from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_semantic_contracts import (  # noqa: E402
    validate_lesson_intake_state,
    validate_lesson_scope_lock,
    validate_next_lesson_decision_lock,
    validate_post_lesson_teacher_card,
    validate_teacher_decision_card,
)


def valid_vocabulary_scope() -> dict:
    return {
        "target_pack": "cafe_core",
        "lesson_vocabulary_set_ref": None,
        "in_class_new_item_count": 10,
        "productive_core_count": 6,
        "receptive_support_count": 4,
        "review_item_ids": [],
        "homework_expansion_count": 2,
    }


def valid_lesson_scope_lock() -> dict:
    return {
        "lesson_scope_lock_id": "lock-001",
        "revision": 1,
        "supersedes": None,
        "lock_status": "locked",
        "approved_by_teacher": True,
        "approval_evidence": "B안으로 승인합니다.",
        "learner": {
            "alias": "synthetic_learner",
            "level": "A1",
            "learner_context_ref": None,
        },
        "lesson": {
            "mode": "mixed",
            "duration_minutes": 50,
            "situation_scope": {
                "pack_ref": "cafe_ordering",
                "sub_situation_ids": ["order_item", "answer_staff_question"],
            },
            "lesson_promise": "주문하고 직원 질문에 답한다",
        },
        "language_targets": [
            {
                "target_ref": "chunk_request_noun_juseyo",
                "treatment": "new",
            },
            {
                "target_ref": "discourse_short_noun_iyo",
                "treatment": "review",
            },
            {
                "target_ref": "register_haeyo_polite",
                "treatment": "retrieval",
            },
            {
                "target_ref": "grammar_request_verb_eo_juseyo",
                "treatment": "transfer",
            },
            {
                "target_ref": "interaction_confirm_and_answer",
                "treatment": "practice",
            },
        ],
        "vocabulary_scope": valid_vocabulary_scope(),
        "material_scope": {
            "student_deck": True,
            "html": True,
            "mobile_cheat_sheet": True,
            "homework": True,
            "quizlet_plan": True,
        },
        "teacher_overrides": [],
        "assumption_locks": [],
        "unresolved_blockers": [],
        "created_artifact_refs": [],
    }


def valid_teacher_decision_card() -> dict:
    return {
        "decision_card_id": "card-001",
        "source_intake_state": "lesson_intake_state.md",
        "teacher_facts": ["A1", "50분"],
        "agent_interpretations": ["듣기 부담 가능성"],
        "teaching_problem": {
            "summary": "후속 질문에 즉답하기",
            "evidence": ["teacher note"],
            "confidence": "medium",
        },
        "options": [
            {
                "option_id": "A",
                "mode": "mixed",
                "situation_scope": {
                    "pack_ref": "cafe_ordering",
                    "sub_situation_ids": ["order_item", "answer_staff_question"],
                },
                "candidate_language_targets": [
                    {
                        "target_ref": "chunk_request_noun_juseyo",
                        "treatment": "new",
                    },
                    {
                        "target_ref": "discourse_short_noun_iyo",
                        "treatment": "review",
                    },
                    {
                        "target_ref": "interaction_confirm_and_answer",
                        "treatment": "practice",
                    },
                ],
                "vocabulary_scope": valid_vocabulary_scope(),
                "benefits": ["연결 연습"],
                "risks": ["시간 관리"],
            }
        ],
        "recommendation": {
            "option_id": "A",
            "rationale": "요청과 증거에 맞음",
            "limitations": ["실제 수업 관찰 전"],
        },
        "required_teacher_decisions": [],
        "assumption_candidates": [],
        "scope_status": "ready_to_lock",
        "advisory_inputs": [],
    }


def valid_next_lesson_lock() -> dict:
    return {
        "next_lesson_decision_lock_id": "next-lock-001",
        "revision": 1,
        "supersedes": None,
        "source_post_lesson_card": "post_lesson_teacher_card.md",
        "lock_status": "locked",
        "approved_by_teacher": True,
        "approval_evidence": "다음 진도로 승인합니다.",
        "selected_direction": {
            "mode": "advance",
            "situation_scope": {
                "pack_ref": "preferences_opinions",
                "sub_situation_ids": ["talk_about_hobbies"],
            },
        },
        "language_targets": [
            {
                "target_ref": "grammar_want_go_sipeoyo",
                "treatment": "new",
            },
            {
                "target_ref": "chunk_request_noun_juseyo",
                "treatment": "carrier",
            },
            {
                "target_ref": "interaction_confirm_and_answer",
                "treatment": "review",
            },
        ],
        "vocabulary_direction": {
            "target_pack": "hobbies_core",
            "lesson_vocabulary_set_ref": None,
            "in_class_new_item_count": 8,
            "productive_core_count": 5,
            "receptive_support_count": 3,
            "review_item_ids": [],
            "carrier_item_ids": ["cafe_ordering"],
            "homework_expansion_count": 2,
        },
        "homework_scope": {
            "estimated_minutes": 8,
            "focus": "듣고 답하기",
            "required_outputs": ["homework_plan"],
        },
        "next_lesson_check": ["직원 질문 즉답"],
        "teacher_notes": [],
        "unresolved_blockers": [],
    }


class ConversationalGuardTests(unittest.TestCase):
    def assert_has_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}, got {errors!r}",
        )

    def test_valid_lesson_scope_lock_passes(self) -> None:
        self.assertEqual(validate_lesson_scope_lock(valid_lesson_scope_lock()), [])

    def test_locked_scope_requires_teacher_approval(self) -> None:
        data = valid_lesson_scope_lock()
        data["approved_by_teacher"] = False
        self.assert_has_error(validate_lesson_scope_lock(data), "approved_by_teacher")

    def test_locked_scope_requires_approval_evidence(self) -> None:
        data = valid_lesson_scope_lock()
        data["approval_evidence"] = ""
        self.assert_has_error(validate_lesson_scope_lock(data), "approval_evidence")

    def test_locked_scope_rejects_unresolved_blockers(self) -> None:
        data = valid_lesson_scope_lock()
        data["unresolved_blockers"] = ["teacher decision missing"]
        self.assert_has_error(validate_lesson_scope_lock(data), "unresolved_blockers")

    def test_vocabulary_count_must_equal_productive_plus_receptive(self) -> None:
        data = valid_lesson_scope_lock()
        data["vocabulary_scope"]["in_class_new_item_count"] = 11
        self.assert_has_error(validate_lesson_scope_lock(data), "vocabulary count")

    def test_language_targets_reject_duplicate_target_treatments(self) -> None:
        data = valid_lesson_scope_lock()
        data["language_targets"].append(
            {
                "target_ref": "chunk_request_noun_juseyo",
                "treatment": "review",
            }
        )
        self.assert_has_error(validate_lesson_scope_lock(data), "multiple treatments")

    def test_lesson_scope_rejects_legacy_target_fields(self) -> None:
        data = valid_lesson_scope_lock()
        data["targets"] = {"approved_new_grammar": ["request_juseyo"]}
        self.assert_has_error(validate_lesson_scope_lock(data), "legacy target field")

    def test_lesson_scope_rejects_primary_situation(self) -> None:
        data = valid_lesson_scope_lock()
        data["lesson"]["primary_situation"] = "cafe"
        self.assert_has_error(validate_lesson_scope_lock(data), "primary_situation")

    def test_situation_scope_requires_pack_and_sub_situations(self) -> None:
        data = valid_lesson_scope_lock()
        data["lesson"]["situation_scope"] = {
            "pack_ref": "",
            "sub_situation_ids": "order_item",
        }
        errors = validate_lesson_scope_lock(data)
        self.assert_has_error(errors, "pack_ref")
        self.assert_has_error(errors, "sub_situation_ids")

    def test_legacy_vocabulary_field_is_rejected(self) -> None:
        data = valid_lesson_scope_lock()
        data["vocabulary_scope"]["vocabulary_count"] = 10
        self.assert_has_error(validate_lesson_scope_lock(data), "legacy vocabulary field")

    def test_ready_teacher_card_cannot_leave_required_decisions(self) -> None:
        data = valid_teacher_decision_card()
        data["required_teacher_decisions"] = ["vocabulary scope"]
        self.assert_has_error(validate_teacher_decision_card(data), "required_teacher_decisions")

    def test_teacher_card_rejects_legacy_candidate_fields(self) -> None:
        data = valid_teacher_decision_card()
        data["options"][0]["new_grammar_candidates"] = ["request_juseyo"]
        self.assert_has_error(validate_teacher_decision_card(data), "legacy target field")

    def test_recommendation_option_must_exist(self) -> None:
        data = valid_teacher_decision_card()
        data["recommendation"]["option_id"] = "missing"
        self.assert_has_error(validate_teacher_decision_card(data), "recommendation.option_id")

    def test_intake_ready_state_rejects_open_blocking_unknown(self) -> None:
        data = {
            "run_id": "run-001",
            "conversation_state": "ready_to_lock",
            "teacher_request": {"raw_request": "수업", "requested_output": []},
            "known_context": {},
            "unknowns": [
                {
                    "unknown_id": "mode",
                    "category": "lesson_mode",
                    "blocking": True,
                    "question": "방향?",
                    "answer": None,
                    "resolution_status": "open",
                }
            ],
            "workspace": {
                "run_dir": "../run",
                "read_allowed": True,
                "write_allowed": False,
            },
        }
        self.assert_has_error(validate_lesson_intake_state(data), "blocking unknown")

    def test_post_lesson_homework_approval_requires_existing_option(self) -> None:
        data = {
            "post_lesson_teacher_card_id": "post-001",
            "source_lesson_result": "../06_lesson_result.md",
            "teacher_observations": [],
            "observed_successes": [],
            "observed_breakdowns": [],
            "evidence_gaps": [],
            "state_update_candidates": [],
            "homework_options": [{"option_id": "A"}],
            "next_lesson_options": [],
            "recommendation": {
                "homework_option": "A",
                "next_lesson_option": None,
                "rationale": "",
            },
            "teacher_approval": {
                "homework_approved": True,
                "homework_option": "B",
                "approval_evidence": "B로 진행",
            },
            "required_teacher_decisions": [],
            "status": "partial",
        }
        self.assert_has_error(
            validate_post_lesson_teacher_card(data),
            "teacher_approval.homework_option",
        )

    def test_carrier_and_review_are_distinct_valid_treatments(self) -> None:
        self.assertEqual(validate_next_lesson_decision_lock(valid_next_lesson_lock()), [])


if __name__ == "__main__":
    unittest.main()
