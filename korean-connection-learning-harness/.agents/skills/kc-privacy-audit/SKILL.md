---
name: kc-privacy-audit
description: "Audit Korean Connection privacy. Use whenever learner biography, exact age, race, nationality, social-account context, follower counts, archive examples, private student cases, or follow-up messages appear."
---

# KC Privacy Audit

Use this skill before tracking or reusing artifacts that include learner context.

## Read First

1. `domain/07_governance/privacy.md`
2. `contracts/privacy_report.md`

## Workflow

1. Scan the supplied artifacts for prohibited tracked details.
2. Identify whether each finding is a legal name, exact age, demographic detail, nationality, social account, follower count, contact detail, private context, or unique identifying combination.
3. Decide pass or blocked.
4. Recommend remove, generalize, or approve-with-reason only when the user explicitly authorizes a narrow untracked use.
5. Return a `privacy_report`.

## Decision Rules

- Private learner details are blockers in tracked fixtures, examples, contracts, and domain files.
- Archive examples must be treated as private unless already fully generalized.
- Generalize to the learning need: for example, use `creator-focused learner` instead of social profile details.
- Do not write final files.

## Output

Return privacy report content, status, exact evidence or description, redactions recommended, and residual risks.
