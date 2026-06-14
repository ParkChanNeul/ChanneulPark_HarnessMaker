# Mission History Schema

## Purpose

Records mission and homework attempts as evidence for retention, motivation, and transfer.

## Mission Record

```yaml
mission_id: "mission id"
assigned_after_lesson: "lesson id"
situation: "real-life or simulated situation"
target_language:
  grammar: []
  expressions: []
  conversation_skills: []
task: "what the learner should do"
difficulty: "low | medium | high"
support_materials:
  - "homework, Quizlet, message, or deck ref"
learner_result:
  status: "not_assigned | assigned | attempted | completed | skipped | unknown"
  evidence: []
  blockers: []
followup_decision: "review | retry | extend | retire | unknown"
```

## Design Rule

Missions should be small enough that the learner can realistically attempt them between lessons. A mission can be simulated if real-world use is unsafe, awkward, or unavailable.
