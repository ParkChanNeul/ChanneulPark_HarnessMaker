# Practice Plan

```yaml
practice_plan_id: "practice-clinic-pharmacy-001"
source_blueprint: "03_lesson_blueprint.md"
practice_ladder:
  controlled:
    - task_id: "controlled-001"
      target: "symptom.bodypart_apayo"
      prompt: "Swap the body part: 머리, 목, 배, 허리."
      model:
        - "머리가 아파요."
        - "목이 아파요."
      evidence: "learner can produce the symptom pattern with correct particle support"
    - task_id: "controlled-002"
      target: "do_dwaeyo"
      prompt: "Choose the check question: 먹다, 마시다, 쉬다."
      model:
        - "먹어도 돼요?"
        - "마셔도 돼요?"
        - "쉬어도 돼요?"
      evidence: "learner recognizes `-아/어도 돼요?` as a check/permission tool"
  guided:
    - task_id: "guided-001"
      target: "concise_information_first"
      prompt: "Choose the next line after the symptom: time clue, repeat request, or check question."
      options:
        - "어제부터요."
        - "다시 한 번 말해 주세요."
        - "이거 먹어도 돼요?"
      evidence: "learner can select a useful next line based on staff prompt"
    - task_id: "guided-002"
      target: "repair_when_confused"
      prompt: "Staff speaks fast. Add one small reaction, then ask again."
      model:
        - "아, 잠깐만요."
        - "다시 한 번 말해 주세요."
      evidence: "learner uses repair instead of freezing"
  independent:
    - task_id: "independent-001"
      target: "symptom.bodypart_apayo"
      prompt: "Walk into a pharmacy role-play. Say one symptom and one time clue without looking at the model."
      evidence: "learner independently produces symptom plus support chunk"
    - task_id: "independent-002"
      target: "confirm_next_step"
      prompt: "After the staff gives a simple instruction, ask one check question without a visible model."
      evidence: "learner independently chooses a next-step check"
  transfer:
    - task_id: "transfer-001"
      target: "do_dwaeyo"
      prompt: "Transfer from PT/gym: `잠깐 쉬어도 돼요?` -> pharmacy: `이거 먹어도 돼요?`."
      evidence: "learner can move the permission/check grammar to a new situation"
    - task_id: "transfer-002"
      target: "request_juseyo"
      prompt: "Transfer from Week 5 repeat request to clinic instructions."
      evidence: "learner retrieves `다시 한 번 말해 주세요` in a changed context"
retrieval_prompts:
  - target: "pt_gym.repeat_request"
    prompt: "What do you say if staff speaks too quickly?"
    expected: "다시 한 번 말해 주세요."
  - target: "pt_gym.pain_stop"
    prompt: "What short word tells the key problem?"
    expected: "아파요."
  - target: "do_dwaeyo"
    prompt: "How do you ask if one action is okay?"
    expected: "-아/어도 돼요?"
roleplay_variations:
  - "pharmacy: one symptom and one time clue"
  - "clinic intake: staff asks what hurts"
  - "pharmacy medicine check: ask if taking it is okay"
  - "fast instruction: ask for repeat"
error_repair_prompts:
  - error: "long English explanation before the symptom"
    repair: "First say one Korean symptom: `머리가 아파요.`"
  - error: "forgetting the particle"
    repair: "Use a chunk, not analysis: `머리가`, `목이`, `배가`, `허리가`."
  - error: "freezing when staff speaks fast"
    repair: "Use the Week 5 repair line: `다시 한 번 말해 주세요.`"
  - error: "asking a medical-detail question outside lesson scope"
    repair: "Keep it as a language check: `이거 먹어도 돼요?` with generic item only."
homework_seed:
  - "Write four symptom chunks: 머리, 목, 배, 허리."
  - "Record one private rehearsal: `머리가 아파요. 어제부터요.`"
  - "Practice one check question: `이거 먹어도 돼요?`"
  - "Next lesson check: Which line came out fastest: symptom, repeat, or check?"
quizlet_seed:
  - card_type: "qna"
    front: "My head hurts."
    back: "머리가 아파요."
  - card_type: "qna"
    front: "Since yesterday."
    back: "어제부터요."
  - card_type: "qna"
    front: "Please say it one more time."
    back: "다시 한 번 말해 주세요."
  - card_type: "qna"
    front: "Can I take this?"
    back: "이거 먹어도 돼요?"
evidence_capture_points:
  - "controlled symptom-swap accuracy"
  - "guided next-line choice"
  - "independent pharmacy role-play without a model"
  - "transfer of `-아/어도 돼요?` from PT/gym to pharmacy"
  - "privacy-safe role-play using generic symptoms only"
```

## Assumptions

- No live Week 5 lesson result was supplied.
- Mission completion remains unknown until a post-lesson or next-lesson check exists.
