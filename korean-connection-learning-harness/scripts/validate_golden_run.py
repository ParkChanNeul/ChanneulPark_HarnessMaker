#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

from structured_artifacts import (
    StructuredArtifactError,
    extract_structured_block,
    is_artifact_ref,
    require_fields,
    resolve_artifact_ref,
)
from validate_semantic_contracts import (
    validate_lesson_intake_state,
    validate_lesson_scope_lock,
    validate_next_lesson_decision_lock,
    validate_post_lesson_teacher_card,
    validate_teacher_decision_card,
    validate_vocabulary_scope,
)


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "fixtures" / "golden" / "conversational_cafe"

ARTIFACTS = {
    "intake": "00_conversation/lesson_intake_state.md",
    "teacher_card": "00_conversation/teacher_decision_card.md",
    "lesson_lock": "00_conversation/lesson_scope_lock.md",
    "post_card": "00_conversation/post_lesson_teacher_card.md",
    "next_lock": "00_conversation/next_lesson_decision_lock.md",
    "snapshot": "01_learner_context_snapshot.md",
    "progression": "02_progression_plan.md",
    "blueprint": "03_lesson_blueprint.md",
    "practice": "04_practice_plan.md",
    "deck": "05_student_deck_spec.md",
    "lesson_result": "06_lesson_result.md",
    "homework": "07_homework_plan.md",
    "quizlet": "08_quizlet_plan.md",
    "message": "09_follow_up_message.md",
    "next_check": "10_next_lesson_check.md",
    "weekly_pack": "10_weekly_learning_pack.md",
    "assessment": "11_assessment_report.md",
}

BASE_REQUIRED = {
    "intake",
    "teacher_card",
    "lesson_lock",
    "post_card",
    "snapshot",
    "progression",
    "blueprint",
    "practice",
    "deck",
    "lesson_result",
    "homework",
    "quizlet",
    "message",
    "weekly_pack",
}

REQUIRED_FIELDS = {
    "snapshot": [
        "snapshot_id",
        "learner_alias",
        "level_band",
        "goals",
        "active_situations",
        "grammar_status",
        "conversation_status",
        "mission_history_summary",
        "privacy_redactions",
        "evidence_notes",
    ],
    "progression": [
        "progression_plan_id",
        "lesson_scope_lock_ref",
        "learner_alias",
        "planning_window",
        "primary_situation",
        "approved_mode",
        "new_target_candidates",
        "review_targets",
        "retrieval_targets",
        "transfer_targets",
        "conversation_skill_targets",
        "vocabulary_scope",
        "teacher_overrides_applied",
        "blocked_targets",
        "spiral_review_plan",
        "next_lesson_rationale",
    ],
    "blueprint": [
        "lesson_blueprint_id",
        "lesson_scope_lock_ref",
        "source_progression_plan",
        "lesson_title",
        "learner_alias",
        "situation",
        "lesson_promise",
        "new_targets",
        "review_targets",
        "retrieval_targets",
        "transfer_targets",
        "conversation_skill_targets",
        "vocabulary_scope",
        "teacher_overrides_applied",
        "culture_point",
        "lesson_flow",
        "assessment_evidence_to_collect",
        "override_reason",
    ],
    "practice": [
        "practice_plan_id",
        "lesson_scope_lock_ref",
        "source_blueprint",
        "vocabulary_scope",
        "practice_ladder",
        "retrieval_prompts",
        "roleplay_variations",
        "error_repair_prompts",
        "homework_seed",
        "quizlet_seed",
        "evidence_capture_points",
        "teacher_overrides_applied",
    ],
    "deck": [
        "student_deck_spec_id",
        "lesson_scope_lock_ref",
        "source_blueprint",
        "deck_mode",
        "slide_count_target",
        "vocabulary_scope",
        "slides",
        "design_notes",
        "non_student_notes",
    ],
    "lesson_result": [
        "lesson_result_id",
        "lesson_id",
        "learner_alias",
        "planned_targets",
        "observed_evidence",
        "followup_inputs",
        "privacy_redactions",
    ],
    "homework": [
        "homework_plan_id",
        "followup_scope",
        "source_lesson_result",
        "source_post_lesson_teacher_card",
        "tasks",
        "support",
    ],
    "quizlet": [
        "quizlet_plan_id",
        "followup_scope",
        "source_post_lesson_teacher_card",
        "source_targets",
        "sets",
        "review_notes",
    ],
    "message": [
        "follow_up_message_id",
        "followup_scope",
        "source_post_lesson_teacher_card",
        "learner_alias",
        "tone",
        "message",
        "privacy_review",
    ],
    "next_check": [
        "next_lesson_check_id",
        "source_lesson_result",
        "source_next_lesson_decision_lock",
        "selected_direction",
        "prior_target_treatments",
        "must_review",
        "should_transfer",
        "learner_question_to_revisit",
        "mission_result_to_check",
        "risk_if_ignored",
        "suggested_next_situation",
    ],
    "weekly_pack": [
        "weekly_learning_pack_id",
        "followup_scope",
        "source_post_lesson_teacher_card",
        "source_next_lesson_decision_lock",
        "review_focus",
        "homework_ref",
        "quizlet_ref",
        "follow_up_message_ref",
        "next_lesson_check_ref",
    ],
}

