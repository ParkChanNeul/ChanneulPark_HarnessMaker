# Contract: Weekly Learning Pack

## Purpose

Bundles approved follow-up artifacts without conflating homework approval and next-lesson approval.

## Producer

`kc_learning_followup_teacher`.

## Consumers

Parent agent, `kc_assessment_reviewer`.

## Required Fields

```yaml
weekly_learning_pack_id: "unique id"
followup_scope: "homework_only | full_followup"
source_post_lesson_teacher_card: "path or id"
source_next_lesson_decision_lock: "path or null"
review_focus: []
homework_ref: "path or id"
quizlet_ref: "path or id"
follow_up_message_ref: "path or id"
next_lesson_check_ref: null
```

## Validation

In `homework_only`, next-lesson references must be null. In `full_followup`, the next lock and next-lesson check are required.
