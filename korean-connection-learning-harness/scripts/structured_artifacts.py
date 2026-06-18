#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


FENCE_PATTERN = re.compile(
    r"^```(?P<label>yaml|json)\s*\n(?P<body>.*?)^```\s*$",
    re.MULTILINE | re.DOTALL,
)
MISSING = object()


class StructuredArtifactError(ValueError):
    pass


def extract_structured_block(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FENCE_PATTERN.search(text)
    if not match:
        raise StructuredArtifactError(
            f"{path}: no yaml or json fenced structured block found"
        )

    body = match.group("body")
    first_body_line = text[: match.start("body")].count("\n") + 1
    try:
        data = json.loads(body)
    except json.JSONDecodeError as error:
        source_line = first_body_line + error.lineno - 1
        raise StructuredArtifactError(
            f"{path}:{source_line}:{error.colno}: {error.msg}"
        ) from error

    if not isinstance(data, dict):
        raise StructuredArtifactError(
            f"{path}:{first_body_line}: structured block must contain an object"
        )
    return data


def is_artifact_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    value = value.strip()
    return (
        value.endswith(".md")
        or "/" in value
        or value.startswith("./")
        or value.startswith("../")
    )


def resolve_artifact_ref(source_path: Path, ref: str) -> Path | None:
    if not is_artifact_ref(ref):
        return None
    candidate = Path(ref)
    if not candidate.is_absolute():
        candidate = source_path.parent / candidate
    return candidate.resolve()


def require_fields(data: dict, fields: list[str], context: str) -> list[str]:
    return [
        f"{context}: missing required field {field}"
        for field in fields
        if field not in data
    ]


def get_nested(data: dict, field_path: str, default: Any = MISSING) -> Any:
    current: Any = data
    for part in field_path.split("."):
        if not isinstance(current, dict) or part not in current:
            if default is MISSING:
                raise KeyError(field_path)
            return default
        current = current[part]
    return current
