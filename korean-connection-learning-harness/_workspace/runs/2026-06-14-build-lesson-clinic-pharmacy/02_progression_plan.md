# Progression Plan

```yaml
progression_plan_id: "progression-clinic-pharmacy-001"
learner_alias: "kc_reference_learner"
planning_window: "next lesson"
primary_situation: "clinic_pharmacy"
new_target_candidates:
  - target_id: "symptom.bodypart_apayo"
    display_name: "[body part] + 이/가 아파요"
    function: "say one simple symptom clearly in a clinic or pharmacy"
    selected: true
    reason: "the learner already has `아파요` as a PT/gym safety line; this lesson transfers it into concise symptom reporting"
review_targets:
  - target_id: "do_dwaeyo"
    display_name: "-아/어도 돼요?"
    reason: "review Week 5 rest permission and transfer it to medicine or next-step checking"
  - target_id: "request_juseyo"
    display_name: "-아/어 주세요"
    reason: "review Week 1 and Week 5 request language through `다시 한 번 말해 주세요`"
  - target_id: "polite_yo"
    display_name: "short polite service answers"
    reason: "clinic/pharmacy service flow needs short polite information, not long explanations"
  - target_id: "reaction_basic"
    display_name: "small reaction before repair"
    reason: "use `아, 네` or `잠깐만요` before asking again when confused"
retrieval_targets:
  - target_id: "pt_gym.repeat_request"
    retrieval_type: "delayed recall in a new clinic/pharmacy role-play"
    prompt: "Staff speaks too quickly. Ask them to say it again."
  - target_id: "pt_gym.pain_stop"
    retrieval_type: "semantic transfer from pain/stop to symptom reporting"
    prompt: "What short line tells the key problem first?"
transfer_targets:
  - target_id: "do_dwaeyo"
    transfer_context: "from `잠깐 쉬어도 돼요?` in PT/gym to `이거 먹어도 돼요?` in pharmacy"
  - target_id: "request_juseyo"
    transfer_context: "from taxi/PT requests to clinic instruction repair"
  - target_id: "symptom.bodypart_apayo"
    transfer_context: "from `아파요` as urgent pain to `[body part] + 이/가 아파요` as main symptom"
conversation_skill_targets:
  - skill_id: "repair_when_confused"
    reason: "the learner needs a safe repeat request when staff speech is fast"
  - skill_id: "confirm_next_step"
    reason: "the learner should check one action without over-explaining"
  - skill_id: "concise_information_first"
    reason: "clinic/pharmacy interactions reward the key fact first"
blocked_targets:
  - target_id: "detailed_medical_history"
    reason: "out of scope and privacy-sensitive"
  - target_id: "honorific_si_production"
    reason: "recognition may appear in staff speech, but production is not needed for this lesson"
spiral_review_plan:
  - target_id: "request_juseyo"
    next_review: "slide 8 repeat request and role-play 2"
  - target_id: "do_dwaeyo"
    next_review: "slide 9 medicine/next-step check"
  - target_id: "symptom.bodypart_apayo"
    next_review: "end-of-lesson transfer and next lesson mission check"
next_lesson_rationale: "After Week 5 PT/gym, the learner has short safety requests but no generic symptom-reporting pattern. Clinic/pharmacy keeps the same pressure profile: fast staff speech, need for concise information, and a safe next-step check."
```

## Rejected Targets

- `schedule_change`: useful later in the same module, but it does not reuse Week 5 pain/safety language as directly.
- `making_friends.ask_back`: valuable module, but the user asked for the next lesson after Week 5 and the curriculum route from PT/gym points first to clinic/pharmacy transfer.
- `medical_vocabulary_list`: too broad and risks privacy/diagnosis drift.

## Evidence Paths

- `/Volumes/위콜라보/gstack/ChanneulPark_italki/curriculum/situation_map.md`
- `/Volumes/위콜라보/gstack/ChanneulPark_italki/curriculum/module_registry.md`
- `/Volumes/위콜라보/gstack/ChanneulPark_italki/curriculum/modules/work_and_appointments.md`
- `/Volumes/위콜라보/gstack/ChanneulPark_italki/lessons/active/week05_pt_gym_korean/lesson_package.md`
- `_workspace/runs/2026-06-14-build-lesson-making-friends`
