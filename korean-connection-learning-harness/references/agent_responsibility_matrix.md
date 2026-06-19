# Agent Responsibility Matrix

## Registry and Coordination

`references/agent_registry.toml` is the machine-readable approved registry. Validators require all entries marked `required = true` and reject unregistered agent TOMLs without assuming a permanent agent count.

Top-level Codex is the parent orchestrator. Subagents return findings, proposed artifacts, evidence paths, blockers, and rerun notes. The parent owns conversation contracts, locks, and final file writes.

## Matrix

| Agent | Skill | Primary Responsibility | Reads | Produces | Lock Boundary |
|---|---|---|---|---|---|
| `kc_learner_state_analyst` | `kc-learner-state-analysis` | safe learner snapshot and state deltas | request, result, learner schemas | snapshot, proposed delta | advisory before lock only when explicitly requested |
| `kc_learning_progression_planner` | `kc-learning-progression-planning` | progression options before lock; approved plan after lock | snapshot, curriculum, scope lock | progression plan | cannot change approved mode, targets, or review exclusion |
| `kc_lesson_architect` | `kc-lesson-architecture` | operationalize approved targets | progression plan, scope lock, lesson domain | lesson blueprint | no target selection |
| `kc_practice_designer` | `kc-practice-design` | practice ladder and evidence capture | blueprint, practice rules, mastery schemas | practice plan, homework/Quizlet seeds | preserve locked target treatment |
| `kc_student_experience_designer` | `kc-student-experience-design` | learner-facing material specs | blueprint, practice, student rules | deck spec, design manifest draft | rendering cannot change scope |
| `kc_learning_followup_teacher` | `kc-learning-followup` | approved homework-only or full follow-up | result, post card, optional next lock | weekly pack, homework, Quizlet, message, optional next outputs | next outputs require next lock |
| `kc_assessment_reviewer` | `kc-assessment-review` | contract, learning, registry, migration, evidence, and approval QA | generated artifacts, locks, language map, packs, profiles, domain docs | assessment report | block unapproved builds, lock drift, formal-only target coverage, and unsupported core coverage |
| `kc_research_synthesizer` | `kc-research-synthesis` | evidence-labeled insight and source-catalog proposals | accessed official sources, research notes, evidence levels | research insight and source record proposals | never invent or mark inaccessible sources reviewed |
| `kc_domain_curator` | `kc-domain-curation` | approved domain and canonical map update proposals | insight proposal, registries, packs, profiles, migration tables, approval rules | domain update proposal | common schemas and human approval required |
| `kc_privacy_auditor` | `kc-privacy-audit` | identifying-data review | target artifacts, privacy rules | privacy report | conditional privacy gate |

## Advisory Mode

Only learner-state analysis and progression planning may be used in front-stage advisory mode, and only with explicit source paths plus a teacher request for evidence. Returned advice is not approval.

## Review Duties

`kc_assessment_reviewer` checks canonical `language_targets`, canonical `situation_scope`, situation, culture, tracked vocabulary, repeated practice, mastery evidence, teacher approval, lock consistency, target surface evidence, registry membership, source-backed core coverage, canonical vocabulary propagation, deck count, follow-up scope, and learner-safe visible titles. Computed semantic validation outranks manually declared assessment status.

`kc_privacy_auditor` blocks real identifying details and archive-derived private context.

## Conditional Routing

Run privacy audit before finalizing student-facing or tracked artifacts when input contains biography, archive material, social account context, demographic details, or identifying combinations.
