# Contract: Teacher Decision Card

## Purpose

Separates teacher facts from AI interpretation and presents bounded lesson directions before approval.

## Producer

Top-level parent using `kc-lesson-turn`; optional specialist results are advisory only.

## Consumers

Teacher, `kc-lesson-unknown`, `kc-lesson-scope-lock`.

## Required Fields

```yaml
decision_card_id: "unique id"
source_intake_state: "path, id, or transcript summary"
teacher_facts: []
agent_interpretations: []
teaching_problem:
  summary: ""
  evidence: []
  confidence: "low | medium | high"
options:
  - option_id: "A"
    mode: "advance | review | mixed | vocabulary_focus | listening_focus | conversation_focus | diagnostic"
    new_grammar_candidates: []
    review_candidates: []
    conversation_targets: []
    vocabulary_scope:
      target_pack: ""
      lesson_vocabulary_set_ref: null
      in_class_new_item_count: 0
      productive_core_count: 0
      receptive_support_count: 0
      review_item_ids: []
      homework_expansion_count: 0
    benefits: []
    risks: []
recommendation:
  option_id: ""
  rationale: ""
  limitations: []
required_teacher_decisions: []
assumption_candidates: []
scope_status: "open | partial | ready_to_lock"
advisory_inputs: []
```

## Validation

A recommendation is not approval. Advisory specialist output cannot set `scope_status` to `locked` or dispatch `build_lesson`. Vocabulary counts must be non-negative integers, and `in_class_new_item_count` must equal `productive_core_count + receptive_support_count`.
