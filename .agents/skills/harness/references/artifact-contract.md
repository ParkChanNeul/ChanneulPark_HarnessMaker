# Workspace Artifact Contract

이 문서는 installed skill runtime에서 사용하는 `_workspace/` artifact 형식이다.

## Required Metadata

각 artifact는 본문 앞에 다음 metadata block을 포함한다.

```yaml
artifact_type: discovery-result
schema_version: 1
producer: parent-orchestrator
source_phase: phase-1
created_at: 2026-01-01T00:00:00Z
status: complete
dependencies: []
```

테스트는 timestamp 값을 고정하지 않고 ISO 8601 형식만 확인한다.

## Artifact Types

- `discovery-result`: domain, constraints, capabilities
- `architecture-result`: selected pattern, alternatives, trade-off
- `skill-design-result`: skill boundaries, references, trigger rules
- `qa-result`: passed/failed checks and boundary findings
- `manifest`: active iteration, artifact status, rerun plan

## Status Values

- `draft`
- `complete`
- `blocked`
- `superseded`
- `failed`

## Parent Ownership

Custom subagents return analysis to the parent. Parent writes `_workspace/discovery.md`, `_workspace/architecture.md`, `_workspace/skills.md`, `_workspace/qa-report.md`, and `_workspace/manifest.md`.
