# Run Handoff Template

```yaml
run_id: "YYYYMMDD-mode-short-label"
front_stage_route: "lesson_intake | lesson_resume | lesson_turn | lesson_unknown | lesson_scope_lock | post_lesson_reflection | next_lesson_decision | null"
mode: "build_lesson | render_materials | post_lesson_followup | review_outputs | research_to_domain | audit_domain | partial_rerun | null"
followup_scope: "homework_only | full_followup | null"
request_ref: "path or transcript summary"
lesson_scope_lock_ref: null
post_lesson_teacher_card_ref: null
next_lesson_decision_lock_ref: null
inputs: []
agents_dispatched: []
advisory_agents: []
proposed_artifacts: []
review_reports: []
privacy_reports: []
blockers: []
parent_decisions: []
next_actions: []
```

Front-stage routes do not become execution modes. Record advisory returns separately from approved decisions.
