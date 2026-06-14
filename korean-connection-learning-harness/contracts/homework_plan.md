# Contract: Homework Plan

## Purpose

Defines compact practice between lessons.

## Producer

`kc_learning_followup_teacher` or `kc_practice_designer`.

## Consumers

Parent agent, learner, `kc_assessment_reviewer`.

## Required Fields

```yaml
homework_plan_id: "unique id"
source_lesson_result: "path or id"
tasks:
  - task_id: "id"
    target: "grammar, expression, or skill id"
    task: "learner-facing instruction"
    estimated_minutes: 5
    success_evidence: "what completion shows"
support:
  examples: []
  hints: []
```

## Validation

Homework should be short, doable, and connected to evidence needed for mastery.
