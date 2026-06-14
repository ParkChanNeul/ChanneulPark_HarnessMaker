# Contract: Progression Plan

## Purpose

Connects the current lesson to long-term grammar, situation, and conversation development.

## Producer

`kc_learning_progression_planner`.

## Consumers

`kc_lesson_architect`, `kc_practice_designer`, `kc_assessment_reviewer`.

## Required Fields

```yaml
progression_plan_id: "unique id"
learner_alias: "non-identifying handle"
planning_window: "next lesson | week | month | module"
primary_situation: "situation id"
new_target_candidates: []
review_targets: []
retrieval_targets: []
transfer_targets: []
conversation_skill_targets: []
blocked_targets: []
spiral_review_plan: []
next_lesson_rationale: "why this lesson now"
```

## Validation

The plan must include review or retrieval unless the learner is in a first diagnostic lesson.
