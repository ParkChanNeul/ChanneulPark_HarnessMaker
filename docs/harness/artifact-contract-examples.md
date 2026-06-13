# Artifact Contract Examples

Developer-facing examples for the runtime contract in `.agents/skills/harness/references/artifact-contract.md`.

## Discovery Example

```yaml
artifact_type: discovery-result
schema_version: 1
producer: parent-orchestrator
source_phase: phase-1
created_at: 2026-01-01T00:00:00Z
status: complete
dependencies: []
```

## Architecture Example

```yaml
artifact_type: architecture-result
schema_version: 1
producer: parent-orchestrator
source_phase: phase-2
created_at: 2026-01-01T00:00:00Z
status: complete
dependencies: [discovery-result]
```
