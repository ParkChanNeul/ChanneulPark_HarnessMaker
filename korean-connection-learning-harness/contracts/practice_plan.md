# Contract: Practice Plan

## Purpose

Turns a lesson blueprint into repeated retrieval, production, and transfer practice.

## Producer

`kc_practice_designer`.

## Consumers

`kc_student_experience_designer`, `kc_learning_followup_teacher`, `kc_assessment_reviewer`.

## Required Fields

```yaml
practice_plan_id: "unique id"
source_blueprint: "path or id"
practice_ladder:
  controlled: []
  guided: []
  independent: []
  transfer: []
retrieval_prompts: []
roleplay_variations: []
error_repair_prompts: []
homework_seed: []
quizlet_seed: []
evidence_capture_points: []
```

## Validation

At least one independent production task and one transfer task are required unless the lesson request explicitly says diagnostic-only.
