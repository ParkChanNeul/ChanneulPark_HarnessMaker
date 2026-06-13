<!--
MODIFICATION NOTICE
Source repository: https://github.com/revfactory/harness
Source commit: cceac68ea1d0ad198ef4b7b906cd238375836387
Modifier: ChanneulPark HarnessMaker
Change: Codex-native port. This active document preserves the upstream Harness behavior and replaces the legacy execution interface with Codex skills, custom subagents, and file-based handoff rules.
-->

# Skill Testing Guide

Skill 품질은 정성 평가와 정량 평가를 함께 사용해 검증한다. 핵심 loop는 작성, 실행, 평가, 개선, 재테스트다.

## Test Prompt Design

테스트 프롬프트는 실제 사용자가 말할 법해야 한다.

- 공식/캐주얼 톤을 섞는다.
- 명시적/암시적 요청을 섞는다.
- 단순 작업과 edge case를 모두 포함한다.
- 파일명, column name, domain constraint 같은 구체 정보를 넣는다.

너무 추상적인 "분석해줘"는 trigger와 output 품질을 검증하기 어렵다.

## With-skill vs Baseline

각 eval은 같은 prompt를 두 조건에서 비교한다.

- with-skill: Harness skill을 사용한다.
- baseline: skill 없이 수행하거나, 기존 version을 사용한다.

Codex-native mode에서는 두 실행을 독립 task로 구성할 수 있지만, 결과 수집과 비교는 parent가 수행한다. timing, token, output path, pass/fail evidence를 즉시 기록한다.

## Assertions

좋은 assertion은 객관적으로 참/거짓을 판정할 수 있다.

- 산출물이 요구된 파일을 생성했는가
- architecture pattern 선택 이유가 request 제약과 연결되는가
- QA가 cross-boundary issue를 확인했는가
- handoff metadata가 contract를 만족하는가

항상 통과하는 assertion은 제거한다. 두 조건 모두 100% 통과하면 skill의 차별 가치를 측정하지 못한다.

## Trigger Evaluation

20개 query를 만든다.

- should-trigger 10개
- should-not-trigger 10개

should-not-trigger는 near-miss가 중요하다. 관련 단어는 있지만 다른 skill이나 일반 답변이 더 적합한 사례를 포함한다.

## Existing Skill Conflict

새 skill description이 기존 skill과 겹치지 않는지 확인한다. should-trigger query가 다른 skill을 강하게 부르면 description boundary를 좁힌다.

## Specialist Evaluation Roles

- Grader: assertion별 pass/fail과 evidence 기록
- Comparator: A/B output을 blind 비교
- Analyzer: non-discriminating assertion, variance, cost trade-off 분석

MVP에서는 이 role도 parent가 수행할 수 있다. Codex-native mode에서는 read-only reviewer로 호출하고 parent가 최종 판단한다.

## Iteration Structure

```text
_workspace/
  iteration-001/
    eval-domain-analysis/
      with_skill/
      without_skill/
      grading.json
    benchmark.json
  iteration-002/
```

이전 iteration은 덮어쓰지 않는다. regression을 확인할 수 있어야 한다.

## Improvement Rules

1. feedback을 일반화한다.
2. 불필요한 instruction을 제거한다.
3. 왜 중요한지 skill에 반영한다.
4. 반복 script는 bundle한다.
5. 수정 후 trigger eval과 representative eval을 다시 실행한다.

## Exit Conditions

- 사용자가 품질을 승인한다.
- 모든 critical assertion이 통과한다.
- near-miss trigger가 안정적이다.
- 더 이상의 변경이 regression risk만 키운다.
