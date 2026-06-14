# Contract: Follow Up Message

## Purpose

Defines a student-safe post-lesson message.

## Producer

`kc_learning_followup_teacher`.

## Consumers

Parent agent, learner, `kc_privacy_auditor`.

## Required Fields

```yaml
follow_up_message_id: "unique id"
learner_alias: "non-identifying handle"
tone: "warm | concise | coaching | formal"
message:
  greeting: "text"
  lesson_win: "text"
  review_focus: "text"
  homework: "text"
  next_step: "text"
privacy_review:
  required: true
  notes: []
```

## Validation

The message may reference learning behavior but not private student identity or sensitive context.
