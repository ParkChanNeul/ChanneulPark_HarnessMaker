#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from structured_artifacts import extract_structured_block
from validate_semantic_contracts import (
    reject_legacy_fields,
    validate_language_targets,
    validate_lesson_scope_lock,
    validate_post_lesson_teacher_card,
    validate_situation_scope,
)

ROOT = Path(__file__).resolve().parents[1]
MAP_ROOT = ROOT / "domain" / "02_language_map"
SITUATION_ROOT = ROOT / "domain" / "03_situations"
PROFILE_ROOT = ROOT / "domain" / "04_profiles"

LEVELS = {"A0", "A1", "A2", "B1", "B2", "C1", "C2", "special_content"}
CONFIDENCE = {"high", "medium", "low"}
LOADS = {"low", "medium", "high"}
STATUSES = {"active", "draft", "deprecated", "reserved"}
VOLATILE_VARIETIES = {"slang", "neologism"}
VOLATILE_REQUIRED = {
    "usage_status",
    "volatility",
    "last_reviewed_at",
    "age_group_affinity",
    "platform_affinity",
    "default_selection_allowed",
}
EXPECTED_REGISTRY_FILES = {
    "grammar_constructions.json",
    "particle_functions.json",
    "register_features.json",
    "discourse_patterns.json",
    "interactional_functions.json",
    "core_interaction_chunks.json",
    "phonology_features.json",
    "orthography_features.json",
}
EXPECTED_ACTIVE_PACKS = {
    "survival_basics",
    "self_introduction",
    "daily_routine",
    "shopping_checkout",
    "cafe_ordering",
    "restaurant_ordering",
    "transport_navigation",
    "directions_location",
    "housing_home",
    "clinic_pharmacy",
    "appointments_scheduling",
    "emergency_problem_reporting",
    "making_friends",
    "small_talk",
    "preferences_opinions",
    "invitations_plans",
    "family_relationships",
    "messaging_calls",
    "conflict_repair",
    "delivery_pickup",
    "banking_payment",
    "public_services",
    "mobile_internet",
    "neighborhood_life",
    "workplace_core",
    "office_work",
}
EXPECTED_RESERVED_PACKS = {
    "service_work",
    "food_service_work",
    "logistics_work",
    "medical_work",
    "education_work",
    "field_work",
}
EXPECTED_PROFILES = {
    "general_adult_conversation",
    "korea_resident_worker",
    "heritage_oral",
    "heritage_reconnection",
    "topik_exam",
}
EXPECTED_PROFILE_ROLES = {
    "general_adult_conversation": {
        "profile_type": "base",
        "status": "active",
        "runtime_selectable": True,
    },
    "korea_resident_worker": {
        "profile_type": "overlay",
        "status": "active",
        "runtime_selectable": True,
    },
    "heritage_oral": {
        "profile_type": "overlay",
        "status": "active",
        "runtime_selectable": True,
    },
    "heritage_reconnection": {
        "profile_type": "overlay",
        "status": "active",
        "runtime_selectable": True,
    },
    "topik_exam": {
        "profile_type": "overlay",
        "status": "reserved",
        "runtime_selectable": False,
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def index_unique(records: list[dict], id_field: str, label: str) -> dict[str, dict]:
    indexed: dict[str, dict] = {}
    for record in records:
        record_id = record.get(id_field)
        if record_id in indexed:
            raise ValueError(f"duplicate {label}: {record_id}")
        indexed[record_id] = record
    return indexed


def load_manifest_data() -> tuple[dict[str, dict], dict[str, dict], dict[str, dict]]:
    manifest = load_json(MAP_ROOT / "registry_manifest.json")
    targets: dict[str, dict] = {}
    for filename in manifest["registry_files"]:
        data = load_json(MAP_ROOT / filename)
        for target_id, record in index_unique(
            data.get("records", []),
            "target_id",
            "target_id",
        ).items():
            if target_id in targets:
                raise ValueError(f"duplicate target_id: {target_id}")
            targets[target_id] = record

    situation_manifest = load_json(SITUATION_ROOT / "situation_pack_manifest.json")
    packs: dict[str, dict] = {}
    for filename in situation_manifest["pack_files"]:
        data = load_json(SITUATION_ROOT / filename)
        for pack_id, pack in index_unique(
            data.get("packs", []),
            "pack_id",
            "pack_id",
        ).items():
            if pack_id in packs:
                raise ValueError(f"duplicate pack_id: {pack_id}")
            packs[pack_id] = pack

    profile_manifest = load_json(PROFILE_ROOT / "profile_manifest.json")
    profile_files = [PROFILE_ROOT / "general_adult_conversation.json"]
    profile_files.extend((PROFILE_ROOT / "overlays").glob("*.json") if (PROFILE_ROOT / "overlays").is_dir() else [])
    profiles: dict[str, dict] = {}
    for path in profile_files:
        profile = load_json(path)
        profile_id = profile.get("profile_id")
        if profile_id in profiles:
            raise ValueError(f"duplicate profile_id: {profile_id}")
        profiles[profile_id] = profile

    declared_profiles = {
        profile_manifest.get("base_profile_ref"),
        *profile_manifest.get("active_overlay_refs", []),
        *profile_manifest.get("reserved_overlay_refs", []),
    }
    if set(profiles) != declared_profiles:
        raise ValueError(
            "profile manifest mismatch: "
            f"declared={sorted(declared_profiles)} actual={sorted(profiles)}"
        )
    return targets, packs, profiles


def require_fields(data: dict, fields: list[str], context: str) -> list[str]:
    return [
        f"{context}: missing required field {field}"
        for field in fields
        if field not in data
    ]


def nested_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in nested_strings(child)]
    if isinstance(value, dict):
        return [
            item
            for key, child in value.items()
            for item in [*nested_strings(key), *nested_strings(child)]
        ]
    return []


def validate_target(
    record: dict,
    target_ids: set[str],
    pack_ids: set[str],
    source_ids: set[str],
    source_locators: dict[str, set[str]] | None = None,
    legacy_ids: set[str] | None = None,
) -> list[str]:
    target_id = record.get("target_id", "<missing>")
    context = f"target {target_id}"
    schema = load_json(MAP_ROOT / "language_target.schema.json")
    errors = require_fields(record, schema["required_fields"], context)
    if legacy_ids:
        used_legacy_ids = sorted(set(nested_strings(record)).intersection(legacy_ids))
        for legacy_id in used_legacy_ids:
            errors.append(f"{context}: new record uses legacy id {legacy_id!r}")
    if record.get("target_type") not in set(schema["target_types"]):
        errors.append(f"{context}: invalid target_type {record.get('target_type')!r}")

    level = record.get("level")
    if not isinstance(level, dict):
        errors.append(f"{context}: level must be an object")
    else:
        if level.get("primary_band") not in LEVELS:
            errors.append(f"{context}: invalid level {level.get('primary_band')!r}")
        if level.get("confidence") not in CONFIDENCE:
            errors.append(f"{context}: invalid confidence {level.get('confidence')!r}")
        for source_ref in level.get("source_refs", []):
            if source_ref not in source_ids:
                errors.append(f"{context}: missing level source_ref {source_ref!r}")

    prerequisites = record.get("prerequisites")
    if not isinstance(prerequisites, dict):
        errors.append(f"{context}: prerequisites must be an object")
    else:
        for relation in ("hard", "soft"):
            refs = prerequisites.get(relation)
            if not isinstance(refs, list):
                errors.append(f"{context}: prerequisites.{relation} must be an array")
                continue
            for ref in refs:
                if ref == target_id:
                    errors.append(f"{context}: self prerequisite is forbidden")
                elif ref not in target_ids:
                    errors.append(f"{context}: missing prerequisite {ref!r}")

    complexity = record.get("complexity")
    if not isinstance(complexity, dict):
        errors.append(f"{context}: complexity must be an object")
    else:
        if not isinstance(complexity.get("prerequisite_depth"), int):
            errors.append(f"{context}: prerequisite_depth must be an integer")
        for field in (
            "morphology_load",
            "semantic_load",
            "processing_load",
            "register_load",
            "discourse_load",
        ):
            if complexity.get(field) not in LOADS:
                errors.append(f"{context}: invalid {field}")

    explanations = record.get("explanations")
    if not isinstance(explanations, dict) or not all(
        isinstance(explanations.get(lang), str) and explanations[lang].strip()
        for lang in ("ko", "en")
    ):
        errors.append(f"{context}: Korean and English explanations are required")

    for source_ref in record.get("source_refs", []):
        if source_ref not in source_ids:
            errors.append(f"{context}: missing source_ref {source_ref!r}")
    evidence = record.get("source_evidence")
    if not isinstance(evidence, list):
        errors.append(f"{context}: source_evidence must be an array")
    else:
        for index, item in enumerate(evidence):
            evidence_context = f"{context}.source_evidence[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{evidence_context}: evidence must be an object")
                continue
            errors.extend(
                require_fields(
                    item,
                    ["source_ref", "locator_ref", "claim_scope"],
                    evidence_context,
                )
            )
            source_ref = item.get("source_ref")
            locator_ref = item.get("locator_ref")
            if source_ref not in source_ids:
                errors.append(
                    f"{evidence_context}: missing source_ref {source_ref!r}"
                )
            elif source_ref not in record.get("source_refs", []):
                errors.append(
                    f"{evidence_context}: source_ref must also appear in "
                    "the target source_refs"
                )
            elif (
                source_locators is not None
                and locator_ref not in source_locators.get(source_ref, set())
            ):
                errors.append(
                    f"{evidence_context}: unknown locator_ref {locator_ref!r}"
                )
            if not isinstance(item.get("claim_scope"), str) or not item.get(
                "claim_scope",
                "",
            ).strip():
                errors.append(f"{evidence_context}: claim_scope must be non-empty")
    for pack_ref in record.get("situation_refs", []):
        if pack_ref not in pack_ids:
            errors.append(f"{context}: missing situation_ref {pack_ref!r}")
    if record.get("status") not in STATUSES:
        errors.append(f"{context}: invalid status {record.get('status')!r}")
    if not record.get("source_refs") and (
        record.get("status") != "draft"
        or record.get("level", {}).get("confidence") != "low"
    ):
        errors.append(
            f"{context}: source-less target must be draft with low confidence"
        )
    varieties = set(record.get("language_varieties", []))
    if varieties.intersection(VOLATILE_VARIETIES):
        errors.extend(
            require_fields(record, sorted(VOLATILE_REQUIRED), context)
        )
        if record.get("default_selection_allowed") is not False:
            errors.append(
                f"{context}: slang/neologism cannot be selected by default"
            )
    examples_data = record.get("examples")
    if not isinstance(examples_data, dict):
        errors.append(f"{context}: examples must be an object")
    elif record.get("target_type") in {
        "grammar_construction",
        "particle_function",
        "register_feature",
    }:
        required_counts = {
            "basic": 4,
            "situation_variants": 3,
            "contrasts": 2,
            "error_examples": 2,
        }
        for field, minimum in required_counts.items():
            if not isinstance(examples_data.get(field), list) or len(
                examples_data[field]
            ) < minimum:
                errors.append(
                    f"{context}: examples.{field} requires at least {minimum}"
                )
    elif record.get("target_type") in {
        "discourse_pattern",
        "interactional_function",
        "core_interaction_chunk",
    }:
        for field, minimum in {
            "situation_examples": 3,
            "register_variants": 2,
        }.items():
            if not isinstance(examples_data.get(field), list) or len(
                examples_data[field]
            ) < minimum:
                errors.append(
                    f"{context}: examples.{field} requires at least {minimum}"
                )
    elif record.get("target_type") in {
        "phonology_feature",
        "orthography_feature",
    }:
        for field, minimum in {"representative": 4, "confusions": 2}.items():
            if not isinstance(examples_data.get(field), list) or len(
                examples_data[field]
            ) < minimum:
                errors.append(
                    f"{context}: examples.{field} requires at least {minimum}"
                )
    if (
        record.get("status") == "active"
        and record.get("target_type") in {"grammar_construction", "register_feature", "phonology_feature"}
        and (not record.get("source_refs") or not record.get("source_evidence"))
    ):
        errors.append(
            f"{context}: active core target requires official source evidence"
        )
    return errors


