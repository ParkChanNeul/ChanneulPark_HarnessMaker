---
name: kc-research-synthesis
description: "Synthesize Korean Connection research. Use for research notes, classroom observations, evidence-level labeling, teaching insight proposals, and research-to-domain intake."
---

# KC Research Synthesis

Use this skill when a research note or teaching observation may affect domain knowledge.

## Read First

1. `domain/06_research/evidence_levels.md`
2. `domain/06_research/insight_promotion_rules.md`
3. `domain/07_governance/source_priority.md`
4. `domain/02_language_map/source_catalog.json`
5. `domain/02_language_map/language_target.schema.json`
6. `contracts/research_insight_proposal.md`

## Workflow

1. Extract the claim and the teaching decision it would affect.
2. Label the evidence level.
3. Separate accessed source evidence, classroom observations, and interpretation.
4. Record source metadata only for material actually accessed.
5. Identify affected registries, Situation Packs, profiles, domain files, and contracts.
6. State expected learning benefit and risks.
7. Recommend reject, collect more evidence, or propose domain update.
8. Return a `research_insight_proposal`.

## Decision Rules

- Do not turn one anecdote into a standard.
- Do not promote private student context into general domain knowledge.
- Keep proposals actionable for lesson generation, follow-up, assessment, or privacy.
- If evidence conflicts with approved domain rules, preserve the conflict and follow source priority.
- Do not invent source IDs, document titles, URLs, retrieval dates, or completed-review claims.
- If official support is unavailable, recommend `status: draft`, `level.confidence: low`, and `source_refs: []`.

## Output

Return proposed insight contract content, evidence level, source notes, risks, recommendation, and blockers. Do not write final files.
