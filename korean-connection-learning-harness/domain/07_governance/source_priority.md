# Source Priority

## Purpose

Resolves conflicts between current instructions, approved domain files, archived material, and external research.

## Priority Order

1. Current user instruction in the active session
2. Approved files under `domain/`
3. Approved files under `contracts/`
4. Current learner state and lesson result evidence
5. Accessed and verified official sources recorded in `domain/02_language_map/source_catalog.json`
6. Existing italki repository as read-only rhythm and structure reference
7. Archive examples as rhythm and structure only
8. External or newly gathered research

## Conflict Handling

When two sources conflict:

- name both sources
- preserve the conflict in the workspace note
- follow the higher-priority source for the current run
- propose a domain update only if the conflict affects repeated future work

## Archive Boundary

Archive lessons and historical cases are not active learner context. Use their pacing, structure, and visual rhythm only after privacy review.

## Language-Map Source Boundary

- Do not use the italki repository, archive lessons, or private curriculum as evidence for canonical A0–A2 language targets.
- Do not create a source ID, publisher, title, URL, retrieval date, or reviewed status for material that was not actually accessed.
- Every catalog record stores `source_id`, `publisher`, `title`, `source_type`, `url`, `retrieved_at`, and `scope_notes`.
- When official evidence is unavailable, keep the target `status: draft`, set `level.confidence: low`, and use `source_refs: []`.
- Missing official support for core grammar, register, or phonology coverage is a completion blocker.
