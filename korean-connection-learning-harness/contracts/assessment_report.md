# Contract: Assessment Report

## Purpose

Reviews artifacts against learning quality, contract completeness, teacher authority, and safety.

## Producer

`kc_assessment_reviewer`.

## Consumers

Parent agent, responsible producer agent.

## Required Fields

```yaml
assessment_report_id: "unique id"
reviewed_artifacts: []
overall_status: "pass | pass_with_notes | blocked"
findings: []
contract_checks: {passed: [], failed: []}
learning_checks: {passed: [], failed: []}
approval_checks:
  lesson_scope_lock_valid: null
  teacher_overrides_preserved: null
  followup_scope_valid: null
  next_lesson_decision_lock_valid: null
privacy_checks: {passed: [], failed: []}
```

## Validation

Assessment cites exact artifacts, distinguishes blockers from notes, and blocks missing or inconsistent teacher approval gates. Golden assessment reports are generated from semantic and cross-artifact validation; a manually edited pass value is invalid.
