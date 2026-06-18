# Korean Connection Learning Harness V2

## Harness: Korean Connection Learning

**Goal:** Operate teacher-approved Korean lesson progression while tracking grammar, vocabulary, practice, mastery, and follow-up.

**Trigger:** For Korean Connection lesson conversation or execution work, use `.agents/skills/korean-connection-orchestrator/SKILL.md`. Bare lesson requests must enter the conversational front stage; simple file questions may be answered directly.

**Reference Boundary:** `/Volumes/위콜라보/gstack/ChanneulPark_italki` is reference-only. Do not modify it from this harness.

**Change History:**

| Date | Change | Target | Reason |
|---|---|---|---|
| 2026-06-14 | Initial V2 harness build | full project | Rebuild around learning progression, practice, and mastery |
| 2026-06-18 | Teacher-in-the-Loop conversational routing | front stage, locks, post-lesson gates | Keep progression decisions under explicit teacher authority |
