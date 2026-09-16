#!/usr/bin/env python3
"""Manage opt-in Codex choice preferences. Python 3.11+, standard library only."""
import argparse
import codecs
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile

BEGIN = '<!-- click-to-answer:begin -->'
END = '<!-- click-to-answer:end -->'
POLICY = Path(__file__).resolve().parents[1] / 'resources' / 'preference.md'


def read(path):
    if path.is_symlink():
        raise ValueError(f'Refusing symlink instruction file: {path}')
    data = path.read_bytes() if path.exists() else b''
    data.decode('utf-8-sig')  # Refuse unknown encodings rather than corrupt user rules.
    return data


def locate(text):
    if BEGIN not in text and END not in text:
        return None
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError('Duplicate or incomplete Click to Answer markers; repair manually.')
    match = re.search(r'(?m)^' + re.escape(BEGIN) + r'\r?\n.*?^' +
                      re.escape(END) + r'\r?\n\r?\n', text, re.DOTALL)
    if not match:
        raise ValueError('Malformed Click to Answer block; refusing to change the file.')
    return match


def instruction_files(root):
    paths = [root / 'AGENTS.override.md', root / 'AGENTS.md']
    data = {p: read(p) for p in paths}
    # Validate both before any writes, even if one file is currently shadowed.
    for raw in data.values():
        locate(raw.decode('utf-8-sig'))
    active = paths[0] if data[paths[0]].decode('utf-8-sig').strip() else paths[1]
    return active, data


def transform(raw, enabled):
    text = raw.decode('utf-8-sig')
    found = locate(text)
    newline = '\r\n' if '\r\n' in text else '\n'
    block = (BEGIN + '\n' + POLICY.read_text(encoding='utf-8').strip() +
             '\n' + END + '\n\n').replace('\n', newline) if enabled else ''
    if found:
        text = text[:found.start()] + block + text[found.end():]
    elif enabled:
        text = block + text
    bom = codecs.BOM_UTF8 if raw.startswith(codecs.BOM_UTF8) else b''
    return bom + text.encode('utf-8')


def replace(path, old, new):
    if old == new:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if read(path) != old:
        raise ValueError(f'File changed during update; retry after reviewing: {path}')
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
    if path.exists():
        backup_dir = path.parent / '.click-to-answer-backups'
        if backup_dir.is_symlink():
            raise ValueError(f'Refusing symlink backup directory: {backup_dir}')
        backup_dir.mkdir(exist_ok=True)
        backup = backup_dir / f'{path.name}.{hashlib.sha256(old).hexdigest()}.bak'
        if backup.is_symlink():
            raise ValueError(f'Refusing symlink backup: {backup}')
        if backup.exists():
            if backup.read_bytes() != old:
                raise ValueError(f'Existing backup does not match: {backup}')
        else:
            # mkstemp creates a private 0600 file on POSIX. Publish only after flush.
            backup_fd, backup_temp = tempfile.mkstemp(prefix='.pending-', dir=backup_dir)
            try:
                with os.fdopen(backup_fd, 'wb') as stream:
                    stream.write(old)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(backup_temp, backup)
            finally:
                if os.path.exists(backup_temp):
                    os.unlink(backup_temp)
    fd, temp_name = tempfile.mkstemp(prefix='.click-to-answer-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(new)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temp_name, mode)
        if read(path) != old:
            raise ValueError(f'Concurrent modification detected: {path}')
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def report(root, home, scope):
    active, data = instruction_files(root)
    installed = [str(p) for p, raw in data.items() if locate(raw.decode('utf-8-sig'))]
    configured = str(active) in installed
    warnings = []
    if any(p != str(active) for p in installed):
        warnings.append('A managed block is shadowed by AGENTS.override.md; re-enable to migrate or disable to clean both files.')
    global_active, global_data = instruction_files(home)
    global_configured = bool(locate(global_data[global_active].decode('utf-8-sig')))
    if scope == 'project' and global_configured:
        warnings.append('Global preference remains active; removing this project block does not disable the global preference.')
    warnings.append('Configuration is not proof of loading: project/nested instructions, custom profiles and instruction size limits may affect behavior. Start a new task to verify.')
    return {'scope': scope, 'target': str(active), 'configured': configured,
            'global_configured': global_configured, 'managed_files': installed,
            'native_choices': 'unknown_until_session_test', 'warnings': warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['enable', 'disable', 'status', 'doctor'])
    parser.add_argument('--scope', required=True, choices=['global', 'project'])
    parser.add_argument('--project', type=Path, help='Exact existing project directory; required for project scope.')
    parser.add_argument('--codex-home', type=Path, help='Overrides CODEX_HOME (default: ~/.codex).')
    parser.add_argument('--dry-run', action='store_true', help='Preview enable/disable without writing.')
    args = parser.parse_args()
    try:
        if args.project is not None:
            args.project = args.project.expanduser().resolve()
        if args.scope == 'project' and (args.project is None or not args.project.is_dir()):
            raise ValueError('Project scope requires --project pointing to an existing directory.')
        if args.scope == 'global' and args.project is not None:
            raise ValueError('--project cannot be used with global scope.')
        home = (args.codex_home or Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')).expanduser().resolve()
        root = args.project.expanduser().resolve() if args.scope == 'project' else home
        if args.scope == 'project' and root == home:
            raise ValueError('Project directory is CODEX_HOME; use global scope explicitly.')
        # Diagnose global files before mutating project files.
        result = report(root, home, args.scope)
        active, data = instruction_files(root)
        updates = {}
        if args.command in ('enable', 'disable'):
            for path, raw in data.items():
                updates[path] = transform(raw, args.command == 'enable' and path == active)
            changed = [str(p) for p in data if updates[p] != data[p]]
            if not args.dry_run:
                # Enable active file first so an interrupted migration remains enabled.
                order = [active] + [p for p in data if p != active]
                for path in order:
                    replace(path, data[path], updates[path])
                result = report(root, home, args.scope)
            result.update(would_change=bool(changed), changed_files=[] if args.dry_run else changed,
                          planned_files=changed, dry_run=args.dry_run)
        if args.command == 'doctor':
            result['checks'] = {
                'instruction_files': 'readable UTF-8; managed markers valid',
                'scope_selection': 'AGENTS.override.md takes precedence when nonempty',
                'session_test': 'In a new Codex task, ask for a harmless YES/NO and a four-option preference. Verify a real response; accepted alone is insufficient.',
                'uninstall': 'Run disable for every enabled scope BEFORE removing the plugin. Backups are retained for manual recovery.'}
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (OSError, ValueError, UnicodeError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=True))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
