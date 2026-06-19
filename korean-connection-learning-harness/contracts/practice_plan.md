# Contract: Practice Plan

## Purpose

Turns an approved lesson blueprint into repeated retrieval, production, and transfer practice.

## Producer

`kc_practice_designer`.

## Consumers

`kc_student_experience_designer`, `kc_learning_followup_teacher`, `kc_assessment_reviewer`.

## Required Fields

```yaml
practice_plan_id: "unique id"
lesson_scope_lock_ref: "path or id"
source_blueprint: "path or id"
situation_scope:
  pack_ref: "canonical situation pack id"
  sub_situation_ids: []
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
practice_ladder:
  controlled:
    - task_id: "id"
      type: "controlled"
      language_targets:
        - target_ref: "canonical language target id"
          treatment: "practice"
      prompt: ""
      examples: []
  guided: []
  independent: []
  transfer: []
retrieval_prompts: []
roleplay_variations: []
error_repair_prompts: []
homework_seed: []
quizlet_seed: []
evidence_capture_points: []
teacher_overrides_applied: []
```

## Validation

Practice must preserve the lock, canonical `situation_scope`, canonical `language_targets`, normalized vocabulary scope, and teacher overrides. Task-level target links also use `language_targets`. Every transfer target needs a transfer task with concrete prompt or example evidence, not ID-only coverage. Independent production and transfer remain required unless the approved scope is diagnostic-only.
