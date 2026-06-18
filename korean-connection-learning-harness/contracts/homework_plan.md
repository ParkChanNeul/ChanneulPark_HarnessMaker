# Contract: Homework Plan

## Purpose

Defines compact teacher-approved practice between lessons.

## Producer

`kc_learning_followup_teacher` or `kc_practice_designer`.

## Consumers

Parent agent, learner, `kc_assessment_reviewer`.

## Required Fields

```yaml
homework_plan_id: "unique id"
followup_scope: "homework_only | full_followup"
source_lesson_result: "path or id"
source_post_lesson_teacher_card: "path or id"
tasks: []
support:
  examples: []
  hints: []
```

## Validation

The selected workload must match the approved Post-Lesson Teacher Card. Homework-only does not require a next lesson lock.
