---
name: kc-lesson-unknown
description: Use when a Korean Connection teacher says they do not know, asks the AI to recommend, or cannot choose lesson quantity, review, progression, or focus.
---

# KC Lesson Unknown

Turn uncertainty into an informed teacher choice rather than an automatic decision.

## Workflow

1. Name the open question.
2. Offer two or three bounded options.
3. Explain workload, benefit, and risk for each option.
4. Recommend a default using the known lesson context.
5. Ask the teacher to approve or change the recommendation.
6. Record an assumption only after explicit approval.

Do not auto-lock because the teacher said “알아서”, “모르겠어”, or “추천해줘”.

## Next Skill Handoff

- Recommended Next Skill: `kc-lesson-turn` or `kc-lesson-scope-lock`
- Why: return the approved assumption to the decision card or lock a complete scope
- Ready To Continue: yes | no
- Need Teacher Confirmation: yes
- Requires run_dir: no until lock creation is approved
- Blocking Conditions: unresolved option or unapproved assumption
- Suggested Prompt: approve one option, such as “10개로 잠가”
