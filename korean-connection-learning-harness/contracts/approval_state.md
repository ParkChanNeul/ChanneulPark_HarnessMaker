# Contract: Approval State

## Purpose

Records human approval or rejection for governance-sensitive changes.

## Producer

Parent agent or human approver.

## Consumers

`kc_domain_curator`, parent agent, validators.

## Required Fields

```yaml
approval_state_id: "unique id"
proposal_ref: "domain update, contract change, privacy exception, or mastery promotion"
decision: "approved | rejected | needs_revision"
approver: "user or role"
decision_date: "YYYY-MM-DD"
scope: "exact files or artifacts covered"
notes: []
expires_after: "optional date or condition"
```

## Validation

Approval applies only to the stated scope. It cannot be generalized to future private data or unrelated domain changes.
