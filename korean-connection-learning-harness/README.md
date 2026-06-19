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

## Canonical A0–A2 Language Map

`domain/02_language_map/` is the fixed teaching map for grammar constructions, particle functions, register features, discourse patterns, interactional functions, core interaction chunks, phonology, and orthography. It is not a lexeme, sense, collocation, or lesson-vocabulary database.

Every active lesson artifact uses one target interface:

```yaml
language_targets:
  - target_ref: "canonical target id"
    treatment: "new | review | retrieval | transfer | practice | carrier | defer"
```

`target_ref` resolves the target and its type through the registries. `treatment` states how the current lesson handles it. Teacher Decision Cards may use the same item shape under `candidate_language_targets` before approval.

Every active artifact uses one situation interface:

```yaml
situation_scope:
  pack_ref: "cafe_ordering"
  sub_situation_ids: []
```

`domain/03_situations/` contains 26 active Situation Packs and six reserved workplace packs. `domain/04_profiles/` contains the general adult conversation base profile plus active and reserved overlays. Runtime selection combines the fixed map with situation need, learner evidence, prerequisites, profile rules, processing load, and teacher approval.

Legacy handling is read-time only. `legacy_aliases.json` contains exact 1:1 aliases; `legacy_migrations.json` contains contextual, split, non-automatic, and manual-review cases. New artifacts may not store legacy IDs or split target fields.

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
5. Verified official sources in `domain/02_language_map/source_catalog.json`
6. Existing italki reference repository for lesson rhythm and structure only
7. Archive and historical examples for rhythm and structure only
8. External research

The italki repository and archive are not language-map seed sources. Source IDs, titles, URLs, access dates, and review status must reflect material actually accessed. A core grammar, register, or phonology record without verified official support remains draft with low confidence and blocks completion.

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
python3.11 scripts/validate_language_map.py
python3.11 scripts/render_language_map_coverage.py --check
python3.11 scripts/validate_contracts.py
python3.11 scripts/validate_agent_boundaries.py
python3.11 scripts/validate_semantic_contracts.py
python3.11 scripts/validate_golden_run.py
python3.11 scripts/validate_conversational_runtime.py
python3.11 scripts/render_golden_assessment.py --check
python3.11 -m unittest discover -s tests -p 'test_*.py'
python3.11 scripts/validate_harness.py
```

Use `python3.11 scripts/build_language_map_seed.py` only for deterministic registry maintenance, followed by both language-map validation commands and the complete harness validation chain.

Use `python3.11 scripts/render_golden_assessment.py --write` only when intentionally maintaining the tracked Golden Fixture.
