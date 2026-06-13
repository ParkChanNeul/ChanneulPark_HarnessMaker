<!--
MODIFICATION NOTICE
Source repository: https://github.com/revfactory/harness
Source commit: cceac68ea1d0ad198ef4b7b906cd238375836387
Modifier: ChanneulPark HarnessMaker
Change: Codex-native port. This active document preserves the upstream Harness behavior and replaces the legacy execution interface with Codex skills, custom subagents, and file-based handoff rules.
-->

# Orchestrator Template

이 문서는 parent orchestrator가 Harness workflow를 실행하는 방식이다. Codex port에서는 legacy team primitive를 사용하지 않고, parent-owned plan, optional custom subagents, `_workspace/` artifact를 사용한다.

## Template A: Portable Parent Orchestrator

Portable mode의 기본 template이다.

### Context Check

1. 사용자 요청이 신규 생성, 확장, 운영 중 무엇인지 판정한다.
2. repository의 기존 skill, agent template, docs, `_workspace/`를 확인한다.
3. runtime dependency가 skill directory 내부에 있는지 확인한다.
4. 실행 중 생성할 artifact와 생략할 artifact를 선언한다.

### Workspace Setup

`_workspace/`는 실행 상태를 보존하는 장소다. 다음 파일을 우선 사용한다.

- `_workspace/discovery.md`
- `_workspace/architecture.md`
- `_workspace/skills.md`
- `_workspace/qa-report.md`
- `_workspace/manifest.md`

각 파일은 artifact metadata를 포함한다. timestamp는 ISO 8601 형식만 요구하고 테스트는 값 자체를 고정하지 않는다.

### Normal Flow

1. Phase 0 audit를 수행한다.
2. Phase 1 discovery를 기록한다.
3. Phase 2 architecture를 선택하고 rejected alternatives를 남긴다.
4. Phase 3 agent definitions를 설계한다.
5. Phase 4 skill boundary와 references를 설계한다.
6. Phase 5 orchestration plan과 handoff를 작성한다.
7. Phase 6 validation plan과 QA 결과를 기록한다.
8. Phase 7 maintenance/evolution 규칙을 manifest에 연결한다.

## Template B: Codex-native Orchestrator

사용자가 Codex-native mode와 delegation을 명시할 때만 사용한다.

### Spawn Conditions

- task가 read-heavy이고 bounded일 것
- output ownership이 parent에게 돌아올 것
- subagent가 repository 파일을 직접 수정하지 않아도 될 것
- 모든 결과를 기다린 뒤 parent가 통합할 수 있을 것

### Suggested Agent Use

- `discovery_analyst`: domain, ambiguity, constraints 분석
- `architecture_designer`: pattern 선택과 trade-off 분석
- `skill_designer`: skill boundary와 reference 설계
- `qa_reviewer`: cross-boundary QA와 completeness 검토

### Fan-in Rule

subagent 결과는 parent가 읽고 다음 순서로 통합한다.

1. conflicting assumptions 식별
2. missing evidence 보완
3. architecture와 skill boundary 조정
4. `_workspace/` artifact 작성
5. validation 실행

## Template C: Hybrid Follow-up

기존 harness에 follow-up 요청이 들어온 경우 전체 재생성보다 부분 재실행을 우선한다.

### Follow-up Classification

| 요청 유형 | 처리 |
| --- | --- |
| 새 domain capability 추가 | discovery와 architecture 영향 분석 |
| agent 하나의 role 수정 | 해당 agent와 관련 skill/QA만 재검토 |
| skill trigger 문제 | skill-writing과 trigger eval만 재실행 |
| QA regression | 관련 boundary와 test fixture만 재실행 |
| upstream 변경 반영 | provenance와 port checklist 갱신 |

## Dependency Ordering

- discovery는 architecture보다 먼저 완료되어야 한다.
- architecture는 agent definition보다 먼저 완료되어야 한다.
- agent definition은 skill boundary와 orchestration보다 먼저 완료되어야 한다.
- QA는 최종 validation이지만, 경계면 검증은 각 module 완료 직후에도 수행할 수 있다.

## Workspace Rotation

`_workspace/`가 커지면 삭제하지 말고 iteration을 나눈다.

```text
_workspace/
  manifest.md
  iteration-001/
  iteration-002/
```

manifest에는 active iteration과 superseded artifact를 적는다. 이전 artifact는 regression 추적에 사용한다.

## Error Flow

### Subagent Failure

- 실패 agent, input, expected output, actual failure를 기록한다.
- 해당 agent 결과에 의존하는 downstream artifact를 pending으로 표시한다.
- retry 가능 여부를 판단한다.

### Partial Failure

- 이미 성공한 artifact는 유지한다.
- 실패한 phase만 재실행한다.
- parent가 merge conflict를 정리할 수 없으면 사용자에게 좁은 질문을 한다.

### Retry Policy

1. 같은 input으로 한 번 재시도한다.
2. 실패가 반복되면 input을 줄이고 assumption을 명시한다.
3. 세 번째 실패 후에는 blocked reason과 필요한 사용자 판단을 기록한다.

## Test Scenarios

### Normal Scenario

- 신규 project request가 들어온다.
- Pipeline pattern이 선택된다.
- parent가 discovery, architecture, skills, QA artifact를 순서대로 작성한다.
- validator가 canonical skill path와 reference link를 통과한다.

### Error Scenario

- architecture subagent가 두 pattern을 conflicting하게 제안한다.
- parent가 rejected alternatives를 비교하고 하나를 선택한다.
- 선택 근거와 버린 이유를 `_workspace/architecture.md`에 기록한다.

### Partial Rerun Scenario

- 사용자가 skill trigger를 수정해 달라고 한다.
- Phase 4와 Phase 6 trigger eval만 재실행한다.
- Phase 1~3은 manifest에서 unchanged로 유지한다.

## Initial Run Keyword

The initial run path is the first full execution of Phase 0 through Phase 7 before follow-up narrowing is available.
