---
name: kc-domain-curation
description: "Curate Korean Connection domain knowledge. Use for domain audits, source-priority decisions, contract drift checks, responsibility matrix updates, and domain update proposals."
---

# KC Domain Curation

Use this skill for domain governance, not routine lesson generation.

## Read First

1. `domain/07_governance/source_priority.md`
2. `domain/07_governance/approval_rules.md`
3. `domain/06_research/insight_promotion_rules.md`
4. `references/agent_responsibility_matrix.md`
5. `references/artifact_dependency_map.md`
6. `contracts/domain_update_proposal.md`
7. `contracts/approval_state.md`

## Workflow

1. Identify the requested domain, contract, or responsibility change.
2. Check source priority and whether the change is already covered.
3. Check affected agents, skills, contracts, and validation scripts.
4. Convert accepted insights into a `domain_update_proposal`.
5. Mark approval requirement and exact scope.
6. Return the proposal and do not apply changes unless the parent provides explicit approval.

## Decision Rules

- Current approved domain files outrank archived examples.
- Research proposals do not become standards without approval.
- Privacy rules can be tightened without expanding private data use; relaxing them needs explicit approval.
- Preserve backward compatibility or state migration needs.

## Output

Return proposed update content, affected paths, approval requirement, compatibility notes, rollback notes, and blockers. Do not write final files.
