#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from structured_artifacts import StructuredArtifactError, extract_structured_block
from validate_golden_run import GOLDEN, build_assessment_data


REPORT = GOLDEN / "11_assessment_report.md"


def render_report(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return (
        "# Assessment Report\n\n"
        "This report is generated from the Golden semantic and cross-artifact "
        "validators. Do not edit the pass status manually.\n\n"
        f"```yaml\n{payload}\n```\n"
    )


def check_report() -> list[str]:
    expected = build_assessment_data(GOLDEN)
    try:
        actual = extract_structured_block(REPORT)
    except (OSError, StructuredArtifactError) as error:
        return [str(error)]
    if actual != expected:
        return [
            "Golden assessment report does not match computed validation results; "
            "run render_golden_assessment.py --write"
        ]
    return []


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.write:
        REPORT.write_text(
            render_report(build_assessment_data(GOLDEN)),
            encoding="utf-8",
        )
        print(f"WROTE: {REPORT.relative_to(GOLDEN.parents[3])}")
        return

    errors = check_report()
    if errors:
        print("FAIL: Golden assessment check failed")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("PASS: Golden assessment matches computed validation results")


if __name__ == "__main__":
    main()
