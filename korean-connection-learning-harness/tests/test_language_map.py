from __future__ import annotations

import subprocess
import sys
import unittest
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_language_map import (  # noqa: E402
    hard_cycle_errors,
    index_unique,
    validate_pack,
    validate_profile,
    validate_profile_role,
    validate_target,
)


class LanguageMapCommandTests(unittest.TestCase):
    fixture_root = ROOT / "tests" / "fixtures" / "language_map"

    def load_fixture(self, relative_path: str) -> dict:
        return json.loads(
            (self.fixture_root / relative_path).read_text(encoding="utf-8")
        )

    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_language_map.py"),
                *args,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def test_current_language_map_passes_validator(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_one_to_one_legacy_alias_resolves(self) -> None:
        result = self.run_validator("--resolve", "polite_yo")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("register_haeyo_polite", result.stdout)

    def test_contextual_legacy_migration_requires_context(self) -> None:
        result = self.run_validator("--resolve", "request_juseyo")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("manual review", result.stdout.lower())

    def test_contextual_legacy_migration_resolves_noun_request(self) -> None:
        result = self.run_validator(
            "--resolve",
            "request_juseyo",
            "--context",
            "noun_item_request",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("chunk_request_noun_juseyo", result.stdout)

    def test_contextual_legacy_migration_resolves_verb_request(self) -> None:
        result = self.run_validator(
            "--resolve",
            "request_juseyo",
            "--context",
            "verb_action_request",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("grammar_request_verb_eo_juseyo", result.stdout)

    def sample_target(self) -> dict:
        return self.load_fixture("valid/target.json")

    def test_invalid_level_is_rejected(self) -> None:
        record = self.load_fixture("invalid/invalid_level.json")
        errors = validate_target(record, {"sample"}, {"pack"}, {"source"})
        self.assertTrue(any("invalid level" in error for error in errors))

    def test_valid_target_fixture_passes(self) -> None:
        errors = validate_target(
            self.sample_target(),
            {"sample"},
            {"pack"},
            {"source"},
            {"source": {"locator"}},
        )
        self.assertEqual(errors, [])

    def test_duplicate_target_id_is_rejected(self) -> None:
        records = self.load_fixture("invalid/duplicate_ids.json")["records"]
        with self.assertRaisesRegex(ValueError, "duplicate target_id"):
            index_unique(records, "target_id", "target_id")

    def test_missing_prerequisite_is_rejected(self) -> None:
        record = self.load_fixture("invalid/missing_prerequisite.json")
        errors = validate_target(record, {"sample"}, {"pack"}, {"source"})
        self.assertTrue(any("missing prerequisite" in error for error in errors))

    def test_legacy_id_in_new_record_is_rejected(self) -> None:
        record = self.load_fixture("invalid/legacy_id.json")
        errors = validate_target(
            record,
            {"sample"},
            {"pack"},
            {"source"},
            legacy_ids={"request_juseyo"},
        )
        self.assertTrue(any("uses legacy id" in error for error in errors))

    def test_hard_cycle_is_rejected(self) -> None:
        records = {
            "a": {"prerequisites": {"hard": ["b"]}},
            "b": {"prerequisites": {"hard": ["a"]}},
        }
        self.assertTrue(hard_cycle_errors(records))

    def test_slang_requires_review_metadata(self) -> None:
        record = self.load_fixture("invalid/slang_missing_review.json")
        errors = validate_target(record, {"sample"}, {"pack"}, {"source"})
        self.assertTrue(any("last_reviewed_at" in error for error in errors))

    def test_reserved_profile_cannot_be_selectable(self) -> None:
        profile = {
            "profile_id": "reserved",
            "profile_type": "overlay",
            "status": "reserved",
            "runtime_selectable": True,
            "priority_situation_refs": [],
            "skill_imbalance_hints": [],
            "explanation_preferences": [],
            "pronunciation_reading_support": [],
            "goal_adjustments": [],
            "default_exclusions": [],
        }
        errors = validate_profile(profile, set())
        self.assertTrue(any("reserved profile" in error for error in errors))

    def test_topik_profile_cannot_become_active(self) -> None:
        profile = {
            "profile_id": "topik_exam",
            "profile_type": "overlay",
            "status": "active",
            "runtime_selectable": True,
        }
        errors = validate_profile_role(profile)
        self.assertTrue(any("status must be 'reserved'" in error for error in errors))
        self.assertTrue(
            any("runtime_selectable must be False" in error for error in errors)
        )

    def test_base_profile_cannot_become_overlay(self) -> None:
        profile = {
            "profile_id": "general_adult_conversation",
            "profile_type": "overlay",
            "status": "active",
            "runtime_selectable": True,
        }
        errors = validate_profile_role(profile)
        self.assertTrue(any("profile_type must be 'base'" in error for error in errors))

    def test_reserved_pack_cannot_be_selectable(self) -> None:
        pack = {
            "pack_id": "reserved",
            "status": "reserved",
            "runtime_selectable": True,
            "title_ko": "",
            "title_en": "",
            "level_range": {"min": "A0", "max": "A2"},
            "profile_affinities": [],
            "sub_situations": [],
            "interactional_function_refs": [],
            "recommended_language_target_refs": [],
            "optional_language_target_refs": [],
            "phonology_focus_refs": [],
            "orthography_focus_refs": [],
            "vocabulary_retrieval": {},
            "transfer_pack_refs": [],
            "source_refs": [],
        }
        errors = validate_pack(pack, set(), {"reserved"}, set())
        self.assertTrue(any("reserved pack" in error for error in errors))

    def test_missing_situation_target_is_rejected(self) -> None:
        pack = {
            "pack_id": "pack",
            "status": "active",
            "runtime_selectable": True,
            "title_ko": "",
            "title_en": "",
            "level_range": {"min": "A0", "max": "A2"},
            "profile_affinities": [],
            "sub_situations": [],
            "interactional_function_refs": [],
            "recommended_language_target_refs": ["missing"],
            "optional_language_target_refs": [],
            "phonology_focus_refs": [],
            "orthography_focus_refs": [],
            "vocabulary_retrieval": {},
            "transfer_pack_refs": [],
            "source_refs": [],
        }
        errors = validate_pack(pack, set(), {"pack"}, set())
        self.assertTrue(any("missing target ref" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
