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
6. `domain/02_language_map/README.md`
7. `domain/02_language_map/registry_manifest.json`
8. `domain/03_situations/situation_pack_manifest.json`
9. `domain/04_profiles/profile_manifest.json`
10. `contracts/domain_update_proposal.md`
11. `contracts/approval_state.md`

## Workflow

1. Identify the requested domain, contract, or responsibility change.
2. Check source priority and whether the change is already covered.
3. Check affected agents, skills, contracts, and validation scripts.
4. For language-map changes, check canonical IDs, hard and soft prerequisites, source records, aliases, contextual migrations, Situation Pack references, profile overlays, and coverage impact.
5. Convert accepted insights into a `domain_update_proposal`.
6. Mark approval requirement and exact scope.
7. Return the proposal and do not apply changes unless the parent provides explicit approval.

## Decision Rules

- Current approved domain files outrank archived examples.
- Research proposals do not become standards without approval.
- Privacy rules can be tightened without expanding private data use; relaxing them needs explicit approval.
- Preserve backward compatibility or state migration needs.
- Keep `legacy_aliases.json` limited to exact 1:1 mappings; use `legacy_migrations.json` for context, splits, non-automatic cases, and manual review.
- New artifacts use only canonical target IDs, `language_targets`, and `situation_scope`.
- Missing official support for core grammar, register, or phonology is a blocker, not a reason to invent a source.

## Output

Return proposed update content, affected paths, approval requirement, compatibility notes, rollback notes, and blockers. Do not write final files.
