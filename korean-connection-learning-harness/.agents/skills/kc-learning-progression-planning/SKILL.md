---
name: kc-learning-progression-planning
description: "Plan Korean Connection learning progression. Use for choosing next lesson targets, grammar sequence, situation sequence, spiral review, retrieval, transfer, and long-term mastery planning."
---

# KC Learning Progression Planning

Use this skill after learner state analysis and before lesson architecture.

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
10. `contracts/progression_plan.md`

## Workflow

1. Start from the requested situation and learner goal.
2. Read the learner snapshot for active grammar, conversation, and mission evidence.
3. Choose at most one default new target for A1-B1 lessons unless there is an override reason.
4. Choose review targets from recent weak or due items.
5. Choose retrieval targets from older items that need delayed recall.
6. Choose transfer targets that move prior language into a non-identical context.
7. Explain why this lesson should happen now.
8. Return a `progression_plan`.

## Decision Rules

- Situation leads target selection; grammar is tracked and sequenced after the situation is chosen.
- Culture can influence sequencing only when it changes language choice or social distance.
- A lesson without retrieval or transfer needs a clear diagnostic or first-lesson reason.
- If mastery evidence is missing, do not guess stability. Flag the missing evidence.

## Output

Return proposed progression plan content, target rationale, rejected targets, evidence paths, and blockers. Do not write final files.
