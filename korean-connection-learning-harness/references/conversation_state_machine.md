# Conversation State Machine

## States

```text
open -> partial -> ready_to_lock -> locked
```

- `open`: core context is absent.
- `partial`: some facts or choices are known, but blockers remain.
- `ready_to_lock`: all required scope values are known and explicit approval is the only remaining step.
- `locked`: approval evidence exists and blockers are empty.

## Backward Transitions

A goal change, duration change, new learner evidence, or request that conflicts with a lock returns the conversation to `partial` or `ready_to_lock`.

## Lock History

Never overwrite a locked contract silently. Use one of:

- incremented lock revision
- new lock with `supersedes`
- new Teacher Decision Card followed by a replacement lock

Old locks remain auditable and must not be treated as active after supersession.
