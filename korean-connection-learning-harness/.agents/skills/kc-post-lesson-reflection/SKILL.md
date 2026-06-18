---
name: kc-post-lesson-reflection
description: Use when a Korean Connection teacher supplies lesson observations or a lesson_result and needs homework and next-lesson options before follow-up generation.
---

# KC Post-Lesson Reflection

Convert observed results into a Post-Lesson Teacher Card without changing learner state or deciding the next lesson.

## Workflow

1. Separate teacher observations from agent interpretations.
2. Compare planned targets with observed successes and breakdowns.
3. Mark evidence gaps rather than inventing mastery.
4. Offer bounded homework options.
5. Offer next-lesson options separately.
6. Recommend one homework option and one next-direction option with limitations.

An approved homework option enables `homework_only`. It does not authorize next-lesson outputs. `full_followup` still requires a locked `next_lesson_decision_lock`.

When an explicit lesson-result path exists and the teacher asks for evidence-based interpretation, the parent may use `kc_learner_state_analyst` in read-only advisory mode. The advisory result cannot mutate state or approve a decision.

## Next Skill Handoff

- Recommended Next Skill: `post_lesson_followup` with `homework_only`, or `kc-next-lesson-decision`
- Why: create approved homework artifacts or lock the separate next-lesson decision
- Ready To Continue: yes when the relevant teacher approval exists
- Need Teacher Confirmation: yes for homework choice and next direction
- Requires run_dir: yes for writing follow-up artifacts
- Blocking Conditions: unapproved homework option for homework_only; missing next lock for full_followup
- Suggested Prompt: approve a homework option and optionally choose the next lesson direction
