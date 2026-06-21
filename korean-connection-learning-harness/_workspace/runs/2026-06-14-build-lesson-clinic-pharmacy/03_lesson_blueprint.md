# Lesson Blueprint

```yaml
lesson_blueprint_id: "blueprint-clinic-pharmacy-001"
lesson_title: "Say the Symptom, Check the Next Step"
learner_alias: "kc_reference_learner"
situation: "clinic_pharmacy"
lesson_promise: "You can say one simple symptom, ask for repeat if needed, and check one next step at a clinic or pharmacy."
new_targets:
  - target_id: "symptom.bodypart_apayo"
    learner_label: "[body part] + 이/가 아파요"
    examples:
      - "머리가 아파요."
      - "목이 아파요."
review_targets:
  - "do_dwaeyo"
  - "request_juseyo"
  - "polite_yo"
  - "reaction_basic"
retrieval_targets:
  - "pt_gym.repeat_request"
  - "pt_gym.pain_stop"
transfer_targets:
  - target_id: "do_dwaeyo"
    transfer_context: "PT/gym rest permission -> pharmacy medicine or next-step check"
  - target_id: "request_juseyo"
    transfer_context: "taxi/PT requests -> clinic instruction repair"
  - target_id: "symptom.bodypart_apayo"
    transfer_context: "pain signal -> symptom report"
conversation_skill_targets:
  - "repair_when_confused"
  - "confirm_next_step"
  - "concise_information_first"
culture_point:
  topic: "key fact first"
  function: "explains why one short symptom plus one check question can sound helpful rather than too little"
lesson_flow:
  - stage: "warmup"
    purpose: "check Week 5 private mission and retrieve slow/repeat/pain lines without storing private details"
  - stage: "model"
    purpose: "hear the clinic/pharmacy minimum chain: symptom, time clue, repeat request, check"
  - stage: "controlled"
    purpose: "substitute body parts into `[body part] + 이/가 아파요`"
  - stage: "guided"
    purpose: "choose the right next line: time clue, repeat request, or check question"
  - stage: "roleplay"
    purpose: "practice pharmacy and clinic mini exchanges with generic symptoms only"
  - stage: "transfer"
    purpose: "move Week 5 permission and repeat tools into a health-service context"
  - stage: "wrap"
    purpose: "choose a private rehearsal mission and define next-lesson evidence"
assessment_evidence_to_collect:
  - "Can retrieve at least one Week 5 line without a model"
  - "Can produce `[body part] + 이/가 아파요` with two generic body parts"
  - "Can add `어제부터요` or `오늘 아침부터요` after the symptom with support"
  - "Can ask `다시 한 번 말해 주세요` when staff speech is fast"
  - "Can produce `이거 먹어도 돼요?` or another `-아/어도 돼요?` check in transfer"
  - "Can complete one role-play without over-explaining or using private medical details"
override_reason: null
```

## Lesson Boundary

This lesson is language practice, not medical advice. Do not ask for real diagnoses, medication names, medical history, or sensitive personal details. Use generic examples or private rehearsal.

## Teacher Note

Keep the culture point under one minute: concise information helps staff respond. Then return to production practice.
