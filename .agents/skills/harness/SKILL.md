---
name: harness
description: 요구사항을 분석해 Codex-compatible agent harness, workflow, skills, QA 규약, portable handoff를 설계하거나 생성할 때 사용한다.
---

<!--
MODIFICATION NOTICE
Source repository: https://github.com/revfactory/harness
Source commit: cceac68ea1d0ad198ef4b7b906cd238375836387
Modifier: ChanneulPark HarnessMaker
Change: Codex-native port. This active document preserves the upstream Harness behavior and replaces the legacy execution interface with Codex skills, custom subagents, and file-based handoff rules.
-->

# Harness Skill

이 skill은 domain-specific agent harness를 설계한다. 목적은 한 번의 답변을 잘 쓰는 것이 아니라, 반복 실행 가능한 역할 분리, skill boundary, orchestration, QA, evolution 규칙을 만드는 것이다.

## Runtime Contract

- Canonical skill source는 `.agents/skills/harness/` 하나다.
- 실행 중 필요한 모든 reference는 `references/` 내부에 있어야 한다.
- `docs/` 아래 문서는 개발자 설명이며 installed skill의 runtime dependency로 삼지 않는다.
- parent orchestrator가 최종 파일 작성과 검증을 소유한다.
- custom subagent는 분석 결과를 반환하고 repository 파일을 직접 수정하지 않는다.

## Execution Modes

### Portable mode

Portable mode가 기본이다.

1. parent agent가 Phase 0부터 Phase 7까지 순차 수행한다.
2. 주요 판단, 산출물, 재실행 가능 로그를 `_workspace/`에 기록한다.
3. custom subagent 없이도 완료 가능해야 한다.
4. 다른 runtime에서도 `_workspace/` 파일 handoff만으로 이어받을 수 있게 작성한다.

### Codex-native mode

Codex-native mode는 사용자가 native agent, custom agent, subagent, delegation, parallel execution을 명시적으로 요청한 경우에만 사용한다.

1. parent가 필요한 custom agents만 선택한다.
2. 독립적인 read-heavy task만 병렬화한다.
3. 모든 custom agent 결과를 기다린 뒤 parent가 통합한다.
4. parent만 `_workspace/` 파일과 최종 산출물을 쓴다.
5. 충돌 가능성이 있는 최종 쓰기와 validation은 parent 책임이다.

사용자 호출 예시는 다음 의미를 포함해야 한다.

```text
Codex-native mode로 실행해.
필요한 custom agents를 명시적으로 spawn하고,
모든 결과를 기다린 뒤 parent가 최종 결과를 통합해.
```

## Source References

이 skill을 사용할 때 필요한 reference를 상황에 맞게 읽는다.

- `references/agent-design-patterns.md`: architecture pattern과 agent 분리 기준
- `references/orchestrator-template.md`: 초기 실행, 후속 실행, dependency ordering, retry, partial failure
- `references/team-examples.md`: 실제 team 구성 예제와 data flow
- `references/skill-writing-guide.md`: skill 작성, trigger, progressive disclosure, scripts/assets 기준
- `references/skill-testing-guide.md`: with-skill/baseline, trigger eval, near-miss, 반복 개선
- `references/qa-agent-guide.md`: cross-boundary validation과 QA 설계
- `references/artifact-contract.md`: `_workspace/` artifact metadata와 파일 형식
- `references/handoff-protocol.md`: parent/subagent handoff 규약

## Phase 0: Existing Harness Audit

요구가 신규 생성인지, 기존 harness 확장인지, 운영/유지보수인지 먼저 판정한다.

### 신규 생성

- domain, target user, 반복 업무, 실패 비용을 식별한다.
- 기존 repository에 skill, agent, workflow 흔적이 없는지 확인한다.
- `_workspace/discovery.md`에 문제 정의와 capability inventory를 기록한다.

### 기존 확장

- 기존 skill, reference, tests, workspace artifact를 읽는다.
- canonical source와 generated artifact를 구분한다.
- 확장 요구가 기존 architecture를 유지하는지, pattern 변경을 요구하는지 판단한다.

### 운영/유지보수

- 최근 변경, 실패한 eval, regression, 사용자 피드백을 먼저 읽는다.
- 전체 재생성보다 부분 재실행을 우선 검토한다.
- workspace rotation이 필요한지 판단한다.

## Phase 1: Domain Analysis

요구사항을 도메인 작업으로 분해한다.

- 주요 task와 반복 task를 식별한다.
- 입력, 출력, 상태, 외부 dependency를 분리한다.
- 사용자 언어의 모호성을 명시한다.
- human review가 필요한 판단과 자동화 가능한 판단을 구분한다.
- capability 목록을 role 후보로 바꾸기 전에 evidence를 남긴다.

Output: `_workspace/discovery.md`

## Phase 2: Architecture Pattern Selection

