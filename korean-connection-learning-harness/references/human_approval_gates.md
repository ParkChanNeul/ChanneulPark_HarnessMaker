# Human Approval Gates

## Lesson Scope Gate

`build_lesson` requires a locked, teacher-approved, blocker-free `lesson_scope_lock`. AI recommendations and advisory findings are not approval.

## Post-Lesson Gates

- Approved homework selection in `post_lesson_teacher_card` authorizes `homework_only`.
- Locked `next_lesson_decision_lock` additionally authorizes `full_followup`, next-lesson checks, state scheduling, and progression-related outputs.

## Governance Gates

Human approval remains required for:

- changing approved `domain/` files
- changing approved `contracts/` policy
- changing agent boundaries or required skills
- promoting research insight to a default rule
- relaxing privacy rules
- using private learner details in tracked artifacts
- overriding mastery promotion rules

## Approval Evidence

Use the controlling contract's teacher approval field and non-empty `approval_evidence`. Generic continuation language cannot approve unresolved scope. Governance changes continue to use `contracts/approval_state.md`.

Semantic validation additionally requires a locked contract to have no unresolved blockers and internally consistent vocabulary counts. Recommendation and advisory fields never satisfy approval.

## Gate Workflow

```text
proposal or decision card
-> reviewer when applicable
-> human decision
-> approval or lock artifact
-> parent applies approved scope only
```

## Rejection and Revision

Preserve rejected proposals in workspace evidence. A rejected or changed lock becomes a revision or superseded lock; rerun only affected producers and downstream reviewers.

## Emergency Privacy Rule

The parent may remove or generalize private details immediately before human approval. This is a safety correction, not a domain policy change.

## Computed Gate Evidence

Golden and CI acceptance comes from semantic validators and executable tests. A manually written `overall_status: pass` cannot override a failed approval, reference, or cross-artifact check.
