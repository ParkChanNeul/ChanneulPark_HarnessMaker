---
name: kc-lesson-architecture
description: Use when an approved Korean Connection lesson scope and progression plan must be operationalized into a lesson blueprint.
---

# KC Lesson Architecture

## Read First

1. `contracts/conversation/lesson_scope_lock.md`
2. `contracts/progression_plan.md`
3. `domain/04_lesson_system/lesson_contract.md`
4. `domain/04_lesson_system/culture_usage_rules.md`
5. `domain/04_lesson_system/student_experience_rules.md`
6. `domain/02_learning_model/pedagogy_principles.md`
7. `contracts/lesson_blueprint.md`

## Workflow

1. Require a valid scope lock and matching progression plan.
2. Copy approved targets, the complete canonical vocabulary scope, and teacher overrides without reinterpretation.
3. State the approved learner action.
4. Place culture only where it explains language choice.
5. Build warmup, model, controlled, guided, role-play, transfer, and wrap stages.
6. Define evidence to collect.
7. Return `lesson_blueprint`.

## Boundary

This role performs approved target operationalization. It does not select replacement targets, add excluded review, change vocabulary load, or alter lesson mode.

## Output

Return blueprint content, lock reference, flow, evidence plan, overrides applied, evidence paths, and blockers. Do not write final files.
