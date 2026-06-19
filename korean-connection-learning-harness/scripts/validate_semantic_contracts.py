#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from structured_artifacts import (
    StructuredArtifactError,
    extract_structured_block,
    require_fields,
)


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "fixtures" / "golden" / "conversational_cafe"

CONVERSATION_STATES = {"open", "partial", "ready_to_lock", "locked"}
SCOPE_STATUSES = {"open", "partial", "ready_to_lock"}
LOCK_STATUSES = {"open", "partial", "locked"}
LESSON_MODES = {
    "advance",
    "review",
    "mixed",
    "vocabulary_focus",
    "listening_focus",
    "conversation_focus",
    "diagnostic",
}
NEXT_LESSON_MODES = {
    "advance",
    "review",
    "mixed",
    "transfer",
    "vocabulary_focus",
    "listening_repair",
    "conversation_repair",
}
PRIOR_TARGET_TREATMENTS = {
    "new",
    "review",
    "retrieval",
    "transfer",
    "practice",
    "carrier",
    "defer",
}
LANGUAGE_TARGET_TREATMENTS = PRIOR_TARGET_TREATMENTS
LEGACY_TARGET_FIELDS = {
    "targets",
    "approved_new_grammar",
    "approved_review_grammar",
    "approved_new_targets",
    "approved_review_targets",
    "new_grammar_candidates",
    "new_target_candidates",
    "review_candidates",
    "review_targets",
    "retrieval_targets",
    "transfer_targets",
    "conversation_targets",
    "conversation_skill_targets",
    "planned_targets",
}
LEGACY_SITUATION_FIELDS = {
    "primary_situation",
    "target_situation",
    "situation",
    "pack_id",
}

VOCABULARY_FIELDS = [
    "target_pack",
    "lesson_vocabulary_set_ref",
    "in_class_new_item_count",
    "productive_core_count",
    "receptive_support_count",
    "review_item_ids",
    "homework_expansion_count",
]
VOCABULARY_DIRECTION_FIELDS = VOCABULARY_FIELDS + ["carrier_item_ids"]
LEGACY_VOCABULARY_FIELDS = {
    "vocabulary_count",
    "in_class_new_items",
    "productive_core",
    "receptive_support",
    "review_items",
    "homework_expansion",
    "new_item_count",
    "new_pack",
    "new_item_target",
    "carrier_items",
    "homework_expansion_target",
}

INTAKE_FIELDS = [
    "run_id",
    "conversation_state",
    "teacher_request",
    "known_context",
    "unknowns",
    "workspace",
]
TEACHER_CARD_FIELDS = [
    "decision_card_id",
    "source_intake_state",
    "teacher_facts",
    "agent_interpretations",
    "teaching_problem",
    "options",
    "recommendation",
    "required_teacher_decisions",
    "assumption_candidates",
    "scope_status",
    "advisory_inputs",
]
LESSON_LOCK_FIELDS = [
    "lesson_scope_lock_id",
    "revision",
    "supersedes",
    "lock_status",
    "approved_by_teacher",
    "approval_evidence",
    "learner",
    "lesson",
    "language_targets",
    "vocabulary_scope",
    "material_scope",
    "teacher_overrides",
    "assumption_locks",
    "unresolved_blockers",
    "created_artifact_refs",
]
POST_LESSON_FIELDS = [
    "post_lesson_teacher_card_id",
    "source_lesson_result",
    "teacher_observations",
    "observed_successes",
    "observed_breakdowns",
    "evidence_gaps",
    "state_update_candidates",
    "homework_options",
    "next_lesson_options",
    "recommendation",
    "teacher_approval",
    "required_teacher_decisions",
    "status",
]
NEXT_LOCK_FIELDS = [
    "next_lesson_decision_lock_id",
    "revision",
    "supersedes",
    "source_post_lesson_card",
    "lock_status",
    "approved_by_teacher",
    "approval_evidence",
    "selected_direction",
    "language_targets",
    "vocabulary_direction",
    "homework_scope",
    "next_lesson_check",
    "teacher_notes",
    "unresolved_blockers",
]


