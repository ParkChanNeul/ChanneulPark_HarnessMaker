# Contract: Design Manifest

## Purpose

Describes rendered materials and the design decisions behind them.

## Producer

`kc_student_experience_designer` or parent renderer.

## Consumers

`kc_assessment_reviewer`, parent agent.

## Required Fields

```yaml
design_manifest_id: "unique id"
material_refs:
  - "path"
source_specs:
  - "student deck spec, practice plan, or blueprint ref"
layout_principles:
  - "specific design decision"
interaction_support:
  - "navigation, print, mobile, or classroom use"
accessibility_checks:
  - "contrast, reading load, touch target, etc."
known_limitations: []
```

## Validation

The manifest must state which source spec each rendered material implements.
