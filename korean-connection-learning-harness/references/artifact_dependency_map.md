# Artifact Dependency Map

## Conversation and Lesson Build Dependencies

```text
lesson_intake_state
  -> teacher_decision_card
      -> lesson_scope_lock (teacher approved)
          -> learner_context_snapshot
              -> progression_plan
                  -> lesson_blueprint
                      -> practice_plan
                          -> student_deck_spec
                              -> design_manifest
                                  -> material_manifest
                                      -> assessment_report
```

Progression, blueprint, practice, and material review must remain consistent with the active lock.

The normalized vocabulary scope is copied without field renaming across:

```text
lesson_scope_lock
-> progression_plan
-> lesson_blueprint
-> practice_plan
-> student_deck_spec
```

Practice tasks carry target IDs so the validator can prove target coverage.

## Follow-Up Dependencies

```text
lesson_result or teacher notes
  -> post_lesson_teacher_card
      -> approved homework option
          -> homework_plan
          -> quizlet_plan
          -> follow_up_message
          -> weekly_learning_pack (homework_only)
      -> next_lesson_decision_lock
          -> next_lesson_check
          -> learner_state_delta scheduling
          -> weekly_learning_pack (full_followup)
```

Homework approval and next-direction approval are separate gates.

## Validation Dependencies

```text
Markdown contract
-> structured artifact loader
-> semantic contract validator
-> Golden cross-artifact validator
-> computed Golden assessment
-> executable unittest
```

The computed assessment consumes validator results. It is not an independent manual pass declaration.

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
| conversation cards and locks | parent orchestrator | teacher approval + assessment when consumed |
| `learner_context_snapshot` | `kc_learner_state_analyst` | `kc_assessment_reviewer` |
| `progression_plan` | `kc_learning_progression_planner` | `kc_assessment_reviewer` |
| `lesson_blueprint` | `kc_lesson_architect` | `kc_assessment_reviewer` |
| `practice_plan` | `kc_practice_designer` | `kc_assessment_reviewer` |
| `student_deck_spec` | `kc_student_experience_designer` | `kc_assessment_reviewer` |
| follow-up artifacts | `kc_learning_followup_teacher` | assessment + conditional privacy |
| `privacy_report` | `kc_privacy_auditor` | parent agent |
| `research_insight_proposal` | `kc_research_synthesizer` | `kc_domain_curator` |
| `domain_update_proposal` | `kc_domain_curator` | human approval |
