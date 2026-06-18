# Contract: Follow Up Message

## Purpose

Defines a student-safe message within the teacher-approved homework scope.

## Producer

`kc_learning_followup_teacher`.

## Consumers

Parent agent, learner, `kc_privacy_auditor`, `kc_assessment_reviewer`.

## Required Fields

```yaml
follow_up_message_id: "unique id"
followup_scope: "homework_only | full_followup"
source_post_lesson_teacher_card: "path or id"
learner_alias: "non-identifying handle"
tone: "warm | concise | coaching | formal"
message: {}
privacy_review:
  required: true
  notes: []
```

## Validation

The message may describe learning behavior but cannot imply an unapproved next direction or contain identifying details.