def validate_language_targets(
    targets: Any,
    context: str,
) -> list[str]:
    if not isinstance(targets, list):
        return [f"{context}: language targets must be an array"]

    errors: list[str] = []
    seen: set[str] = set()
    for index, target in enumerate(targets):
        target_context = f"{context}[{index}]"
        if not isinstance(target, dict):
            errors.append(f"{target_context}: target must be an object")
            continue
        errors.extend(
            require_fields(target, ["target_ref", "treatment"], target_context)
        )
        unexpected = sorted(set(target) - {"target_ref", "treatment"})
        if unexpected:
            errors.append(
                f"{target_context}: unexpected fields {', '.join(unexpected)}"
            )
        target_ref = target.get("target_ref")
        if not isinstance(target_ref, str) or not target_ref.strip():
            errors.append(f"{target_context}: target_ref must be non-empty")
        elif target_ref in seen:
            errors.append(
                f"{context}: target {target_ref!r} cannot have multiple treatments"
            )
        else:
            seen.add(target_ref)
        treatment = target.get("treatment")
        if treatment not in LANGUAGE_TARGET_TREATMENTS:
            errors.append(f"{target_context}: invalid treatment {treatment!r}")
    return errors


def validate_situation_scope(scope: Any, context: str) -> list[str]:
    if not isinstance(scope, dict):
        return [f"{context}: situation_scope must be an object"]
    errors = require_fields(scope, ["pack_ref", "sub_situation_ids"], context)
    unexpected = sorted(set(scope) - {"pack_ref", "sub_situation_ids"})
    if unexpected:
        errors.append(f"{context}: unexpected fields {', '.join(unexpected)}")
    if not isinstance(scope.get("pack_ref"), str) or not scope.get(
        "pack_ref", ""
    ).strip():
        errors.append(f"{context}: pack_ref must be non-empty")
    sub_situations = scope.get("sub_situation_ids")
    if not isinstance(sub_situations, list) or not all(
        isinstance(item, str) and item.strip() for item in sub_situations
    ):
        errors.append(f"{context}: sub_situation_ids must be an array of strings")
    elif len(sub_situations) != len(set(sub_situations)):
        errors.append(f"{context}: sub_situation_ids must be unique")
    return errors


def reject_legacy_fields(data: Any, context: str) -> list[str]:
    if not isinstance(data, dict):
        return []
    errors: list[str] = []
    for field in sorted(LEGACY_TARGET_FIELDS.intersection(data)):
        errors.append(f"{context}: legacy target field {field} is forbidden")
    for field in sorted(LEGACY_SITUATION_FIELDS.intersection(data)):
        errors.append(f"{context}: legacy situation field {field} is forbidden")
    return errors


def _is_non_negative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _has_authority_field(value: Any) -> bool:
    authority_fields = {
        "approved_by_teacher",
        "approval_evidence",
        "lock_status",
        "build_lesson",
        "dispatch_build",
    }
    if isinstance(value, dict):
        if authority_fields.intersection(value):
            return True
        return any(_has_authority_field(item) for item in value.values())
    if isinstance(value, list):
        return any(_has_authority_field(item) for item in value)
    return False


def _has_vocabulary_override(data: dict) -> bool:
    for override in data.get("teacher_overrides", []):
        if not isinstance(override, dict):
            continue
        rule = str(override.get("rule", "")).lower()
        if "vocabulary" in rule and "count" in rule:
            return True
    return False


