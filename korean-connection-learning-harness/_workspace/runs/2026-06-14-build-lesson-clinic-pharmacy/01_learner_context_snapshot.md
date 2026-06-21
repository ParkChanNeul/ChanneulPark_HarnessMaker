# Learner Context Snapshot

```yaml
snapshot_id: "snapshot-clinic-pharmacy-001"
learner_alias: "kc_reference_learner"
level_band: "A1"
goals:
  - "handle short Korean service and appointment moments without freezing"
  - "state one simple symptom and ask one safe next-step question"
active_situations:
  - "pt_gym"
  - "clinic_pharmacy"
  - "work_and_appointments"
grammar_status:
  stable: []
  active_review:
    - target_id: "request_juseyo"
      display_name: "-아/어 주세요 for clear requests"
      status: "guided"
      evidence: "Week 1 taxi request and Week 5 PT/gym slow/repeat/stop requests"
    - target_id: "do_dwaeyo"
      display_name: "-아/어도 돼요? for permission or checking"
      status: "introduced"
      evidence: "Week 3 shopping permission check and Week 5 rest permission"
    - target_id: "polite_yo"
      display_name: "-요 polite short answers"
      status: "guided"
      evidence: "Week 1-5 student-facing materials use short polite service lines"
    - target_id: "reaction_basic"
      display_name: "simple reaction before continuing"
      status: "modeled"
      evidence: "Week 2 fan interaction and Week 4 creator reaction review"
  needs_repair:
    - target_id: "repair_when_confused"
      display_name: "ask for repeat under pressure"
      status: "needs_retrieval"
      evidence: "Week 5 mission asks which safety line came out fastest; delayed evidence unknown"
conversation_status:
  strengths:
    - "can work with short mission-first Korean lines"
    - "has repeated role-play exposure across taxi, fan, cafe/shopping, creator, and PT/gym situations"
  needs_practice:
    - skill_id: "repair_when_confused"
      status: "guided"
      evidence: "Week 5 repeat/slow-down lines need delayed retrieval in a new situation"
    - skill_id: "confirm_next_step"
      status: "introduced"
      evidence: "Week 5 permission/check language can transfer to pharmacy or clinic"
    - skill_id: "concise_information_first"
      status: "unseen"
      evidence: "agent_inferred from clinic_pharmacy situation pressure"
mission_history_summary:
  - "Week 5 private mission: choose one PT/gym line or rehearse it privately before the next session"
  - "No live post-lesson result was supplied, so mission completion is unknown"
privacy_redactions:
  - "Week 1-4 archive context was generalized to curriculum sequence only"
  - "No legal names, exact age, nationality, social-account details, medical history, diagnosis, or medication names are stored"
evidence_notes:
  observed:
    - "Week 1: taxi survival with request and confusion repair"
    - "Week 2: fan interaction with reaction language"
    - "Week 3: cafe/shopping with short service flow and permission checks"
    - "Week 4: creator voice levels and cumulative review"
    - "Week 5: PT/gym safe request, repeat, pause, pain, and stop language"
  learner_reported: []
  agent_inferred:
    - "clinic_pharmacy is the next useful transfer because it reuses safety, repeat, and permission language from Week 5"
    - "symptom reporting should be introduced as a compact, generic pattern rather than as real medical disclosure"
```

## Blockers

None.

## Privacy Trigger

Privacy audit is required because archive material was consulted and the next situation is health-adjacent. The lesson uses only generic symptom examples and private rehearsal options.
