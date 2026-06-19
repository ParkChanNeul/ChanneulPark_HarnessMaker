# Contract: Next Lesson Check

## Purpose

Creates the approved handoff from the current lesson to the next lesson.

## Producer

`kc_learning_followup_teacher` or `kc_assessment_reviewer`.

## Consumers

`kc_learner_state_analyst`, `kc_learning_progression_planner`, parent agent.

## Required Fields

```yaml
next_lesson_check_id: "unique id"
source_lesson_result: "path or id"
source_next_lesson_decision_lock: "path or id"
selected_direction: "approved mode"
situation_scope:
  pack_ref: "canonical situation pack id"
  sub_situation_ids: []
language_targets:
  - target_ref: "canonical language target id"
    treatment: "new | review | retrieval | transfer | practice | carrier | defer"
must_review: []
should_transfer: []
learner_question_to_revisit: []
mission_result_to_check: []
risk_if_ignored: []
```

## Validation

This contract is forbidden in homework-only scope and its canonical `situation_scope` and `language_targets` must match a locked next-lesson decision.
