# Learner Model Schema

## Purpose

Defines the minimum learner snapshot needed to plan Korean Connection lessons without storing real student-identifying information in tracked files.

## Required Fields

```yaml
learner_alias: "non-identifying handle"
current_level: "A0 | A1 | A2 | B1 | B2 | unknown"
learning_goals:
  - "specific communicative goal"
priority_situations:
  - "situation id or short label"
known_constraints:
  time_per_week: "optional"
  preferred_material_style: "optional"
  accessibility_needs: "optional"
grammar_mastery_refs:
  - "grammar target id"
conversation_mastery_refs:
  - "conversation skill id"
mission_history_refs:
  - "mission id"
last_lesson_result_ref: "lesson result id or null"
privacy_notes:
  - "what was redacted or generalized"
```

## Privacy Rule

Use aliases, ranges, generalized goals, and learning evidence. Do not store legal names, exact age, private social accounts, follower counts, race, nationality, contact details, payment details, or sensitive life context.

## Planning Use

The learner state analyst may infer learning needs from evidence, but must label each inference as `observed`, `learner_reported`, or `agent_inferred`.