def validation_warnings(targets: dict[str, dict]) -> list[str]:
    warnings: list[str] = []
    band_order = {
        "A0": 0,
        "A1": 1,
        "A2": 2,
        "B1": 3,
        "B2": 4,
        "C1": 5,
        "C2": 6,
        "special_content": 7,
    }
    for target_id, record in targets.items():
        target_band = record.get("level", {}).get("primary_band")
        for relation in ("hard", "soft"):
            for ref in record.get("prerequisites", {}).get(relation, []):
                ref_band = targets.get(ref, {}).get("level", {}).get("primary_band")
                if (
                    target_band in band_order
                    and ref_band in band_order
                    and band_order[ref_band] > band_order[target_band]
                ):
                    warnings.append(
                        f"level inversion: {target_id} ({target_band}) "
                        f"depends on {ref} ({ref_band})"
                    )
    soft_graph = {
        target_id: record.get("prerequisites", {}).get("soft", [])
        for target_id, record in targets.items()
    }
    for left, refs in soft_graph.items():
        for right in refs:
            if left in soft_graph.get(right, []):
                message = f"soft prerequisite cycle: {left} <-> {right}"
                if message not in warnings and (
                    f"soft prerequisite cycle: {right} <-> {left}" not in warnings
                ):
                    warnings.append(message)
    return warnings


