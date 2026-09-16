"""CLI integration tests: each test operates on real temporary instruction files."""
import json
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

CLI = Path(__file__).resolve().parents[1] / 'plugins/click-to-answer/scripts/preferences.py'


class PreferencesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / 'codex'
        self.project = self.root / 'project'
        self.project.mkdir()

    def run_cli(self, command, scope='project', ok=True, extra=()):
        args = [sys.executable, '-X', 'utf8', str(CLI), command,
                '--scope', scope, '--codex-home', str(self.home)]
        if scope == 'project':
            args += ['--project', str(self.project)]
        result = subprocess.run(args + list(extra), capture_output=True, text=True,
                                encoding='utf-8')
        self.assertEqual(result.returncode, 0 if ok else 2, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        if not ok:
            self.assertIn('error', payload)
        return payload

    def test_enable_is_idempotent_and_disable_restores_original_bytes(self):
        path = self.project / 'AGENTS.md'
        original = b'\xef\xbb\xbf# Existing\r\nKeep this.\r\n'
        path.write_bytes(original)
        self.run_cli('enable')
        enabled = path.read_bytes()
        self.assertIn(original[3:], enabled)
        self.assertTrue(enabled.startswith(b'\xef\xbb\xbf'))
        self.assertTrue(self.run_cli('status')['configured'])
        self.run_cli('enable')
        self.assertEqual(path.read_bytes(), enabled)
        backups = list((self.project / '.click-to-answer-backups').glob('*.bak'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
        self.run_cli('disable')
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse(self.run_cli('status')['configured'])

    def test_nonempty_override_wins_and_empty_override_does_not(self):
        base = self.project / 'AGENTS.md'
        override = self.project / 'AGENTS.override.md'
        base.write_text('base', encoding='utf-8')
        override.write_text('override', encoding='utf-8')
        result = self.run_cli('enable')
        self.assertEqual(Path(result['target']), override)
        self.assertEqual(base.read_text(), 'base')
        self.run_cli('disable')
        self.assertEqual(override.read_text(), 'override')
        override.write_text('  \n', encoding='utf-8')
        self.assertEqual(Path(self.run_cli('enable')['target']), base)

    def test_later_override_is_reported_and_disable_cleans_inactive_block(self):
        self.run_cli('enable')
        override = self.project / 'AGENTS.override.md'
        override.write_text('new override', encoding='utf-8')
        status = self.run_cli('status')
        self.assertFalse(status['configured'])
        self.assertTrue(status['warnings'])
        self.run_cli('disable')
        self.assertEqual((self.project / 'AGENTS.md').read_bytes(), b'')
        self.assertEqual(override.read_text(), 'new override')

    def test_disable_preserves_unrelated_edits_made_after_enable(self):
        path = self.project / 'AGENTS.md'
        path.write_bytes(b'Existing without final newline')
        self.run_cli('enable')
        with path.open('ab') as f:
            f.write(b'\nNew user rule\n')
        self.run_cli('disable')
        self.assertEqual(path.read_bytes(), b'Existing without final newline\nNew user rule\n')

    def test_malformed_marker_refuses_write(self):
        path = self.project / 'AGENTS.md'
        original = b'Important\n<!-- click-to-answer:begin -->\nunfinished'
        path.write_bytes(original)
        self.run_cli('enable', ok=False)
        self.run_cli('disable', ok=False)
        self.assertEqual(path.read_bytes(), original)

    def test_status_and_doctor_do_not_create_files_or_claim_ui_support(self):
        result = self.run_cli('doctor', scope='global')
        self.assertFalse(self.home.exists())
        self.assertFalse(result['configured'])
        self.assertEqual(result['native_choices'], 'unknown_until_session_test')

    def test_project_disable_reports_remaining_global_configuration(self):
        self.run_cli('enable', scope='global')
        self.run_cli('enable')
        result = self.run_cli('disable')
        self.assertFalse(result['configured'])
        self.assertTrue(result['global_configured'])
        self.assertTrue(result['warnings'])

    def test_preview_does_not_write(self):
        result = self.run_cli('enable', extra=['--dry-run'])
        self.assertTrue(result['would_change'])
        self.assertFalse((self.project / 'AGENTS.md').exists())

    def test_non_utf8_is_not_overwritten(self):
        path = self.project / 'AGENTS.md'
        path.write_bytes(b'\xff\xfe\x00broken')
        self.run_cli('enable', ok=False)
        self.assertEqual(path.read_bytes(), b'\xff\xfe\x00broken')

    def test_existing_missing_project_is_not_silently_created(self):
        self.project = self.root / 'typo'
        self.run_cli('enable', ok=False)
        self.assertFalse(self.project.exists())

    def test_codex_home_environment_is_respected(self):
        env = dict(os.environ, CODEX_HOME=str(self.home))
        result = subprocess.run([sys.executable, str(CLI), 'enable', '--scope', 'global'],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / 'AGENTS.md').exists())

    def test_tilde_project_path_is_expanded_before_validation(self):
        env = dict(os.environ, HOME=str(self.root), USERPROFILE=str(self.root))
        result = subprocess.run([sys.executable, str(CLI), 'status', '--scope', 'project',
                                 '--project', '~/project', '--codex-home', str(self.home)],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reenable_migrates_shadowed_block_and_preserves_both_files(self):
        base = self.project / 'AGENTS.md'
        override = self.project / 'AGENTS.override.md'
        base.write_bytes(b'base original\r\n')
        self.run_cli('enable')
        override.write_bytes(b'override original\n')
        self.run_cli('enable')
        self.assertEqual(base.read_bytes(), b'base original\r\n')
        once = override.read_bytes()
        self.assertTrue(self.run_cli('status')['configured'])
        self.run_cli('enable')
        self.assertEqual(override.read_bytes(), once)
        self.run_cli('disable')
        self.assertEqual(override.read_bytes(), b'override original\n')

    def test_disable_removes_blocks_from_both_candidate_files(self):
        self.run_cli('enable')
        base = self.project / 'AGENTS.md'
        override = self.project / 'AGENTS.override.md'
        override.write_bytes(base.read_bytes() + b'override suffix')
        self.run_cli('disable')
        self.assertEqual(base.read_bytes(), b'')
        self.assertEqual(override.read_bytes(), b'override suffix')

    @unittest.skipIf(os.name == 'nt', 'POSIX permission bits are not Windows ACLs')
    def test_backup_does_not_expose_private_instruction_permissions(self):
        path = self.project / 'AGENTS.md'
        path.write_bytes(b'private rules')
        path.chmod(0o600)
        self.run_cli('enable')
        backup = next((self.project / '.click-to-answer-backups').glob('*.bak'))
        self.assertEqual(backup.stat().st_mode & 0o077, 0)

    def test_interrupted_backup_publish_leaves_original_and_allows_retry(self):
        spec = importlib.util.spec_from_file_location('preferences_under_test', CLI)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        path = self.project / 'AGENTS.md'
        path.write_bytes(b'original')
        with mock.patch.object(module.os, 'replace', side_effect=OSError('simulated interruption')):
            with self.assertRaises(OSError):
                module.replace(path, b'original', b'updated')
        self.assertEqual(path.read_bytes(), b'original')
        self.assertEqual(list((self.project / '.click-to-answer-backups').glob('*.bak')), [])
        module.replace(path, b'original', b'updated')
        self.assertEqual(path.read_bytes(), b'updated')


if __name__ == '__main__':
    unittest.main()
