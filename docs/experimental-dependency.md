# Codex Runtime Notes

Harness no longer depends on an experimental team runtime flag. The Codex port uses parent-mediated coordination:

1. The parent agent reads `.agents/skills/harness/SKILL.md`.
2. The parent selects custom agents from `.codex/agents/*.toml`.
3. Independent work can be dispatched in bounded parallel.
4. Subagents return findings, proposed content, evidence paths, and blocked status.
5. The parent compares all results, sends follow-up prompts when needed, and writes final files.

## Why This Matters

The upstream Harness workflow relied on direct multi-agent coordination. Codex does not need that runtime primitive to preserve the workflow semantics. The parent agent owns orchestration, dependency tracking, conflict resolution, workspace handoff, and final writes.

## Stable Generated Paths

Generated harnesses should use:

```text
.codex/agents/{domain_agent}.toml
.agents/skills/{domain_skill}/SKILL.md
.agents/skills/{domain_orchestrator}/SKILL.md
AGENTS.md
_workspace/
```

Do not create `.codex/skills/`.

## Compatibility Policy

- If Codex custom agent TOML fields change, update `.codex/agents/*.toml`, `.codex/config.toml.example`, and `scripts/validate_codex_port.py` in the same release.
- If skill loading behavior changes, update `.agents/skills/harness/SKILL.md` and all installer tests before publishing.
- If parent-mediated bounded parallel execution is unavailable, Harness should fall back to sequential parent dispatch while preserving workspace artifacts and validation reports.