def hard_cycle_errors(targets: dict[str, dict]) -> list[str]:
    graph = {
        target_id: record.get("prerequisites", {}).get("hard", [])
        for target_id, record in targets.items()
    }
    visiting: set[str] = set()
    visited: set[str] = set()
    errors: list[str] = []

    def visit(node: str, path: list[str]) -> None:
        if node in visiting:
            start = path.index(node)
            errors.append("hard prerequisite cycle: " + " -> ".join(path[start:] + [node]))
            return
        if node in visited:
            return
        visiting.add(node)
        for child in graph.get(node, []):
            visit(child, path + [child])
        visiting.remove(node)
        visited.add(node)

    for target_id in graph:
        visit(target_id, [target_id])
    return errors


def validate_pack(pack: dict, target_ids: set[str], pack_ids: set[str], profile_ids: set[str]) -> list[str]:
    context = f"pack {pack.get('pack_id', '<missing>')}"
    schema = load_json(SITUATION_ROOT / "situation_pack.schema.json")
    errors = require_fields(pack, schema["required_fields"], context)
    if pack.get("status") == "reserved" and pack.get("runtime_selectable") is not False:
        errors.append(f"{context}: reserved pack must not be runtime selectable")
    if pack.get("status") == "active" and pack.get("runtime_selectable") is not True:
        errors.append(f"{context}: active pack must be runtime selectable")
    for field in ("recommended_language_target_refs", "optional_language_target_refs", "interactional_function_refs", "phonology_focus_refs", "orthography_focus_refs"):
        for ref in pack.get(field, []):
            if ref not in target_ids:
                errors.append(f"{context}: missing target ref {ref!r}")
    for ref in pack.get("transfer_pack_refs", []):
        if ref not in pack_ids:
            errors.append(f"{context}: missing transfer_pack_ref {ref!r}")
    for ref in pack.get("profile_affinities", []):
        if ref not in profile_ids:
            errors.append(f"{context}: missing profile affinity {ref!r}")
    return errors


