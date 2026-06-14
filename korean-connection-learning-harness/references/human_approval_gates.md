# Human Approval Gates

## Required Gates

Human approval is required for:

- changing approved files under `domain/`
- changing approved files under `contracts/`
- changing agent boundaries or required skills
- promoting a research insight to a default rule
- relaxing privacy rules
- using private learner details in any tracked artifact
- overriding mastery promotion rules

## Approval Artifact

Use `contracts/approval_state.md` for structured approval records.

## Gate Workflow

```text
proposal artifact
-> reviewer report
-> human decision
-> approval_state
-> parent applies approved scope only
```

## Rejection Workflow

If approval is rejected or needs revision:

- preserve the proposal in `_workspace/runs/`
- record the decision and reason
- do not apply the proposed domain or contract change
- rerun only the affected producer if a revision is requested

## Emergency Privacy Rule

If a privacy issue is found, the parent can remove or generalize private details immediately before human approval. This is a safety correction, not a domain policy change.
