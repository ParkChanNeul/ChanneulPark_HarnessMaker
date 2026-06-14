# Learner Context Snapshot

```yaml
snapshot_id: "snapshot-friends-001"
learner_alias: "friends_learner"
level_band: "A1"
goals:
  - "ask casual questions and respond naturally when meeting peers"
active_situations:
  - "making_friends"
grammar_status:
  stable: []
  active_review:
    - target_id: "questions.basic"
      status: "guided"
      evidence: "fixture known_evidence.grammar"
    - target_id: "topic.marker"
      status: "controlled"
      evidence: "fixture known_evidence.grammar"
  needs_repair: []
conversation_status:
  strengths:
    - "completed a short greeting role-play"
  needs_practice:
    - skill_id: "reaction.simple"
      status: "modeled"
      evidence: "fixture known_evidence.conversation"
    - skill_id: "ask_back"
      status: "unseen"
      evidence: "agent_inferred from making_friends situation: conversation stops after one answer"
mission_history_summary:
  - "completed a short greeting role-play"
privacy_redactions:
  - "source fixture already generalized; no personal identifiers supplied"
evidence_notes:
  observed:
    - "grammar target questions.basic is guided"
    - "grammar target topic.marker is controlled"
    - "mission history contains a completed short greeting role-play"
  learner_reported:
    - "lesson goal is to ask casual questions and respond naturally when meeting peers"
  agent_inferred:
    - "ask-back and reaction timing should be prioritized because the making_friends situation breaks when conversation stops after one answer"
```

## Blockers

None.
