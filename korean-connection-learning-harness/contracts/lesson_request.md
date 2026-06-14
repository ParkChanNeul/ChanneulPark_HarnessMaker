# Contract: Lesson Request

## Purpose

Starts a lesson or material-generation run.

## Producer

Parent agent or user.

## Consumers

`kc_learner_state_analyst`, `kc_learning_progression_planner`, `kc_lesson_architect`.

## Required Fields

```yaml
request_id: "unique id"
mode: "build_lesson | render_materials | post_lesson_followup | review_outputs | partial_rerun"
learner_alias: "non-identifying handle"
lesson_goal: "communicative goal"
target_situation: "situation id or label"
time_box_minutes: 30
known_inputs:
  learner_context_snapshot: "path or null"
  lesson_result: "path or null"
  progression_plan: "path or null"
constraints:
  - "specific limit or preference"
```

## Validation

The request must not contain private learner-identifying details. Missing learner evidence must be marked `unknown`, not invented.
