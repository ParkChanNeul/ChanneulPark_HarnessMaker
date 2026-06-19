# Runtime Workflows

## Shared Runtime Rules

- The parent reads `.agents/skills/korean-connection-orchestrator/SKILL.md` before running the harness.
- Front-stage conversational routing is separate from execution modes.
- The parent dispatches approved custom agents with explicit inputs, expected contracts, evidence requirements, and completion criteria.
- Subagents do not write final files. The parent writes handoffs, compares evidence, requests follow-up, and writes final artifacts.

## Front-Stage Conversational Routing

```text
bare request -> lesson_intake
rich input -> lesson_turn
unknown choice -> lesson_unknown
explicit run -> lesson_resume
teacher approval -> lesson_scope_lock
lesson result or notes -> post_lesson_reflection
teacher next-direction approval -> next_lesson_decision
```

Front-stage runs no specialist by default. With an explicit learner-context or lesson-result path and a teacher request for evidence, learner-state and progression agents may return read-only advisory findings. Advice cannot approve scope or start a build.

## Mode: `build_lesson`

```text
locked lesson_scope_lock
-> kc_learner_state_analyst
-> kc_learning_progression_planner
-> kc_lesson_architect
-> kc_practice_designer
-> kc_student_experience_designer
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
-> parent writes approved artifacts
```

Without a valid lock, return `BLOCKED: approved lesson_scope_lock is required` and do not dispatch agents. Completion requires learner snapshot, progression plan, lesson blueprint, practice plan, student deck spec, and assessment report, all consistent with the lock.

## Mode: `render_materials`

```text
approved lesson_blueprint + practice_plan + student_deck_spec
-> kc_student_experience_designer
-> parent renderer
-> material_manifest
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
```

Rendering cannot change locked targets. Completion requires material manifest and review result.

## Mode: `post_lesson_followup`

A lesson result or teacher note first produces a Post-Lesson Teacher Card.

### Scope: `homework_only`

Requires an approved homework option in that card. Produces weekly pack without next-lesson fields, homework plan, Quizlet plan, and follow-up message.

### Scope: `full_followup`

Additionally requires a locked `next_lesson_decision_lock`. May produce next lesson check, evidence-supported state delta, and next-progression handoffs.

Both scopes run `kc_learning_followup_teacher`, `kc_assessment_reviewer`, and conditional privacy audit.

## Mode: `review_outputs`

```text
target artifacts
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
-> parent records pass, fixes, or blockers
```

Review lock consistency when lesson or follow-up artifacts are present.

## Mode: `research_to_domain`

```text
verified source catalog entry or research note
-> kc_research_synthesizer
-> language-map coverage and migration assessment
-> kc_domain_curator
-> human approval gate
-> parent applies approved changes only when requested
```

Research may propose. It does not silently rewrite approved domain knowledge. Language-map work must preserve the common target interface, canonical situation scope, registry IDs, source verification status, and the alias-versus-migration boundary.

## Mode: `audit_domain`

```text
domain + contracts + references + agents + skills
-> kc_domain_curator
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
```

Use this mode to detect drift, missing contract coverage, stale responsibilities, and registry mismatches.

## Mode: `partial_rerun`

```text
changed input
-> owning agent
-> downstream consumers only
-> reviewer
-> parent updates affected artifacts
```

A lock change creates a revision or superseding lock. Do not silently mutate approval history.

## Failure Handling

- Missing input: stop with exact paths and required contract.
- Missing lesson lock: return the exact build blocker and recommend the relevant front-stage skill.
- Missing next lock: allow only explicitly requested `homework_only`; otherwise block.
- Contract mismatch: rerun the owning producer with reviewer evidence.
- Privacy issue: block tracked output until the parent removes or generalizes the detail.
- Conflicting evidence: preserve both claims and follow source priority.

## Validation Workflow

```text
validate_structure
-> validate_language_map
-> render_language_map_coverage --check
-> validate_contracts
-> validate_agent_boundaries
-> validate_semantic_contracts
-> validate_golden_run
-> validate_conversational_runtime
-> render_golden_assessment --check
-> unittest discover
-> privacy and core-term checks
```

`validate_contracts` checks documentation structure and canonical field definitions. Artifact values are parsed and checked by the semantic and Golden validators. The conversational runtime validator does not call the full harness validator, preventing recursive execution.

## Test Artifact Roles

- Markdown Acceptance Scenario: human-readable requirement.
- Executable Unit Test: proves pass and fail behavior.
- Golden Fixture: complete valid example flow.
- Golden Assessment: validator-computed report for that flow.
