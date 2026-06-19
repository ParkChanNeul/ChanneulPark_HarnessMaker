# Contract: Learner Context Snapshot

## Purpose

Captures the safe, current learner state used for one run.

## Producer

`kc_learner_state_analyst`.

## Consumers

`kc_learning_progression_planner`, `kc_lesson_architect`, `kc_practice_designer`, `kc_learning_followup_teacher`.

## Required Fields

```yaml
snapshot_id: "unique id"
learner_alias: "non-identifying handle"
level_band: "A0 | A1 | A2 | B1 | B2 | unknown"
goals: []
active_situations: []
language_target_status:
  stable: []
  active_review: []
  needs_repair: []
conversation_status:
  strengths: []
  needs_practice: []
mission_history_summary: []
privacy_redactions: []
evidence_notes:
  observed: []
  learner_reported: []
  agent_inferred: []
```

## Validation

Every inference must be labeled. The snapshot cannot expose real names, exact age, race, private accounts, or follower counts.
