# Contract: Assessment Report

## Purpose

Reviews artifacts against learning quality, contract completeness, and safety.

## Producer

`kc_assessment_reviewer`.

## Consumers

Parent agent, responsible producer agent.

## Required Fields

```yaml
assessment_report_id: "unique id"
reviewed_artifacts: []
overall_status: "pass | pass_with_notes | blocked"
findings:
  - severity: "blocker | major | minor | note"
    artifact: "path or id"
    issue: "what failed"
    evidence: "specific evidence"
    required_fix: "smallest fix"
contract_checks:
  passed: []
  failed: []
learning_checks:
  passed: []
  failed: []
privacy_checks:
  passed: []
  failed: []
```

## Validation

Assessment must cite exact artifacts and distinguish blockers from improvement notes.
