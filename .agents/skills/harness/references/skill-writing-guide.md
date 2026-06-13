<!--
MODIFICATION NOTICE
Source repository: https://github.com/revfactory/harness
Source commit: cceac68ea1d0ad198ef4b7b906cd238375836387
Modifier: ChanneulPark HarnessMaker
Change: Codex-native port. This active document preserves the upstream Harness behavior and replaces the legacy execution interface with Codex skills, custom subagents, and file-based handoff rules.
-->

# Skill Writing Guide

Harness가 생성하는 skill은 agent에게 반복 가능한 행동을 제공한다. 좋은 skill은 trigger가 명확하고, runtime dependency가 self-contained이며, instruction이 실행 가능한 형태다.

## Description Design

`description`은 skill discovery의 핵심이다.

- 언제 사용해야 하는지 구체적으로 쓴다.
- 비슷하지만 다른 작업에서는 trigger되지 않도록 boundary를 쓴다.
- keyword 나열보다 user intent를 설명한다.
- near-miss를 상상하고 제외 조건을 반영한다.

## Why First

instruction은 단순 절차보다 왜 그 절차가 필요한지 알려야 한다. agent는 새로운 상황에서 판단해야 하므로, 원칙과 trade-off를 같이 제공한다.

## Imperative Style

모호한 설명보다 실행 명령을 사용한다.

- 좋음: "먼저 기존 artifact를 읽고 변경 범위를 계산한다."
- 약함: "기존 artifact를 읽는 것이 좋다."

## Progressive Disclosure

모든 내용을 `SKILL.md`에 넣지 않는다. parent skill은 routing과 phase를 담고, 세부 기준은 `references/`로 나눈다.

- architecture 기준은 `agent-design-patterns.md`
- orchestration은 `orchestrator-template.md`
- testing은 `skill-testing-guide.md`
- QA는 `qa-agent-guide.md`

## Self-contained Runtime

installed skill만으로 실행되어야 한다.

- runtime reference는 skill directory 내부에 둔다.
- absolute local path를 쓰지 않는다.
- developer-only docs를 runtime dependency로 만들지 않는다.
- source repository의 install manifest를 skill package에 포함하지 않는다.

## Scripts and Assets

반복 작업이 안정적이고 deterministic하면 `scripts/`로 옮긴다. 단, MVP는 외부 dependency 없는 문서를 우선한다. script를 넣을 때는 입력/출력, failure message, idempotency를 문서화한다.

## Skill Boundary

skill이 맡는 일과 맡지 않는 일을 쓴다.

- 맡는 일: harness generation, workflow design, role definition, QA protocol
- 맡지 않는 일: landing page, marketplace packaging, runtime-specific legacy plugin packaging

## Generalization

사용자 feedback을 특정 test case에만 맞추지 않는다. 원인과 원리를 찾아 instruction에 반영한다. 한 예시를 통과하기 위해 넓은 trigger를 망가뜨리지 않는다.

## Anti-patterns

- 전체 원본 문서를 짧은 summary로 대체
- runtime path를 두 군데에 mirror
- model name을 hard-code
- subagent에게 final write를 맡김
- QA를 파일 존재 확인으로 축소
- near-miss trigger 검증 생략

## Output Shape

좋은 skill은 다음 산출물을 만든다.

- role definitions
- skill boundaries
- phase workflow
- architecture decision
- orchestration protocol
- QA checks
- maintenance/evolution rule

각 산출물은 `_workspace/` artifact contract를 따른다.
