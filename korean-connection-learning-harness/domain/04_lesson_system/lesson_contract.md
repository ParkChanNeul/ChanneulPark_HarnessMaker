# Lesson Contract

## Default A1-B1 Contract

```yaml
language_targets:
  structure:
    target_ref: "canonical target id"
    treatment: "new | review | retrieval | transfer | practice | carrier | defer"
  default_new_max: 1
  default_review_min: 2
  default_review_max: 4
  retrieval_required: true
  transfer_required: true
situation_scope:
  pack_ref: "canonical situation pack id"
  sub_situation_ids: []
major_culture_points:
  default_max: 1
independent_production:
  required: true
next_lesson_check:
  required_in_full_followup: true
```

## Required Distinctions

Every lesson blueprint stores one canonical `language_targets` array. Treatment distinguishes new, review, retrieval, transfer, practice, carrier, and defer. `situation_scope` is the only situation truth.

## Teacher-Approved Override

Defaults guide recommendations but do not override a locked teacher decision. A teacher may choose no separate review; prior targets can remain as carrier, retrieval, transfer, or defer. Record the choice in `teacher_overrides` and preserve it downstream.

## Override Rule

Any exception to default target counts requires an override reason or controlling teacher override reference.
