# Contract: Weekly Learning Pack

## Purpose

Bundles student-facing follow-up after a lesson or sequence.

## Producer

`kc_learning_followup_teacher`.

## Consumers

Parent agent, `kc_assessment_reviewer`.

## Required Fields

```yaml
weekly_learning_pack_id: "unique id"
learner_alias: "non-identifying handle"
source_lesson_result: "path or id"
review_focus: []
homework_ref: "path or id"
quizlet_ref: "path or id"
mission_ref: "path or id"
follow_up_message_ref: "path or id"
next_lesson_check_ref: "path or id"
```

## Validation

The pack must connect each activity to a target from the lesson result or progression plan.
