<!--
MODIFICATION NOTICE
Source repository: https://github.com/revfactory/harness
Source commit: cceac68ea1d0ad198ef4b7b906cd238375836387
Modifier: ChanneulPark HarnessMaker
Change: Codex-native port. This active document preserves the upstream Harness behavior and replaces the legacy execution interface with Codex skills, custom subagents, and file-based handoff rules.
-->

# Team Examples

이 문서는 Harness가 만들 수 있는 실제 team 구성 예제를 보존한다. Codex port에서는 모든 예제가 parent-owned orchestration과 read-only custom subagent 결과 반환으로 표현된다.

## Example 1: Research Synthesis Team

### Scenario

여러 자료를 읽고 시장/기술/경쟁 관점을 통합해 의사결정 문서를 만든다.

### Roles

- discovery researcher: source inventory와 신뢰도 평가
- market analyst: 시장 signal과 사용자 pain point 분석
- technical analyst: 구현 가능성과 risk 분석
- synthesis parent: conflict를 해소하고 최종 brief 작성

### Pattern

Fan-out/Fan-in. 세 analyst는 독립 자료를 읽고 parent가 하나의 synthesis로 통합한다.

### Data Flow

1. parent가 질문과 evidence boundary를 정한다.
2. analyst들이 결과를 반환한다.
3. parent가 중복, 충돌, missing source를 정리한다.
4. `_workspace/discovery.md`와 `_workspace/architecture.md`를 작성한다.

## Example 2: Fiction Writing Harness

### Scenario

장편 SF 소설의 설정, 플롯, 인물, 장면 초안을 반복적으로 만든다.

### Roles

- worldbuilder: 세계관 규칙과 제약
- plot architect: arc, act, sequence 설계
- character designer: 인물 욕망과 conflict
- reviewer: continuity와 tone 검토
- parent editor: canon bible과 chapter plan 통합

### Pattern

Producer-Reviewer + Pipeline. 설정과 플롯이 먼저 나오고, reviewer가 continuity issue를 찾는다.

### Handoff

각 role은 직접 원고를 덮어쓰지 않고 canon delta를 반환한다. parent editor가 최종 text와 changelog를 쓴다.

## Example 3: Webtoon Producer-Reviewer

### Scenario

웹툰 episode를 기획하고 컷 구성, 대사, QA를 반복한다.

### Roles

- episode planner: 사건 흐름과 cliffhanger
- panel designer: 컷 단위 framing
- dialogue writer: 말투와 감정선
- continuity reviewer: 설정/이전 회차 충돌 검토
- parent producer: 최종 episode spec 통합

### Pattern

Producer-Reviewer. reviewer는 문제를 발견하고 parent producer에게 수정 제안을 반환한다.

### Validation

- 각 컷이 episode 목적에 기여하는가
- dialogue가 character voice와 일치하는가
- 이전 회차 설정과 모순되지 않는가

## Example 4: Code Review Team

### Scenario

큰 diff를 architecture, security, test, integration 관점으로 검토한다.

### Roles

- architecture reviewer: module boundary와 dependency
- security reviewer: trust boundary와 unsafe input
- test reviewer: missing coverage와 flaky risk
- integration reviewer: API, type, route, state boundary consistency
- parent maintainer: severity 정렬과 actionable report 작성

### Pattern

Expert Pool + Fan-out/Fan-in. 모든 reviewer가 항상 필요한 것은 아니지만 큰 diff에서는 병렬 분석이 유효하다.

### Output

parent maintainer는 finding을 severity, file path, line reference, reproduction, fix direction으로 정리한다.

## Example 5: Migration Supervisor

### Scenario

legacy runtime interface를 Codex-compatible structure로 옮긴다.

### Roles

- source auditor: 원본 feature와 runtime-specific primitive 분리
- port designer: Codex 대응 구조 설계
- installer engineer: safe installation과 rollback 구현
- QA reviewer: canonical 영역에 legacy runtime dependency가 남았는지 검증
- parent supervisor: final source tree, tests, provenance 통합

### Pattern

Supervisor + Pipeline. parent가 dependency ordering과 final write를 통제한다.

### Failure Handling

- 원본 heading이 누락되면 port checklist를 실패시킨다.
- runtime-specific primitive를 제거했는데 대체 동작이 없으면 migration gap으로 기록한다.
- installer가 unmanaged file을 만나면 실패하고 사용자 파일을 보존한다.

## Reuse Notes

이 예제들은 그대로 복사하기보다 domain에 맞게 role 이름과 artifact를 바꿔 사용한다. 중요한 것은 pattern, data flow, ownership, QA boundary다.
