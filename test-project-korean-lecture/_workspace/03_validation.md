# Phase 6 검증 기록

## 구조 검증

- `.codex/agents/lesson_planner.toml`: 생성
- `.codex/agents/activity_designer.toml`: 생성
- `.codex/agents/lesson_reviewer.toml`: 생성
- `.agents/skills/korean-lesson-planning/SKILL.md`: 생성
- `.agents/skills/korean-activity-design/SKILL.md`: 생성
- `.agents/skills/korean-lesson-review/SKILL.md`: 생성
- `.agents/skills/korean-lecture-orchestrator/SKILL.md`: 생성
- `AGENTS.md`: 생성

## 검증 기준

- custom agent TOML에 `name`, `description`, `sandbox_mode`, `developer_instructions` 포함
- `sandbox_mode = "read-only"` 사용
- 스킬 `SKILL.md`에 YAML frontmatter 포함
- 오케스트레이터에 실행 모드, 에이전트 구성, 데이터 흐름, 에러 핸들링, 테스트 시나리오 포함

## 미해결 가정

- 실제 학습자 수준, 주제, 수업 시간은 사용자 요청 시 매번 다시 확인한다.
- 이 하네스는 테스트 프로젝트용 최소 구성이다.
