# A0–A2 Language Map Audit

## Baseline

- Root commit: `d863847369a1aaa33675741e76aef3d58a4ccd84`
- Branch: `main`
- Initial worktree: clean
- Existing validators and 21 unit tests passed before the migration.

## Legacy Seed Findings

- `polite_yo` is stored as grammar although its primary teaching role is register selection.
- `iyo_order` is stored as grammar although its primary role is a short noun-answer discourse pattern.
- `request_juseyo` combines `N 주세요` item requests and `V-아/어 주세요` action requests. The old seed calls noun use an error while the Golden Cafe correctly teaches item requests.
- Existing situation fields mix modules, situations, sub-situations, and conversation functions.
- Existing learner state has no reusable profile/overlay model.

## Migration Decisions

- `polite_yo` → `register_haeyo_polite` through a 1:1 alias.
- `iyo_order` → `discourse_short_noun_iyo` through a 1:1 alias.
- `request_juseyo` has no alias. Context determines:
  - noun/item request → `chunk_request_noun_juseyo`
  - verb/action request → `grammar_request_verb_eo_juseyo`
  - missing or mixed context → manual review
- Active artifacts use only:

```yaml
language_targets:
  - target_ref: "canonical target id"
    treatment: "new | review | retrieval | transfer | practice | carrier | defer"

situation_scope:
  pack_ref: "canonical situation pack id"
  sub_situation_ids: []
```

- Historical `_workspace/runs/` artifacts remain unchanged and are interpreted only at ingestion.

## Contract and Validator Impact

- Teacher Decision Card uses `candidate_language_targets`.
- Approved locks and every downstream lesson artifact use `language_targets`.
- Situation truth is stored only in `situation_scope`; legacy situation labels may be rendered as derived display text.
- Golden validation must check canonical registry membership, exact cross-artifact propagation, and concrete surface evidence for transfer tasks.
- Teacher-in-the-Loop approval fields and lock semantics remain unchanged.

## Preserved Principles

- Situation-led planning does not imply a fixed curriculum sequence.
- Level is recommendation metadata, not a hard learner gate.
- Stable mastery still requires independent production and later retrieval or transfer.
- New domain defaults require explicit approval.
- No real learner-identifying data is introduced.
