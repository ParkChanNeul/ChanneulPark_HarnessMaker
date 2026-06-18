# Approval Rules

## Purpose

Defines when the parent can write output directly and when teacher or governance approval is required.

## Parent-Owned Writes

The parent may write generated lesson artifacts, review reports, workspace handoffs, conversation cards, locks after approval, and proposed domain updates.

## Teacher Decision Gates

- Lesson generation requires a locked `lesson_scope_lock`.
- Homework-only follow-up requires approved homework in `post_lesson_teacher_card`.
- Next-lesson and progression outputs require a locked `next_lesson_decision_lock`.
- Generic continuation language cannot satisfy a missing gate.

## Governance Approval Required

Human approval is required before changing approved domain files, changing contract policy, promoting research to a default, changing agent responsibilities, relaxing privacy, or marking a target stable without evidence.

## Approval State

Governance-sensitive changes reference `approval_state`. Lesson decisions use the dedicated conversation lock contracts and session evidence.

## Revision Rule

Never silently overwrite a lock. Create a revision or superseding lock and preserve the earlier record.

## Partial Rerun Rule

Rerun the owning producer and downstream reviewer only. Lock revisions invalidate only artifacts controlled by changed fields.
