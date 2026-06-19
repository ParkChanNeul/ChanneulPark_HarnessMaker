---
name: korean-connection-orchestrator
description: Use when operating Korean Connection lesson conversations, approved lesson builds, material rendering, post-lesson follow-up, output review, research curation, domain audit, or partial reruns.
---

# Korean Connection Orchestrator

The top-level Codex agent is the parent orchestrator. There is no separate orchestrator agent TOML.

## Read First

1. `AGENTS.md`
2. `README.md`
3. `references/conversational_teacher_loop.md`
4. `references/conversation_state_machine.md`
5. `references/runtime_workflows.md`
6. `references/agent_registry.toml`
7. `references/agent_responsibility_matrix.md`
8. `references/artifact_dependency_map.md`
9. `references/human_approval_gates.md`
10. `domain/07_governance/source_priority.md`
11. `domain/07_governance/privacy.md`
12. `domain/02_language_map/README.md`
13. `domain/02_language_map/registry_manifest.json`
14. `domain/03_situations/situation_pack_manifest.json`
15. `domain/04_profiles/profile_manifest.json`

## Core Principles

```text
Situation-led
Culture-explained
Grammar-and-vocabulary tracked
Practice-repeated
Mastery-verified
Teacher-approved progression
```

## Routing Model

Front-stage conversational skill routing and back-stage execution modes are separate. A conversational route produces questions, options, or locks; it is not an execution mode and does not dispatch the production chain by default.

## Front-Stage Conversational Routing

- `lesson_intake` → `kc-lesson-intake`
- `lesson_resume` → `kc-lesson-resume`
- `lesson_turn` → `kc-lesson-turn`
- `lesson_unknown` → `kc-lesson-unknown`
- `lesson_scope_lock` → `kc-lesson-scope-lock`
- `post_lesson_reflection` → `kc-post-lesson-reflection`
- `next_lesson_decision` → `kc-next-lesson-decision`

### Bare Invocation

“다음 수업 만들어줘” or a partial situation request routes to `lesson_intake`. Do not call `build_lesson`.

### Non-linear Entry

Preserve supplied level, duration, situation, grammar, vocabulary count, and output preferences. Ask only for missing blockers. Rich input may route directly to `lesson_turn`, but it never bypasses teacher approval.

### Resume Safety

`lesson_resume` requires an exact `run_dir` or `run_id`. Never infer the most recent run, the only run, or a fixture.

### Unknown and Continue Safety

Unknown answers route to bounded choices and a recommendation. The phrase `continue does not approve` any missing lock field: “진행”, “계속”, “다음”, or “좋아” cannot bypass blockers.

### Advisory Specialist Exception

Front-stage uses no specialist agent by default. If an explicit learner-context or lesson-result path exists and the teacher asks for evidence-based reasoning, the parent may dispatch `kc_learner_state_analyst` and `kc_learning_progression_planner` in read-only advisory mode. Their findings remain proposals. They cannot write files, approve a lock, or trigger a build.

## Parent Responsibilities

1. Select a conversational route or execution mode.
2. Keep teacher facts, AI interpretation, recommendations, and approvals distinct.
3. Dispatch only agents approved in `references/agent_registry.toml`.
4. Provide explicit input paths, output contracts, and completion criteria.
5. Write final artifacts and lock revisions; subagents return proposals only.
6. Preserve teacher overrides through progression, architecture, follow-up, and assessment.
7. Run privacy review when identifying context appears.
8. Run semantic, cross-artifact, and executable acceptance validation before accepting a Golden or runtime assessment result.
9. Resolve lesson targets through the canonical registries and preserve the single `language_targets` and `situation_scope` interfaces.
10. Keep 1:1 legacy aliases separate from contextual or manual migrations.

## Execution Modes

### `build_lesson`

Require a `lesson_scope_lock` path with `lock_status: locked`, `approved_by_teacher: true`, non-empty `approval_evidence`, and `unresolved_blockers: []`.

If the gate fails, return exactly:

```text
BLOCKED: approved lesson_scope_lock is required
```

Recommend `kc-lesson-intake`, `kc-lesson-turn`, or `kc-lesson-scope-lock`; do not dispatch the specialist chain.

After the gate passes, run learner-state analysis, progression planning, lesson architecture, practice design, student experience design, assessment review, and conditional privacy audit. Every downstream artifact must reference the approved lock and preserve overrides.

### `render_materials`

Render from an approved lesson blueprint, practice plan, and deck spec. Run student-experience design, parent rendering, assessment review, and conditional privacy audit. Rendering cannot change locked lesson targets.

### `post_lesson_followup`

Choose one scope; these are subscopes, not new execution modes.

- `homework_only`: requires a Post-Lesson Teacher Card with an approved homework option and approval evidence. May create homework, Quizlet, follow-up message, and a weekly pack without next-lesson fields.
- `full_followup`: requires the approved Post-Lesson Teacher Card plus a locked `next_lesson_decision_lock`. May additionally create `next_lesson_check`, learner-state scheduling, and next-progression-related artifacts.

A lesson result or teacher note first routes through `post_lesson_reflection`. Do not auto-select homework or next direction.

### `review_outputs`

Run assessment review and conditional privacy audit against supplied artifacts. Review lock consistency when lesson or follow-up artifacts are present.

### `research_to_domain`

Run research synthesis, source verification, language-map coverage and migration assessment, domain curation, and the existing human approval gate. Research cannot silently rewrite approved domain knowledge. Never invent source metadata or mark inaccessible material reviewed.

### `audit_domain`

Run domain curation, assessment review, and conditional privacy audit to identify drift and proposed fixes.

### `partial_rerun`

Identify the changed input, rerun its owner and downstream consumers, then review. A lock change creates a revision or superseded lock; never silently mutate approval history.

## Failure Handling

- Missing input: stop with the exact missing path or contract.
- Missing lesson lock: return the exact build blocker and front-stage handoff.
- Missing next lock in full follow-up: downgrade only if the teacher explicitly requests `homework_only`; otherwise block.
- Contract failure: rerun the owning producer with reviewer evidence.
- Privacy blocker: generalize the detail and rerun privacy review.
- Conflicting evidence: preserve both claims and follow source priority.

## Completion Criteria

A conversation is complete when it reaches the requested teacher decision boundary. An execution run is complete only when its required approval contracts, generated artifacts, reviewer status, privacy status, canonical language targets, canonical situation scope, canonical vocabulary scope, source requirements, and cross-artifact links are valid. Target-ID-only practice coverage is insufficient: prompts or examples must visibly realize the target. A manually written `overall_status: pass` is not evidence; calculated validation results control acceptance.
