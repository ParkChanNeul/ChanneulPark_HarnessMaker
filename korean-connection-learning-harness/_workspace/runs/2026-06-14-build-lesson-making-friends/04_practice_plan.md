# Practice Plan

```yaml
practice_plan_id: "practice-friends-001"
source_blueprint: "03_lesson_blueprint.md"
practice_ladder:
  controlled:
    - task_id: "controlled-001"
      target: "ask_back.topic_marker"
      prompt: "저는 ___ 좋아해요. ___은/는요?"
      evidence: "learner can place topic marker on the returned topic"
    - task_id: "controlled-002"
      target: "questions.basic"
      prompt: "Choose the correct question for name, hobby, or hometown."
      evidence: "learner recognizes and forms basic question frames"
  guided:
    - task_id: "guided-001"
      target: "reaction.simple"
      prompt: "Choose one reaction, then ask back: 좋아요 / 진짜요? / 저도요."
      evidence: "learner can combine reaction plus ask-back with options"
    - task_id: "guided-002"
      target: "ask_back"
      prompt: "Answer the question and choose the best ask-back."
      evidence: "learner does not stop after one answer"
  independent:
    - task_id: "independent-001"
      target: "ask_back.topic_marker"
      prompt: "Meet a new peer. Answer two questions and ask each one back without looking at the model."
      evidence: "learner independently produces ask-back pattern"
  transfer:
    - task_id: "transfer-001"
      target: "ask_back.topic_marker"
      prompt: "You meet someone after class. They ask about weekend plans. Answer, react, and ask back."
      evidence: "learner uses the target outside the original hobby/name prompt"
retrieval_prompts:
  - target: "greeting.basic"
    prompt: "Start the role-play without notes."
  - target: "questions.basic"
    prompt: "Ask one question from memory before the choices appear."
roleplay_variations:
  - "new classmate"
  - "friend of a friend"
  - "club signup table"
error_repair_prompts:
  - error: "answer only, no ask-back"
    repair: "Add ___은/는요? after your answer."
  - error: "reaction after ask-back feels late"
    repair: "Use reaction first, then ask back."
homework_seed:
  - "Write three answer + ask-back pairs about hobby, food, and weekend."
quizlet_seed:
  - card_type: "qna"
    front: "A: 저는 커피 좋아해요. ___"
    back: "B: 저는 차 좋아해요. 커피는요?"
evidence_capture_points:
  - "controlled substitution accuracy"
  - "guided reaction + ask-back completion"
  - "independent role-play without model"
  - "transfer role-play success"
```