def validate_profile(profile: dict, pack_ids: set[str]) -> list[str]:
    context = f"profile {profile.get('profile_id', '<missing>')}"
    schema = load_json(PROFILE_ROOT / "profile.schema.json")
    errors = require_fields(profile, schema["required_fields"], context)
    if profile.get("status") == "reserved" and profile.get("runtime_selectable") is not False:
        errors.append(f"{context}: reserved profile must not be runtime selectable")
    for ref in profile.get("priority_situation_refs", []):
        if ref not in pack_ids:
            errors.append(f"{context}: missing priority situation {ref!r}")
    return errors


def validate_profile_role(profile: dict) -> list[str]:
    profile_id = profile.get("profile_id")
    expected = EXPECTED_PROFILE_ROLES.get(profile_id)
    if expected is None:
        return [f"profile {profile_id!r}: unapproved profile"]
    errors: list[str] = []
    for field, expected_value in expected.items():
        if profile.get(field) != expected_value:
            errors.append(
                f"profile {profile_id}: {field} must be {expected_value!r}"
            )
    return errors


def resolve_legacy(legacy_id: str, context: str | None) -> tuple[int, str]:
    aliases = load_json(MAP_ROOT / "legacy_aliases.json")["aliases"]
    if legacy_id in aliases:
        return 0, aliases[legacy_id]
    migrations = load_json(MAP_ROOT / "legacy_migrations.json")["migrations"]
    migration = next(
        (item for item in migrations if item.get("legacy_id") == legacy_id),
        None,
    )
    if migration is None:
        return 1, f"unknown legacy id: {legacy_id}"
    if context and context in migration.get("context_rules", {}):
        return 0, ",".join(migration["context_rules"][context])
    return 1, f"manual review required for {legacy_id}"


