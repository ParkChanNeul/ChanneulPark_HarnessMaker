# Contract: Domain Update Proposal

## Purpose

Describes a proposed change to approved domain or contract files.

## Producer

`kc_domain_curator`.

## Consumers

Parent agent, human approver.

## Required Fields

```yaml
domain_update_proposal_id: "unique id"
source_insight_refs: []
target_files: []
change_summary: "what should change"
proposed_patch_summary: []
reason: "why this improves the harness"
backward_compatibility: []
approval_required: true
rollback_notes: []
```

## Validation

The proposal does not modify approved files by itself. It must wait for human approval.
