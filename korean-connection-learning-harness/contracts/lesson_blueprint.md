# Contract: Lesson Blueprint

## Purpose

Operationalizes an approved lesson scope before material design.

## Producer

`kc_lesson_architect`.

## Consumers

`kc_practice_designer`, `kc_student_experience_designer`, `kc_assessment_reviewer`.

## Required Fields

```yaml
lesson_blueprint_id: "unique id"
lesson_scope_lock_ref: "path or id"
source_progression_plan: "path or id"
lesson_title: "student-safe title"
learner_alias: "non-identifying handle"
situation_scope:
  pack_ref: "canonical situation pack id"
  sub_situation_ids: []
lesson_promise: "approved learner action"
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
culture_point: {}
lesson_flow: []
assessment_evidence_to_collect: []
override_reason: null
```

## Validation

Canonical `language_targets`, `situation_scope`, normalized vocabulary scope, lesson promise, and overrides must match the lock and progression plan. The architect cannot select replacement targets.
