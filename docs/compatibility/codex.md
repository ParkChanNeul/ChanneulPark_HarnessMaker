# Codex Compatibility

## Skill Discovery

Project skills are installed under `.agents/skills/<name>/`. User skills are installed under `~/.agents/skills/<name>/`. HarnessMaker uses `.agents/skills/harness/` as the only canonical skill source.

## Custom Agents

Project custom agents are installed under `.codex/agents/*.toml`; user custom agents under `~/.codex/agents/*.toml`. HarnessMaker agent templates define `name`, `description`, `sandbox_mode = "read-only"`, and `developer_instructions`. They do not set a model.

Custom agents do not run merely because files exist. Native mode starts only when the user explicitly requests custom agents, subagents, delegation, or parallel execution.

## Read-only Policy

Custom agents use read-only sandbox configuration and explicit no-write instructions. Runtime overrides from the parent session may still apply, so this is a policy and guardrail, not a complete security boundary.

## Config Example

`.codex/config.toml.example` is not active config. Users manually merge relevant settings into `.codex/config.toml` in trusted projects. User scope installs use `~/.codex/harnessmaker.config.toml.example` to avoid implying global activation.
