# Progression Plan

```yaml
progression_plan_id: "progression-friends-001"
learner_alias: "friends_learner"
planning_window: "next lesson"
primary_situation: "making_friends"
new_target_candidates:
  - target_id: "ask_back.topic_marker"
    display_name: "Ask the same question back with 은/는요?"
    function: "keep a peer conversation moving after answering"
    selected: true
review_targets:
  - target_id: "questions.basic"
    reason: "already guided; needed to form peer questions"
  - target_id: "topic.marker"
    reason: "already controlled; needed for the ask-back pattern"
  - target_id: "greeting.basic"
    reason: "retrieve from completed greeting role-play"
retrieval_targets:
  - target_id: "greeting.basic"
    retrieval_type: "delayed role-play opening"
  - target_id: "questions.basic"
    retrieval_type: "prompt-free question recall"
transfer_targets:
  - target_id: "ask_back.topic_marker"
    transfer_context: "new peer after class or club signup"
conversation_skill_targets:
  - skill_id: "reaction.simple"
    reason: "move from modeled reaction to guided production"
  - skill_id: "ask_back"
    reason: "prevent conversation from stopping after one answer"
blocked_targets: []
spiral_review_plan:
  - target_id: "ask_back.topic_marker"
    next_review: "end of lesson transfer role-play"
  - target_id: "questions.basic"
    next_review: "next lesson warmup"
next_lesson_rationale: "The learner already has guided questions and controlled topic-marker knowledge. The next useful step is to use those pieces in the social action of asking the same question back."
```

## Rejected Targets

- `honorifics.register_shift`: too broad for this A1 peer situation.
- `past_tense.storytelling`: useful later, but it would distract from the immediate conversation-stop problem.
