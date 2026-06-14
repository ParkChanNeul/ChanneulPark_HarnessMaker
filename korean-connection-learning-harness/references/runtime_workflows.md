# Runtime Workflows

## Shared Runtime Rules

- The parent agent reads `.agents/skills/korean-connection-orchestrator/SKILL.md` before running the harness.
- The parent dispatches custom agents with explicit inputs, expected output contracts, evidence requirements, and completion criteria.
- Subagents do not write final files. They return proposed content and path recommendations.
- The parent writes `_workspace/` handoffs, compares conflicting evidence, requests follow-up when needed, and writes final artifacts.

## Mode: `build_lesson`

```text
lesson_request
-> kc_learner_state_analyst
-> kc_learning_progression_planner
-> kc_lesson_architect
-> kc_practice_designer
-> kc_student_experience_designer
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
-> parent writes approved artifacts
```

Completion requires `learner_context_snapshot`, `progression_plan`, `lesson_blueprint`, `practice_plan`, `student_deck_spec`, and `assessment_report`.

## Mode: `render_materials`

```text
lesson_blueprint + practice_plan + student_deck_spec
-> kc_student_experience_designer
-> parent renderer
-> material_manifest
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
```

Completion requires a `material_manifest` and a review result.

## Mode: `post_lesson_followup`

```text
lesson_result
-> kc_learning_followup_teacher
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
-> parent writes weekly learning pack and next lesson check
```

Completion requires `weekly_learning_pack`, `homework_plan`, `quizlet_plan`, `follow_up_message`, and `next_lesson_check`.

## Mode: `review_outputs`

```text
target artifacts
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
-> parent records pass, fixes, or blockers
```

Use this mode for quality checks without generating new lesson content.

## Mode: `research_to_domain`

```text
research note
-> kc_research_synthesizer
-> kc_domain_curator
-> human approval gate
-> parent applies approved domain changes only if requested
```

Research may propose. It does not silently rewrite approved domain knowledge.

## Mode: `audit_domain`

```text
domain + contracts + references + agents + skills
-> kc_domain_curator
-> kc_assessment_reviewer
-> optional kc_privacy_auditor
```

Use this mode to detect drift, missing contract coverage, and stale responsibilities.

## Mode: `partial_rerun`

```text
changed input
-> owning agent
-> downstream consumers only
-> reviewer
-> parent updates affected artifacts
```

Do not rerun upstream agents unless the changed input invalidates their evidence.

## Failure Handling

- Missing required input: stop and return a blocker with exact missing paths.
- Contract mismatch: rerun the owning producer with the reviewer finding.
- Privacy issue: block tracked output until the parent removes or generalizes the detail.
- Conflicting evidence: preserve both claims in `_workspace/` and follow source priority for the current run.
