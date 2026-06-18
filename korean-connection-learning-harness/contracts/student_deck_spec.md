# Contract: Student Deck Spec

## Purpose

Specifies student-facing slide content from an approved lesson before rendering.

## Producer

`kc_student_experience_designer`.

## Consumers

Parent renderer, `kc_assessment_reviewer`.

## Required Fields

```yaml
student_deck_spec_id: "unique id"
lesson_scope_lock_ref: "path or id"
source_blueprint: "path or id"
deck_mode: "student_deck"
slide_count_target: "number or range"
vocabulary_scope:
  target_pack: ""
  lesson_vocabulary_set_ref: null
  in_class_new_item_count: 0
  productive_core_count: 0
  receptive_support_count: 0
  review_item_ids: []
  homework_expansion_count: 0
slides:
  - slide_id: "id"
    student_title: ""
    purpose: ""
    content_blocks: []
    interaction: "say | choose | repeat | react | roleplay | recall | reflect"
design_notes: {pacing: [], visual_rhythm: [], accessibility: []}
non_student_notes: []
```

## Validation

Slides remain learner-facing and mission-first. `slide_count_target` must equal the actual slide count, every slide must contain the documented fields, and slide IDs must be unique. Rendering cannot add targets or expose internal planning labels.
