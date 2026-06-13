# Harness Codex Port

This repository packages the Harness meta-skill for Codex. Harness builds domain-specific agent and skill systems in a target repository while preserving the upstream Harness workflow: audit, architecture selection, agent definition, skill writing, orchestration, testing, and maintenance.

## Canonical Paths

- Harness skill: `.agents/skills/harness/SKILL.md`
- Harness references: `.agents/skills/harness/references/`
- Repo custom agents: `.codex/agents/*.toml`
- Generated domain agents in a target repo: `.codex/agents/{domain_agent}.toml`
- Generated domain skills in a target repo: `.agents/skills/{domain_skill}/SKILL.md`
- Generated domain orchestrator in a target repo: `.agents/skills/{domain_orchestrator}/SKILL.md`
- Runtime handoff workspace in a target repo: `_workspace/`

Do not create `.codex/skills/`. Project skills live under `.agents/skills/`.

## Runtime Model

Codex Harness uses parent-mediated coordination. The parent agent selects custom subagents, gives each one explicit inputs and completion criteria, waits for all independent results, compares conflicting evidence, sends follow-up prompts when needed, and writes final target files.

Subagents should return findings, proposed content, evidence paths, and blocked status to the parent. The parent owns final file creation, `AGENTS.md` pointer updates, and `_workspace/` handoff artifacts.

## Workspace Role

`_workspace/` stores intermediate audits, handoffs, validation notes, partial rerun state, and generated evidence. Preserve it unless the user explicitly asks to clean it.

## Tests

Use these checks before publishing changes:

```bash
python3 scripts/validate_codex_port.py
python3 -m pytest
python3 scripts/test_install_harness.py
```

If optional installer or test tooling is absent in a branch, run the preservation and legacy-token checks documented in `.agents/skills/harness/SKILL.md` and report the gap.

## Migration Pointer

This branch keeps the target repository history, imports upstream `revfactory/harness` at `cceac68ea1d0ad198ef4b7b906cd238375836387`, then ports only the runtime paths and coordination primitives to Codex-native structure.
