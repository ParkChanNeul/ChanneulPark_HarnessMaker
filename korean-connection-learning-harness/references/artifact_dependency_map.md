# Artifact Dependency Map

## Lesson Build Dependencies

```text
lesson_request
  -> learner_context_snapshot
      -> progression_plan
          -> lesson_blueprint
              -> practice_plan
                  -> student_deck_spec
                      -> design_manifest
                          -> material_manifest
                              -> assessment_report
```

## Follow-Up Dependencies

```text
lesson_result
  -> homework_plan
  -> quizlet_plan
  -> follow_up_message
  -> next_lesson_check
  -> weekly_learning_pack
  -> learner_state_delta
      -> next learner_context_snapshot
```

## Research Dependencies

```text
research note
  -> research_insight_proposal
      -> domain_update_proposal
          -> approval_state
              -> approved domain or contract update
```

## Privacy Dependencies

```text
artifact with learner context
  -> privacy_report
      -> pass: parent may continue
      -> blocked: parent removes or generalizes detail
```

## Contract Ownership

| Contract | Owning Producer | Required Reviewer |
|---|---|---|
| `learner_context_snapshot` | `kc_learner_state_analyst` | `kc_assessment_reviewer` |
| `learner_state_delta` | `kc_learning_followup_teacher`, `kc_assessment_reviewer` | `kc_assessment_reviewer` |
| `progression_plan` | `kc_learning_progression_planner` | `kc_assessment_reviewer` |
| `lesson_blueprint` | `kc_lesson_architect` | `kc_assessment_reviewer` |
| `practice_plan` | `kc_practice_designer` | `kc_assessment_reviewer` |
| `student_deck_spec` | `kc_student_experience_designer` | `kc_assessment_reviewer` |
| `follow_up_message` | `kc_learning_followup_teacher` | `kc_privacy_auditor` when learner context appears |
| `privacy_report` | `kc_privacy_auditor` | Parent agent |
| `research_insight_proposal` | `kc_research_synthesizer` | `kc_domain_curator` |
| `domain_update_proposal` | `kc_domain_curator` | Human approval |
