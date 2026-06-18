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
practice_ladder: {controlled: [], guided: [], independent: [], transfer: []}
retrieval_prompts: []
roleplay_variations: []
error_repair_prompts: []
homework_seed: []
quizlet_seed: []
evidence_capture_points: []
teacher_overrides_applied: []
```

## Validation

Practice must preserve the lock and include independent production and transfer unless the approved scope is diagnostic-only.