def validate_vocabulary_scope(
    scope: Any,
    context: str,
    *,
    direction: bool = False,
    allow_count_override: bool = False,
) -> list[str]:
    if not isinstance(scope, dict):
        return [f"{context}: vocabulary scope must be an object"]

    required = VOCABULARY_DIRECTION_FIELDS if direction else VOCABULARY_FIELDS
    errors = require_fields(scope, required, context)
    for field in sorted(LEGACY_VOCABULARY_FIELDS.intersection(scope)):
        errors.append(f"{context}: legacy vocabulary field {field} is forbidden")

    count_fields = [
        "in_class_new_item_count",
        "productive_core_count",
        "receptive_support_count",
        "homework_expansion_count",
    ]
    for field in count_fields:
        if field in scope and not _is_non_negative_integer(scope[field]):
            errors.append(f"{context}: {field} must be a non-negative integer")

    if (
        all(_is_non_negative_integer(scope.get(field)) for field in count_fields[:3])
        and scope["in_class_new_item_count"]
        != scope["productive_core_count"] + scope["receptive_support_count"]
        and not allow_count_override
    ):
        errors.append(
            f"{context}: vocabulary count must equal productive_core_count "
            "+ receptive_support_count"
        )

    for field in ["review_item_ids"] + (["carrier_item_ids"] if direction else []):
        if field in scope and not isinstance(scope[field], list):
            errors.append(f"{context}: {field} must be an array")
    return errors


def validate_lesson_intake_state(data: dict) -> list[str]:
    context = "lesson_intake_state"
    errors = require_fields(data, INTAKE_FIELDS, context)
    state = data.get("conversation_state")
    if state not in CONVERSATION_STATES:
        errors.append(f"{context}: invalid conversation_state {state!r}")
    if state == "locked":
        errors.append(f"{context}: locked state must be created by Lesson Scope Lock")

    workspace = data.get("workspace")
    if not isinstance(workspace, dict):
        errors.append(f"{context}: workspace must be an object")
    else:
        for field in ["read_allowed", "write_allowed"]:
            if not isinstance(workspace.get(field), bool):
                errors.append(f"{context}: workspace.{field} must be boolean")
        if workspace.get("read_allowed") and not workspace.get("run_dir"):
            errors.append(f"{context}: read_allowed requires explicit workspace.run_dir")

    blocking_open = [
        unknown
        for unknown in data.get("unknowns", [])
        if isinstance(unknown, dict)
        and unknown.get("blocking") is True
        and unknown.get("resolution_status") == "open"
    ]
    if blocking_open and state in {"ready_to_lock", "locked"}:
        errors.append(
            f"{context}: blocking unknown cannot remain open in {state} state"
        )
    return errors


def validate_teacher_decision_card(data: dict) -> list[str]:
    context = "teacher_decision_card"
    errors = require_fields(data, TEACHER_CARD_FIELDS, context)
    status = data.get("scope_status")
    if status not in SCOPE_STATUSES:
        errors.append(f"{context}: invalid scope_status {status!r}")
    if status == "ready_to_lock" and data.get("required_teacher_decisions"):
        errors.append(
            f"{context}: ready_to_lock requires empty required_teacher_decisions"
        )

    options = data.get("options", [])
    option_ids: list[Any] = []
    if not isinstance(options, list):
        errors.append(f"{context}: options must be an array")
        options = []
    for index, option in enumerate(options):
        option_context = f"{context}.options[{index}]"
        if not isinstance(option, dict):
            errors.append(f"{option_context}: option must be an object")
            continue
        errors.extend(
            require_fields(
                option,
                [
                    "option_id",
                    "mode",
                    "situation_scope",
                    "candidate_language_targets",
                    "vocabulary_scope",
                    "benefits",
                    "risks",
                ],
                option_context,
            )
        )
        option_ids.append(option.get("option_id"))
        if option.get("mode") not in LESSON_MODES:
            errors.append(f"{option_context}: invalid mode {option.get('mode')!r}")
        errors.extend(reject_legacy_fields(option, option_context))
        errors.extend(
            validate_situation_scope(
                option.get("situation_scope"),
                f"{option_context}.situation_scope",
            )
        )
        errors.extend(
            validate_language_targets(
                option.get("candidate_language_targets"),
                f"{option_context}.candidate_language_targets",
            )
        )
        errors.extend(
            validate_vocabulary_scope(
                option.get("vocabulary_scope"),
                f"{option_context}.vocabulary_scope",
            )
        )

    if len(option_ids) != len(set(option_ids)):
        errors.append(f"{context}: option_id values must be unique")
    recommendation = data.get("recommendation", {})
    recommendation_id = (
        recommendation.get("option_id") if isinstance(recommendation, dict) else None
    )
    if recommendation_id not in option_ids:
        errors.append(
            f"{context}: recommendation.option_id must reference an existing option"
        )
    if _has_authority_field(recommendation):
        errors.append(f"{context}: recommendation cannot contain approval authority")
    if _has_authority_field(data.get("advisory_inputs")):
        errors.append(f"{context}: advisory_inputs cannot contain lock authority")
    return errors


