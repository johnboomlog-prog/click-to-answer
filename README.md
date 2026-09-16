<img src="plugins/click-to-answer/assets/logo.svg" width="72" alt="Click to Answer logo">

# Click to Answer

**Less typing. More choosing. Persistent native-choice preferences for Codex.**

[简体中文](README.zh-CN.md) · [Compatibility](docs/compatibility.md) · [Publishing](docs/publishing.md)

Enable once. In subsequent Codex tasks, prefer native YES/NO and numbered choices when a user decision is needed. Keep free text for answers that do not fit a menu.

This is an opt-in instruction manager, not a client UI patch. Codex must provide a permitted native choice tool. It cannot force buttons into unsupported clients or guarantee every model response follows the preference.

## What you get

- Project or global scope; no per-conversation skill invocation required once configured.
- `enable`, `disable`, `status`, `doctor`, and a write-free preview.
- Idempotent updates, backups, atomic file replacement, and preservation of unrelated instructions.
- No server, account, API key, telemetry, or third-party Python packages.
- A Codex plugin for conversational setup and the same standalone CLI for GitHub users.

## Quick start from a source ZIP or Git checkout

Requires **Python 3.11+**. Open a terminal in this repository after extracting the source ZIP or cloning it. On Windows, `py -3` may be used instead of `python`.

```sh
# Preview the exact global target without changing it.
python plugins/click-to-answer/scripts/preferences.py enable --scope global --dry-run

# Enable for future Codex tasks on this machine/profile.
python plugins/click-to-answer/scripts/preferences.py enable --scope global

# Inspect configuration; this does not pretend to verify UI rendering.
python plugins/click-to-answer/scripts/preferences.py doctor --scope global

# Remove only this tool's global instruction block.
python plugins/click-to-answer/scripts/preferences.py disable --scope global
```

To configure only the current project, use `--scope project --project .`. The project directory must already exist. Global scope honors `CODEX_HOME`; `--codex-home PATH` explicitly selects another profile.

**Start a new Codex task after changing configuration.** Ask it to present a harmless YES/NO preference and a four-format choice. Click and submit an answer; the client may require both selection and submission. The CLI cannot introspect native tools inside your task.

## Plugin setup

Install from the public GitHub marketplace:

```sh
codex plugin marketplace add https://github.com/johnboomlog-prog/click-to-answer.git
codex plugin add click-to-answer@click-to-answer
```

In a new Codex task, select **Click to Answer** and say:

> Enable persistent clickable answers for this project.

You can also ask to enable globally, inspect status, disable, or run a live demo. The setup skill uses the same CLI. Installing the plugin by itself does **not** edit global preferences. Public directory submission is a separate review process and is not yet complete.

## How persistence works

The CLI manages one marked block in the selected scope's `AGENTS.override.md` when nonempty, otherwise `AGENTS.md`. The block contains the full preference; it does not point into a versioned plugin cache. Each changed existing file is backed up beside it in `.click-to-answer-backups/`. Existing UTF-8 BOM and CRLF/LF content are preserved. Unknown encodings, symbolic-link instruction files, malformed blocks and duplicate markers are refused rather than overwritten.

`status` reports whether the selected file contains the managed block. It cannot prove a live task loaded it. Other project instructions, nested directories, custom profiles and context limits can affect the result.

**Disable before uninstalling the plugin.** Remove the preference in every scope where you enabled it. Project disable does not suppress a global preference. Backup files are retained for manual recovery and may contain private instructions; do not commit them. Never restore an old whole-file backup over later edits without reviewing the difference.

## Reliability and scope

Choices are used for actual questions, not ordinary numbered explanations. Answers are never inferred from preselection, silence or tool acceptance. Permission prompts retain the host's approval mechanism. When native choices are unavailable, the assistant explains that limitation and uses text.

The 0.2.0 Windows desktop smoke test displayed choices and received matching answers in all ten prompted scenarios, including four options, long labels and mixed languages. Two panels collapsed and were restored through the answer entry. This does not establish automatic triggering reliability or cross-client support. See the [test record](docs/choice-ui-test-2026-09-16.md) and [compatibility record](docs/compatibility.md). No staged illustration is presented as a real UI recording.

## Development

```sh
python -m unittest discover -s tests -v
python scripts/build_release.py
```

Builds a plugin ZIP, a clean source ZIP and SHA-256 checksums in `dist/`. Local conversation logs and workstation-specific development records are excluded. CI runs tests on Windows, macOS and Linux; configured CI is not evidence those remote jobs have run.

See [CONTRIBUTING.md](CONTRIBUTING.md). MIT licensed. If this saves you repetitive typing, a star helps others find it; reproducible compatibility reports are equally welcome.
