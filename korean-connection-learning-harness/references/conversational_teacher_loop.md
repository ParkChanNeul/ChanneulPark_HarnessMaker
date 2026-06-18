# Conversational Teacher Loop

## Principle

AI proposes options and rationale. The teacher decides progression, review intensity, vocabulary load, homework scope, and next-lesson direction. Specialist agents operationalize locked decisions.

## Front Stage

```text
teacher request
-> intake or rich turn
-> unknown resolution when needed
-> Teacher Decision Card
-> explicit teacher approval
-> Lesson Scope Lock
```

Front-stage is parent-led. Specialists are optional read-only advisors only when an explicit learner-context or lesson-result path exists and the teacher asks for evidence-based reasoning.

## Back Stage

```text
locked lesson_scope_lock
-> existing specialist chain
-> lock-aware assessment
```

No specialist may change a locked target or reintroduce a teacher-excluded review requirement.

## Post Stage

```text
lesson result or teacher notes
-> Post-Lesson Teacher Card
-> approved homework option
-> homework_only outputs

Post-Lesson Teacher Card
-> teacher next-direction choice
-> Next Lesson Decision Lock
-> full_followup outputs
```

## Handoff Rule

A recommendation is never automatic execution. Every conversational skill ends with a standard Next Skill Handoff that names blockers and whether teacher confirmation or a run directory is required.

## Validation Boundary

Conversational cards and locks are parsed as structured artifacts in the Golden flow. Documentation presence alone is not acceptance.

```text
contract documentation
-> semantic state and approval validation
-> cross-artifact consistency validation
-> executable positive and negative tests
```

The canonical vocabulary scope must remain identical from the approved lock through progression, blueprint, practice, and deck.
