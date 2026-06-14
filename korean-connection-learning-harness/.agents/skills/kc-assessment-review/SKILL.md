---
name: kc-assessment-review
description: "Review Korean Connection learning artifacts. Use for contract validation, lesson QA, grammar-practice balance, mastery evidence checks, student deck checks, follow-up checks, and acceptance reports."
---

# KC Assessment Review

Use this skill whenever generated Korean Connection artifacts need quality review.

## Read First

1. `domain/02_learning_model/pedagogy_principles.md`
2. `domain/02_learning_model/mastery_definition.md`
3. `domain/04_lesson_system/lesson_contract.md`
4. `domain/07_governance/privacy.md`
5. Relevant contracts for the artifacts being reviewed
6. `contracts/assessment_report.md`

## Review Checklist

1. Contract completeness: required fields are present and semantically filled.
2. Learning principle: situation-led, culture-explained, grammar-tracked, practice-repeated, mastery-verified.
3. Target balance: new, review, retrieval, transfer, and conversation skill targets are explicit.
4. Practice quality: controlled, guided, independent, and transfer practice are present where required.
5. Evidence: mastery updates cite evidence and do not overpromote.
6. Student experience: visible titles are student-safe and not internal reasoning labels.
7. Privacy: obvious private details are absent or routed to privacy audit.

## Severity

- `blocker`: output is unsafe, private, contract-invalid, or unusable.
- `major`: output can be fixed but would weaken learning quality.
- `minor`: improvement that does not block use.
- `note`: observation or residual risk.

## Output

Return an `assessment_report` with exact artifact references, findings, evidence, required fixes, and pass status. Do not write final files.
