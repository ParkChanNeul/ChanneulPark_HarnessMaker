# Contract: Progression Plan

## Purpose

Structures teacher-approved progression while preserving long-term grammar, vocabulary, situation, and conversation development.

## Producer

`kc_learning_progression_planner`.

## Consumers

`kc_lesson_architect`, `kc_practice_designer`, `kc_assessment_reviewer`.

## Required Fields

```yaml
progression_plan_id: "unique id"
lesson_scope_lock_ref: "path or id"
learner_alias: "non-identifying handle"
planning_window: "next lesson | week | month | module"
situation_scope:
  pack_ref: "canonical situation pack id"
  sub_situation_ids: []
approved_mode: "advance | review | mixed | vocabulary_focus | listening_focus | conversation_focus | diagnostic"
language_targets:
  - target_ref: "canonical language target id"
    treatment: "new | review | retrieval | transfer | practice | carrier | defer"
vocabulary_scope:
  target_pack: ""
  lesson_vocabulary_set_ref: null
  in_class_new_item_count: 0
  productive_core_count: 0
  receptive_support_count: 0
  review_item_ids: []
  homework_expansion_count: 0
teacher_overrides_applied: []
blocked_targets: []
spiral_review_plan: []
next_lesson_rationale: "why this approved lesson now"
```

## Validation

The plan must exactly match the controlling lock's canonical `situation_scope`, `language_targets`, and normalized vocabulary scope. Review may be absent when the teacher explicitly excludes it; prior targets may instead be carrier, retrieval, transfer, or defer.
