# Conversational Runtime Audit

## Audit Scope

- Repository root: `/Volumes/위콜라보/ChanneulPark_HarnessMaker`
- Harness target: `korean-connection-learning-harness/`
- Baseline branch: `main`
- Baseline commit: `e4d8b9178cd81e5de1c9c53b2dc577baebc374bb`
- Existing italki repository was not read or modified during this change.

## Existing Linear Entry

The original orchestrator exposed `build_lesson` directly from a lesson request. The chain moved from `lesson_request` to learner analysis, progression planning, lesson architecture, practice, student experience, and assessment without a conversation contract that proved the teacher had selected and approved the scope.

`post_lesson_followup` likewise accepted a `lesson_result` and allowed the follow-up agent to choose homework and next-lesson direction in one step.

## Teacher Approval Gaps

- Bare requests could be interpreted as permission to build.
- The progression planner chose sequence, review, retrieval, and transfer targets without a teacher-owned scope lock.
- The lesson architect still described target selection as part of its role.
- A lesson result could trigger homework and next-lesson planning without a post-lesson teacher decision.
- Existing contracts represented generated artifacts but not conversational uncertainty, recommendation, approval evidence, or lock revision.

## Required Lock Gates

- `lesson_scope_lock`: required before `build_lesson` dispatches specialist agents.
- approved `post_lesson_teacher_card`: sufficient for `homework_only` outputs.
- `next_lesson_decision_lock`: additionally required for `full_followup`, `next_lesson_check`, learner-state scheduling, and next-progression results.

## Existing Agents Preserved

All current specialist agents remain approved and reusable. No conversational agent TOML is added. The top-level parent runs front-stage skills directly.

Rules change for:

- `kc_learning_progression_planner`: advisory options before lock; approved-plan structuring after lock.
- `kc_lesson_architect`: approved target operationalization only.
- `kc_learning_followup_teacher`: post-lesson card and follow-up scope aware.
- `kc_assessment_reviewer`: validates teacher approval gates and lock consistency.

## Compatible Execution Modes

The existing execution modes remain unchanged:

- `build_lesson`
- `render_materials`
- `post_lesson_followup`
- `review_outputs`
- `research_to_domain`
- `audit_domain`
- `partial_rerun`

The seven conversational steps are front-stage routes, not execution modes.
