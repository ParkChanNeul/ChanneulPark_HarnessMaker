# Agent Responsibility Matrix

## Coordination Rule

Top-level Codex is the parent orchestrator. Subagents return findings, proposed artifacts, evidence paths, blockers, and rerun notes. The parent owns final file writes.

## Matrix

| Agent | Skill | Primary Responsibility | Reads | Produces | Write Boundary |
|---|---|---|---|---|---|
| `kc_learner_state_analyst` | `kc-learner-state-analysis` | Build safe learner snapshot and state deltas | lesson request, lesson result, learner state schemas | `learner_context_snapshot`, proposed `learner_state_delta` | read-only |
| `kc_learning_progression_planner` | `kc-learning-progression-planning` | Choose sequence, review, retrieval, and transfer targets | learner snapshot, curriculum, mastery schemas | `progression_plan` | read-only |
| `kc_lesson_architect` | `kc-lesson-architecture` | Design lesson blueprint around situation and target mix | progression plan, lesson system domain docs | `lesson_blueprint` | read-only |
| `kc_practice_designer` | `kc-practice-design` | Build practice ladder and evidence capture | lesson blueprint, practice ladder, mastery schemas | `practice_plan`, homework/quizlet seeds | read-only |
| `kc_student_experience_designer` | `kc-student-experience-design` | Turn blueprint and practice into student-facing material specs | lesson blueprint, practice plan, student experience rules | `student_deck_spec`, `design_manifest` draft | read-only |
| `kc_learning_followup_teacher` | `kc-learning-followup` | Convert result into weekly pack, homework, Quizlet, and next lesson check | lesson result, practice plan, learner snapshot | `weekly_learning_pack`, `homework_plan`, `quizlet_plan`, `follow_up_message`, `next_lesson_check`, proposed `learner_state_delta` | read-only |
| `kc_assessment_reviewer` | `kc-assessment-review` | Review quality, contracts, learning balance, and evidence | generated artifacts, contracts, domain docs | `assessment_report` | read-only |
| `kc_research_synthesizer` | `kc-research-synthesis` | Convert research notes into bounded insight proposals | research notes, evidence levels, source priority | `research_insight_proposal` | read-only |
| `kc_domain_curator` | `kc-domain-curation` | Convert approved insights into domain update proposals | insight proposal, domain docs, approval rules | `domain_update_proposal` | read-only |
| `kc_privacy_auditor` | `kc-privacy-audit` | Detect private or identifying learner data | target artifacts, privacy governance | `privacy_report` | read-only |

## Review Duties

`kc_assessment_reviewer` must check that:

- situation leads the lesson
- culture explains language choice instead of replacing practice
- grammar and expressions are tracked as cumulative targets
- practice includes retrieval, independent production, and transfer
- mastery claims are evidence-based
- student-facing artifacts hide internal reasoning labels

`kc_privacy_auditor` must block real identifying details and archive-derived private context.

## Conditional Routing

Run `kc_privacy_auditor` before finalizing student-facing or tracked artifacts when the input includes learner biography, archive material, social account context, demographic details, or any phrase that looks identifying.
