# Student Deck Spec

```yaml
student_deck_spec_id: "deckspec-friends-001"
source_blueprint: "03_lesson_blueprint.md"
deck_mode: "student_deck"
slide_count_target: 10
slides:
  - slide_id: "s01"
    student_title: "Today's Mission"
    purpose: "set the learner action"
    content_blocks:
      - "Answer. React. Ask back."
      - "Goal: keep a short peer conversation alive."
    interaction: "reflect"
  - slide_id: "s02"
    student_title: "Start Without Notes"
    purpose: "delayed greeting retrieval"
    content_blocks:
      - "Say hello and introduce yourself."
      - "No script for the first try."
    interaction: "say"
  - slide_id: "s03"
    student_title: "The Ask-Back Move"
    purpose: "introduce the new target"
    content_blocks:
      - "저는 음악 좋아해요."
      - "음악은요?"
      - "Use 은/는요? to send the question back."
    interaction: "repeat"
  - slide_id: "s04"
    student_title: "Choose the Best Reply"
    purpose: "controlled form and meaning check"
    content_blocks:
      - "A asks: 취미가 뭐예요?"
      - "Choose the reply that keeps talking."
    interaction: "choose"
  - slide_id: "s05"
    student_title: "Add a Reaction"
    purpose: "combine reaction timing with ask-back"
    content_blocks:
      - "좋아요."
      - "진짜요?"
      - "저도요."
    interaction: "choose"
  - slide_id: "s06"
    student_title: "Build Your Answer"
    purpose: "guided production"
    content_blocks:
      - "Answer one question."
      - "Add one reaction."
      - "Ask it back."
    interaction: "transform"
  - slide_id: "s07"
    student_title: "Meet a New Classmate"
    purpose: "independent role-play"
    content_blocks:
      - "Two questions."
      - "Two answers."
      - "Two ask-backs."
    interaction: "roleplay"
  - slide_id: "s08"
    student_title: "New Place, Same Skill"
    purpose: "transfer"
    content_blocks:
      - "You meet someone after class."
      - "Use the same move with weekend plans."
    interaction: "roleplay"
  - slide_id: "s09"
    student_title: "Tiny Mission"
    purpose: "between-lesson practice"
    content_blocks:
      - "Write three answer + ask-back pairs."
      - "Try one aloud without looking."
    interaction: "prepare a mission"
  - slide_id: "s10"
    student_title: "Quick Recall"
    purpose: "end-of-lesson retrieval"
    content_blocks:
      - "What do you say after your answer?"
      - "Say it from memory."
    interaction: "recall"
design_notes:
  pacing:
    - "Keep modeling short and spend most time on ask-back production."
    - "Move from visible model to no-model role-play by slide 7."
  visual_rhythm:
    - "Use one sentence pair per slide when possible."
    - "Keep reaction choices visually separate from ask-back pattern."
  accessibility:
    - "Avoid dense grammar explanation text."
    - "Keep Korean and English support visually distinct."
non_student_notes:
  - "Do not show teacher-side reasoning labels as visible slide titles."
  - "Teacher can explain that asking back shows interest, but visible slides should stay action-first."
```
