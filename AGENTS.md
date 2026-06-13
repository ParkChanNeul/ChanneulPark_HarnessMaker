# WHAT

이 저장소는 요구사항을 분석해 Codex-compatible harness를 생성하는 도구다.

# WHY

역할(role), workflow, skill, QA 규약을 반복 가능하고 검증 가능한 형태로 만든다. 원본 Harness의 판단 기준을 보존하되 실행 인터페이스는 Codex 환경에 맞춘다.

# HOW

- Canonical skill: `.agents/skills/harness/SKILL.md`
- Runtime references: `.agents/skills/harness/references/`
- Developer documents: `docs/`
- Runtime handoffs: `_workspace/`
- Native agent templates: `.codex/agents/`
- 설치 manifest는 source tree에 커밋하지 않는다.
- 변경 완료 전 `python3.11 scripts/validate_codex_port.py`와 unit test를 실행한다.