REFERENCE_FIELDS = {
    "run_dir",
    "source_intake_state",
    "learner_context_ref",
    "source_lesson_result",
    "source_post_lesson_card",
    "lesson_scope_lock_ref",
    "source_progression_plan",
    "source_blueprint",
    "source_post_lesson_teacher_card",
    "source_next_lesson_decision_lock",
    "homework_ref",
    "quizlet_ref",
    "follow_up_message_ref",
    "next_lesson_check_ref",
    "reviewed_artifacts",
    "created_artifact_refs",
}

INTERNAL_SLIDE_TITLES = {
    "Cultural Tension",
    "Korean Social Rule",
    "Social Meaning",
    "Language Mechanism",
    "Grammar Tool",
}

CONTRACT_CHECK_NAMES = [
    "structured payloads parse",
    "required fields complete",
    "artifact references resolve",
    "lesson scope lock matches progression",
    "progression matches blueprint",
    "blueprint targets are covered by practice",
    "deck contract matches slides",
    "followup scope matches next lesson lock",
]

PRIVATE_PATTERNS = [
    "legal_name",
    "private_social_account",
    "follower_count",
    "exact_age",
]


def _load_artifacts(
    golden: Path,
    *,
    include_assessment: bool = False,
) -> tuple[dict[str, dict], list[str]]:
    artifacts: dict[str, dict] = {}
    errors: list[str] = []
    required = set(BASE_REQUIRED)
    if include_assessment:
        required.add("assessment")

    for name, rel in ARTIFACTS.items():
        if name == "assessment" and not include_assessment:
            continue
        path = golden / rel
        if not path.is_file():
            if name in required:
                errors.append(f"missing Golden artifact: {rel}")
            continue
        try:
            artifacts[name] = extract_structured_block(path)
        except (OSError, StructuredArtifactError) as error:
            errors.append(str(error))
    return artifacts, errors