def schema_migration_gate_errors() -> list[str]:
    errors: list[str] = []
    manifest = load_json(MAP_ROOT / "registry_manifest.json")
    if set(manifest.get("registry_files", [])) != EXPECTED_REGISTRY_FILES:
        errors.append("schema gate requires exactly the eight canonical registries")

    aliases = load_json(MAP_ROOT / "legacy_aliases.json").get("aliases", {})
    migrations = load_json(MAP_ROOT / "legacy_migrations.json").get(
        "migrations",
        [],
    )
    if "request_juseyo" in aliases:
        errors.append("schema gate forbids request_juseyo as a one-to-one alias")
    request_migration = next(
        (
            item
            for item in migrations
            if item.get("legacy_id") == "request_juseyo"
        ),
        None,
    )
    expected_contexts = {
        "noun_item_request": ["chunk_request_noun_juseyo"],
        "verb_action_request": ["grammar_request_verb_eo_juseyo"],
    }
    if request_migration is None:
        errors.append("schema gate requires contextual request_juseyo migration")
    else:
        for context, expected in expected_contexts.items():
            if request_migration.get("context_rules", {}).get(context) != expected:
                errors.append(
                    f"schema gate request_juseyo context {context!r} is invalid"
                )

    golden = ROOT / "tests" / "fixtures" / "golden" / "conversational_cafe"
    lock = extract_structured_block(
        golden / "00_conversation" / "lesson_scope_lock.md"
    )
    errors.extend(validate_lesson_scope_lock(lock))
    errors.extend(reject_legacy_fields(lock, "golden.lesson_scope_lock"))
    errors.extend(
        validate_language_targets(
            lock.get("language_targets"),
            "golden.lesson_scope_lock.language_targets",
        )
    )
    errors.extend(
        validate_situation_scope(
            lock.get("lesson", {}).get("situation_scope"),
            "golden.lesson_scope_lock.lesson.situation_scope",
        )
    )
    if lock.get("lock_status") != "locked" or lock.get("approved_by_teacher") is not True:
        errors.append("schema gate requires the existing Teacher-in-the-Loop lock")

    post_card = extract_structured_block(
        golden / "00_conversation" / "post_lesson_teacher_card.md"
    )
    errors.extend(validate_post_lesson_teacher_card(post_card))
    errors.extend(reject_legacy_fields(post_card, "golden.post_lesson_teacher_card"))
    return errors