`references/agent-design-patterns.md`의 6개 pattern registry를 기준으로 선택한다.

- 단일 흐름과 의존성이 강하면 Pipeline을 우선한다.
- 독립 조사 후 통합이면 Fan-out/Fan-in을 선택한다.
- 필요할 때 호출되는 전문가 집합이면 Expert Pool을 선택한다.
- 품질 개선 loop가 핵심이면 Producer-Reviewer를 선택한다.
- 중앙 조정자가 planning과 allocation을 계속 수행하면 Supervisor를 선택한다.
- 하위 단위가 다시 분해되는 복합 구조면 Hierarchical Delegation을 선택한다.

선택 이유, trade-off, rejected alternatives를 기록한다. simple task에서는 agent 수를 늘리지 않는다.

Output: `_workspace/architecture.md`

## Phase 3: Agent Definition

각 agent는 다음을 가져야 한다.

- responsibility: 맡는 문제와 맡지 않는 문제
- input contract: 읽어야 할 artifact와 source
- output contract: parent에게 반환할 결과 형식
- boundary: 직접 쓰기 금지 영역과 handoff 방식
- reuse criterion: 다른 harness에서도 재사용 가능한지

Codex-native mode에서는 `.codex/agents/*.toml` template을 참고하되, parent가 결과를 통합한다. agent 이름은 파일명과 일치하는 snake_case를 사용한다.

## Phase 4: Skill Generation

skill은 agent가 반복적으로 잘해야 하는 행동을 캡슐화한다.

- `description`은 trigger boundary를 명확히 쓴다.
- near-miss query에서 잘못 trigger되지 않게 한다.
- 긴 reference는 progressive disclosure로 나눈다.
- 반복 실행 코드는 `scripts/`로 둘 수 있으나 MVP runtime은 dependency 없는 문서를 우선한다.
- skill 내부 runtime link는 skill directory 내부만 참조한다.

Output: `_workspace/skills.md`

## Phase 5: Orchestration

orchestrator는 초기 실행과 후속 실행을 다르게 처리한다.

### Initial Run

1. context와 mode를 확인한다.
2. `_workspace/manifest.md` 또는 phase별 artifact를 만든다.
3. phase dependency를 ordering한다.
4. subagent가 필요한 경우 명시적으로 spawn하고 결과를 기다린다.
5. parent가 통합 결과를 기록한다.

### Follow-up Run

1. `_workspace/manifest.md`와 최근 artifact status를 읽는다.
2. 사용자 요청이 전체 재실행인지 부분 재실행인지 판정한다.
3. 영향 범위를 계산하고 필요한 phase만 갱신한다.
4. 오래된 artifact는 삭제보다 rotation 또는 superseded 표시를 우선한다.

### Error Flow

- subagent 실패는 parent가 실패 원인, 영향 artifact, retry 여부를 기록한다.
- partial failure에서는 완료 artifact를 보존하고 누락 artifact만 재실행한다.
- 같은 실패가 반복되면 assumption을 줄이고 사용자 확인이 필요한 질문을 분리한다.

Output: `_workspace/manifest.md`와 phase artifacts

## Phase 6: Validation and Testing

검증은 파일 존재 확인으로 끝나지 않는다.

- with-skill vs baseline 비교를 설계한다.
- trigger와 near-miss query를 만든다.
- generated workflow가 실제 사용 예시를 통과하는지 확인한다.
- QA는 component 존재보다 boundary consistency를 우선한다.
- Codex-native mode에서는 parent가 모든 subagent 결과를 기다린 뒤 validation을 실행한다.

Output: `_workspace/qa-report.md`

## Phase 7: Evolution and Maintenance

완성 후에도 harness는 유지보수 대상이다.

- 사용자 피드백과 regression을 `_workspace/`에 연결한다.
- skill description 변경은 trigger eval로 검증한다.
- architecture pattern 변경은 rejected alternatives까지 갱신한다.
- workspace가 커지면 iteration 단위로 rotation하고 manifest에 active artifact를 명시한다.
- upstream 판단자료가 변경되면 provenance와 port checklist를 갱신한다.

## Partial Rerun Rules

- discovery만 바뀌면 architecture 이후 phase를 영향 분석한다.
- architecture가 바뀌면 agent, skill, orchestration, QA를 재검토한다.
- skill만 바뀌면 trigger eval과 with-skill/baseline eval을 우선 실행한다.
- QA 실패는 실패 boundary와 관련 agent만 재호출한다.

## Completion Checklist

- Phase 0 branch가 명시됨
- Phase 1~6 artifact가 존재하거나 생략 사유가 있음
- Phase 7 maintenance rule이 있음
- architecture pattern 선택과 trade-off가 기록됨
- custom subagent 호출 조건이 명시됨
- 모든 중요한 결과가 `_workspace/`에 기록됨
- validation이 실행되거나 실행 불가 사유가 기록됨
