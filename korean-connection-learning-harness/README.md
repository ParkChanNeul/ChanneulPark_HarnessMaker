# Korean Connection Learning Harness V2

This project is a Codex-native, Teacher-in-the-Loop harness for Korean Connection learning operations.

It does not extend or copy the existing italki lesson builder. The existing italki repository is read-only reference material, not a production dependency.

## Conversational Teacher Loop

```text
teacher request
-> context and unknowns
-> options and AI recommendation
-> teacher approval
-> Lesson Scope Lock
-> specialist execution
-> lesson result reflection
-> homework approval
-> optional Next Lesson Decision Lock
```

Bare requests do not build lessons. Rich input reduces questions but never bypasses the approval gate. An exact `run_dir` is required to resume an existing run.

## Core Learning Loop

```text
approved lesson scope
-> learner state analysis
-> teacher-compliant progression plan
-> lesson blueprint
-> repeated practice design
-> student deck and HTML material design
-> lesson result
-> approved follow-up
-> mastery evidence review
-> next lesson input when separately locked
```

## Learning Principles

```text
Situation-led
Culture-explained
Grammar-and-vocabulary tracked
Practice-repeated
Mastery-verified
Teacher-approved progression
```

Culture explains why a form matters, where it is safe, and how it changes relationship distance. Grammar, vocabulary, and expressions remain cumulative skills that need retrieval, production, transfer, and delayed review. AI recommends; the teacher approves progression.

## Existing Execution Modes

The seven execution modes remain `build_lesson`, `render_materials`, `post_lesson_followup`, `review_outputs`, `research_to_domain`, `audit_domain`, and `partial_rerun`. Conversational routes are not execution modes.

- `build_lesson` requires a valid `lesson_scope_lock`.
- `post_lesson_followup` supports `homework_only` from an approved Post-Lesson Teacher Card.
- `full_followup` additionally requires a locked Next Lesson Decision Lock before next-lesson or progression outputs.

## Agent Model

The current specialist agents remain read-only and are registered in `references/agent_registry.toml`. Validators read the registry rather than assuming a permanent count, so future approved grammar, lexicon, or vocabulary agents can be added without rewriting count assertions.

## Source Priority

1. Current user instructions
2. Approved documents in `domain/`
3. Approved documents in `contracts/`
4. Current learner evidence and approval locks
5. Existing italki reference repository
6. Archive and historical examples
7. External research

## Safety Boundaries

- Do not store real student-identifying information in tracked files.
- Do not use the existing italki repo as a production dependency.
- Do not copy archive lessons, student cases, or private context into active examples.
- Do not create a nested Git repository.
- Do not infer the latest run or treat fixtures as active learner state.

## Validation

Validation has four distinct layers:

- Contract Documentation Validation checks contract names, sections, and canonical field definitions.
- Semantic Artifact Validation parses JSON-compatible YAML payloads and checks state, lock, approval, enum, and vocabulary rules.
- Cross-artifact Validation checks references and consistency from lock through progression, blueprint, practice, deck, and follow-up.
- Executable Acceptance Tests use `unittest` to prove valid cases pass and invalid cases fail.

The Markdown files under `tests/acceptance/` remain human-readable requirements. The Golden Fixture under `tests/fixtures/golden/conversational_cafe/` is a complete valid contract flow. Its Assessment Report is generated from validator output, not manually declared.

```bash
python3.11 scripts/validate_structure.py
python3.11 scripts/validate_contracts.py
python3.11 scripts/validate_agent_boundaries.py
python3.11 scripts/validate_semantic_contracts.py
python3.11 scripts/validate_golden_run.py
python3.11 scripts/validate_conversational_runtime.py
python3.11 scripts/render_golden_assessment.py --check
python3.11 -m unittest discover -s tests -p 'test_*.py'
python3.11 scripts/validate_harness.py
```

Use `python3.11 scripts/render_golden_assessment.py --write` only when intentionally maintaining the tracked Golden Fixture.
