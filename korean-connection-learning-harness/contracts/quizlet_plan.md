# Contract: Quizlet Plan

## Purpose

Prepares approved spaced vocabulary and expression practice.

## Producer

`kc_learning_followup_teacher` or `kc_practice_designer`.

## Consumers

Parent agent, learner, `kc_assessment_reviewer`.

## Required Fields

```yaml
quizlet_plan_id: "unique id"
followup_scope: "homework_only | full_followup"
source_post_lesson_teacher_card: "path or id"
source_targets: []
sets: []
review_notes: []
```

## Validation

Cards must match the approved homework focus and support retrieval rather than recognition only.
