# Lesson Contract

## Default A1-B1 Contract

```yaml
new_targets:
  default_max: 1
review_targets:
  default_min: 2
  default_max: 4
retrieval_targets:
  required: true
transfer:
  required: true
major_culture_points:
  default_max: 1
independent_production:
  required: true
next_lesson_check:
  required: true
```

## Required Distinctions

Every lesson blueprint must distinguish:

- new grammar or expression targets
- review targets
- retrieval targets
- transfer targets
- conversation skill targets
- culture explanation point
- evidence to collect

## Override Rule

Any exception to the default target count requires `override_reason`.
