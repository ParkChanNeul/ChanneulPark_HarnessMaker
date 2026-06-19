# Contract: Lesson Scope Lock

## Purpose

Records the teacher-approved lesson scope that gates `build_lesson`.

## Producer

Top-level parent using `kc-lesson-scope-lock`.

## Consumers

`kc_learner_state_analyst`, `kc_learning_progression_planner`, `kc_lesson_architect`, `kc_assessment_reviewer`, parent orchestrator.

## Required Fields

```yaml
lesson_scope_lock_id: "unique id"
revision: 1
supersedes: null
lock_status: "open | partial | locked"
approved_by_teacher: false
approval_evidence: ""
learner:
  alias: "non-identifying handle"
  level: "A0 | A1 | A2 | B1 | B2 | bounded range"
  learner_context_ref: null
lesson:
  mode: "advance | review | mixed | vocabulary_focus | listening_focus | conversation_focus | diagnostic"
  duration_minutes: 50
  situation_scope:
    pack_ref: "canonical situation pack id"
    sub_situation_ids: []
  lesson_promise: ""
language_targets:
  - target_ref: "canonical language target id"
    treatment: "new | review | retrieval | transfer | practice | carrier | defer"
vocabulary_scope:
  target_pack: ""
  lesson_vocabulary_set_ref: null
  in_class_new_item_count: 0
  productive_core_count: 0
  receptive_support_count: 0
  review_item_ids: []
  homework_expansion_count: 0
material_scope:
  student_deck: true
  html: true
  mobile_cheat_sheet: true
  homework: true
  quizlet_plan: true
teacher_overrides:
  - rule: "default or recommendation"
    decision: "teacher decision"
    rationale: "teacher rationale or session context"
assumption_locks:
  - field: "field name"
    value: "approved value"
    recommended_by_ai: true
    approved_by_teacher: true
unresolved_blockers: []
created_artifact_refs: []
```

## Validation

When `lock_status` is `locked`, `approved_by_teacher` must be true, `approval_evidence` must be non-empty, and `unresolved_blockers` must be empty. `situation_scope` and `language_targets` are the only canonical situation and target truth; split target fields and `primary_situation` are forbidden. Vocabulary counts must be non-negative integers, and `in_class_new_item_count` must equal `productive_core_count + receptive_support_count` unless a specific vocabulary-count Teacher Override is recorded. A locked contract is immutable; changes require a revision or superseding lock.
