# Contract: Lesson Request

## Purpose

Starts an existing execution mode after front-stage routing has supplied its required approval contracts.

## Producer

Parent agent or user.

## Consumers

Parent orchestrator and relevant specialist agents.

## Required Fields

```yaml
request_id: "unique id"
mode: "build_lesson | render_materials | post_lesson_followup | review_outputs | research_to_domain | audit_domain | partial_rerun"
followup_scope: "homework_only | full_followup | null"
learner_alias: "non-identifying handle"
lesson_goal: "communicative goal"
target_situation: "situation id or label"
time_box_minutes: 30
known_inputs:
  lesson_scope_lock: "path or null"
  post_lesson_teacher_card: "path or null"
  next_lesson_decision_lock: "path or null"
  learner_context_snapshot: "path or null"
  lesson_result: "path or null"
constraints: []
```

## Validation

Front-stage routes are not values of `mode`. `build_lesson` requires the lesson lock. Homework-only requires the approved card. Full follow-up additionally requires the next lock.
