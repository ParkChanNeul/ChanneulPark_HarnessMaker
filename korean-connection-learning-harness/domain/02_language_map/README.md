# Korean Connection Language Map

This directory stores the canonical A0–A2 teaching map. It is not a lexeme,
sense, collocation, or lesson-vocabulary database.

All registry records implement the common target interface documented in
`language_target.schema.json`. Levels are recommendation metadata. Runtime
selection must also consider situation need, learner state, prerequisites,
processing load, and teacher approval.

`legacy_aliases.json` contains only exact 1:1 mappings.
`legacy_migrations.json` contains contextual, split, and manual-review rules.
Historical artifacts may be interpreted through these files; new artifacts
must use canonical IDs and the single `language_targets` structure.
