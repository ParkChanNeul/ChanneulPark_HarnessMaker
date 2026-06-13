#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit('Python 3.11+ is required. Use python3.11 if python3 is older.')

PACKAGE = 'ChanneulPark HarnessMaker'
VERSION = '0.1.0'
REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = '.agents/skills/harness/.harnessmaker-install.json'

@dataclass
class InstallResult:
    ok: bool
    messages: list[str] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return 'sha256:' + h.hexdigest()


def safe_join(root: Path, rel: str | Path) -> Path:
    rel_path = Path(rel)
    if rel_path.is_absolute():
        raise ValueError(f'absolute path is not allowed: {rel}')
    if '..' in rel_path.parts:
        raise ValueError(f'path traversal is not allowed: {rel}')
    root_resolved = root.resolve()
    candidate = root_resolved / rel_path
    parent_resolved = candidate.parent.resolve(strict=False)
    if os.path.commonpath([str(root_resolved), str(parent_resolved)]) != str(root_resolved):
        raise ValueError(f'destination escapes target root: {rel}')
    return candidate


def ensure_no_symlink_parent(root: Path, dest: Path) -> None:
    root_resolved = root.resolve()
    current = root_resolved
    rel_parts = dest.relative_to(root_resolved).parts[:-1]
    for part in rel_parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise ValueError(f'symlink parent is not allowed: {current}')


def iter_files(base: Path):
    for path in sorted(base.rglob('*')):
        if path.is_file():
            if path.name == '.harnessmaker-install.json':
                continue
            if '__pycache__' in path.parts:
                continue
            yield path


def build_plan(repo_root: Path, scope: str, with_agent_templates: bool) -> list[tuple[str, Path]]:
    plan: list[tuple[str, Path]] = []
    skill_root = repo_root / '.agents' / 'skills' / 'harness'
    for src in iter_files(skill_root):
        rel = src.relative_to(repo_root).as_posix()
        plan.append((rel, src))
    if with_agent_templates:
        for src in sorted((repo_root / '.codex' / 'agents').glob('*.toml')):
            plan.append((src.relative_to(repo_root).as_posix(), src))
        config_src = repo_root / '.codex' / 'config.toml.example'
        if scope == 'user':
            plan.append(('.codex/harnessmaker.config.toml.example', config_src))
        else:
            plan.append(('.codex/config.toml.example', config_src))
    for rel, _ in plan:
        safe_join(Path('/tmp'), rel)
    return plan


def load_manifest(root: Path) -> dict | None:
    path = safe_join(root, MANIFEST_REL)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def verify_existing_manifest(root: Path, manifest: dict | None) -> tuple[bool, list[str]]:
    if manifest is None:
        return True, []
    messages = []
    for rel, meta in manifest.get('installed_files', {}).items():
        dest = safe_join(root, rel)
        if not dest.exists():
            messages.append(f'partial install: managed file missing: {rel}')
            continue
        if dest.is_symlink():
            messages.append(f'symlink managed file is not allowed: {rel}')
            continue
        actual = sha256_file(dest)
        if actual != meta.get('sha256'):
            messages.append(f'managed file modified: {rel}')
    return not messages, messages


def component_list(with_agent_templates: bool) -> list[str]:
    comps = ['skill']
    if with_agent_templates:
        comps.extend(['agent-templates', 'config-example'])
    return comps


