# Fixture: Privacy Failure

This fixture intentionally uses placeholder markers, not real private data.

```yaml
learner_alias: "privacy_case"
unsafe_text:
  - "[EXACT_AGE] learner with [PRIVATE_SOCIAL_ACCOUNT] and [FOLLOWER_COUNT] followers"
  - "lesson note includes a unique private biography"
expected_result: "privacy audit blocks and recommends generalization"
safe_generalization:
  - "creator-focused learner"
  - "public-facing communication goal"
```
