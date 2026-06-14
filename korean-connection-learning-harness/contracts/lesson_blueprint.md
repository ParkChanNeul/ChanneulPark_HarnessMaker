# Contract: Lesson Blueprint

## Purpose

Defines the lesson before material design.

## Producer

`kc_lesson_architect`.

## Consumers

`kc_practice_designer`, `kc_student_experience_designer`, `kc_assessment_reviewer`.

## Required Fields

```yaml
lesson_blueprint_id: "unique id"
lesson_title: "student-safe title"
learner_alias: "non-identifying handle"
situation: "primary situation"
lesson_promise: "what the learner can do after the lesson"
new_targets: []
review_targets: []
retrieval_targets: []
transfer_targets: []
conversation_skill_targets: []
culture_point:
  topic: "one point max by default"
  function: "how it explains language choice"
lesson_flow:
  - stage: "warmup | model | controlled | guided | roleplay | transfer | wrap"
    purpose: "why this stage exists"
assessment_evidence_to_collect: []
override_reason: "required only when violating default target counts"
```

## Validation

Visible titles must not expose internal reasoning headings such as `Cultural Tension`, `Social Meaning`, or `Grammar Tool`.
