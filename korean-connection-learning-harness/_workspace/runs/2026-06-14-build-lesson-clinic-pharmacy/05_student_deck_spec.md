# Student Deck Spec

```yaml
student_deck_spec_id: "deckspec-clinic-pharmacy-001"
source_blueprint: "03_lesson_blueprint.md"
deck_mode: "student_deck"
slide_count_target: 14
slides:
  - slide_id: "s01"
    student_title: "Today's Mission"
    purpose: "set the learner action"
    content_blocks:
      - "Say one symptom."
      - "Ask again if needed."
      - "Check one next step."
    interaction: "reflect"
  - slide_id: "s02"
    student_title: "Week 5 Quick Check"
    purpose: "retrieve PT/gym safety language"
    content_blocks:
      - "Too fast: 천천히 해 주세요."
      - "Missed it: 다시 한 번 말해 주세요."
      - "Pain: 아파요."
    interaction: "recall"
  - slide_id: "s03"
    student_title: "Clinic / Pharmacy Map"
    purpose: "show the minimum chain"
    content_blocks:
      - "1. Symptom"
      - "2. Time"
      - "3. Repeat"
      - "4. Check"
    interaction: "choose"
  - slide_id: "s04"
    student_title: "Say One Symptom"
    purpose: "introduce new target"
    content_blocks:
      - "머리가 아파요."
      - "[body part] + 이/가 아파요"
    interaction: "repeat"
  - slide_id: "s05"
    student_title: "Swap the Body Part"
    purpose: "controlled substitution"
    content_blocks:
      - "머리 -> 머리가 아파요."
      - "목 -> 목이 아파요."
      - "배 -> 배가 아파요."
      - "허리 -> 허리가 아파요."
    interaction: "transform"
  - slide_id: "s06"
    student_title: "Add One Time Clue"
    purpose: "support chunk after symptom"
    content_blocks:
      - "어제부터요."
      - "오늘 아침부터요."
      - "머리가 아파요. 어제부터요."
    interaction: "say"
  - slide_id: "s07"
    student_title: "Keep It Short"
    purpose: "culture point as language choice"
    content_blocks:
      - "Key fact first."
      - "One symptom is enough to start."
      - "Extra details only when asked."
    interaction: "choose"
  - slide_id: "s08"
    student_title: "Ask Again"
    purpose: "retrieve Week 5 repair"
    content_blocks:
      - "아, 잠깐만요."
      - "다시 한 번 말해 주세요."
    interaction: "repeat"
  - slide_id: "s09"
    student_title: "Check the Next Step"
    purpose: "transfer `-아/어도 돼요?`"
    content_blocks:
      - "이거 먹어도 돼요?"
      - "커피 마셔도 돼요?"
      - "운동해도 돼요?"
    interaction: "transform"
  - slide_id: "s10"
    student_title: "Choose Your Line"
    purpose: "guided next-line choice"
    content_blocks:
      - "Staff speaks fast."
      - "Staff asks since when."
      - "You need to check medicine."
    interaction: "choose"
  - slide_id: "s11"
    student_title: "Pharmacy Role-Play"
    purpose: "independent symptom plus time production"
    content_blocks:
      - "Walk in."
      - "Say one symptom."
      - "Add one time clue."
    interaction: "roleplay"
  - slide_id: "s12"
    student_title: "Clinic Role-Play"
    purpose: "repair and check under light pressure"
    content_blocks:
      - "Staff gives an instruction."
      - "Ask again."
      - "Check one next step."
    interaction: "roleplay"
  - slide_id: "s13"
    student_title: "New Place, Same Skill"
    purpose: "transfer from PT/gym to clinic/pharmacy"
    content_blocks:
      - "PT/Gym: 잠깐 쉬어도 돼요?"
      - "Pharmacy: 이거 먹어도 돼요?"
      - "Same tool: -아/어도 돼요?"
    interaction: "transform"
  - slide_id: "s14"
    student_title: "Tiny Mission"
    purpose: "between-lesson private rehearsal and recall"
    content_blocks:
      - "Private rehearsal only."
      - "Say: 머리가 아파요. 어제부터요."
      - "Check: 이거 먹어도 돼요?"
    interaction: "prepare a mission"
design_notes:
  pacing:
    - "Start with Week 5 retrieval before introducing clinic/pharmacy."
    - "Keep the symptom pattern small and repeat it across slides 4-6."
    - "Move to no-model role-play by slide 11."
  visual_rhythm:
    - "Use a clear four-step map early."
    - "Keep Korean chunks large and isolated."
    - "Use separate color accents for symptom, time, repeat, and check."
  accessibility:
    - "Short lines per slide."
    - "High contrast text."
    - "Keyboard navigation and print support in HTML."
    - "No medical history or private learner detail visible."
non_student_notes:
  - "Do not turn the clinic/pharmacy situation into medical advice."
  - "Teacher-side source reasoning stays in markdown artifacts, not visible slide titles."
```

## Material Recommendation

Render as a single-file local HTML deck at `07_student_deck.html`, following the output shape of `_workspace/runs/2026-06-14-build-lesson-making-friends/07_student_deck.html`.
