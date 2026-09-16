# Public listing draft / 上架草稿

Name: Click to Answer · 点选回答

Version: 0.2.0. Category: Productivity. Shape: skills-only plugin with local Python setup script. Intended surface: Codex environments permitting Python and local instruction-file access.

Short description: Less typing. More choosing. Persistent native-choice preferences for Codex.

Long description: Enable project or global preference rules so future Codex tasks favor native YES/NO and numbered choices when user input is needed. Includes status, diagnostics, preview and precise removal. Existing instructions are preserved and backed up. Installation does not automatically enable the preference. Native tools and their permissions remain controlled by the host; unsupported environments fall back to text. No universal UI or model-compliance guarantee.

Release notes: Adds opt-in persistence CLI, override-file selection, byte-preserving updates, backup and removal, setup-focused skill, and tests. Daily rules do not require per-task skill invocation. Disabling a project preference does not suppress a global one.

## Five positive test cases

1. Enable in a temporary project containing existing rules. Verify original content is preserved, status selects the active file, and a backup exists. Enable again and verify no duplicate block or file change.
2. Enable globally in a temporary CODEX_HOME. Open a compatible new task in that profile and ask a harmless YES/NO preference. Submit a real reply; do not interpret tool acceptance as an answer.
3. Ask a four-option format preference. Submit a real reply. If capacity is three, verify grouping retains all four options.
4. Add an unrelated rule after enabling, then disable. Verify both the old and newly added unrelated rules remain byte-for-byte. Check the correct scope; other scopes may still be enabled.
5. Add a nonempty AGENTS.override.md after enabling AGENTS.md. Verify status reports the shadowed block; re-enable migrates the managed block to the override and preserves both files' unrelated content.

## Three negative test cases

1. Request a normal numbered explanation or current-conversation demo. No persistent configuration is modified without a setup request; normal lists are not questions.
2. No permitted native input tool, or only a Plan tool in Default. Report fallback; never fake a button or switch modes to evade restrictions.
3. A preference tool forbids permission approvals. Do not use it to authorize deletion, publication or installations. Silence, preselection and timeout are not consent.

## Data handling and permissions

The setup script reads AGENTS.md / AGENTS.override.md in the explicitly selected scope and writes its own block there upon enable/disable requests. Changed existing files are copied into local `.click-to-answer-backups/` and retained after disable. It performs no network calls and has no telemetry, account service or credential collection. User questions and choices remain handled by the host product. This disclosure is not a substitute for the publisher's actual public privacy policy.

## Remaining public submission requirements

- Verified publisher identity and Apps Management write access.
- Confirm the verified Platform identity matches the public GitHub maintainer identity and listing URLs in the manifest. Support: https://github.com/johnboomlog-prog/click-to-answer/issues.
- Confirm regional availability and review policy attestations.
- Included SVG logo is source artwork; export any additional portal-required format.
- Local CLI startup-rule loading and ten desktop choice scenarios, including four choices, were observed on 2026-09-16. Two panels required reopening. See the repository's docs/choice-ui-test-2026-09-16.md; this is not proof of automatic triggering reliability in fresh tasks.
- Submit for review, then publish only after approval. Neither acceptance nor directory placement is guaranteed.

Official instructions: https://developers.openai.com/plugins/deploy/submission
