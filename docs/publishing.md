# Publishing checklist

## GitHub

The repository and marketplace are prepared for publication; no owner or remote URL is assumed. Select an actual GitHub account and repository before pushing. Keep the repository name `click-to-answer` unless another name is wanted.

1. Run `python -m unittest discover -s tests -v` and `python scripts/build_release.py`.
2. Review tracked files. `.gitignore` excludes local dialogue evidence, development notes, archives and backups. Never force-add these private records.
3. Set the real remote, push the reviewed source, then run CI and check its results. CI configuration alone is not passing CI.
4. Create a release tagged `v0.2.0`; attach the plugin ZIP, source ZIP and SHA256SUMS.txt from `dist/`.
5. Add the actual repository URL to public documentation and plugin metadata. The local marketplace can be added with `codex plugin marketplace add .`; after publication, use the actual repository URL instead of `.`.
6. Record a short real demonstration showing enable, a new task, a choice staying visible, and a submitted answer. Do not use a mock animation as evidence of working UI.

The GitHub Actions workflow only tests/builds artifacts. It never publishes a release automatically.

## Official plugin directory

The plugin is skills-only with a bundled local setup script. Surface support for executing that script must be stated. Marketplace review acceptance is not guaranteed.

Public submission requires a verified publisher, matching author/developer identity, public support/website/privacy/terms URLs, a logo and test cases. `Local developer` in the development manifest must be replaced with the real publisher name. The logo source is included as SVG; export any additional format required by the portal before submission.

Use the draft in `plugins/click-to-answer/SUBMISSION.md`. Review the exact package, permissions and policy attestations before submitting; publication is separate from submission and approval.

References checked 2026-09-16:

- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/build/plugins
- https://learn.chatgpt.com/docs/agent-configuration/agents-md

## Upgrade and uninstall

Updating the plugin does not silently rewrite existing persistent instructions. Run enable again in each desired scope to apply the current bundled policy. Before uninstalling, run disable in every enabled scope. Removing the plugin through Codex cannot be assumed to remove independently stored AGENTS rules. Backups remain until manually reviewed and removed.
