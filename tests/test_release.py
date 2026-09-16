import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    def test_archives_include_runtime_and_exclude_private_development_records(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_release.py'),
                                     '--output', folder], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            products = json.loads(result.stdout)
            with zipfile.ZipFile(products['plugin']) as archive:
                self.assertIsNone(archive.testzip())
                for name in ['.codex-plugin/plugin.json', 'scripts/preferences.py',
                             'resources/preference.md', 'skills/click-to-answer/SKILL.md']:
                    self.assertEqual(archive.read(name), (ROOT / 'plugins/click-to-answer' / name).read_bytes())
            with zipfile.ZipFile(products['source']) as archive:
                self.assertIn('.agents/plugins/marketplace.json', archive.namelist())
                self.assertIn('README.md', archive.namelist())
                self.assertFalse(any(x.startswith(('docs/superpowers/', '.git/')) or
                                     x in ('docs/live-test.md', 'docs/verification.md') or
                                     '__pycache__' in x for x in archive.namelist()))
                fixture = Path(folder) / 'checkout'
                archive.extractall(fixture)
            private_dir = fixture / 'plugins/click-to-answer/.click-to-answer-backups'
            private_dir.mkdir()
            (private_dir / 'secret.bak').write_text('private instruction copy')
            (fixture / 'plugins/click-to-answer/AGENTS.md').write_text('private project rules')
            (fixture / 'plugins/click-to-answer/scripts/.env').write_text('private local config')
            rebuilt = subprocess.run([sys.executable, str(fixture / 'scripts/build_release.py'),
                                      '--output', str(Path(folder) / 'rebuilt')],
                                     capture_output=True, text=True)
            self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr)
            for product in json.loads(rebuilt.stdout).values():
                with zipfile.ZipFile(product) as archive:
                    self.assertFalse(any('.click-to-answer-backups' in name or
                                         name.endswith(('AGENTS.md', '.env')) for name in archive.namelist()))
