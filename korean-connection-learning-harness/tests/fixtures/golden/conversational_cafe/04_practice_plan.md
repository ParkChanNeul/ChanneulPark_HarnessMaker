# Practice Plan

```yaml
{
  "practice_plan_id": "cafe-practice-001",
  "lesson_scope_lock_ref": "00_conversation/lesson_scope_lock.md",
  "source_blueprint": "03_lesson_blueprint.md",
  "vocabulary_scope": {
    "target_pack": "cafe_core",
    "lesson_vocabulary_set_ref": null,
    "in_class_new_item_count": 10,
    "productive_core_count": 6,
    "receptive_support_count": 4,
    "review_item_ids": [],
    "homework_expansion_count": 2
  },
  "practice_ladder": {
    "controlled": [
      {
        "task_id": "controlled-menu-001",
        "type": "controlled",
        "targets": [
          "iyo_order"
        ],
        "prompt": "메뉴를 보고 N-(이)요로 고르기"
      }
    ],
    "guided": [
      {
        "task_id": "guided-order-001",
        "type": "guided",
        "targets": [
          "request_juseyo",
          "listen_answer_confirm"
        ],
        "prompt": "메뉴와 직원 질문 카드를 보고 주문 조합하기"
      }
    ],
    "independent": [
      {
        "task_id": "independent-roleplay-001",
        "type": "roleplay",
        "targets": [
          "request_juseyo",
          "listen_answer_confirm"
        ],
        "prompt": "메뉴 도움 없이 주문하고 직원 질문에 답하기"
      }
    ],
    "transfer": [
      {
        "task_id": "transfer-takeout-001",
        "type": "transfer",
        "targets": [
          "request_juseyo_to_takeout"
        ],
        "prompt": "포장 주문으로 바꾸어 요청하기"
      }
    ]
  },
  "retrieval_prompts": [
    {
      "prompt_id": "retrieval-polite-001",
      "targets": [
        "polite_yo"
      ],
      "prompt": "존댓말 짧은 답을 모델 없이 말하기"
    }
  ],
  "roleplay_variations": [
    "매장",
    "포장"
  ],
  "error_repair_prompts": [
    "다시 말씀해 주세요"
  ],
  "homework_seed": [
    "직원 질문 듣고 답하기"
  ],
  "quizlet_seed": [
    "메뉴와 Q&A"
  ],
  "evidence_capture_points": [
    "독립 주문",
    "질문 응답",
    "포장 주문 전이"
  ],
  "teacher_overrides_applied": []
}
```
