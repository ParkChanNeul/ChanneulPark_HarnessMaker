---
name: kc-learner-state-analysis
description: "Analyze Korean Connection learner state. Use for learner context snapshots, lesson-result intake, grammar mastery updates, conversation mastery updates, mission history, and privacy-safe learner summaries."
---

# KC Learner State Analysis

Use this skill when a run needs a safe learner snapshot or proposed state update.

## Read First

1. `domain/05_learner_state/learner_model.schema.md`
2. `domain/05_learner_state/grammar_mastery.schema.md`
3. `domain/05_learner_state/conversation_mastery.schema.md`
4. `domain/05_learner_state/mission_history.schema.md`
5. `domain/07_governance/privacy.md`
6. `contracts/learner_context_snapshot.md`
7. `contracts/learner_state_delta.md`

## Workflow

1. Inventory supplied inputs: lesson request, prior snapshot, lesson result, mission history, teacher notes, and available evidence.
2. Remove or generalize identifying details before analysis.
3. Separate facts into `observed`, `learner_reported`, and `agent_inferred`.
4. Summarize current grammar targets by status.
5. Summarize conversation skills by status.
6. Summarize mission history and between-lesson behavior.
7. Identify missing evidence that affects the next lesson.
8. Return a `learner_context_snapshot` and, when evidence supports it, a proposed `learner_state_delta`.

## Decision Rules

- Use `unknown` instead of inventing missing learner state.
- Do not mark grammar or conversation targets stable without delayed retrieval or transfer evidence.
- If source material includes private biography, exact age, race, nationality, social-account context, or follower counts, request privacy audit.
- Keep the pedagogical need and remove the identifying detail.

## Output

Return proposed contract content, evidence paths, assumptions, blockers, and privacy redactions. Do not write final files.
