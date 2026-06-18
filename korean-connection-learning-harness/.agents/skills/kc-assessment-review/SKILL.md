---
name: kc-assessment-review
description: Use when Korean Connection artifacts need contract, learning-quality, approval-gate, lock-consistency, privacy, or student-experience review.
---

# KC Assessment Review

## Read First

1. `domain/02_learning_model/pedagogy_principles.md`
2. `domain/02_learning_model/mastery_definition.md`
3. `domain/04_lesson_system/lesson_contract.md`
4. `domain/07_governance/approval_rules.md`
5. `domain/07_governance/privacy.md`
6. controlling conversation locks and relevant artifact contracts
7. `contracts/assessment_report.md`

## Review Checklist

1. Required fields are semantically filled.
2. Situation, culture, tracked grammar/vocabulary, practice, and mastery evidence align.
3. Lesson build has a valid teacher-approved scope lock.
4. Progression and blueprint match the lock.
5. Teacher overrides are preserved through downstream artifacts.
6. No agent automatically chooses advance, review, or vocabulary scope.
7. Homework-only contains no next-lesson outputs.
8. Full follow-up matches the next-lesson lock.
9. Student-facing titles hide internal reasoning.
10. Private details are absent or routed to privacy audit.
11. Canonical vocabulary fields and count equations are preserved across the lock, progression, blueprint, practice, and deck.
12. A Golden assessment pass is accepted only when it matches computed validator output.

## Severity

Use `blocker`, `major`, `minor`, or `note`. Gate violations are blockers.

## Output

Return assessment report content, exact artifact evidence, smallest required fixes, residual risks, and pass status. Do not write final files.
