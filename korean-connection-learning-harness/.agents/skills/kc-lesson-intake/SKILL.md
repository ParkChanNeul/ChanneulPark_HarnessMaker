---
name: kc-lesson-intake
description: Use when a Korean Connection teacher gives an incomplete lesson request without an approved scope or asks to start planning a lesson conversationally.
---

# KC Lesson Intake

Interpret the teacher's initial request without building a lesson or choosing progression.

## Rules

1. Separate provided facts from unknowns.
2. Do not infer a recent learner, run, fixture, or workspace.
3. Do not read existing run files unless the teacher provides an exact `run_dir` or `run_id`.
4. Do not create files or lock scope during bare intake.
5. Ask only the highest-impact missing questions and do not repeat information already supplied.
6. Route rich input to `kc-lesson-turn`; route an explicit run reference to `kc-lesson-resume`.

## Intake Categories

Learner type, level, lesson duration, target situation, teacher goal, previous lesson, lesson direction, target learner action, and requested outputs.

## Output

```markdown
# Korean Connection Lesson Intake

## 현재 이해한 요청
## 이미 확정된 내용
## 먼저 확인할 내용
## 아직 실행하지 않은 작업
```

## Next Skill Handoff

- Recommended Next Skill: `kc-lesson-turn` or `kc-lesson-resume`
- Why: turn known facts and remaining choices into a teacher decision card, or resume an explicitly named run
- Ready To Continue: yes | no
- Need Teacher Confirmation: yes
- Requires run_dir: yes only for resume
- Blocking Conditions: list unresolved context required for the next decision
- Suggested Prompt: answer the listed questions or provide an exact run path
