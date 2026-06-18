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
primary_situation: "situation id"
approved_mode: "advance | review | mixed | vocabulary_focus | listening_focus | conversation_focus | diagnostic"
new_target_candidates: []
review_targets: []
retrieval_targets: []
transfer_targets: []
conversation_skill_targets: []
vocabulary_scope: {}
teacher_overrides_applied: []
blocked_targets: []
spiral_review_plan: []
next_lesson_rationale: "why this approved lesson now"
```

## Validation

The plan must match the controlling lock. Review may be empty when the teacher explicitly excludes separate review; prior targets may instead be carrier, retrieval, transfer, or defer.
