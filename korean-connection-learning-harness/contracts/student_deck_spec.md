# Contract: Student Deck Spec

## Purpose

Specifies student-facing slide content before rendering.

## Producer

`kc_student_experience_designer`.

## Consumers

Parent renderer, `kc_assessment_reviewer`.

## Required Fields

```yaml
student_deck_spec_id: "unique id"
source_blueprint: "path or id"
deck_mode: "student_deck"
slide_count_target: "number or range"
slides:
  - slide_id: "id"
    student_title: "visible title"
    purpose: "teaching purpose"
    content_blocks: []
    interaction: "say | choose | transform | roleplay | reflect | none"
design_notes:
  pacing: []
  visual_rhythm: []
  accessibility: []
non_student_notes: []
```

## Validation

Slides must be learner-facing and mission-first. Internal planning labels cannot appear as slide titles.
