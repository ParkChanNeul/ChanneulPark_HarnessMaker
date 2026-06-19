# Lesson Blueprint

```yaml
{
  "lesson_blueprint_id": "cafe-blueprint-001",
  "lesson_scope_lock_ref": "00_conversation/lesson_scope_lock.md",
  "source_progression_plan": "02_progression_plan.md",
  "lesson_title": "카페에서 주문하고 답하기",
  "learner_alias": "synthetic_cafe_learner",
  "situation_scope": {
    "pack_ref": "cafe_ordering",
    "sub_situation_ids": [
      "order_item",
      "answer_staff_question",
      "request_takeout"
    ]
  },
  "lesson_promise": "주문하고 직원 질문에 짧게 답한다",
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
  "teacher_overrides_applied": [],
  "culture_point": {
    "topic": "짧은 서비스 응답",
    "function": "빠른 흐름에서 자연스러운 답을 설명"
  },
  "lesson_flow": [
    "warmup",
    "model",
    "controlled",
    "guided",
    "roleplay",
    "transfer",
    "wrap"
  ],
  "assessment_evidence_to_collect": [
    "독립 주문",
    "후속 질문 즉답"
  ],
  "override_reason": null
}
```
