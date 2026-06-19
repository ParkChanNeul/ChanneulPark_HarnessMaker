# Practice Plan

```yaml
{
  "practice_plan_id": "cafe-practice-001",
  "lesson_scope_lock_ref": "00_conversation/lesson_scope_lock.md",
  "source_blueprint": "03_lesson_blueprint.md",
  "situation_scope": {
    "pack_ref": "cafe_ordering",
    "sub_situation_ids": [
      "order_item",
      "answer_staff_question",
      "request_takeout"
    ]
  },
  "language_targets": [
    {
      "target_ref": "chunk_request_noun_juseyo",
      "treatment": "new"
    },
    {
      "target_ref": "discourse_short_noun_iyo",
      "treatment": "review"
    },
    {
      "target_ref": "register_haeyo_polite",
      "treatment": "retrieval"
    },
    {
      "target_ref": "grammar_request_verb_eo_juseyo",
      "treatment": "transfer"
    },
    {
      "target_ref": "interaction_confirm_and_answer",
      "treatment": "practice"
    }
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
  "practice_ladder": {
    "controlled": [
      {
        "task_id": "controlled-menu-001",
        "type": "controlled",
        "language_targets": [
          {
            "target_ref": "discourse_short_noun_iyo",
            "treatment": "practice"
          }
        ],
        "prompt": "메뉴를 보고 N-(이)요로 고르기",
        "examples": [
          "아메리카노요.",
          "라테요."
        ]
      }
    ],
    "guided": [
      {
        "task_id": "guided-order-001",
        "type": "guided",
        "language_targets": [
          {
            "target_ref": "chunk_request_noun_juseyo",
            "treatment": "practice"
          },
          {
            "target_ref": "interaction_confirm_and_answer",
            "treatment": "practice"
          }
        ],
        "prompt": "메뉴와 직원 질문 카드를 보고 주문 조합하기",
        "examples": [
          "아메리카노 주세요.",
          "네, 맞아요."
        ]
      }
    ],
    "independent": [
      {
        "task_id": "independent-roleplay-001",
        "type": "roleplay",
        "language_targets": [
          {
            "target_ref": "chunk_request_noun_juseyo",
            "treatment": "practice"
          },
          {
            "target_ref": "interaction_confirm_and_answer",
            "treatment": "practice"
          }
        ],
        "prompt": "메뉴 도움 없이 주문하고 직원 질문에 답하기",
        "examples": [
          "라테 한 잔 주세요.",
          "네, 포장이에요."
        ]
      }
    ],
    "transfer": [
      {
        "task_id": "transfer-takeout-001",
        "type": "transfer",
        "language_targets": [
          {
            "target_ref": "grammar_request_verb_eo_juseyo",
            "treatment": "practice"
          }
        ],
        "prompt": "포장해 주세요, 데워 주세요, 빼 주세요, 넣어 주세요 중 알맞은 동사 요청을 사용한다.",
        "examples": [
          "포장해 주세요.",
          "데워 주세요.",
          "얼음은 빼 주세요.",
          "시럽은 넣어 주세요."
        ]
      }
    ]
  },
  "retrieval_prompts": [
    {
      "prompt_id": "retrieval-polite-001",
      "language_targets": [
        {
          "target_ref": "register_haeyo_polite",
          "treatment": "practice"
        }
      ],
      "prompt": "존댓말 짧은 답을 모델 없이 말하기",
      "examples": [
        "네, 맞아요.",
        "아니요, 괜찮아요."
      ]
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
