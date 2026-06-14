# Contract: Material Manifest

## Purpose

Lists all generated materials for a run.

## Producer

Parent agent.

## Consumers

`kc_assessment_reviewer`, `kc_learning_followup_teacher`.

## Required Fields

```yaml
material_manifest_id: "unique id"
run_id: "id"
materials:
  - path: "path"
    type: "student_deck | html | homework | quizlet | followup | review | other"
    source_contract: "path or id"
    intended_user: "student | teacher | parent | reviewer"
status: "draft | reviewed | approved | blocked"
known_gaps: []
```

## Validation

Every material needs a source contract and intended user.
