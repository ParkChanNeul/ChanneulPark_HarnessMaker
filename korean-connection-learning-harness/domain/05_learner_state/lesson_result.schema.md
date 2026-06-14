# Lesson Result Schema

## Purpose

Turns a completed lesson into structured evidence for the next lesson, follow-up message, and mastery updates.

## Result Record

```yaml
lesson_result_id: "lesson result id"
lesson_id: "lesson id"
learner_alias: "non-identifying handle"
date: "YYYY-MM-DD or lesson slot"
planned_targets:
  new: []
  review: []
  retrieval: []
  transfer: []
observed_evidence:
  strengths: []
  breakdowns: []
  successful_retrieval: []
  independent_production: []
  transfer_attempts: []
missed_items:
  - "planned item not reached"
state_delta_refs:
  - "learner state delta id"
followup_needed:
  homework: true
  quizlet: true
  next_lesson_check: true
teacher_notes:
  - "non-private teaching note"
```

## Next Lesson Rule

Every lesson result must produce at least one concrete input for the next lesson: a review target, a repair target, a transfer target, or a learner question.
