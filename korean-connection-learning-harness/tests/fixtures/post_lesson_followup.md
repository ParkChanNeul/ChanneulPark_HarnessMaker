# Fixture: Post Lesson Follow-Up

```yaml
lesson_result_id: "result-001"
lesson_id: "making-friends-lesson-001"
learner_alias: "friends_learner"
situation_scope:
  pack_ref: "making_friends"
  sub_situation_ids: ["answer", "react", "ask_back"]
language_targets:
  - target_ref: "grammar_question_haeyo"
    treatment: "new"
  - target_ref: "chunk_hello_annyeonghaseyo"
    treatment: "review"
  - target_ref: "particle_topic_eunneun"
    treatment: "review"
  - target_ref: "chunk_thanks_gamsahamnida"
    treatment: "retrieval"
  - target_ref: "interaction_ask_back"
    treatment: "transfer"
observed_evidence:
  successful:
    - "used greeting.basic without prompt"
  breakdowns:
    - "needed model to ask the same question back"
  missed:
    - "did not reach final transfer role-play"
followup_inputs:
  homework:
    - "practice asking the same question back"
  quizlet:
    - "Q&A cards for question and answer pairs"
  next_lesson_check:
    - "retry transfer role-play"
privacy_redactions: []
```
