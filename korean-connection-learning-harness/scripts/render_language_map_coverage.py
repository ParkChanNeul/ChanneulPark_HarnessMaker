#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from validate_language_map import (
    EXPECTED_ACTIVE_PACKS,
    EXPECTED_PROFILES,
    EXPECTED_REGISTRY_FILES,
    EXPECTED_RESERVED_PACKS,
    MAP_ROOT,
    load_json,
    load_manifest_data,
    validate_profile_role,
    validation_warnings,
)


REPORT = MAP_ROOT / "coverage_summary.json"
CORE_TYPES = {
    "grammar_construction",
    "register_feature",
    "phonology_feature",
}


def build_coverage() -> dict:
    targets, packs, profiles = load_manifest_data()
    by_band = Counter(
        record.get("level", {}).get("primary_band") for record in targets.values()
    )
    by_registry = Counter(record.get("target_type") for record in targets.values())
    source_less = sorted(
        target_id
        for target_id, record in targets.items()
        if not record.get("source_refs")
    )
    draft_or_low = sorted(
        target_id
        for target_id, record in targets.items()
        if record.get("status") == "draft"
        or record.get("level", {}).get("confidence") == "low"
    )
    active_core_without_source = sorted(
        target_id
        for target_id, record in targets.items()
        if record.get("target_type") in CORE_TYPES
        and record.get("status") == "active"
        and (
            not record.get("source_refs")
            or not record.get("source_evidence")
        )
    )
    pack_connections = {
        pack_id: len(
            set(pack.get("recommended_language_target_refs", []))
            | set(pack.get("optional_language_target_refs", []))
            | set(pack.get("interactional_function_refs", []))
            | set(pack.get("phonology_focus_refs", []))
            | set(pack.get("orthography_focus_refs", []))
        )
        for pack_id, pack in sorted(packs.items())
    }
    empty_packs = sorted(
        pack_id for pack_id, count in pack_connections.items() if count == 0
    )
    active_packs = sorted(
        pack_id
        for pack_id, pack in packs.items()
        if pack.get("status") == "active"
    )
    reserved_packs = sorted(
        pack_id
        for pack_id, pack in packs.items()
        if pack.get("status") == "reserved"
    )
    active_overlays = sorted(
        profile_id
        for profile_id, profile in profiles.items()
        if profile.get("profile_type") == "overlay"
        and profile.get("status") == "active"
    )
    reserved_profiles = sorted(
        profile_id
        for profile_id, profile in profiles.items()
        if profile.get("status") == "reserved"
    )

    blockers: list[str] = []
    manifest = load_json(MAP_ROOT / "registry_manifest.json")
    if set(manifest.get("registry_files", [])) != EXPECTED_REGISTRY_FILES:
        blockers.append("registry manifest does not contain exactly eight registries")
    for band in ("A0", "A1", "A2"):
        if by_band[band] == 0:
            blockers.append(f"no targets populated for {band}")
    for target_type in (
        "grammar_construction",
        "particle_function",
        "register_feature",
        "discourse_pattern",
        "interactional_function",
        "core_interaction_chunk",
        "phonology_feature",
        "orthography_feature",
    ):
        if by_registry[target_type] == 0:
            blockers.append(f"empty registry: {target_type}")
    if set(active_packs) != EXPECTED_ACTIVE_PACKS:
        blockers.append("active situation pack set does not match the approved 26")
    if set(reserved_packs) != EXPECTED_RESERVED_PACKS:
        blockers.append("reserved situation pack set does not match the approved 6")
    if empty_packs:
        blockers.append("empty situation packs exist")
    if active_core_without_source:
        blockers.append("active core targets without official source evidence exist")
    if set(profiles) != EXPECTED_PROFILES:
        blockers.append("profile set does not match the approved five profiles")
    if any(validate_profile_role(profile) for profile in profiles.values()):
        blockers.append("profile roles, status, or runtime selection do not match")

    return {
        "schema_version": 1,
        "generated_from": "registry_manifest.json",
        "populate_scope": ["A0", "A1", "A2"],
        "target_counts_by_level": {
            band: by_band[band] for band in ("A0", "A1", "A2")
        },
        "target_counts_by_registry": dict(sorted(by_registry.items())),
        "situation_pack_connections": pack_connections,
        "active_pack_count": len(active_packs),
        "active_pack_refs": active_packs,
        "reserved_pack_count": len(reserved_packs),
        "reserved_pack_refs": reserved_packs,
        "empty_pack_refs": empty_packs,
        "profile_count": len(profiles),
        "active_overlay_refs": active_overlays,
        "reserved_profile_refs": reserved_profiles,
        "phonology_count": by_registry["phonology_feature"],
        "orthography_count": by_registry["orthography_feature"],
        "source_less_target_refs": source_less,
        "draft_or_low_confidence_target_refs": draft_or_low,
        "active_core_without_source_evidence": active_core_without_source,
        "warnings": validation_warnings(targets),
        "blockers": blockers,
        "coverage_status": "pass" if not blockers else "blocked",
    }


def render(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = build_coverage()
    if args.write:
        REPORT.write_text(render(expected), encoding="utf-8")
        print(f"WROTE: {REPORT.relative_to(MAP_ROOT.parents[1])}")
        return

    if not REPORT.is_file():
        print("FAIL: coverage summary is missing")
        raise SystemExit(1)
    actual = json.loads(REPORT.read_text(encoding="utf-8"))
    if actual != expected:
        print(
            "FAIL: coverage summary is stale; "
            "run render_language_map_coverage.py --write"
        )
        raise SystemExit(1)
    if expected["blockers"]:
        print("FAIL: language map coverage has blockers")
        for blocker in expected["blockers"]:
            print(f"- {blocker}")
        raise SystemExit(1)
    print("PASS: language map coverage summary matches current registries")


if __name__ == "__main__":
    main()
