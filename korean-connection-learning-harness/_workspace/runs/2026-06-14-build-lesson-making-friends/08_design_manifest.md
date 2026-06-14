# Design Manifest

```yaml
design_manifest_id: "design-friends-001"
material_refs:
  - "07_student_deck.html"
source_specs:
  - "03_lesson_blueprint.md"
  - "04_practice_plan.md"
  - "05_student_deck_spec.md"
layout_principles:
  - "Single-file HTML deck so the material can open locally without a dev server."
  - "Ten slide sequence follows the student_deck_spec exactly."
  - "Student-facing slides use action titles and avoid teacher-side reasoning labels."
  - "Visual rhythm separates mission, Korean line practice, choices, reaction timing, role-play, transfer, mission, and recall."
  - "Color accents distinguish action types without relying on one hue family."
interaction_support:
  - "Previous and next icon buttons."
  - "Keyboard navigation with arrow keys, PageUp/PageDown, Home, and End."
  - "Print mode outputs each slide as a full-page handout."
  - "Responsive layout stacks grids on small screens."
accessibility_checks:
  - "Buttons have aria-label and title text."
  - "Slide counter and progress bar provide position feedback."
  - "Text uses high contrast against warm paper and white surfaces."
  - "Korean and English support are visually separated."
  - "No external fonts, scripts, CDNs, or remote assets."
known_limitations:
  - "This is a static prototype deck, not a generated PDF."
  - "Choice buttons are presentational for classroom interaction; they do not score learner answers."
```

## Source Mapping

| Source | Implemented In |
|---|---|
| `03_lesson_blueprint.md` | mission, lesson promise, stages, evidence footers |
| `04_practice_plan.md` | controlled choice, guided reaction, independent role-play, transfer, mission, recall |
| `05_student_deck_spec.md` | ten slide titles, purposes, interactions, pacing, accessibility |
