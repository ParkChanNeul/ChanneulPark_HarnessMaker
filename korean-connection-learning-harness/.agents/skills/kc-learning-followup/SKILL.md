---
name: kc-learning-followup
description: Use when approved Korean Connection post-lesson decisions must become homework-only or full follow-up artifacts.
---

# KC Learning Follow-Up

## Read First

1. `domain/04_lesson_system/mission_and_followup.md`
2. `domain/04_lesson_system/homework_and_retention.md`
3. `contracts/lesson_result.md`
4. `contracts/conversation/post_lesson_teacher_card.md`
5. `contracts/conversation/next_lesson_decision_lock.md`
6. `contracts/weekly_learning_pack.md`
7. `contracts/homework_plan.md`
8. `contracts/quizlet_plan.md`
9. `contracts/follow_up_message.md`
10. `contracts/next_lesson_check.md`
11. `contracts/learner_state_delta.md`

## Scope: `homework_only`

Require observed lesson evidence and an approved homework option. Produce homework, Quizlet, follow-up message, and a weekly pack with null next-lesson fields. Do not create next lesson check, progression direction, or learner-state scheduling.

## Scope: `full_followup`

Additionally require a locked next-lesson decision. Produce homework-only artifacts plus next lesson check and evidence-supported state/progression handoffs.

## Decision Rules

- Base follow-up on observed evidence, not planned coverage.
- Preserve teacher-selected workload, direction, and prior-target treatment.
- Do not turn `carrier` into explicit review.
- Keep homework small and privacy-safe.
- Promote no mastery state without evidence.

## Output

Return proposed artifacts, source card, next-lock reference when required, follow-up scope, evidence paths, and blockers. Do not write final files.
