---
name: korean-lecture-orchestrator
description: "한국어 강의 자동화 하네스 오케스트레이터. 한국어 수업안, 강의 계획, 활동지, 말하기 연습, 숙제, 검수 리포트 생성 요청 시 lesson_planner, activity_designer, lesson_reviewer를 조율한다. 재실행, 업데이트, 수정, 보완, 이전 결과 기반 개선 요청에도 사용한다."
---

# Korean Lecture Orchestrator

한국어 강의 자동화 하네스를 조율하여 수업 설계안, 활동 패키지, 검수 리포트, 최종 수업 자료를 생성한다.

## 실행 모드: 에이전트 팀

## 아키텍처 패턴

Pipeline + Producer-Reviewer.

- lesson_planner가 수업 목표와 흐름을 설계한다.
- activity_designer가 수업 활동과 숙제를 만든다.
- lesson_reviewer가 목표-활동 정렬, 시간 배분, 한국어 자연성을 검수한다.
- parent가 결과를 비교하고 최종 수업 자료를 작성한다.

## 에이전트 구성

| 팀원 | 에이전트 타입 | 역할 | 스킬 | 출력 |
|------|-------------|------|------|------|
| lesson_planner | custom | 수업 목표, 표현, 시간표 설계 | korean-lesson-planning | `_workspace/01_lesson_plan.md` |
| activity_designer | custom | 활동지, 말하기 연습, 숙제 설계 | korean-activity-design | `_workspace/02_activity_pack.md` |
| lesson_reviewer | custom | 수준, 시간, 자연성, 정렬 검수 | korean-lesson-review | `_workspace/03_review_report.md` |
| parent | orchestrator | 통합, 충돌 조정, 최종 작성 | 이 스킬 | `outputs/korean_lesson_package.md` |

## 워크플로우

### Phase 0: 컨텍스트 확인

1. `_workspace/` 존재 여부를 확인한다.
2. 기존 결과가 없으면 초기 실행으로 진행한다.
3. 기존 결과가 있고 사용자가 부분 수정, 재실행, 업데이트, 보완을 요청하면 해당 산출물만 재호출한다.
4. 새 요청이면 기존 `_workspace/`를 보존하고 새 입력을 `_workspace/00_input/request.md`에 기록한다.

### Phase 1: 준비

1. 사용자 요청에서 학습자 수준, 수업 시간, 주제, 목표 기능을 추출한다.
2. 정보가 부족하면 기본값을 둔다.
   - 수준: A2
   - 시간: 60분
   - 목표: 말하기 중심 수업
3. parent가 입력을 `_workspace/00_input/request.md`에 저장한다.

### Phase 2: 설계

lesson_planner를 dispatch한다.

```yaml
agent_file: .codex/agents/lesson_planner.toml
skill: korean-lesson-planning
input: _workspace/00_input/request.md
expected_output: _workspace/01_lesson_plan.md
completion_criteria:
  - 학습 목표 1-2개 포함
  - 핵심 표현 3-5개 포함
  - 45-60분 수업 흐름 포함
```

### Phase 3: 활동 제작

activity_designer를 dispatch한다.

```yaml
agent_file: .codex/agents/activity_designer.toml
skill: korean-activity-design
input:
  - _workspace/00_input/request.md
  - _workspace/01_lesson_plan.md
expected_output: _workspace/02_activity_pack.md
completion_criteria:
  - controlled practice 포함
  - free practice 또는 역할극 포함
  - 숙제 포함
```

### Phase 4: 검수

lesson_reviewer를 dispatch한다.

```yaml
agent_file: .codex/agents/lesson_reviewer.toml
skill: korean-lesson-review
input:
  - _workspace/01_lesson_plan.md
  - _workspace/02_activity_pack.md
expected_output: _workspace/03_review_report.md
completion_criteria:
  - 판정 포함
  - high/medium/low 수정 제안 포함
  - 목표-활동 정렬 검토 포함
```

### Phase 5: 통합

1. parent가 세 산출물을 모두 읽는다.
2. lesson_reviewer의 high 이슈는 반드시 반영한다.
3. medium 이슈는 시간과 목표에 맞으면 반영한다.
4. 최종 수업 자료를 `outputs/korean_lesson_package.md`에 작성한다.
5. 사용자에게 생성 파일과 미해결 가정을 요약한다.

## 데이터 흐름

```text
user request
  -> parent saves _workspace/00_input/request.md
  -> lesson_planner produces _workspace/01_lesson_plan.md
  -> activity_designer reads plan and produces _workspace/02_activity_pack.md
  -> lesson_reviewer reads plan + activities and produces _workspace/03_review_report.md
  -> parent integrates outputs/korean_lesson_package.md
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 수준 정보 없음 | A2로 가정하고 가정 섹션에 명시 |
| 시간 정보 없음 | 60분 수업으로 작성 |
| lesson_planner 실패 | parent가 요청을 좁혀 1회 재시도 |
| activity_designer 실패 | lesson plan만으로 간단 활동 2개를 parent가 작성하고 누락 명시 |
| lesson_reviewer 실패 | 검수 미완료로 표시하고 최종 산출물에 residual risk 기록 |
| 목표와 활동 충돌 | lesson_reviewer 의견을 우선하고 parent가 활동을 수정 |

## 테스트 시나리오

### 정상 흐름

1. 사용자가 "A2 학습자에게 병원 예약 표현을 가르치는 60분 수업안을 만들어줘"라고 요청한다.
2. lesson_planner가 목표, 표현, 시간표를 작성한다.
3. activity_designer가 말하기 활동과 숙제를 작성한다.
4. lesson_reviewer가 수준과 시간 배분을 검수한다.
5. parent가 `outputs/korean_lesson_package.md`를 작성한다.

### 에러 흐름

1. 사용자가 "한국어 수업 만들어줘"처럼 주제와 수준을 생략한다.
2. parent는 A2, 60분, 말하기 중심 수업으로 가정한다.
3. lesson_reviewer는 가정이 과한지 검토한다.
4. 최종 산출물의 가정 섹션에 부족한 정보를 명시한다.
