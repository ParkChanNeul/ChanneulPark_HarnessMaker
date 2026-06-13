# Upstream Provenance

## Source of Truth

- Repository: https://github.com/revfactory/harness
- Recorded source commit: `cceac68ea1d0ad198ef4b7b906cd238375836387`
- Implementation-time checkout: `cceac68ea1d0ad198ef4b7b906cd238375836387`
- Commit verification: `git cat-file -e cceac68ea1d0ad198ef4b7b906cd238375836387^{commit}` succeeded in the local upstream clone.
- Local clone path during implementation: sibling repository outside this source tree.

## License and Notice

- License: Apache License 2.0
- Upstream `LICENSE`: present
- Upstream `NOTICE`: not found at the checked revision
- Upstream `COPYRIGHT`: not found at the checked revision
- Upstream separate third-party attribution file: not found at the checked revision

## Read and Ported Files

| Upstream file | Active target | Classification |
| --- | --- | --- |
| `skills/harness/SKILL.md` | `.agents/skills/harness/SKILL.md` | ported from upstream + Codex runtime substitution |
| `skills/harness/references/agent-design-patterns.md` | `.agents/skills/harness/references/agent-design-patterns.md` | ported from upstream + Codex runtime substitution |
| `skills/harness/references/orchestrator-template.md` | `.agents/skills/harness/references/orchestrator-template.md` | ported from upstream + Codex runtime substitution |
| `skills/harness/references/team-examples.md` | `.agents/skills/harness/references/team-examples.md` | ported from upstream + Codex runtime substitution |
| `skills/harness/references/skill-writing-guide.md` | `.agents/skills/harness/references/skill-writing-guide.md` | ported from upstream + Codex runtime substitution |
| `skills/harness/references/skill-testing-guide.md` | `.agents/skills/harness/references/skill-testing-guide.md` | ported from upstream + Codex runtime substitution |
| `skills/harness/references/qa-agent-guide.md` | `.agents/skills/harness/references/qa-agent-guide.md` | ported from upstream + Codex runtime substitution |

## Codex Runtime Substitutions

- Legacy skill location changed to `.agents/skills/harness/`.
- Legacy agent definitions changed to `.codex/agents/*.toml` templates.
- Legacy team primitives are replaced by explicit Codex custom subagent delegation and parent-owned `_workspace/` artifacts.
- Model-specific defaults are removed.
- Runtime-required artifact and handoff contracts are placed inside the skill `references/` directory.

## ChanneulPark Extensions

- installer with manifest-based managed-file safety
- Codex custom agent templates
- architecture pattern machine-readable registry
- port checklist for source coverage validation
- Python unittest-based installer and schema tests

## Excluded Upstream Files

Landing pages, images, privacy page, marketplace packaging material, and plugin packaging files are excluded from the MVP because the scope is Codex-native harness generation, not marketing or legacy packaging.
