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
situation: "primary situation"
lesson_promise: "approved learner action"
new_targets: []
review_targets: []
retrieval_targets: []
transfer_targets: []
conversation_skill_targets: []
vocabulary_scope: {}
teacher_overrides_applied: []
culture_point: {}
lesson_flow: []
assessment_evidence_to_collect: []
override_reason: null
```

## Validation

Targets, vocabulary, mode, and overrides must match the lock and progression plan. The architect cannot select replacement targets.
