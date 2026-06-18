# Contract: Learner State Delta

## Purpose

Records evidence-supported state changes and, in full follow-up only, approved scheduling handoffs.

## Producer

`kc_learning_followup_teacher` or `kc_assessment_reviewer`.

## Consumers

Parent agent, next learner-state analysis.

## Required Fields

```yaml
delta_id: "unique id"
source_artifact: "lesson result or assessment path"
followup_scope: "full_followup"
source_next_lesson_decision_lock: "path or id"
grammar_updates: []
vocabulary_updates: []
conversation_updates: []
mission_updates: []
review_schedule_updates: []
approval_needed: []
```

## Validation

No status is promoted without evidence. Scheduling and next-progression changes require a locked next-lesson decision.
