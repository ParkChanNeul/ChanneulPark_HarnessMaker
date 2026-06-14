# Contract: Learner State Delta

## Purpose

Records how a run should update learner state.

## Producer

`kc_learning_followup_teacher` or `kc_assessment_reviewer`.

## Consumers

Parent agent, next `kc_learner_state_analyst` run.

## Required Fields

```yaml
delta_id: "unique id"
source_artifact: "lesson_result, assessment_report, or follow_up_message path"
grammar_updates:
  - target_id: "id"
    from_status: "status"
    to_status: "status"
    evidence: []
conversation_updates:
  - skill_id: "id"
    from_status: "status"
    to_status: "status"
    evidence: []
mission_updates: []
review_schedule_updates: []
approval_needed:
  - "promotion or governance decision"
```

## Validation

No status may be promoted without evidence. `stable` requires delayed retrieval or transfer evidence.
