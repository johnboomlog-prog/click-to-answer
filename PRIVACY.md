# Privacy and data handling

Effective date: 2026-09-16. Applies to the Click to Answer code distributed in this repository.

Click to Answer has no hosted service, analytics, telemetry, account system or credential collection. Its bundled Python script makes no network requests and does not send instruction files or answers to the project maintainer.

The script reads `AGENTS.md` and `AGENTS.override.md` in the selected project or Codex profile to locate its preference block. Project diagnostics also read the global instruction candidates to report whether a global preference remains enabled. Enable and disable update instruction files in the requested scope. Changed existing files are backed up locally in `.click-to-answer-backups/` next to those files.

Backups can contain private instructions. They remain after disable or uninstall and are under your control; review and remove them locally when no longer needed. Do not attach backups or unredacted instruction files to public issues.

Codex and its native input tools process conversation messages and selected answers under the host provider's policies. GitHub processes downloads, accounts and issue submissions under GitHub's policies. This project does not replace either provider's policies.

For questions, use this repository's Issues page without posting secrets or personal data. Information you voluntarily post in public issues is visible to others.
