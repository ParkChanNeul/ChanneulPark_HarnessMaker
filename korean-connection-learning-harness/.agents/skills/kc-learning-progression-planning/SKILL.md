---
name: kc-learning-progression-planning
description: Use when Korean Connection needs evidence-based progression options before teacher approval or a progression plan after an approved lesson scope lock.
---

# KC Learning Progression Planning

## Read First

1. `domain/02_learning_model/pedagogy_principles.md`
2. `domain/02_learning_model/grammar_progression.md`
3. `domain/02_learning_model/vocabulary_progression.md`
4. `domain/02_learning_model/conversation_skill_progression.md`
5. `domain/02_learning_model/mastery_definition.md`
6. `domain/03_curriculum/situation_map.md`
7. `domain/03_curriculum/module_map.md`
8. `domain/03_curriculum/sequence_rules.md`
9. `domain/03_curriculum/spiral_review_rules.md`
10. `contracts/conversation/lesson_scope_lock.md`
11. `contracts/progression_plan.md`

## Before Lock: Advisory Mode

With explicit learner-context or lesson-result paths and a teacher request for reasoning, return bounded options with evidence, burden, risks, and limitations. Do not select the final direction, create a lock, write files, or start a build.

## After Lock: Planning Workflow

1. Require `lesson_scope_lock_ref`.
2. Read learner evidence and the approved situation, mode, targets, vocabulary scope, and overrides.
3. Structure approved new targets.
4. Select review, retrieval, and transfer only within the lock's allowed treatment.
5. Explain why the approved lesson should happen now.
6. Return `progression_plan`.

## Decision Rules

- Do not change locked grammar, vocabulary count, or mode.
- Do not reintroduce explicit review excluded by the teacher.
- Prior targets may be retrieval, carrier, transfer, or defer.
- Missing evidence becomes a blocker or limitation, not an automatic direction change.

## Output

Return plan content, lock reference, target rationale, rejected alternatives, teacher overrides applied, evidence paths, and blockers. Do not write final files.
