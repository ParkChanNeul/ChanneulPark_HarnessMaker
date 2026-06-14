# Grammar Progression

Grammar progression is a mastery map, not a list of interesting grammar tools.

## Required Grammar Item Fields

```yaml
grammar_id:
form:
level:
prerequisites: []
social_functions: []
first_exposure_situations: []
review_situations: []
retrieval_situations: []
transfer_situations: []
common_errors: []
mastery_requirements:
  recognition:
  guided_production:
  independent_production:
  transfer:
review_schedule:
  - next_lesson
  - after_2_lessons
  - after_4_lessons
```

## Mastery States

```text
introduced -> recognized -> guided -> independent -> transferred -> retained
```

## Initial V2 Grammar Seeds

```yaml
- grammar_id: request_juseyo
  form: "-주세요"
  level: A1
  prerequisites: []
  social_functions: [request, help, safety, service_flow]
  first_exposure_situations: [taxi, cafe]
  review_situations: [shopping, pt_gym, clinic_pharmacy]
  retrieval_situations: [restaurant, directions]
  transfer_situations: [appointment, creator_comment_cta]
  common_errors:
    - using noun_plus_juseyo_only
    - missing verb transformation
    - overusing where softer refusal is needed
  mastery_requirements:
    recognition: identify the request function in staff or teacher prompts
    guided_production: produce with a prompt in three situations
    independent_production: produce without model in two role plays
    transfer: use in one new situation after the first exposure lesson
  review_schedule: [next_lesson, after_2_lessons, after_4_lessons]

- grammar_id: polite_yo
  form: "-요"
  level: A1
  prerequisites: []
  social_functions: [safe_politeness, stranger_distance, soft_answer]
  first_exposure_situations: [survival_korean, daily_life]
  review_situations: [making_friends, shopping, appointment]
  retrieval_situations: [short_answer, soft_refusal]
  transfer_situations: [reaction_before_answer, ask_back]
  common_errors:
    - dropping politeness under pressure
    - using overly formal endings in casual service flow
  mastery_requirements:
    recognition: distinguish polite from casual examples
    guided_production: answer guided questions with polite endings
    independent_production: answer and ask back once without a model
    transfer: carry the ending into a new short conversation
  review_schedule: [next_lesson, after_2_lessons, after_4_lessons]

- grammar_id: iyo_order
  form: "-(이)요"
  level: A1
  prerequisites: [polite_yo]
  social_functions: [short_order, identify_item, low_burden_answer]
  first_exposure_situations: [cafe]
  review_situations: [restaurant, shopping]
  retrieval_situations: [checkout, pickup]
  transfer_situations: [ticket_counter, appointment_name_check]
  common_errors:
    - making a long full sentence in fast service flow
    - omitting quantity or packaging cue
  mastery_requirements:
    recognition: understand why a short noun phrase is natural
    guided_production: build three item plus quantity answers
    independent_production: order one item in role play
    transfer: use the short presentation pattern outside cafe ordering
  review_schedule: [next_lesson, after_2_lessons, after_4_lessons]
```
