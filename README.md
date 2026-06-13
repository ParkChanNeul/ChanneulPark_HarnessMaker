# ChanneulPark HarnessMaker

ChanneulPark HarnessMaker는 요구사항을 분석해 Codex-native이면서 portable한 Harness를 만드는 MVP 프로젝트다. 원본 [revfactory/harness](https://github.com/revfactory/harness)의 핵심 문서와 판단 기준을 기준 commit `cceac68ea1d0ad198ef4b7b906cd238375836387`에서 직접 읽고, Codex skill 및 custom subagent 구조로 변환했다.

## 원본 Harness와의 관계

원본 Harness는 domain analysis, architecture pattern 선택, 역할별 agent 정의, skill 작성, orchestration, testing, QA를 하나의 meta-skill로 묶는다. 이 저장소는 해당 기능을 축약하지 않고 Codex 구조로 옮긴다. 단, 실행 인터페이스는 Codex의 `.agents/skills`와 `.codex/agents`를 사용한다.

`meta-harness`는 이번 MVP의 source나 dependency가 아니다. 포팅 기준은 `revfactory/harness` 하나다.

## 실행 모드

### Portable mode

기본 모드다. parent agent가 모든 phase를 순차적으로 수행하고, 주요 판단과 산출물을 `_workspace/`에 기록한다. custom subagent 없이도 동작해야 하며 다른 agent runtime에서도 file-based workflow로 재사용할 수 있다.

예시:

```text
$harness 이 프로젝트의 요구사항을 분석하고 portable mode로 역할, workflow, skill, QA 규약을 설계해줘.
```

### Codex-native mode

사용자가 native agent, subagent, delegation, parallel execution을 명시적으로 요청할 때만 사용한다. 필요한 custom agents를 선택적으로 spawn하고, 독립적인 read-heavy 작업만 병렬화한다. 모든 agent 결과를 기다린 뒤 parent가 `_workspace/` 파일 작성, 최종 통합, validation을 책임진다.

예시:

```text
$harness 이 프로젝트를 Codex-native mode로 분석해줘.
필요한 custom agents를 명시적으로 spawn하고,
모든 결과를 기다린 뒤 parent가 최종 설계를 통합해줘.
```

Custom agents use `sandbox_mode = "read-only"` and explicit no-write instructions by default. Parent-session runtime overrides may still apply, so this setting is not treated as an absolute security boundary.

## 설치 요구사항

- Python 3.11+
- 외부 Python dependency 없음
- `python3`가 3.11 미만이면 `python3.11`을 사용한다.

## Project scope 설치

```bash
python3.11 scripts/install_harness.py   --scope project   --target /path/to/repo
```

agent template까지 설치:

```bash
python3.11 scripts/install_harness.py   --scope project   --target /path/to/repo   --with-agent-templates
```

## User scope 설치

```bash
python3.11 scripts/install_harness.py --scope user
```

user scope에서 agent template까지 설치하면 config 예시는 `~/.codex/harnessmaker.config.toml.example`에 놓인다. 실제 Codex project config는 `.codex/config.toml`이며, HarnessMaker는 기존 config를 자동 생성하거나 덮어쓰지 않는다.

## 안전한 재설치

설치 스크립트는 기본적으로 기존 파일을 덮어쓰지 않는다. 설치가 성공하면 target skill 디렉터리에 `.harnessmaker-install.json` manifest를 마지막 단계에서 생성한다. 이 파일은 source tree에는 포함하지 않는다.

- 설치된 파일과 source가 같으면 반복 설치는 idempotent no-op이다.
- managed file이 수정된 경우 기본 실행은 실패한다.
- `--force`는 manifest가 관리하는 HarnessMaker 파일만 백업 후 교체한다.
- manifest에 없는 동일 이름 파일은 사용자 파일로 간주하고 `--force`로도 자동 교체하지 않는다.
- `.codex`가 파일인 target은 agent template 설치 시에만 실패한다. skill-only 설치는 `.codex`를 건드리지 않는다.

Dry run:

```bash
python3.11 scripts/install_harness.py   --scope project   --target /tmp/harnessmaker-smoke   --with-agent-templates   --dry-run
```

## 생성되는 산출물

- 역할별 agent definition
- skill definition
- 단계별 workflow
- architecture pattern 선택
- orchestration 규약
- handoff 규약
- QA 및 검증 규칙
- Codex custom subagent template
- portable file-based workflow

## `_workspace/` 규약

이 저장소의 `_workspace/`는 개발 및 예시용 placeholder다. installer는 target repository에 `_workspace/`를 강제로 만들지 않는다. 실제 Harness 실행 중 parent agent가 필요하면 생성한다. runtime artifact는 commit하지 않는 것이 기본이다.

## 검증

```bash
python3.11 scripts/validate_codex_port.py
python3.11 scripts/test_install_harness.py
python3.11 -m unittest discover -s tests
```

선택적 Codex runtime eval:

```bash
python3.11 tests/evals/run_architecture_eval.py
```

Codex CLI가 없거나 인증되지 않으면 eval은 skip된다.

## 라이선스 및 attribution

원본 `revfactory/harness`는 Apache License 2.0이다. `LICENSE`, `THIRD_PARTY_NOTICES.md`, `docs/upstream/provenance.md`에 출처와 변환 내역을 기록했다. upstream에는 `NOTICE`, `COPYRIGHT`, 별도 third-party attribution 파일이 없음을 확인했다.

## MVP 한계

- 실제 Codex runtime에서 subagent 호출 품질은 optional eval로만 확인한다.
- installer는 기존 `.codex/config.toml` 병합을 수행하지 않는다.
- architecture selection은 natural-language skill 판단이므로 unit test는 fixture schema를 검증하고, 실제 판단 검증은 optional runtime eval로 분리한다.

## English Summary

ChanneulPark HarnessMaker is a Codex-native port of the core revfactory Harness workflow. It installs a self-contained `.agents/skills/harness` skill and optional `.codex/agents` templates while preserving portable file-based handoff rules.
