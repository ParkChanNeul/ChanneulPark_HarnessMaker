# Design Manifest

```yaml
design_manifest_id: "design-clinic-pharmacy-001"
material_refs:
  - "07_student_deck.html"
source_specs:
  - "03_lesson_blueprint.md"
  - "04_practice_plan.md"
  - "05_student_deck_spec.md"
layout_principles:
  - "Single-file HTML deck so it can open locally without a dev server."
  - "Four-step visual map keeps the lesson situation-led: symptom, time, repeat, check."
  - "Student-facing titles are action-oriented and avoid teacher-side reasoning labels."
  - "Large Korean chunks support speaking practice under pressure."
  - "Separate accents distinguish symptom, time, repair, check, and transfer without relying on one hue family."
interaction_support:
  - "Previous and next icon buttons."
  - "Keyboard navigation with arrow keys, PageUp/PageDown, Home, and End."
  - "Progress bar and slide counter."
  - "Print mode renders each slide as a page."
  - "Responsive single-column layout on small screens."
accessibility_checks:
  - "High-contrast text on light surfaces."
  - "Short visible lines and large Korean phrases."
  - "Buttons include aria-label and title text."
  - "No external fonts, scripts, CDNs, remote assets, or autoplay media."
  - "No real medical details, diagnosis, medication names, or private learner context."
known_limitations:
  - "Static HTML deck only; no PDF export was generated."
  - "Choice and role-play sections are classroom prompts, not scored interactions."
```

## Source Mapping

| Source | Implemented In |
|---|---|
| `03_lesson_blueprint.md` | mission, promise, stages, culture point, evidence-safe role-play |
| `04_practice_plan.md` | controlled body-part swap, guided choice, independent role-play, transfer, mission |
| `05_student_deck_spec.md` | 14 slide titles, purposes, interactions, visual rhythm, accessibility |

## Render Notes

The deck follows the structure of `_workspace/runs/2026-06-14-build-lesson-making-friends/07_student_deck.html` but uses new clinic/pharmacy content and current V2 contract language.
