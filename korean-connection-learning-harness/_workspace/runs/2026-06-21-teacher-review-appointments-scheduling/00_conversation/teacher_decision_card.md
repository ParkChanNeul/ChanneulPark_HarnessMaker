# Teacher Decision Card: Appointment Change Vertical Slice

```yaml
{
  "decision_card_id": "teacher-card-2026-06-21-appointments",
  "source_intake_state": "user-approved direction plus 2026-06-14 clinic/pharmacy read-only evidence",
  "teacher_facts": [
    "Default duration is 90 minutes; supported range is 60–120 minutes.",
    "Primary situation is appointments_scheduling: reschedule, cancel, confirm_time.",
    "Transfer situation is messaging_calls: open, request, close.",
    "The lesson promise is to state a short physical condition, change or cancel an appointment, and confirm a new time.",
    "The vocabulary selection is manual and remains proposed.",
    "No final lesson materials or HTML may be created before teacher review."
  ],
  "agent_interpretations": [
    "The prior clinic/pharmacy lesson exposed short symptom, time, request, and confirmation language, but did not establish live mastery.",
    "The new lesson should move from a health-state opener into appointment adjustment without repeating clinic vocabulary drills.",
    "interaction_adjust_appointment is A2 metadata, so production should stay inside a short fixed chain and bounded roleplay.",
    "The apology line 갑자기 연락해서 죄송합니다 can be practiced as a fixed interactional chunk while grammar_reason_eoseo remains deferred."
  ],
  "teaching_problem": {
    "summary": "Move from a short reason statement to a polite appointment change, cancellation, or time confirmation without overloading the learner with explanation grammar.",
    "evidence": [
      "Previous materials exposed 아파요, 오늘 아침부터요, V-아/어 주세요, and short confirmation behavior.",
      "No live learner result confirms independent retrieval or transfer.",
      "The proposed target set contains one new grammar target and several interaction targets."
    ],
    "confidence": "high"
  },
  "options": [
    {
      "option_id": "A_90_CORE",
      "mode": "mixed",
      "situation_scope": {
        "pack_ref": "appointments_scheduling",
        "sub_situation_ids": [
          "reschedule",
          "cancel",
          "confirm_time"
        ]
      },
      "candidate_language_targets": [
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
      "benefits": [
        "Uses the previous short health-state language as a bridge instead of reteaching clinic content.",
        "Keeps the core mission visible through reschedule, cancel, and confirm_time practice.",
        "Allows a messaging/call transfer without adding a second primary situation."
      ],
      "risks": [
        "Ten in-class new items may be dense in the 60-minute version.",
        "interaction_adjust_appointment is above the learner's A1 band and requires chunk-level scaffolding.",
        "The fixed apology line contains -아서, which could accidentally pull deferred reason grammar into the core lesson."
      ]
    }
  ],
  "recommendation": {
    "option_id": "A_90_CORE",
    "rationale": "Use 90 minutes as the default, keep grammar_reason_eoseo deferred, and let 60/120 minutes compress or extend practice without changing the approved core chain.",
    "limitations": [
      "This is a review proposal, not teacher approval.",
      "No learner performance evidence exists after the previous lesson.",
      "The transfer pack appears only in the preview until the teacher approves the scope."
    ]
  },
  "required_teacher_decisions": [
    "Approve or revise the 90-minute default and the 60/120-minute variants.",
    "Approve or revise 6 productive, 4 receptive, 4 review, and 2 homework items.",
    "Confirm whether 내일 can remain review despite no visible prior exposure evidence.",
    "Confirm grammar_reason_eoseo stays deferred except for an optional 120-minute extension.",
    "Confirm 갑자기 연락해서 죄송합니다 is taught as a fixed apology chunk, not a reason-grammar lesson.",
    "Approve messaging_calls as the transfer situation."
  ],
  "assumption_candidates": [
    {
      "field": "learner level",
      "proposed_value": "A1",
      "reason": "Previous learner snapshot labels the learner A1."
    },
    {
      "field": "material scope after approval",
      "proposed_value": "student deck later; no HTML in this review run",
      "reason": "The current request stops at Teacher Review."
    }
  ],
  "scope_status": "partial",
  "advisory_inputs": [
    "00_previous_lesson_snapshot.md",
    "01_lesson_vocabulary_set.md",
    "02_vertical_slice_preview.md",
    "Canonical target records extracted by requested IDs only.",
    "Canonical situation records extracted for clinic_pharmacy, appointments_scheduling, and messaging_calls only."
  ]
}
```

## Review Status

강사 검토 대기. 이 Card는 추천이며 승인 권한을 갖지 않는다.