def validate_all() -> list[str]:
    errors: list[str] = []
    try:
        targets, packs, profiles = load_manifest_data()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        return [str(error)]
    manifest = load_json(MAP_ROOT / "registry_manifest.json")
    if set(manifest.get("registry_files", [])) != EXPECTED_REGISTRY_FILES:
        errors.append("registry manifest must contain exactly eight canonical registries")
    active_packs = {
        pack_id
        for pack_id, pack in packs.items()
        if pack.get("status") == "active"
    }
    reserved_packs = {
        pack_id
        for pack_id, pack in packs.items()
        if pack.get("status") == "reserved"
    }
    if active_packs != EXPECTED_ACTIVE_PACKS:
        errors.append("active situation packs must match the approved set of 26")
    if reserved_packs != EXPECTED_RESERVED_PACKS:
        errors.append("reserved situation packs must match the approved set of 6")
    if set(profiles) != EXPECTED_PROFILES:
        errors.append("profiles must match the approved base, overlays, and TOPIK reserve")
    for profile in profiles.values():
        errors.extend(validate_profile_role(profile))

    source_catalog = load_json(MAP_ROOT / "source_catalog.json")
    source_ids = [source.get("source_id") for source in source_catalog.get("sources", [])]
    source_locators: dict[str, set[str]] = {}
    if len(source_ids) != len(set(source_ids)):
        errors.append("source catalog contains duplicate source_id")
    for source in source_catalog.get("sources", []):
        errors.extend(
            require_fields(
                source,
                [
                    "source_id",
                    "publisher",
                    "title",
                    "source_type",
                    "url",
                    "retrieved_at",
                    "scope_notes",
                ],
                f"source {source.get('source_id', '<missing>')}",
            )
        )
        locators = source.get("evidence_locators")
        if not isinstance(locators, dict) or not locators:
            errors.append(
                f"source {source.get('source_id', '<missing>')}: "
                "evidence_locators must be a non-empty object"
            )
        else:
            for locator_ref, locator in locators.items():
                if not isinstance(locator, str) or not locator.strip():
                    errors.append(
                        f"source {source.get('source_id', '<missing>')}: "
                        f"locator {locator_ref!r} must be non-empty"
                    )
            source_locators[source.get("source_id")] = set(locators)

    aliases = load_json(MAP_ROOT / "legacy_aliases.json")["aliases"]
    migrations = load_json(MAP_ROOT / "legacy_migrations.json")["migrations"]
    migration_ids = {item.get("legacy_id") for item in migrations}
    legacy_ids = set(aliases).union(migration_ids)
    if set(aliases).intersection(migration_ids):
        errors.append("legacy id cannot exist in both aliases and migrations")
    if "request_juseyo" in aliases:
        errors.append("request_juseyo must not be a one-to-one alias")
    for canonical in aliases.values():
        if canonical not in targets:
            errors.append(f"legacy alias points to missing target {canonical!r}")
    for migration in migrations:
        for refs in migration.get("context_rules", {}).values():
            for ref in refs:
                if ref not in targets:
                    errors.append(f"legacy migration points to missing target {ref!r}")

    target_ids = set(targets)
    pack_ids = set(packs)
    profile_ids = set(profiles)
    source_id_set = set(source_ids)
    for record in targets.values():
        errors.extend(
            validate_target(
                record,
                target_ids,
                pack_ids,
                source_id_set,
                source_locators,
                legacy_ids,
            )
        )
    errors.extend(hard_cycle_errors(targets))
    for profile in profiles.values():
        errors.extend(validate_profile(profile, pack_ids))
    for pack in packs.values():
        errors.extend(validate_pack(pack, target_ids, pack_ids, profile_ids))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resolve")
    parser.add_argument("--context")
    parser.add_argument("--schema-migration-gate", action="store_true")
    args = parser.parse_args()
    if args.resolve:
        code, message = resolve_legacy(args.resolve, args.context)
        print(message)
        raise SystemExit(code)
    if args.schema_migration_gate:
        errors = schema_migration_gate_errors()
        if errors:
            print("FAIL: schema and migration gate failed")
            for error in errors:
                print(f"- {error}")
            raise SystemExit(1)
        print("PASS: schema, migration, Golden Cafe, and teacher gate are valid")
        return

    errors = validate_all()
    if errors:
        print("FAIL: language map validation failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    targets, _packs, _profiles = load_manifest_data()
    for warning in validation_warnings(targets):
        print(f"WARNING: {warning}")
    print("PASS: language map schema, registries, migrations, profiles, and packs are valid")


if __name__ == "__main__":
    main()
