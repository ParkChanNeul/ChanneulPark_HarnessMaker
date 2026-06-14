# Contract: Quizlet Plan

## Purpose

Prepares card content for spaced vocabulary and expression practice.

## Producer

`kc_learning_followup_teacher` or `kc_practice_designer`.

## Consumers

Parent agent, learner.

## Required Fields

```yaml
quizlet_plan_id: "unique id"
source_targets: []
sets:
  - set_name: "learner-facing set name"
    card_type: "reference | qna | mixed"
    cards:
      - front: "prompt"
        back: "answer"
        tags: []
review_notes: []
```

## Validation

Cards should support retrieval, not only recognition. Q&A cards should prompt production when possible.
