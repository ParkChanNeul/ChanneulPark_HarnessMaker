# Privacy Report

```yaml
privacy_report_id: "privacy-clinic-pharmacy-001"
reviewed_artifacts:
  - "00_run_handoff.md"
  - "01_learner_context_snapshot.md"
  - "02_progression_plan.md"
  - "03_lesson_blueprint.md"
  - "04_practice_plan.md"
  - "05_student_deck_spec.md"
  - "07_student_deck.html"
  - "08_design_manifest.md"
  - "09_material_manifest.md"
  - "10_render_assessment_report.md"
status: "pass"
findings:
  - severity: "minor"
    artifact: "00_run_handoff.md"
    detail_type: "private_context"
    evidence: "Week 1-4 archive material was consulted"
    required_action: "generalize"
  - severity: "minor"
    artifact: "07_student_deck.html"
    detail_type: "other"
    evidence: "generic health-adjacent lines such as `머리가 아파요` and `이거 먹어도 돼요?` appear"
    required_action: "approve_with_reason"
redactions_recommended:
  - "Continue using `kc_reference_learner` rather than any real learner name."
  - "Do not add diagnosis, medication names, medical history, exact age, nationality, social accounts, or follower counts."
  - "Keep missions private-rehearsal by default unless a future user explicitly approves a public-content use."
```

## Approval Reason

The health-adjacent examples are generic classroom language and do not disclose a real learner's medical context. Archive material is cited only as sequence evidence and is not copied into student-facing examples.
