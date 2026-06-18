---
name: kc-next-lesson-decision
description: Use when a Korean Connection teacher explicitly chooses the next lesson direction and how prior grammar or vocabulary should be reviewed, reused, transferred, or deferred.
---

# KC Next Lesson Decision

Lock the teacher's next-lesson choice after reflection.

## Decisions

Select a direction from `advance`, `review`, `mixed`, `transfer`, `vocabulary_focus`, `listening_repair`, or `conversation_repair`. Assign each prior target one treatment: `explicit_review`, `retrieval`, `carrier`, `transfer`, or `defer`.

Natural reuse as `carrier` is not explicit review. Preserve a teacher decision to advance without converting it into a review lesson.

## Lock Rule

Require explicit approval evidence and no unresolved blockers. Do not interpret a generic continuation phrase as approval. Revise or supersede an existing lock instead of silently overwriting it.

## Next Skill Handoff

- Recommended Next Skill: `post_lesson_followup` with `full_followup`
- Why: the locked next direction now authorizes next-lesson check and progression-related outputs
- Ready To Continue: yes only when the lock is valid
- Need Teacher Confirmation: no after valid explicit approval; otherwise yes
- Requires run_dir: yes
- Blocking Conditions: missing direction, target treatment, homework scope, or approval evidence
- Suggested Prompt: run full_followup using the post-lesson card and next-lesson lock
