# Claude to Codex Migration

This document is historical migration context, not canonical runtime instruction.

| Claude Harness | Codex 대응 |
| --- | --- |
| `.claude/agents/*.md` | `.codex/agents/*.toml` templates |
| `.claude/skills/*` | `.agents/skills/*` |
| `CLAUDE.md` | `AGENTS.md` |
| `TeamCreate` | explicit Codex custom subagent delegation requested by user |
| `SendMessage` | subagent result returned to parent, then parent writes `_workspace/` |
| `TaskCreate` | parent orchestrator phase/task plan |
| `TeamDelete` | subagent thread completion and parent cleanup |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | removed; no experimental flag required in canonical docs |
| `model: "opus"` | no hard-coded model; Codex defaults or user config apply |

Migration principle: remove legacy execution commands only after preserving the function they served. Team creation becomes explicit delegation; message passing becomes returned findings plus parent-owned artifacts; deletion becomes completion and cleanup in manifest.
