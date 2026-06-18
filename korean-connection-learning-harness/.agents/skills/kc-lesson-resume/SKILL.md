---
name: kc-lesson-resume
description: Use when a Korean Connection teacher explicitly supplies an existing run_dir or run_id and wants to inspect or continue that exact lesson conversation.
---

# KC Lesson Resume

Resume only the workspace explicitly named by the teacher.

## Preconditions

- Accept `run_dir=_workspace/runs/<run_id>` or an exact `run_id` that resolves unambiguously.
- If neither is present, stop and request one.
- Never infer the latest run, the only run, or a fixture as active learner context.

## Read-Only Behavior

Read the named run and report locked decisions, open decisions, artifacts, blockers, and the next recommended conversational step. A read request does not authorize file modification.

## Output

```markdown
# Lesson Workspace Resume

## 현재 Run 상태
## 잠긴 결정
## 아직 열린 결정
## 생성된 산출물
## 다음 권장 단계
```

## Next Skill Handoff

- Recommended Next Skill: the next incomplete conversational skill
- Why: continue from the exact recorded state without guessing
- Ready To Continue: yes | no
- Need Teacher Confirmation: yes when any decision remains open
- Requires run_dir: yes
- Blocking Conditions: missing or ambiguous run reference, invalid contract, or unresolved lock field
- Suggested Prompt: confirm the proposed next decision for this run
