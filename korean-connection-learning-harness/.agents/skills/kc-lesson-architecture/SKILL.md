---
name: kc-lesson-architecture
description: "Architect Korean Connection lessons. Use for lesson blueprints, situation-led lesson flow, target balance, culture explanation placement, evidence capture, and learner-safe lesson titles."
---

# KC Lesson Architecture

Use this skill to turn a progression plan into a lesson blueprint.

## Read First

1. `domain/04_lesson_system/lesson_contract.md`
2. `domain/04_lesson_system/culture_usage_rules.md`
3. `domain/04_lesson_system/student_experience_rules.md`
4. `domain/02_learning_model/pedagogy_principles.md`
5. `contracts/lesson_blueprint.md`

## Workflow

1. State the learner action: what the learner should be able to do in the situation.
2. Select new, review, retrieval, transfer, and conversation skill targets from the progression plan.
3. Place one culture point only where it explains a language decision.
4. Build a lesson flow from warmup through model, controlled practice, guided practice, role-play, transfer, and wrap.
5. Name evidence that should be collected during the lesson.
6. Add an override reason if target counts violate the default contract.
7. Return a `lesson_blueprint`.

## Decision Rules

- Do not use culture as the final outcome. It is an explanation layer.
- Do not put internal reasoning headings in student-facing titles.
- Keep the blueprint practical enough to render into student materials.
- Make all target categories explicit, even when a category is intentionally empty.

## Output

Return proposed lesson blueprint content, flow, evidence plan, override reasons, evidence paths, and blockers. Do not write final files.
