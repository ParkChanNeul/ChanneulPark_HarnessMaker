# Contract: Research Insight Proposal

## Purpose

Packages new research or observation before it can become domain knowledge.

## Producer

`kc_research_synthesizer`.

## Consumers

`kc_domain_curator`, parent agent.

## Required Fields

```yaml
research_insight_proposal_id: "unique id"
claim: "teaching insight"
evidence_level: "0 | 1 | 2 | 3 | 4"
source_notes: []
affected_domain_files: []
affected_contracts: []
expected_learning_benefit: "retention, transfer, clarity, etc."
risks_or_counterexamples: []
recommended_action: "reject | collect_more_evidence | propose_domain_update"
```

## Validation

Claims based on external or anecdotal evidence must not be written as approved standards.
