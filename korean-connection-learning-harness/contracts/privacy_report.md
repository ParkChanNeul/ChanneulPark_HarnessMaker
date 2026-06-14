# Contract: Privacy Report

## Purpose

Reports whether artifacts contain private or identifying learner details.

## Producer

`kc_privacy_auditor`.

## Consumers

Parent agent, `kc_assessment_reviewer`.

## Required Fields

```yaml
privacy_report_id: "unique id"
reviewed_artifacts: []
status: "pass | blocked"
findings:
  - severity: "blocker | major | minor"
    artifact: "path or id"
    detail_type: "name | exact_age | race | nationality | social_account | follower_count | private_context | other"
    evidence: "short excerpt or description"
    required_action: "remove | generalize | approve_with_reason"
redactions_recommended: []
```

## Validation

Any real identifying detail is a blocker unless the current user explicitly approves that exact use for an untracked output.
