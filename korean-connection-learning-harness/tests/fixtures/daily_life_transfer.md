# Fixture: Daily Life Transfer

```yaml
request_id: "daily-transfer-001"
mode: "build_lesson"
learner_alias: "daily_life_learner"
current_level: "A1"
lesson_goal: "transfer ordering language into a convenience-store situation"
situation_scope:
  pack_ref: "shopping_checkout"
  sub_situation_ids: ["find_item", "ask_price", "pay_or_decline"]
known_evidence:
  language_targets:
    - target_ref: "chunk_request_noun_juseyo"
      status: "stable"
    - target_ref: "grammar_copula_ieyo_yeyo"
      status: "active_review"
    - target_ref: "particle_subject_iga"
      status: "active_review"
    - target_ref: "chunk_how_much_eolmayeyo"
      status: "needs_repair"
privacy_notes:
  - "no private learner data"
```
