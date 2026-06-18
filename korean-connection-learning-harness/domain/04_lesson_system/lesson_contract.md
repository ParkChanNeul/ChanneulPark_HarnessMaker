# Lesson Contract

## Default A1-B1 Contract

```yaml
new_targets:
  default_max: 1
review_targets:
  default_min: 2
  default_max: 4
retrieval_targets:
  required: true
transfer:
  required: true
major_culture_points:
  default_max: 1
independent_production:
  required: true
next_lesson_check:
  required_in_full_followup: true
```

## Required Distinctions

Every lesson blueprint distinguishes new, review, retrieval, transfer, conversation, vocabulary, culture explanation, and evidence targets.

## Teacher-Approved Override

Defaults guide recommendations but do not override a locked teacher decision. A teacher may choose no separate review; prior targets can remain as carrier, retrieval, transfer, or defer. Record the choice in `teacher_overrides` and preserve it downstream.

## Override Rule

Any exception to default target counts requires an override reason or controlling teacher override reference.
