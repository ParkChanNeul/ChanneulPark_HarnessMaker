# Contract: Lesson Result

## Purpose

Records what happened in a completed lesson.

## Producer

Parent agent, teacher, or `kc_learning_followup_teacher`.

## Consumers

`kc_learner_state_analyst`, `kc_assessment_reviewer`, `kc_learning_progression_planner`.

## Required Fields

```yaml
lesson_result_id: "unique id"
lesson_id: "id"
learner_alias: "non-identifying handle"
situation_scope:
  pack_ref: "canonical situation pack id"
  sub_situation_ids: []
language_targets:
  - target_ref: "canonical language target id"
    treatment: "new | review | retrieval | transfer | practice | carrier | defer"
observed_evidence:
  successful: []
  breakdowns: []
  missed: []
followup_inputs:
  homework: []
  quizlet: []
  next_lesson_check: []
privacy_redactions: []
```

## Validation

The result must preserve the canonical `situation_scope` and `language_targets` from the lesson and distinguish observed evidence from teacher inference.
