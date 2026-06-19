# Korean Connection Learning Harness V2

## Harness: Korean Connection Learning

**Goal:** Operate teacher-approved Korean lesson progression while tracking grammar, vocabulary, practice, mastery, and follow-up.

**Trigger:** For Korean Connection lesson conversation, execution work, A0–A2 language-map maintenance, Situation Pack maintenance, or profile maintenance, use `.agents/skills/korean-connection-orchestrator/SKILL.md`. Bare lesson requests must enter the conversational front stage; simple file questions may be answered directly.

**Reference Boundary:** `/Volumes/위콜라보/gstack/ChanneulPark_italki` is reference-only. Do not modify it from this harness.

**Change History:**

| Date | Change | Target | Reason |
|---|---|---|---|
| 2026-06-14 | Initial V2 harness build | full project | Rebuild around learning progression, practice, and mastery |
| 2026-06-18 | Teacher-in-the-Loop conversational routing | front stage, locks, post-lesson gates | Keep progression decisions under explicit teacher authority |
| 2026-06-18 | Semantic validation hardening | contracts, Golden Fixture, validators, tests, CI | Make approval, vocabulary, references, and cross-artifact consistency executable |
| 2026-06-19 | A0–A2 canonical language map | eight target registries, Situation Packs, profiles, migration, validators | Replace split target and situation truths with registry-backed common contracts |
