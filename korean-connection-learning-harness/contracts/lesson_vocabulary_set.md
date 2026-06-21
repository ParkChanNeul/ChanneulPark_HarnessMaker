# Contract: Lesson Vocabulary Set

## Purpose

Stores the lesson-specific vocabulary selection by instructional role and records the teacher approval boundary between a `proposed` set and a `locked` set.

## Producer

Top-level parent in the teacher-approved lesson planning flow. `selection_mode: manual` accepts teacher or planner input directly and does not require an external source, web search, retrieval service, or lexeme database.

## Consumers

`kc_learning_progression_planner`, `kc_lesson_architect`, `kc_practice_designer`, `kc_student_experience_designer`, `kc_learning_followup_teacher`, `kc_assessment_reviewer`, and the parent orchestrator.

## Required Fields

```yaml
lesson_vocabulary_set_id: "unique id"
revision: 1
supersedes: null
selection_status: "proposed | locked | superseded"
selection_mode: "manual | suggest"
lesson_scope_lock_ref: null
target_pack: ""
approved_by_teacher: false
approval_evidence: ""
counts:
  review: 0
  productive_core: 0
  receptive_support: 0
  homework_expansion: 0
items:
  - item_id: "unique within this set"
    surface_form: ""
    item_type: "word | chunk | collocation"
    gloss_en: ""
    role: "review | productive_core | receptive_support | homework_expansion"
    collocations: []
    example_ko: ""
    example_en: ""
    production_prompt: ""
    target_refs: []
    situation_refs: []
    notes: ""
created_artifact_refs: []
```

## Validation

`item_id` values must be unique within the set. `item_id`, `surface_form`, `role`, and `item_type` must be non-empty, and `role` and `item_type` must use the documented enums. Each declared role count must equal the number of Items assigned to that role. `counts.productive_core + counts.receptive_support` must equal the controlling Lesson Scope Lock's `vocabulary_scope.in_class_new_item_count`.

Every provided `target_ref` must be a Canonical Language Target ID and must occur in the controlling Lesson Scope Lock's `language_targets`. `target_refs`, `situation_refs`, and `production_prompt` allow selected vocabulary to connect to approved Language Targets, situations, and concrete practice.

A `proposed` set may remain unapproved. A `locked` set requires `approved_by_teacher: true`, non-empty `approval_evidence`, and a `lesson_scope_lock_ref` that matches the controlling `lesson_scope_lock_id`. Once locked, the artifact is immutable; any vocabulary change requires a higher `revision` or a new artifact whose `supersedes` points to the locked artifact.

This contract does not define web retrieval, external-source requirements, a lexeme or sense database, or automatic vocabulary selection. `selection_mode: manual` is valid without those systems.
