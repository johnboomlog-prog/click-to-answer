#!/usr/bin/env python3
"""Build source/plugin ZIPs from explicit public paths, not the working directory."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/click-to-answer'
PLUGIN_FILES = ['.codex-plugin/plugin.json', 'README.md', 'SUBMISSION.md', 'LICENSE',
                'assets/logo.svg', 'scripts/preferences.py', 'resources/preference.md',
                'skills/click-to-answer/SKILL.md',
                'skills/click-to-answer/agents/openai.yaml',
                'skills/click-to-answer/references/setup.md']
PUBLIC = ['README.md', 'README.zh-CN.md', 'LICENSE', 'CONTRIBUTING.md', 'PRIVACY.md', 'TERMS.md', '.gitignore',
          '.agents/plugins/marketplace.json', '.github/workflows/ci.yml',
          'scripts/build_release.py', 'tests/test_preferences.py', 'tests/test_release.py',
          'docs/compatibility.md', 'docs/publishing.md',
          'docs/choice-ui-test-2026-09-16.md']


def files(paths):
    for path in paths:
        if not path.is_file():
            raise ValueError(f'Missing release input: {path}')
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != ROOT.parent):
            raise ValueError(f'Release input traverses a symlink: {path}')
        yield path


def archive(destination, paths, base):
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as output:
        for path in files(paths):
            info = zipfile.ZipInfo(path.relative_to(base).as_posix(), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, path.read_bytes())
    with zipfile.ZipFile(destination) as check:
        if check.testzip() is not None:
            raise ValueError(f'Archive integrity check failed: {destination}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    version = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))['version']
    if not version or any(c not in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-+' for c in version):
        raise ValueError('Unsafe release version')
    folder = args.output.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    plugin = folder / f'click-to-answer-{version}.zip'
    source = folder / f'click-to-answer-source-{version}.zip'
    plugin_paths = [PLUGIN / path for path in PLUGIN_FILES]
    archive(plugin, plugin_paths, PLUGIN)
    archive(source, [ROOT / path for path in PUBLIC] + plugin_paths, ROOT)
    sums = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in [plugin, source])
    (folder / 'SHA256SUMS.txt').write_text(sums, encoding='utf-8')
    print(json.dumps({'plugin': str(plugin), 'source': str(source)}, ensure_ascii=True))


if __name__ == '__main__':
    main()
