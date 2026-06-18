---
name: kc-lesson-turn
description: Use when a Korean Connection teacher has supplied lesson context and needs options, trade-offs, and an AI recommendation before approving lesson scope.
---

# KC Lesson Turn

Create a human-readable Teacher Decision Card. Do not generate lesson materials.

## Workflow

1. Separate teacher facts from agent interpretations.
2. Diagnose the teaching problem in one sentence and cite available evidence.
3. Offer two to four relevant directions from `advance`, `review`, `mixed`, `vocabulary_focus`, `listening_focus`, `conversation_focus`, or `diagnostic`.
4. Show benefits, learner burden, risks, grammar treatment, and vocabulary scope.
5. Recommend one option with rationale and limitations.
6. List decisions still required before scope can lock.

## Advisory Specialist Exception

Front-stage is parent-led by default. When the teacher supplies an explicit learner-context or lesson-result path and asks for evidence-based reasoning, the parent may call `kc_learner_state_analyst` and `kc_learning_progression_planner` in read-only advisory mode. Their results are proposals only. They cannot lock scope, write workspace artifacts, or start `build_lesson`.

## Output

Use the Teacher Decision Card headings defined in `contracts/conversation/teacher_decision_card.md`. Keep the primary card in Korean; append machine-readable fields only when useful.

## Next Skill Handoff

- Recommended Next Skill: `kc-lesson-unknown` or `kc-lesson-scope-lock`
- Why: resolve an unknown or request explicit approval of a complete option
- Ready To Continue: yes | no
- Need Teacher Confirmation: yes
- Requires run_dir: no until the teacher authorizes a run or lock write
- Blocking Conditions: list decisions required for `ready_to_lock`
- Suggested Prompt: choose an option and confirm remaining scope values
