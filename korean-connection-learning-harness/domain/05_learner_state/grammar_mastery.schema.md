# Language Target Mastery Schema

## Purpose

Tracks canonical language targets as cumulative skills rather than one-time lesson topics.

## Target Record

```yaml
target_ref: "canonical language target id"
display_name: "short learner-facing label"
function: "what the learner can do with it"
level_band: "A0 | A1 | A2 | B1 | B2 | C1 | C2 | special_content"
status: "unseen | introduced | controlled | guided | independent | transfer_attempted | stable | needs_repair"
last_seen_lesson: "lesson id or null"
next_review_due: "date or lesson slot"
evidence:
  retrieval:
    count: 0
    notes: []
  production:
    count: 0
    notes: []
  transfer:
    count: 0
    notes: []
common_errors:
  - "error pattern"
repair_plan:
  - "next practice move"
```

## Promotion Rule

Do not promote a target to `stable` until the learner has produced it independently in a non-identical situation and has retrieved it in a later lesson or follow-up.

## Repair Rule

If a learner repeatedly recognizes a target but cannot produce it, the status is `guided` or `needs_repair`, not `stable`.
