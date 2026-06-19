# Language Target Progression

Grammar progression is part of the canonical language map rather than a
standalone seed list.

## Canonical Source

- Registry manifest: `domain/02_language_map/registry_manifest.json`
- Grammar constructions: `domain/02_language_map/grammar_constructions.json`
- Other target types: particle, register, discourse, interaction, chunk,
  phonology, and orthography registries beside the grammar registry.

## Artifact Interface

```yaml
language_targets:
  - target_ref: "canonical target id"
    treatment: "new | review | retrieval | transfer | practice | carrier | defer"
```

The registry determines `target_type`. Artifacts do not duplicate it.

## Progression Rule

Level is recommendation metadata, not a hard gate. Select a target from:

```text
situation need
+ learner evidence
+ hard and soft prerequisites
+ processing load
+ teacher decision
```

Stable mastery still requires independent production plus later retrieval or
transfer evidence.

## Legacy Boundary

Historical IDs are interpreted only through:

- `domain/02_language_map/legacy_aliases.json`
- `domain/02_language_map/legacy_migrations.json`

New artifacts may not use legacy IDs or split target arrays.
