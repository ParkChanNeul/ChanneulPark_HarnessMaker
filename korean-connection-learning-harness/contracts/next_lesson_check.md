# Contract: Next Lesson Check

## Purpose

Creates the handoff from the current lesson to the next lesson.

## Producer

`kc_learning_followup_teacher` or `kc_assessment_reviewer`.

## Consumers

`kc_learner_state_analyst`, `kc_learning_progression_planner`, parent agent.

## Required Fields

```yaml
next_lesson_check_id: "unique id"
source_lesson_result: "path or id"
must_review: []
should_transfer: []
learner_question_to_revisit: []
mission_result_to_check: []
risk_if_ignored: []
suggested_next_situation: "situation id or unknown"
```

## Validation

Must contain at least one concrete next action unless the course is complete.