def validate_lesson_scope_lock(data: dict) -> list[str]:
    context = "lesson_scope_lock"
    errors = require_fields(data, LESSON_LOCK_FIELDS, context)
    revision = data.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        errors.append(f"{context}: revision must be an integer >= 1")
    status = data.get("lock_status")
    if status not in LOCK_STATUSES:
        errors.append(f"{context}: invalid lock_status {status!r}")

    lesson = data.get("lesson")
    if not isinstance(lesson, dict):
        errors.append(f"{context}: lesson must be an object")
    else:
        if lesson.get("mode") not in LESSON_MODES:
            errors.append(f"{context}: invalid lesson.mode {lesson.get('mode')!r}")
        duration = lesson.get("duration_minutes")
        if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
            errors.append(f"{context}: lesson.duration_minutes must be positive integer")
        errors.extend(reject_legacy_fields(lesson, f"{context}.lesson"))
        errors.extend(
            validate_situation_scope(
                lesson.get("situation_scope"),
                f"{context}.lesson.situation_scope",
            )
        )

    errors.extend(reject_legacy_fields(data, context))
    errors.extend(
        validate_language_targets(
            data.get("language_targets"),
            f"{context}.language_targets",
        )
    )

    if status == "locked":
        if data.get("approved_by_teacher") is not True:
            errors.append(f"{context}: locked requires approved_by_teacher true")
        if not str(data.get("approval_evidence", "")).strip():
            errors.append(f"{context}: locked requires non-empty approval_evidence")
        if data.get("unresolved_blockers"):
            errors.append(f"{context}: locked requires empty unresolved_blockers")

    errors.extend(
        validate_vocabulary_scope(
            data.get("vocabulary_scope"),
            f"{context}.vocabulary_scope",
            allow_count_override=_has_vocabulary_override(data),
        )
    )
    return errors


