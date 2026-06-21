# Lesson Scope Lock: Appointment Change Proposal

```yaml
{
  "lesson_scope_lock_id": "lesson-scope-2026-06-21-appointments",
  "revision": 1,
  "supersedes": null,
  "lock_status": "partial",
  "approved_by_teacher": false,
  "approval_evidence": "",
  "learner": {
    "alias": "kc_reference_learner",
    "level": "A1",
    "learner_context_ref": "../00_previous_lesson_snapshot.md"
  },
  "lesson": {
    "mode": "mixed",
    "duration_minutes": 90,
    "situation_scope": {
      "pack_ref": "appointments_scheduling",
      "sub_situation_ids": [
        "reschedule",
        "cancel",
        "confirm_time"
      ]
    },
    "lesson_promise": "몸 상태를 짧게 말하고 예약이나 약속을 변경 또는 취소한 뒤 새로운 시간을 확인할 수 있다."
  },
  "language_targets": [
    {
      "target_ref": "grammar_want_go_sipeoyo",
      "treatment": "new"
    },
    {
      "target_ref": "grammar_request_verb_eo_juseyo",
      "treatment": "review"
    },
    {
      "target_ref": "register_haeyo_polite",
      "treatment": "retrieval"
    },
    {
      "target_ref": "interaction_adjust_appointment",
      "treatment": "practice"
    },
    {
      "target_ref": "interaction_apologize",
      "treatment": "practice"
    },
    {
      "target_ref": "interaction_confirm_and_answer",
      "treatment": "practice"
    },
    {
      "target_ref": "grammar_reason_eoseo",
      "treatment": "defer"
    }
  ],
  "vocabulary_scope": {
    "target_pack": "appointments_reschedule_manual_v1",
    "lesson_vocabulary_set_ref": "../01_lesson_vocabulary_set.md",
    "in_class_new_item_count": 10,
    "productive_core_count": 6,
    "receptive_support_count": 4,
    "review_item_ids": [
      "review-apheuda",
      "review-oneul",
      "review-naeil",
      "review-achim"
    ],
    "homework_expansion_count": 2
  },
  "material_scope": {
    "student_deck": false,
    "html": false,
    "mobile_cheat_sheet": false,
    "homework": false,
    "quizlet_plan": false
  },
  "teacher_overrides": [
    {
      "rule": "default lesson duration",
      "decision": "90 minutes with documented 60-minute compression and 120-minute extension",
      "rationale": "The user fixed the default and supported range for this review slice."
    },
    {
      "rule": "reason grammar in the core lesson",
      "decision": "Keep grammar_reason_eoseo deferred in 60/90 minutes.",
      "rationale": "Use 몸이 안 좋아요. 예약을 바꾸고 싶어요. as two short sentences before any reason-chain extension."
    },
    {
      "rule": "current artifact production gate",
      "decision": "Stop after scope, proposed vocabulary, and vertical slice preview.",
      "rationale": "Teacher approval is required before final plans or student materials."
    }
  ],
  "assumption_locks": [

  ],
  "unresolved_blockers": [
    "Teacher has not approved the lesson duration variant.",
    "Teacher has not approved the vocabulary set.",
    "Teacher has not confirmed 내일 as review.",
    "Teacher has not approved messaging_calls transfer.",
    "Teacher has not approved the fixed apology chunk treatment."
  ],
  "created_artifact_refs": [
    "teacher_decision_card.md",
    "../00_previous_lesson_snapshot.md",
    "../01_lesson_vocabulary_set.md",
    "../02_vertical_slice_preview.md"
  ]
}
```

## Gate Status

`partial`. `build_lesson`, final Progression Plan, Lesson Blueprint, Practice Plan, Student Deck, and HTML rendering remain blocked.
