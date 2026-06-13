<!--
MODIFICATION NOTICE
Source repository: https://github.com/revfactory/harness
Source commit: cceac68ea1d0ad198ef4b7b906cd238375836387
Modifier: ChanneulPark HarnessMaker
Change: Codex-native port. This active document preserves the upstream Harness behavior and replaces the legacy execution interface with Codex skills, custom subagents, and file-based handoff rules.
-->

# QA Agent Guide

QA는 단순 존재 확인이 아니라 통합 정합성 검증이다. Harness에서 QA role은 module boundary, data shape, state transition, route, generated artifact contract를 교차 비교한다.

## Common Missed Defects

### Boundary Mismatch

두 component가 각각 맞아도 연결이 틀릴 수 있다.

| Boundary | Failure |
| --- | --- |
| API response to hook type | producer shape와 consumer type이 다름 |
| route file to link | 실제 page path와 href가 다름 |
| state map to update code | 허용 transition과 실제 status update가 다름 |
| generated spec to skill | skill이 spec의 boundary를 반영하지 않음 |
| handoff result to artifact | subagent output이 artifact contract metadata를 충족하지 않음 |

## Cross-boundary Validation

QA는 항상 양쪽을 동시에 읽는다.

- producer와 consumer
- architecture decision과 agent definition
- skill description과 trigger eval
- orchestration plan과 handoff artifact
- generated output과 validation rule

## QA Design Principles

1. 존재 확인보다 연결 검증을 우선한다.
2. build pass를 runtime correctness로 착각하지 않는다.
3. assertion은 evidence와 함께 기록한다.
4. reviewer는 직접 최종 파일을 수정하지 않고 parent에게 issue를 반환한다.
5. 각 module 완료 직후 incremental QA를 실행한다.

## Checklist Template

### Harness Structure

- [ ] canonical skill path가 하나인가
- [ ] runtime reference가 skill directory 내부에 있는가
- [ ] optional Codex agent templates가 model을 hard-code하지 않는가
- [ ] parent-only final write 원칙이 문서화되어 있는가

### Architecture

- [ ] 선택 pattern이 request dependency와 맞는가
- [ ] rejected alternatives가 기록되었는가
- [ ] simple task를 불필요하게 multi-agent화하지 않았는가
- [ ] 병렬 agent가 같은 output을 소유하지 않는가

### Skill

- [ ] description이 trigger와 near-miss를 구분하는가
- [ ] reference link가 설치 후에도 유효한가
- [ ] progressive disclosure가 과도한 summary로 변하지 않았는가
- [ ] testing guide와 QA guide가 연결되는가

### Handoff

- [ ] artifact metadata가 존재하는가
- [ ] dependency가 존재하는 artifact를 가리키는가
- [ ] stale artifact가 active로 남아 있지 않은가
- [ ] partial failure status가 분명한가

## QA Report Shape

```markdown
# QA Report

metadata...

## Summary

## Passed Checks

## Failed Checks

## Cross-boundary Findings

## Required Follow-up
```

## Severity

- Critical: final output이 틀리거나 사용자 파일을 위험하게 덮어쓸 수 있음
- High: workflow 재실행이나 validation을 깨뜨림
- Medium: documentation과 implementation 불일치
- Low: maintenance clarity 문제

## Parent Integration

QA reviewer가 결과를 반환하면 parent는 finding을 중복 제거하고, 수정하거나 residual risk로 남긴다. 최종 validation 실행과 보고는 parent 책임이다.
