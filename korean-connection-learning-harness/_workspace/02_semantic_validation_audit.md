# Semantic Validation Audit

## Baseline

Base commit: `0572962ed0051b3974980280752dd30fea1819c6`

The following commands all passed before this hardening work:

```text
python3.11 scripts/validate_structure.py
python3.11 scripts/validate_contracts.py
python3.11 scripts/validate_agent_boundaries.py
python3.11 scripts/validate_conversational_runtime.py
python3.11 scripts/validate_harness.py
```

The pass result proves that the current validators check file structure and selected strings, but not artifact meaning.

## Contract And Fixture Gaps

### Lesson Intake State

- The Golden fixture contains the documented top-level fields.
- Its only blocking unknown is already `confirmed`, but `conversation_state` remains `partial`.
- No validator checks whether open blocking unknowns agree with the state.

### Teacher Decision Card

The Golden fixture omits documented required fields:

- `source_intake_state`
- `teaching_problem`
- `required_teacher_decisions`
- `assumption_candidates`
- `advisory_inputs`

Individual options also omit documented target arrays. The current validator checks only that the contract document contains selected strings.

### Lesson Scope Lock

The Golden fixture omits:

- `supersedes`

The lock uses duplicate legacy vocabulary fields instead of one canonical vocabulary scope.

### Post-Lesson Teacher Card

- `source_lesson_result` is `../../06_lesson_result.md`.
- From `00_conversation/post_lesson_teacher_card.md`, that path resolves outside the Golden run and does not exist.
- `status` is `ready_to_lock` while `required_teacher_decisions` still contains the next-lesson direction.

### Next Lesson Decision Lock

The Golden fixture omits:

- `supersedes`

Its vocabulary direction uses a separate legacy naming scheme rather than the canonical count fields.

## Vocabulary Scope Duplication

The active contracts and Golden fixtures use overlapping names for the same meaning:

```text
vocabulary_count
in_class_new_items
productive_core
receptive_support
review_items
homework_expansion
new_item_count
new_pack
new_item_target
carrier_items
homework_expansion_target
```

No current validator rejects these fields or verifies:

```text
in_class_new_item_count
= productive_core_count + receptive_support_count
```

## Cross-Artifact Gaps

No current validator compares:

- Lesson Scope Lock targets with Progression Plan targets
- Progression Plan targets and vocabulary scope with Lesson Blueprint
- Blueprint targets with Practice Plan task coverage
- Locked vocabulary counts with downstream artifacts
- Follow-up scope with Next Lesson Decision Lock
- Prior-target treatment in the next lock with the next-lesson check

The current files can therefore contradict each other while every validator passes.

## Deck Gap

The Golden Student Deck declares:

```text
slide_count_target: 10
```

but contains one slide. No current validator compares the declared count with the actual slide list or checks per-slide required fields.

## Acceptance Gap

The Markdown files under `tests/acceptance/` are human-readable scenarios only. Current validators check that the files exist, but do not execute positive or negative behavior.

Examples that currently have no executable proof:

- invalid locked approval is rejected
- broken relative paths are rejected
- vocabulary count mismatches are rejected
- lock/progression target drift is rejected
- homework-only output cannot contain next-lesson artifacts

## Assessment Gap

`11_assessment_report.md` manually declares `overall_status: pass`. That value is not generated from validator results and is not compared with computed contract, approval, or privacy checks.

The report can therefore claim pass even when the Golden run contains broken paths, missing required fields, inconsistent vocabulary scope, and an incomplete deck.
