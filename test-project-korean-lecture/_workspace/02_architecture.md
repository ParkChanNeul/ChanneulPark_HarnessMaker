# Phase 2 아키텍처 설계

## 도메인

한국어 강의 자동화.

## 작업 유형

- 수업 목표 설계
- 수업 흐름 작성
- 활동지와 말하기 연습 생성
- 숙제 작성
- 수준/시간/한국어 자연성 검수

## 실행 모드

에이전트 팀.

## 아키텍처 패턴

Pipeline + Producer-Reviewer.

```text
lesson_planner
  -> activity_designer
      -> lesson_reviewer
          -> parent integration
```

## 에이전트

| 에이전트 | 역할 | 파일 |
|----------|------|------|
| lesson_planner | 수업 목표와 흐름 설계 | `.codex/agents/lesson_planner.toml` |
| activity_designer | 활동지와 숙제 설계 | `.codex/agents/activity_designer.toml` |
| lesson_reviewer | 수준, 시간, 자연성 검수 | `.codex/agents/lesson_reviewer.toml` |

## 스킬

| 스킬 | 용도 |
|------|------|
| korean-lesson-planning | 수업 설계 |
| korean-activity-design | 활동 제작 |
| korean-lesson-review | 검수 |
| korean-lecture-orchestrator | 전체 조율 |
