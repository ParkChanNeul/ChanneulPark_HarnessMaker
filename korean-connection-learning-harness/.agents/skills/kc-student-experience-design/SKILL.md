---
name: kc-student-experience-design
description: "Design Korean Connection student experience. Use for student deck specs, HTML material specs, slide pacing, mission-first classroom rhythm, visual rhythm from archives, learner-safe titles, and design manifests."
---

# KC Student Experience Design

Use this skill when converting lesson and practice plans into student-facing material specs.

## Read First

1. `domain/04_lesson_system/student_experience_rules.md`
2. `domain/04_lesson_system/mission_and_followup.md`
3. `contracts/student_deck_spec.md`
4. `contracts/design_manifest.md`
5. `contracts/material_manifest.md`
6. `domain/07_governance/privacy.md`

## Workflow

1. Identify the learner-facing mission and keep it visible early.
2. Convert the lesson flow into a student deck spec.
3. Convert practice moves into slide interactions or material sections.
4. Copy the complete canonical vocabulary scope from the blueprint.
5. Keep slide titles student-safe and action-oriented.
6. Use archive-style rhythm only as structure, never as copied content or private context.
7. Add pacing, visual rhythm, and accessibility notes.
8. Return `student_deck_spec` and draft `design_manifest`.

## Decision Rules

- Default teaching-material mode is `student_deck`.
- Do not expose internal headings such as `Cultural Tension`, `Korean Social Rule`, `Social Meaning`, `Language Mechanism`, or `Grammar Tool`.
- Every visible section should help the learner say, choose, transform, role-play, or remember something.
- `slide_count_target` must equal the actual number of complete slide objects.
- Request privacy audit if learner-specific context appears.

## Output

Return proposed deck spec, design manifest, material path recommendations, accessibility checks, and blockers. Do not write final rendered files.
