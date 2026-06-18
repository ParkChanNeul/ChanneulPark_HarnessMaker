---
name: kc-lesson-scope-lock
description: Use when a Korean Connection teacher explicitly approves a complete lesson direction and asks to lock scope before specialist lesson generation.
---

# KC Lesson Scope Lock

Create an executable lesson contract only after explicit teacher approval.

## Lock Preconditions

Require learner level or bounded range, duration, situation, mode, new grammar decision, review decision, conversation goal, vocabulary scope, and material scope. Empty review grammar is allowed when the teacher explicitly chooses no separate review.

Approval evidence must quote or faithfully summarize the teacher's decision. Generic “진행”, “계속”, “좋아”, or “다음” does not approve an incomplete scope.

## Write Rule

Write under `_workspace/runs/<run_id>/00_conversation/lesson_scope_lock.md` only when the teacher provides a run directory, requests a new run, or explicitly authorizes lock creation. Do not silently overwrite a locked contract. Create a revision or mark the old lock superseded.

## Build Readiness

A build is ready only when `lock_status: locked`, `approved_by_teacher: true`, `approval_evidence` is non-empty, and `unresolved_blockers: []`.

## Next Skill Handoff

- Recommended Next Skill: `build_lesson`
- Why: specialist agents may operationalize the teacher-approved scope
- Ready To Continue: yes only for a valid locked contract
- Need Teacher Confirmation: no after explicit valid approval; otherwise yes
- Requires run_dir: yes for writing the lock and build artifacts
- Blocking Conditions: any missing required scope field or unresolved blocker
- Suggested Prompt: run `build_lesson` with the locked contract path
