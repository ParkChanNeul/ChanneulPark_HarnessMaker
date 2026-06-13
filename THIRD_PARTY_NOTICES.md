# Third Party Notices

## revfactory/harness

- Repository: https://github.com/revfactory/harness
- Source commit used for this MVP: `cceac68ea1d0ad198ef4b7b906cd238375836387`
- License: Apache License 2.0
- Local source of truth during implementation: sibling clone checked out at the commit above
- NOTICE/COPYRIGHT status: upstream repository contains `LICENSE`; no `NOTICE`, `COPYRIGHT`, or separate third-party attribution file was found at the checked revision.

## Components adapted

The following upstream documents were read directly and ported into Codex-native active documents:

- `skills/harness/SKILL.md`
- `skills/harness/references/agent-design-patterns.md`
- `skills/harness/references/orchestrator-template.md`
- `skills/harness/references/team-examples.md`
- `skills/harness/references/skill-writing-guide.md`
- `skills/harness/references/skill-testing-guide.md`
- `skills/harness/references/qa-agent-guide.md`

## Major changes

- Legacy runtime paths such as `.claude/skills` are not used in canonical execution files.
- Legacy agent team primitives such as TeamCreate, TaskCreate, SendMessage, and TeamDelete are documented only as migration history and are replaced by Codex custom subagent delegation plus parent-owned file handoff.
- Model-specific settings such as `model: "opus"` are removed from active runtime templates.
- `.agents/skills/harness/` is the single canonical skill source.
- `.codex/skills/` is intentionally not created.

This file is attribution and migration context. It is not an execution instruction for a legacy runtime.
