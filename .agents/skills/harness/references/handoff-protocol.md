# Handoff Protocol

이 문서는 parent orchestrator와 optional Codex custom subagents 사이의 handoff 규약이다.

## Principles

- subagent는 repository 파일과 `_workspace/` 파일을 직접 수정하지 않는다.
- subagent는 bounded analysis result를 parent에게 반환한다.
- parent는 모든 결과를 기다린 뒤 통합하고 파일을 쓴다.
- 병렬 subagent가 같은 output을 소유하지 않는다.

## Subagent Result Shape

```markdown
## Scope

## Inputs Read

## Findings

## Assumptions

## Risks

## Recommended Artifact Update
```

## Parent Write Targets

- discovery result → `_workspace/discovery.md`
- architecture result → `_workspace/architecture.md`
- skill design result → `_workspace/skills.md`
- QA result → `_workspace/qa-report.md`

## Partial Failure

실패한 subagent의 downstream artifact는 pending으로 둔다. parent는 성공한 artifact를 보존하고 실패 범위만 재시도한다.

## Workspace Rotation

반복 실행 시 이전 결과를 삭제하지 않고 iteration directory나 manifest status로 교체 관계를 표시한다.
