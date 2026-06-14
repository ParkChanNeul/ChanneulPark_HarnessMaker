# Korean Connection Learning Harness V2

This project is a Codex-native harness for Korean Connection learning operations.

It does not extend or copy the existing italki lesson builder. The existing italki repository is a read-only reference for prior domain knowledge, useful patterns, and known bias.

## Core Loop

```text
learner state analysis
-> long-term progression plan
-> lesson blueprint
-> repeated practice design
-> student deck and HTML material design
-> lesson result
-> weekly learning pack, homework, Quizlet, mission
-> mastery evidence review
-> next lesson input
```

## Learning Principle

```text
Situation-led
Culture-explained
Grammar-tracked
Practice-repeated
Mastery-verified
```

Culture is not a replacement for grammar. Culture explains why a form matters, where it is safe, and how it changes relationship distance. Grammar and expressions remain cumulative skills that need retrieval, production, transfer, and delayed review.

## Source Priority

1. Current user instructions
2. Approved documents in `domain/`
3. Approved documents in `contracts/`
4. Existing italki reference repository
5. Archive and historical examples

## Safety Boundaries

- Do not store real student-identifying information in tracked files.
- Do not use the existing italki repo as a production dependency.
- Do not copy archive lessons, student cases, or private context into active examples.
- Do not create a nested Git repository.
