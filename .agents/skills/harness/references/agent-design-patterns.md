<!--
MODIFICATION NOTICE
Source repository: https://github.com/revfactory/harness
Source commit: cceac68ea1d0ad198ef4b7b906cd238375836387
Modifier: ChanneulPark HarnessMaker
Change: Codex-native port. This active document preserves the upstream Harness behavior and replaces the legacy execution interface with Codex skills, custom subagents, and file-based handoff rules.
-->

# Agent Design Patterns

이 문서는 Harness가 선택할 수 있는 6개 architecture pattern과 agent 분리 기준을 정의한다. Codex port에서는 pattern 이름과 판단 기준을 보존하고, 실행 방식만 parent-owned orchestration과 custom subagent delegation으로 바꾼다.

## Execution Model

Portable mode에서는 parent agent가 모든 role을 순차 실행한다. Codex-native mode에서는 사용자가 명시적으로 delegation을 요청했을 때만 custom subagent를 사용한다. subagent는 read-heavy analysis를 수행하고 결과를 반환한다. parent는 최종 파일 쓰기, conflict resolution, validation을 맡는다.

## Pattern Registry

### 1. Pipeline

순차 단계가 분명하고 앞 단계 output이 다음 단계 input이 되는 경우 사용한다. discovery → architecture → skill → QA처럼 dependency가 선형이면 가장 단순하고 안전하다.

- 장점: 재실행 범위가 명확하다.
- 위험: 병렬화 기회가 작다.
- Codex 사용: parent-only 또는 단계별 bounded subagent 호출.

### 2. Fan-out/Fan-in

서로 독립적인 조사나 분석을 병렬 수행한 뒤 하나의 통합 결과로 모을 때 사용한다.

- 장점: read-heavy discovery를 빠르게 확장한다.
- 위험: 동일 파일을 여러 agent가 수정하면 충돌한다.
- Codex 사용: subagent는 결과만 반환하고 parent가 fan-in summary를 작성한다.

### 3. Expert Pool

필요할 때만 호출되는 specialist 집합이다. 모든 specialist가 항상 실행되지는 않는다.

- 장점: domain-specific expertise를 재사용한다.
- 위험: 호출 조건이 흐리면 비용과 복잡도가 증가한다.
- Codex 사용: architecture, skill, QA처럼 명확한 specialty를 둔다.

### 4. Producer-Reviewer

한 역할이 산출물을 만들고 다른 역할이 검토한다. quality loop, writing, code review, design review에 적합하다.

- 장점: 품질 기준을 분리한다.
- 위험: reviewer가 산출물을 직접 고치면 ownership이 흐려진다.
- Codex 사용: reviewer는 issue와 recommendation을 반환하고 parent가 수정 여부를 결정한다.

### 5. Supervisor

중앙 coordinator가 task allocation, progress tracking, dependency ordering을 계속 수행한다.

- 장점: 복잡한 프로젝트의 상태 관리를 한 곳에 둔다.
- 위험: supervisor가 모든 세부 작업을 재검토하면 병목이 된다.
- Codex 사용: parent orchestrator가 supervisor 역할을 한다.

### 6. Hierarchical Delegation

큰 목표가 하위 목표로 나뉘고, 각 하위 목표가 다시 workflow를 가진다.

- 장점: 대형 시스템을 모듈 단위로 나눌 수 있다.
- 위험: depth가 깊어질수록 context drift가 생긴다.
- Codex 사용: MVP에서는 depth 1을 기본으로 제한하고 parent가 모든 결과를 통합한다.

## Selection Criteria

| 질문 | 선호 패턴 |
| --- | --- |
| 단계가 선형으로 의존하는가? | Pipeline |
| 독립 조사 후 통합인가? | Fan-out/Fan-in |
| 필요할 때만 전문가를 부르는가? | Expert Pool |
| 생성과 검토 loop가 핵심인가? | Producer-Reviewer |
| 중앙 조정자가 계속 배정해야 하는가? | Supervisor |
| 하위 프로젝트가 다시 분해되는가? | Hierarchical Delegation |

## Agent Split Criteria

agent를 분리할 때는 다음 조건 중 둘 이상이 충족되어야 한다.

- 서로 다른 evidence source를 읽는다.
- output format과 success criterion이 다르다.
- 병렬 실행해도 파일 write conflict가 없다.
- 독립적으로 재실행할 수 있다.
- 실패 시 영향 범위가 분리된다.

다음 경우에는 분리하지 않는다.

- 단순히 섹션 이름만 다른 경우
- 같은 파일을 동시에 고쳐야 하는 경우
- parent가 판단할 수 있는 작은 task인 경우
- subagent 호출 비용이 결과 품질보다 큰 경우

## Skill vs Agent

- Skill: 반복 가능한 행동 지침과 reference bundle.
- Agent: 특정 run에서 맡는 bounded role.
- Workflow: agent와 skill이 어떤 순서로 협력하는지에 대한 실행 규약.

## Composite Patterns

실제 harness는 하나의 pattern만 쓰지 않을 수 있다. 예를 들어 Supervisor + Fan-out/Fan-in은 discovery 병렬화 후 중앙 통합에 적합하다. Producer-Reviewer + Pipeline은 skill 작성 후 QA loop에 적합하다. 단, MVP에서는 composite를 쓰더라도 parent-only final write 원칙을 유지한다.