def validate_post_lesson_teacher_card(data: dict) -> list[str]:
    context = "post_lesson_teacher_card"
    errors = require_fields(data, POST_LESSON_FIELDS, context)
    status = data.get("status")
    if status not in SCOPE_STATUSES:
        errors.append(f"{context}: invalid status {status!r}")
    errors.extend(reject_legacy_fields(data, context))

    next_options = data.get("next_lesson_options")
    if not isinstance(next_options, list):
        errors.append(f"{context}: next_lesson_options must be an array")
    else:
        for index, option in enumerate(next_options):
            option_context = f"{context}.next_lesson_options[{index}]"
            if not isinstance(option, dict):
                errors.append(f"{option_context}: option must be an object")
                continue
            errors.extend(
                require_fields(
                    option,
                    [
                        "option_id",
                        "mode",
                        "situation_scope",
                        "candidate_language_targets",
                        "reason",
                        "risk",
                    ],
                    option_context,
                )
            )
            if option.get("mode") not in NEXT_LESSON_MODES:
                errors.append(
                    f"{option_context}: invalid mode {option.get('mode')!r}"
                )
            errors.extend(reject_legacy_fields(option, option_context))
            errors.extend(
                validate_situation_scope(
                    option.get("situation_scope"),
                    f"{option_context}.situation_scope",
                )
            )
            errors.extend(
                validate_language_targets(
                    option.get("candidate_language_targets"),
                    f"{option_context}.candidate_language_targets",
                )
            )

    option_ids = {
        option.get("option_id")
        for option in data.get("homework_options", [])
        if isinstance(option, dict)
    }
    approval = data.get("teacher_approval", {})
    if not isinstance(approval, dict):
        errors.append(f"{context}: teacher_approval must be an object")
        return errors
    if approval.get("homework_approved") is True:
        if approval.get("homework_option") not in option_ids:
            errors.append(
                f"{context}: teacher_approval.homework_option must reference "
                "an existing homework option"
            )
        if not str(approval.get("approval_evidence", "")).strip():
            errors.append(
                f"{context}: approved homework requires non-empty approval_evidence"
            )
    if _has_authority_field(
        {
            "recommendation": data.get("recommendation"),
            "next_lesson_options": data.get("next_lesson_options"),
        }
    ):
        errors.append(f"{context}: card cannot approve Next Lesson Lock")
    return errors


def validate_next_lesson_decision_lock(data: dict) -> list[str]:
    context = "next_lesson_decision_lock"
    errors = require_fields(data, NEXT_LOCK_FIELDS, context)
    revision = data.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        errors.append(f"{context}: revision must be an integer >= 1")
    status = data.get("lock_status")
    if status not in LOCK_STATUSES:
        errors.append(f"{context}: invalid lock_status {status!r}")

    direction = data.get("selected_direction")
    if not isinstance(direction, dict):
        errors.append(f"{context}: selected_direction must be an object")
    elif direction.get("mode") not in NEXT_LESSON_MODES:
        errors.append(
            f"{context}: invalid selected_direction.mode {direction.get('mode')!r}"
        )
    else:
        errors.extend(reject_legacy_fields(direction, f"{context}.selected_direction"))
        errors.extend(
            validate_situation_scope(
                direction.get("situation_scope"),
                f"{context}.selected_direction.situation_scope",
            )
        )

    if status == "locked":
        if data.get("approved_by_teacher") is not True:
            errors.append(f"{context}: locked requires approved_by_teacher true")
        if not str(data.get("approval_evidence", "")).strip():
            errors.append(f"{context}: locked requires non-empty approval_evidence")
        if data.get("unresolved_blockers"):
            errors.append(f"{context}: locked requires empty unresolved_blockers")

    errors.extend(reject_legacy_fields(data, context))
    errors.extend(
        validate_language_targets(
            data.get("language_targets"),
            f"{context}.language_targets",
        )
    )

    errors.extend(
        validate_vocabulary_scope(
            data.get("vocabulary_direction"),
            f"{context}.vocabulary_direction",
            direction=True,
        )
    )
    return errors


def validate_golden_conversation(golden: Path = GOLDEN) -> list[str]:
    validators = {
        "lesson_intake_state.md": validate_lesson_intake_state,
        "teacher_decision_card.md": validate_teacher_decision_card,
        "lesson_scope_lock.md": validate_lesson_scope_lock,
        "post_lesson_teacher_card.md": validate_post_lesson_teacher_card,
        "next_lesson_decision_lock.md": validate_next_lesson_decision_lock,
    }
    errors: list[str] = []
    for filename, validator in validators.items():
        path = golden / "00_conversation" / filename
        try:
            data = extract_structured_block(path)
        except (OSError, StructuredArtifactError) as error:
            errors.append(str(error))
            continue
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in validator(data))
    return errors


def main() -> None:
    errors = validate_golden_conversation()
    if errors:
        print("FAIL: semantic contract validation failed")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("PASS: semantic contracts are valid")


if __name__ == "__main__":
    main()
