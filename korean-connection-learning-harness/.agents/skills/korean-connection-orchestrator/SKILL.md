---
name: korean-connection-orchestrator
description: "Operate Korean Connection Learning Harness V2. Use for build_lesson, render_materials, post_lesson_followup, review_outputs, research_to_domain, audit_domain, and partial_rerun workflows."
---

# Korean Connection Orchestrator

This skill coordinates the Korean Connection Learning Harness V2. The top-level Codex agent is the parent orchestrator. There is no separate orchestrator agent TOML.

## Read First

1. `AGENTS.md`
2. `README.md`
3. `references/runtime_workflows.md`
4. `references/agent_responsibility_matrix.md`
5. `references/artifact_dependency_map.md`
6. `references/human_approval_gates.md`
7. `domain/07_governance/source_priority.md`
8. `domain/07_governance/privacy.md`

## Core Principle

```text
Situation-led / Culture-explained / Grammar-tracked / Practice-repeated / Mastery-verified
```

## Parent Responsibilities

1. Select the mode.
2. Identify required inputs and missing blockers.
3. Dispatch custom agents with explicit input paths, output contracts, and completion criteria.
4. Store intermediate handoffs under `_workspace/runs/` when useful.
5. Compare conflicting evidence and follow source priority.
6. Request follow-up from producer agents when reviewers find blockers.
7. Run privacy audit when learner-identifying or archive-derived context appears.
8. Write final artifacts only after required review.

## Modes

### `build_lesson`

Run:

1. `kc_learner_state_analyst`
2. `kc_learning_progression_planner`
3. `kc_lesson_architect`
4. `kc_practice_designer`
5. `kc_student_experience_designer`
6. `kc_assessment_reviewer`
7. `kc_privacy_auditor` when triggered

Required outputs: learner snapshot, progression plan, lesson blueprint, practice plan, student deck spec, assessment report.

### `render_materials`

Run `kc_student_experience_designer`, parent rendering, `kc_assessment_reviewer`, and conditional privacy audit.

Required outputs: design manifest, material manifest, assessment report.

### `post_lesson_followup`

Run `kc_learning_followup_teacher`, `kc_assessment_reviewer`, and conditional privacy audit.

Required outputs: weekly learning pack, homework plan, Quizlet plan, follow-up message, next lesson check, proposed state delta.

### `review_outputs`

Run `kc_assessment_reviewer` and conditional privacy audit against supplied artifacts.

Required output: assessment report and, if triggered, privacy report.

### `research_to_domain`

Run `kc_research_synthesizer`, then `kc_domain_curator`, then stop at human approval unless the user explicitly asks to apply approved changes.

Required outputs: research insight proposal and domain update proposal.

### `audit_domain`

Run `kc_domain_curator`, `kc_assessment_reviewer`, and conditional privacy audit.

Required outputs: drift notes, assessment report, and proposed fixes.

### `partial_rerun`

Identify the changed input, rerun the owning agent and downstream consumers only, then rerun the reviewer.

## Failure Handling

- Missing input: stop with exact missing path and required contract.
- Contract failure: rerun the owning producer with the reviewer finding.
- Privacy blocker: remove or generalize the detail, then rerun privacy audit.
- Conflicting evidence: preserve both claims in `_workspace/` and follow source priority.

## Completion Criteria

A run is complete only when required contracts exist in proposed or written form, reviewer blockers are resolved, privacy blockers are resolved, and the parent reports validation status.
