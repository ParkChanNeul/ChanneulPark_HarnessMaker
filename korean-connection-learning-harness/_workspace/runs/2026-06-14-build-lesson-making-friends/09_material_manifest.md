# Material Manifest

```yaml
material_manifest_id: "materials-friends-001"
run_id: "2026-06-14-build-lesson-making-friends"
materials:
  - path: "07_student_deck.html"
    type: "html"
    source_contract: "05_student_deck_spec.md"
    intended_user: "student"
  - path: "08_design_manifest.md"
    type: "other"
    source_contract: "contracts/design_manifest.md"
    intended_user: "reviewer"
status: "reviewed"
known_gaps:
  - "No PDF export was generated."
  - "No deterministic renderer script exists yet; this sample was rendered by the parent agent from the deck spec."
```

## Review Note

This material bundle is suitable as a render_materials smoke test for the V2 harness.
