# Post-Lesson Teacher Card

```yaml
{
  "post_lesson_teacher_card_id": "cafe-post-card-001",
  "source_lesson_result": "../06_lesson_result.md",
  "teacher_observations": [
    "10개 중 7개를 독립적으로 말함",
    "직원 질문에서 반응이 느림"
  ],
  "observed_successes": [
    "주문 표현 독립 생산"
  ],
  "observed_breakdowns": [
    "후속 질문 듣기와 즉답"
  ],
  "evidence_gaps": [
    "지연 회상"
  ],
  "state_update_candidates": [
    "chunk_request_noun_juseyo independent 후보"
  ],
  "homework_options": [
    {
      "option_id": "A",
      "estimated_minutes": 8,
      "focus": "듣고 짧게 답하기",
      "reason": "관찰된 breakdown"
    }
  ],
  "next_lesson_options": [
    {
      "option_id": "B",
      "mode": "advance",
      "situation_scope": {
        "pack_ref": "preferences_opinions",
        "sub_situation_ids": [
          "talk_about_hobbies"
        ]
      },
      "candidate_language_targets": [
        {
          "target_ref": "grammar_want_go_sipeoyo",
          "treatment": "new"
        },
        {
          "target_ref": "chunk_request_noun_juseyo",
          "treatment": "carrier"
        },
        {
          "target_ref": "interaction_confirm_and_answer",
          "treatment": "review"
        }
      ],
      "reason": "강사가 새 진도를 선호",
      "risk": "듣기 repair를 carrier와 retrieval로 유지해야 함"
    }
  ],
  "recommendation": {
    "homework_option": "A",
    "next_lesson_option": "B",
    "rationale": "짧은 듣기 숙제 후 새 진도 가능"
  },
  "teacher_approval": {
    "homework_approved": true,
    "homework_option": "A",
    "approval_evidence": "A 숙제로 진행해 주세요."
  },
  "required_teacher_decisions": [
    "next lesson direction"
  ],
  "status": "partial"
}
```
