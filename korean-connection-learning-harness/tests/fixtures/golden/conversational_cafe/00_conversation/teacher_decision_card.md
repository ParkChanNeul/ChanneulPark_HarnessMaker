# Teacher Decision Card

## 한 줄 진단

학생은 주문 표현을 알고 있지만 직원의 후속 질문에 즉시 반응하는 연습이 필요하다.

```yaml
{
  "decision_card_id": "cafe-card-001",
  "source_intake_state": "lesson_intake_state.md",
  "teacher_facts": [
    "A1",
    "50분",
    "카페 상황"
  ],
  "agent_interpretations": [
    "후속 질문 반응이 핵심 부담일 수 있음"
  ],
  "teaching_problem": {
    "summary": "주문 후 직원 질문에 짧게 답하기",
    "evidence": [
      "강사 요청: order and respond without freezing"
    ],
    "confidence": "medium"
  },
  "options": [
    {
      "option_id": "A",
      "mode": "advance",
      "new_grammar_candidates": [
        "request_juseyo"
      ],
      "review_candidates": [],
      "conversation_targets": [],
      "vocabulary_scope": {
        "target_pack": "cafe_core",
        "lesson_vocabulary_set_ref": null,
        "in_class_new_item_count": 10,
        "productive_core_count": 6,
        "receptive_support_count": 4,
        "review_item_ids": [],
        "homework_expansion_count": 2
      },
      "benefits": [
        "새 표현 확장"
      ],
      "risks": [
        "반응 연습 부족"
      ]
    },
    {
      "option_id": "B",
      "mode": "mixed",
      "new_grammar_candidates": [
        "request_juseyo"
      ],
      "review_candidates": [
        "iyo_order"
      ],
      "conversation_targets": [
        "listen_answer_confirm"
      ],
      "vocabulary_scope": {
        "target_pack": "cafe_core",
        "lesson_vocabulary_set_ref": null,
        "in_class_new_item_count": 10,
        "productive_core_count": 6,
        "receptive_support_count": 4,
        "review_item_ids": [],
        "homework_expansion_count": 2
      },
      "benefits": [
        "주문과 후속 질문을 함께 연습"
      ],
      "risks": [
        "시간 관리 필요"
      ]
    }
  ],
  "recommendation": {
    "option_id": "B",
    "rationale": "후속 질문 대응을 포함할 수 있음",
    "limitations": [
      "실제 수업 관찰 전 추정"
    ]
  },
  "required_teacher_decisions": [],
  "assumption_candidates": [],
  "scope_status": "ready_to_lock",
  "advisory_inputs": []
}
```
