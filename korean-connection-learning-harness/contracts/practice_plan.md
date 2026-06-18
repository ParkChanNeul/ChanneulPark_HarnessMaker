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
      targets: []
      prompt: ""
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

Practice must preserve the lock, normalized vocabulary scope, and target IDs. Every new target must appear in a practice task, every review target must appear in practice or retrieval, every transfer target must appear in a transfer task, and every conversation target must appear in guided, independent, or role-play practice. Independent production and transfer remain required unless the approved scope is diagnostic-only.
