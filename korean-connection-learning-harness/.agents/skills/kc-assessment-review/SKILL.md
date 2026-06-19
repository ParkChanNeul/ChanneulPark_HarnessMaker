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
7. `domain/02_language_map/registry_manifest.json`
8. `domain/02_language_map/source_catalog.json`
9. `domain/03_situations/situation_pack_manifest.json`
10. `domain/04_profiles/profile_manifest.json`
11. `contracts/assessment_report.md`

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
13. Active artifacts use only the common `language_targets` item shape and canonical `situation_scope`.
14. Every `target_ref` resolves through a registry; target type is not duplicated in artifacts.
15. Legacy aliases are 1:1 only, contextual migrations remain separate, and new artifacts contain no legacy IDs.
16. Practice coverage is visible in prompts or examples; target references alone do not count.
17. Core grammar, register, and phonology coverage has verified official support or remains blocked.

## Severity

Use `blocker`, `major`, `minor`, or `note`. Gate violations are blockers.

## Output

Return assessment report content, exact artifact evidence, smallest required fixes, residual risks, and pass status. Do not write final files.
