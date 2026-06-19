# Contract: Post-Lesson Teacher Card

## Purpose

Separates observed lesson evidence from interpretation and records teacher-approved homework independently from next-lesson direction.

## Producer

Top-level parent using `kc-post-lesson-reflection`.

## Consumers

Teacher, `kc-next-lesson-decision`, `kc_learning_followup_teacher`, `kc_assessment_reviewer`.

## Required Fields

```yaml
post_lesson_teacher_card_id: "unique id"
source_lesson_result: "path, id, or teacher note"
teacher_observations: []
observed_successes: []
observed_breakdowns: []
evidence_gaps: []
state_update_candidates: []
homework_options:
  - option_id: "A"
    estimated_minutes: 10
    focus: ""
    reason: ""
next_lesson_options:
  - option_id: "A"
    mode: "advance | review | mixed | transfer | vocabulary_focus | listening_repair | conversation_repair"
    situation_scope:
      pack_ref: "canonical situation pack id"
      sub_situation_ids: []
    candidate_language_targets:
      - target_ref: "canonical target id"
        treatment: "new | review | retrieval | transfer | practice | carrier | defer"
    reason: ""
    risk: ""
recommendation:
  homework_option: ""
  next_lesson_option: ""
  rationale: ""
teacher_approval:
  homework_approved: false
  homework_option: null
  approval_evidence: ""
required_teacher_decisions: []
status: "open | partial | ready_to_lock"
```

## Validation

Observed and inferred claims must remain distinct. Every next-lesson option uses canonical `situation_scope` and `candidate_language_targets`; split target fields and legacy IDs are forbidden. `homework_only` requires `homework_approved: true` and approval evidence. This card alone cannot authorize `next_lesson_check` or progression decisions.