def install(*, scope: str, target: Path | None = None, repo_root: Path = REPO_ROOT, with_agent_templates: bool = False, force: bool = False, dry_run: bool = False, home_dir: Path | None = None) -> InstallResult:
    messages: list[str] = []
    repo_root = repo_root.resolve()
    if scope not in {'project', 'user'}:
        return InstallResult(False, [f'invalid scope: {scope}'])
    if scope == 'project':
        if target is None:
            return InstallResult(False, ['--target is required for project scope'])
        install_root = target.resolve()
        if install_root == repo_root:
            return InstallResult(False, ['source and target repository are the same; refusing to install into source tree'])
    else:
        install_root = (home_dir or Path.home()).resolve()

    if with_agent_templates:
        codex_path = install_root / '.codex'
        if codex_path.exists() and codex_path.is_file():
            return InstallResult(False, [f'.codex is a file; cannot install agent templates under {codex_path}'])

    try:
        plan = build_plan(repo_root, scope, with_agent_templates)
    except Exception as exc:
        return InstallResult(False, [str(exc)])

    manifest = load_manifest(install_root)
    ok, manifest_errors = verify_existing_manifest(install_root, manifest)
    if not ok:
        if not force:
            return InstallResult(False, manifest_errors + ['rerun with --force only for managed modified files; incomplete installs require manual cleanup'])
        if any(msg.startswith('partial install') for msg in manifest_errors):
            return InstallResult(False, manifest_errors + ['partial install cannot be force-overwritten automatically'])
        messages.extend(manifest_errors)

    existing_managed = set((manifest or {}).get('installed_files', {}).keys())
    planned_hashes = {rel: sha256_file(src) for rel, src in plan}
    to_copy: list[tuple[str, Path]] = []

    for rel, src in plan:
        try:
            dest = safe_join(install_root, rel)
            ensure_no_symlink_parent(install_root, dest)
        except Exception as exc:
            return InstallResult(False, [str(exc)])
        if dest.is_symlink():
            return InstallResult(False, [f'symlink destination is not allowed: {rel}'])
        if dest.exists():
            if rel not in existing_managed:
                return InstallResult(False, [f'unmanaged existing file blocks install: {rel}'])
            current_hash = sha256_file(dest)
            recorded_hash = manifest['installed_files'][rel]['sha256']
            if current_hash != recorded_hash and not force:
                return InstallResult(False, [f'managed file modified: {rel}; use --force to replace managed files'])
            if current_hash == planned_hashes[rel]:
                continue
        to_copy.append((rel, src))

    next_components = sorted(set((manifest or {}).get('components', [])) | set(component_list(with_agent_templates)))
    next_installed = dict((manifest or {}).get('installed_files', {}))
    for rel, _ in plan:
        next_installed[rel] = {'sha256': planned_hashes[rel]}
    next_manifest = {
        'schema_version': 1,
        'package': PACKAGE,
        'package_version': VERSION,
        'scope': scope,
        'components': next_components,
        'installed_files': dict(sorted(next_installed.items())),
    }

    if dry_run:
        messages.append('DRY RUN: no files changed')
        messages.extend([f'would install {rel}' for rel, _ in to_copy])
        messages.append(f'would write manifest: {MANIFEST_REL}')
        return InstallResult(True, messages)

    backups: list[tuple[Path, Path]] = []
    created: list[Path] = []
    changed: list[str] = []
    manifest_path = safe_join(install_root, MANIFEST_REL)
    rollback_root = Path(tempfile.mkdtemp(prefix='harnessmaker-rollback-'))
    try:
        try:
            with tempfile.TemporaryDirectory(prefix='harnessmaker-stage-') as tmp:
                staging = Path(tmp) / 'staging'
                for rel, src in plan:
                    staged = safe_join(staging, rel)
                    staged.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, staged)
                    if sha256_file(staged) != planned_hashes[rel]:
                        raise RuntimeError(f'staging hash mismatch: {rel}')
                backup_root = rollback_root / 'backups'
                for rel, _ in to_copy:
                    dest = safe_join(install_root, rel)
                    if dest.exists():
                        backup = safe_join(backup_root, rel)
                        backup.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(dest, backup)
                        backups.append((dest, backup))
                    else:
                        created.append(dest)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(safe_join(staging, rel), dest)
                    changed.append(rel)
                if manifest_path.exists():
                    backup = backup_root / 'manifest.json'
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(manifest_path, backup)
                    backups.append((manifest_path, backup))
                else:
                    created.append(manifest_path)
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                temp_manifest = manifest_path.with_suffix('.json.tmp')
                created.append(temp_manifest)
                temp_manifest.write_text(json.dumps(next_manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                os.replace(temp_manifest, manifest_path)
                changed.append(MANIFEST_REL)
        except Exception as exc:
            rollback_errors = []
            for dest, backup in reversed(backups):
                try:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup, dest)
                except Exception as rollback_exc:
                    rollback_errors.append(f'failed to restore {dest}: {rollback_exc}')
            for path in reversed(created):
                try:
                    if path.exists() or path.is_symlink():
                        path.unlink()
                except Exception as rollback_exc:
                    rollback_errors.append(f'failed to remove {path}: {rollback_exc}')
            return InstallResult(False, [f'install failed and rollback attempted: {exc}', *rollback_errors])
    finally:
        shutil.rmtree(rollback_root, ignore_errors=True)

    if not to_copy:
        messages.append('installation is already up to date')
    else:
        messages.extend([f'installed {rel}' for rel in changed])
    return InstallResult(True, messages, changed)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Install ChanneulPark HarnessMaker skill and optional Codex agent templates.')
    parser.add_argument('--scope', choices=['project', 'user'], required=True)
    parser.add_argument('--target', type=Path)
    parser.add_argument('--with-agent-templates', action='store_true')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    result = install(scope=args.scope, target=args.target, with_agent_templates=args.with_agent_templates, force=args.force, dry_run=args.dry_run)
    stream = sys.stdout if result.ok else sys.stderr
    for message in result.messages:
        print(message, file=stream)
    return 0 if result.ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
