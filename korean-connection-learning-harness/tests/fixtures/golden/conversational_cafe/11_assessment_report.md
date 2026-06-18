# Assessment Report

This report is generated from the Golden semantic and cross-artifact validators. Do not edit the pass status manually.

```yaml
{
  "assessment_report_id": "cafe-assessment-001",
  "reviewed_artifacts": [
    "00_conversation/lesson_intake_state.md",
    "00_conversation/teacher_decision_card.md",
    "00_conversation/lesson_scope_lock.md",
    "00_conversation/post_lesson_teacher_card.md",
    "00_conversation/next_lesson_decision_lock.md",
    "01_learner_context_snapshot.md",
    "02_progression_plan.md",
    "03_lesson_blueprint.md",
    "04_practice_plan.md",
    "05_student_deck_spec.md",
    "06_lesson_result.md",
    "07_homework_plan.md",
    "08_quizlet_plan.md",
    "09_follow_up_message.md",
    "10_next_lesson_check.md",
    "10_weekly_learning_pack.md"
  ],
  "overall_status": "pass",
  "findings": [],
  "contract_checks": {
    "passed": [
      "structured payloads parse",
      "required fields complete",
      "artifact references resolve",
      "lesson scope lock matches progression",
      "progression matches blueprint",
      "blueprint targets are covered by practice",
      "deck contract matches slides",
      "followup scope matches next lesson lock"
    ],
    "failed": []
  },
  "learning_checks": {
    "passed": [
      "situation-led",
      "grammar-and-vocabulary tracked",
      "teacher-approved progression"
    ],
    "failed": []
  },
  "approval_checks": {
    "lesson_scope_lock_valid": true,
    "teacher_overrides_preserved": true,
    "followup_scope_valid": true,
    "next_lesson_decision_lock_valid": true
  },
  "privacy_checks": {
    "passed": [
      "synthetic data only"
    ],
    "failed": []
  }
}
```
