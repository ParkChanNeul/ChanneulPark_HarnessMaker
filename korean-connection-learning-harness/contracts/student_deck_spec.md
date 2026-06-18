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
slides: []
design_notes: {pacing: [], visual_rhythm: [], accessibility: []}
non_student_notes: []
```

## Validation

Slides remain learner-facing and mission-first. Rendering cannot add targets or expose internal planning labels.
