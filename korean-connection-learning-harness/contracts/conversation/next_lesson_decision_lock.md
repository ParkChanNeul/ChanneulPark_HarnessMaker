# Contract: Next Lesson Decision Lock

## Purpose

Records the teacher-approved next lesson direction and prior-target treatment required for full follow-up.

## Producer

Top-level parent using `kc-next-lesson-decision`.

## Consumers

`kc_learning_followup_teacher`, `kc_learning_progression_planner`, `kc_assessment_reviewer`, parent orchestrator.

## Required Fields

```yaml
next_lesson_decision_lock_id: "unique id"
revision: 1
supersedes: null
source_post_lesson_card: "path or id"
lock_status: "open | partial | locked"
approved_by_teacher: false
approval_evidence: ""
selected_direction:
  mode: "advance | review | mixed | transfer | vocabulary_focus | listening_repair | conversation_repair"
  primary_situation: ""
  approved_new_targets: []
prior_targets:
  - target_id: "id"
    treatment: "explicit_review | retrieval | carrier | transfer | defer"
vocabulary_direction:
  target_pack: ""
  lesson_vocabulary_set_ref: null
  in_class_new_item_count: 0
  productive_core_count: 0
  receptive_support_count: 0
  review_item_ids: []
  carrier_item_ids: []
  homework_expansion_count: 0
homework_scope:
  estimated_minutes: 0
  focus: ""
  required_outputs: []
next_lesson_check: []
teacher_notes: []
unresolved_blockers: []
```

## Validation

A locked decision requires teacher approval evidence and no blockers. Vocabulary counts must be non-negative integers and internally consistent. `carrier` is natural reuse, not explicit review, and one prior target cannot have both treatments. Changes require a revision or superseding lock.