def _walk_reference_values(value: Any, key: str | None = None):
    if key in REFERENCE_FIELDS:
        if isinstance(value, str):
            yield value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    yield item
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from _walk_reference_values(child, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_reference_values(child, key)


def _compare(
    errors: list[str],
    label: str,
    left: Any,
    right: Any,
) -> None:
    if left != right:
        errors.append(f"{label} mismatch: {left!r} != {right!r}")


def _task_targets(tasks: Any) -> set[str]:
    targets: set[str] = set()
    if not isinstance(tasks, list):
        return targets
    for task in tasks:
        if isinstance(task, dict):
            values = task.get("targets", [])
            if isinstance(values, list):
                targets.update(value for value in values if isinstance(value, str))
    return targets


def _validate_references(
    golden: Path,
    artifacts: dict[str, dict],
) -> list[str]:
    errors: list[str] = []
    for name, data in artifacts.items():
        source = golden / ARTIFACTS[name]
        for ref in _walk_reference_values(data):
            if not is_artifact_ref(ref):
                continue
            resolved = resolve_artifact_ref(source, ref)
            if resolved is None or not resolved.exists():
                errors.append(
                    f"{ARTIFACTS[name]}: referenced path does not exist: {ref}"
                )
    return errors


def _validate_required_fields(artifacts: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for name, fields in REQUIRED_FIELDS.items():
        if name not in artifacts:
            continue
        errors.extend(require_fields(artifacts[name], fields, ARTIFACTS[name]))
    return errors


def _validate_semantics(artifacts: dict[str, dict]) -> list[str]:
    validators: dict[str, Callable[[dict], list[str]]] = {
        "intake": validate_lesson_intake_state,
        "teacher_card": validate_teacher_decision_card,
        "lesson_lock": validate_lesson_scope_lock,
        "post_card": validate_post_lesson_teacher_card,
        "next_lock": validate_next_lesson_decision_lock,
    }
    errors: list[str] = []
    for name, validator in validators.items():
        if name in artifacts:
            errors.extend(
                f"{ARTIFACTS[name]}: {error}" for error in validator(artifacts[name])
            )
    for name in ["progression", "blueprint", "practice", "deck"]:
        if name in artifacts:
            errors.extend(
                f"{ARTIFACTS[name]}: {error}"
                for error in validate_vocabulary_scope(
                    artifacts[name].get("vocabulary_scope"),
                    f"{name}.vocabulary_scope",
                )
            )
    return errors


def _validate_lock_to_progression(artifacts: dict[str, dict]) -> list[str]:
    if not {"lesson_lock", "progression"}.issubset(artifacts):
        return []
    lock = artifacts["lesson_lock"]
    progression = artifacts["progression"]
    lesson = lock.get("lesson", {})
    targets = lock.get("targets", {})
    errors: list[str] = []
    _compare(errors, "lesson mode", lesson.get("mode"), progression.get("approved_mode"))
    _compare(
        errors,
        "primary situation",
        lesson.get("primary_situation"),
        progression.get("primary_situation"),
    )
    _compare(
        errors,
        "new grammar",
        targets.get("approved_new_grammar"),
        progression.get("new_target_candidates"),
    )
    _compare(
        errors,
        "review grammar",
        targets.get("approved_review_grammar"),
        progression.get("review_targets"),
    )
    _compare(
        errors,
        "retrieval targets",
        targets.get("retrieval_targets"),
        progression.get("retrieval_targets"),
    )
    _compare(
        errors,
        "transfer targets",
        targets.get("transfer_targets"),
        progression.get("transfer_targets"),
    )
    _compare(
        errors,
        "conversation targets",
        targets.get("conversation_skill_targets"),
        progression.get("conversation_skill_targets"),
    )
    _compare(
        errors,
        "vocabulary scope",
        lock.get("vocabulary_scope"),
        progression.get("vocabulary_scope"),
    )
    return errors


def _validate_progression_to_blueprint(artifacts: dict[str, dict]) -> list[str]:
    if not {"lesson_lock", "progression", "blueprint"}.issubset(artifacts):
        return []
    lock = artifacts["lesson_lock"]
    progression = artifacts["progression"]
    blueprint = artifacts["blueprint"]
    errors: list[str] = []
    pairs = [
        ("new targets", "new_target_candidates", "new_targets"),
        ("review targets", "review_targets", "review_targets"),
        ("retrieval targets", "retrieval_targets", "retrieval_targets"),
        ("transfer targets", "transfer_targets", "transfer_targets"),
        (
            "conversation targets",
            "conversation_skill_targets",
            "conversation_skill_targets",
        ),
        ("vocabulary scope", "vocabulary_scope", "vocabulary_scope"),
        (
            "teacher overrides",
            "teacher_overrides_applied",
            "teacher_overrides_applied",
        ),
    ]
    for label, progression_field, blueprint_field in pairs:
        _compare(
            errors,
            label,
            progression.get(progression_field),
            blueprint.get(blueprint_field),
        )
    _compare(
        errors,
        "blueprint situation",
        progression.get("primary_situation"),
        blueprint.get("situation"),
    )
    _compare(
        errors,
        "lesson promise",
        lock.get("lesson", {}).get("lesson_promise"),
        blueprint.get("lesson_promise"),
    )
    return errors


def _validate_blueprint_to_practice(artifacts: dict[str, dict]) -> list[str]:
    if not {"blueprint", "practice"}.issubset(artifacts):
        return []
    blueprint = artifacts["blueprint"]
    practice = artifacts["practice"]
    errors: list[str] = []
    _compare(
        errors,
        "practice vocabulary scope",
        blueprint.get("vocabulary_scope"),
        practice.get("vocabulary_scope"),
    )
    _compare(
        errors,
        "practice teacher overrides",
        blueprint.get("teacher_overrides_applied"),
        practice.get("teacher_overrides_applied"),
    )

    ladder = practice.get("practice_ladder", {})
    if not isinstance(ladder, dict):
        return errors + ["practice_ladder must be an object"]
    controlled = _task_targets(ladder.get("controlled"))
    guided = _task_targets(ladder.get("guided"))
    independent = _task_targets(ladder.get("independent"))
    transfer = _task_targets(ladder.get("transfer"))
    retrieval = _task_targets(practice.get("retrieval_prompts"))
    all_practice = controlled | guided | independent | transfer

    for target in blueprint.get("new_targets", []):
        if target not in all_practice:
            errors.append(f"new target {target!r} is not covered by practice")
    for target in blueprint.get("review_targets", []):
        if target not in all_practice | retrieval:
            errors.append(f"review target {target!r} is not covered by practice")
    for target in blueprint.get("retrieval_targets", []):
        if target not in retrieval:
            errors.append(f"retrieval target {target!r} has no retrieval prompt")
    for target in blueprint.get("transfer_targets", []):
        if target not in transfer:
            errors.append(f"transfer target {target!r} has no transfer task")
    conversation_practice = guided | independent
    for target in blueprint.get("conversation_skill_targets", []):
        if target not in conversation_practice:
            errors.append(
                f"conversation target {target!r} is not covered by "
                "guided or independent roleplay"
            )
    if not practice.get("evidence_capture_points"):
        errors.append("practice plan requires evidence_capture_points")
    return errors


def _validate_deck(artifacts: dict[str, dict]) -> list[str]:
    if "deck" not in artifacts:
        return []
    deck = artifacts["deck"]
    errors: list[str] = []
    slides = deck.get("slides")
    if not isinstance(slides, list):
        return ["student deck slides must be an array"]
    if deck.get("slide_count_target") != len(slides):
        errors.append(
            "slide_count_target does not match actual slides length: "
            f"{deck.get('slide_count_target')!r} != {len(slides)}"
        )
    slide_ids: list[Any] = []
    for index, slide in enumerate(slides):
        context = f"slides[{index}]"
        if not isinstance(slide, dict):
            errors.append(f"{context} must be an object")
            continue
        errors.extend(
            require_fields(
                slide,
                ["slide_id", "student_title", "purpose", "content_blocks", "interaction"],
                context,
            )
        )
        slide_ids.append(slide.get("slide_id"))
        if slide.get("student_title") in INTERNAL_SLIDE_TITLES:
            errors.append(
                f"{context} exposes internal planning label "
                f"{slide.get('student_title')!r}"
            )
    if len(slide_ids) != len(set(slide_ids)):
        errors.append("slide_id values must be unique")
    if not slides or "미션" not in str(slides[0].get("student_title", "")):
        errors.append("student deck must begin with a mission-first slide")
    if not any(
        slide.get("interaction") == "roleplay"
        or "독립" in str(slide.get("purpose", ""))
        for slide in slides
        if isinstance(slide, dict)
    ):
        errors.append("student deck requires independent speech or roleplay")
    if "blueprint" in artifacts:
        _compare(
            errors,
            "deck vocabulary scope",
            artifacts["blueprint"].get("vocabulary_scope"),
            deck.get("vocabulary_scope"),
        )
    return errors


def _validate_followup(artifacts: dict[str, dict]) -> list[str]:
    if "weekly_pack" not in artifacts:
        return []
    pack = artifacts["weekly_pack"]
    scope = pack.get("followup_scope")
    errors: list[str] = []
    if scope not in {"homework_only", "full_followup"}:
        return [f"invalid followup_scope {scope!r}"]

    for name in ["homework", "quizlet", "message"]:
        if name in artifacts and artifacts[name].get("followup_scope") != scope:
            errors.append(f"{name} followup_scope does not match weekly pack")

    if scope == "homework_only":
        if pack.get("source_next_lesson_decision_lock") is not None:
            errors.append(
                "homework_only requires source_next_lesson_decision_lock == null"
            )
        if pack.get("next_lesson_check_ref") is not None:
            errors.append("homework_only requires next_lesson_check_ref == null")
        if "next_check" in artifacts:
            errors.append("homework_only forbids a next lesson check artifact")
        return errors

    if not pack.get("source_next_lesson_decision_lock") or "next_lock" not in artifacts:
        errors.append("full_followup requires a valid next lesson decision lock")
    if not pack.get("next_lesson_check_ref") or "next_check" not in artifacts:
        errors.append("full_followup requires a valid next_lesson_check_ref")
    if {"next_lock", "next_check"}.issubset(artifacts):
        next_lock = artifacts["next_lock"]
        next_check = artifacts["next_check"]
        _compare(
            errors,
            "next lesson selected direction",
            next_lock.get("selected_direction", {}).get("mode"),
            next_check.get("selected_direction"),
        )
        _compare(
            errors,
            "next lesson situation",
            next_lock.get("selected_direction", {}).get("primary_situation"),
            next_check.get("suggested_next_situation"),
        )
        _compare(
            errors,
            "prior target treatment",
            next_lock.get("prior_targets"),
            next_check.get("prior_target_treatments"),
        )
    return errors


def _privacy_errors(golden: Path) -> list[str]:
    errors: list[str] = []
    for path in golden.rglob("*.md"):
        content = path.read_text(encoding="utf-8").lower()
        for pattern in PRIVATE_PATTERNS:
            if pattern in content:
                errors.append(
                    f"{path.relative_to(golden)} contains private marker {pattern}"
                )
    return errors


def collect_golden_errors(golden: Path = GOLDEN) -> list[str]:
    artifacts, errors = _load_artifacts(golden)
    errors.extend(_validate_required_fields(artifacts))
    errors.extend(_validate_semantics(artifacts))
    errors.extend(_validate_references(golden, artifacts))
    errors.extend(_validate_lock_to_progression(artifacts))
    errors.extend(_validate_progression_to_blueprint(artifacts))
    errors.extend(_validate_blueprint_to_practice(artifacts))
    errors.extend(_validate_deck(artifacts))
    errors.extend(_validate_followup(artifacts))
    errors.extend(_privacy_errors(golden))
    return errors


def build_assessment_data(golden: Path = GOLDEN) -> dict:
    artifacts, load_errors = _load_artifacts(golden)
    errors = load_errors + collect_golden_errors(golden)
    errors = list(dict.fromkeys(errors))
    lesson_lock_valid = (
        "lesson_lock" in artifacts
        and validate_lesson_scope_lock(artifacts["lesson_lock"]) == []
    )
    next_scope = artifacts.get("weekly_pack", {}).get("followup_scope")
    next_lock_valid = (
        True
        if next_scope == "homework_only"
        else "next_lock" in artifacts
        and validate_next_lesson_decision_lock(artifacts["next_lock"]) == []
    )
    overrides_preserved = False
    if {"lesson_lock", "progression", "blueprint", "practice"}.issubset(artifacts):
        expected = artifacts["lesson_lock"].get("teacher_overrides", [])
        overrides_preserved = all(
            artifacts[name].get("teacher_overrides_applied") == expected
            for name in ["progression", "blueprint", "practice"]
        )
    followup_errors = _validate_followup(artifacts)
    privacy_errors = _privacy_errors(golden)

    reviewed = [
        rel
        for name, rel in ARTIFACTS.items()
        if name != "assessment" and (golden / rel).is_file()
    ]
    return {
        "assessment_report_id": "cafe-assessment-001",
        "reviewed_artifacts": reviewed,
        "overall_status": "pass" if not errors else "blocked",
        "findings": [
            {
                "severity": "blocker",
                "artifact": "golden/conversational_cafe",
                "issue": error,
                "evidence": "computed by semantic and cross-artifact validators",
                "required_fix": "align the fixture with its controlling contract",
            }
            for error in errors
        ],
        "contract_checks": {
            "passed": CONTRACT_CHECK_NAMES if not errors else [],
            "failed": errors,
        },
        "learning_checks": {
            "passed": [
                "situation-led",
                "grammar-and-vocabulary tracked",
                "teacher-approved progression",
            ]
            if not errors
            else [],
            "failed": [],
        },
        "approval_checks": {
            "lesson_scope_lock_valid": lesson_lock_valid,
            "teacher_overrides_preserved": overrides_preserved,
            "followup_scope_valid": not followup_errors,
            "next_lesson_decision_lock_valid": next_lock_valid,
        },
        "privacy_checks": {
            "passed": ["synthetic data only"] if not privacy_errors else [],
            "failed": privacy_errors,
        },
    }


def _validate_assessment_report(
    golden: Path,
    artifacts: dict[str, dict],
) -> list[str]:
    expected = build_assessment_data(golden)
    report = artifacts.get("assessment")
    if report is None:
        return ["assessment report is missing or unparseable"]
    errors: list[str] = []
    for field in [
        "overall_status",
        "contract_checks",
        "approval_checks",
        "privacy_checks",
    ]:
        if report.get(field) != expected.get(field):
            errors.append(
                f"assessment report {field} does not match computed result"
            )
    return errors


def validate_golden_run(
    golden: Path = GOLDEN,
    *,
    check_assessment: bool = True,
) -> list[str]:
    errors = collect_golden_errors(golden)
    if check_assessment:
        artifacts, assessment_load_errors = _load_artifacts(
            golden,
            include_assessment=True,
        )
        errors.extend(assessment_load_errors)
        errors.extend(_validate_references(golden, artifacts))
        errors.extend(_validate_assessment_report(golden, artifacts))
    return list(dict.fromkeys(errors))


def main() -> None:
    errors = validate_golden_run()
    if errors:
        print("FAIL: Golden run validation failed")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("PASS: Golden conversational cafe run is valid")


if __name__ == "__main__":
    main()
