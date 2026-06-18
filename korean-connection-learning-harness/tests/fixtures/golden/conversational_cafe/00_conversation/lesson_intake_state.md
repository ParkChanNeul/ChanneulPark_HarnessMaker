# Lesson Intake State

```yaml
{
  "run_id": "demo-conversational-cafe",
  "conversation_state": "ready_to_lock",
  "teacher_request": {
    "raw_request": "A1 카페 수업을 만들고 싶어.",
    "requested_output": [
      "student_deck",
      "html",
      "homework",
      "quizlet_plan"
    ]
  },
  "known_context": {
    "learner_type": "existing",
    "learner_level": "A1",
    "lesson_duration_minutes": 50,
    "target_situation": "cafe",
    "teacher_goal": "order and respond without freezing",
    "previous_lesson_ref": "synthetic-previous-lesson"
  },
  "unknowns": [
    {
      "unknown_id": "direction",
      "category": "lesson_mode",
      "blocking": true,
      "question": "새 진도와 복습을 어떻게 섞을까요?",
      "answer": "mixed",
      "resolution_status": "confirmed"
    }
  ],
  "workspace": {
    "run_dir": "../",
    "read_allowed": true,
    "write_allowed": true
  }
}
```
