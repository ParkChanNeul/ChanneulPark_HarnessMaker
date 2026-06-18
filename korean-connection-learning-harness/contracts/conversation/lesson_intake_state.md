# Contract: Lesson Intake State

## Purpose

Records known facts, unknowns, and workspace permissions before lesson scope is locked.

## Producer

Top-level parent using `kc-lesson-intake` or `kc-lesson-resume`.

## Consumers

`kc-lesson-turn`, `kc-lesson-unknown`, `kc-lesson-scope-lock`.

## Required Fields

```yaml
run_id: "optional until a workspace is approved"
conversation_state: "open | partial | ready_to_lock | locked"
teacher_request:
  raw_request: ""
  requested_output: []
known_context:
  learner_type: "new | existing | unknown"
  learner_level: ""
  lesson_duration_minutes: null
  target_situation: ""
  teacher_goal: ""
  previous_lesson_ref: null
unknowns:
  - unknown_id: "id"
    category: "scope category"
    blocking: true
    question: "teacher-facing question"
    answer: null
    resolution_status: "open | assumed | confirmed"
workspace:
  run_dir: null
  read_allowed: false
  write_allowed: false
```

## Validation

No run may be inferred. `read_allowed` requires an explicit run reference. `write_allowed` requires a teacher request to create a run or write a lock.
