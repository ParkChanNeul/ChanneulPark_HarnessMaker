#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]

EXECUTION_MODES = [
    'build_lesson', 'render_materials', 'post_lesson_followup', 'review_outputs',
    'research_to_domain', 'audit_domain', 'partial_rerun',
]

CORE_TERMS = [
    'Situation-led', 'Culture-explained', 'Grammar-and-vocabulary tracked',
    'Practice-repeated', 'Mastery-verified', 'Teacher-approved progression',
]

LEGACY_PRIVATE_PATTERNS = [
    r'\bBritish\b', r'\bBlack\b', r'\bTikTok\b', r'\b20\s?yo\b',
    r'\b20-year\b', r'\b1M\+?\b', r'\b\d+\s*(?:M|million)\+?\s+followers\b',
]


def fail(message: str) -> None:
    print(f'FAIL: {message}')
    sys.exit(1)


def run_command(args: list[str], label: str) -> None:
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        fail(f'{label} failed:\n{result.stdout}')
    print(result.stdout.strip())


def scan_text_files() -> list[Path]:
    return [
        path for path in ROOT.rglob('*')
        if path.is_file() and '.git' not in path.parts and path.suffix in {'.json', '.md', '.toml', '.py', '.txt'}
    ]


def main() -> None:
    for script in [
        'validate_structure.py',
        'validate_language_map.py',
        'validate_contracts.py',
        'validate_agent_boundaries.py',
        'validate_semantic_contracts.py',
        'validate_golden_run.py',
        'validate_conversational_runtime.py',
    ]:
        run_command(
            [sys.executable, str(ROOT / 'scripts' / script)],
            script,
        )
    run_command(
        [
            sys.executable,
            str(ROOT / 'scripts' / 'render_language_map_coverage.py'),
            '--check',
        ],
        'render_language_map_coverage.py --check',
    )
    run_command(
        [
            sys.executable,
            str(ROOT / 'scripts' / 'render_golden_assessment.py'),
            '--check',
        ],
        'render_golden_assessment.py --check',
    )
    run_command(
        [
            sys.executable,
            '-m',
            'unittest',
            'discover',
            '-s',
            'tests',
            '-p',
            'test_*.py',
        ],
        'unittest discover',
    )

    orchestrator = ROOT / '.agents' / 'skills' / 'korean-connection-orchestrator' / 'SKILL.md'
    orchestrator_text = orchestrator.read_text(encoding='utf-8')
    failures: list[str] = []

    for mode in EXECUTION_MODES:
        if f'### `{mode}`' not in orchestrator_text:
            failures.append(f'orchestrator missing execution mode {mode}')

    combined = '\n'.join([
        (ROOT / 'README.md').read_text(encoding='utf-8'),
        orchestrator_text,
        (ROOT / 'domain' / '02_learning_model' / 'pedagogy_principles.md').read_text(encoding='utf-8'),
    ])
    for term in CORE_TERMS:
        if term not in combined:
            failures.append(f'missing core term {term}')

    registry_data = tomllib.loads((ROOT / 'references' / 'agent_registry.toml').read_text(encoding='utf-8'))
    matrix = (ROOT / 'references' / 'agent_responsibility_matrix.md').read_text(encoding='utf-8')
    for entry in registry_data.get('agents', []):
        if entry.get('required') is True and entry.get('status') == 'approved' and entry.get('name') not in matrix:
            failures.append(f"responsibility matrix missing {entry.get('name')}")

    for path in scan_text_files():
        content = path.read_text(encoding='utf-8', errors='ignore')
        for pattern in LEGACY_PRIVATE_PATTERNS:
            if re.search(pattern, content, flags=re.IGNORECASE):
                failures.append(f'legacy private pattern {pattern!r} found in {path.relative_to(ROOT)}')

    if failures:
        fail('\n'.join(f'- {failure}' for failure in failures))
    print('PASS: harness validates end to end')


if __name__ == '__main__':
    main()
