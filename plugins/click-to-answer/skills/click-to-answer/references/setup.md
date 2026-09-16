# Commands

The CLI is `../../../scripts/preferences.py` relative to this reference directory, or `../../scripts/preferences.py` relative to the skill directory. Resolve an absolute path before running it. Python 3.11+ is required. Run the same interpreter with `-X utf8`.

From the plugin root:

```sh
python -X utf8 scripts/preferences.py enable --scope global --dry-run
python -X utf8 scripts/preferences.py enable --scope global
python -X utf8 scripts/preferences.py status --scope global
python -X utf8 scripts/preferences.py doctor --scope global
python -X utf8 scripts/preferences.py disable --scope global
```

For project scope use `--scope project --project "EXACT_PROJECT_DIRECTORY"`. Never silently substitute a different checkout. Global scope honors `CODEX_HOME` and permits an explicit `--codex-home`.

Successful commands output JSON and exit 0. Operational errors output JSON `error` and exit 2. Parser errors may use standard argparse stderr. Preview reports current status plus planned_files, not future status. `configured` means the active instruction file contains the managed block, not that this task has loaded it or that buttons render. `global_configured` can explain why project disable does not turn off a global preference.

Changed existing files are backed up in `.click-to-answer-backups/` beside the instruction file. Disable removes managed blocks from both AGENTS.md and AGENTS.override.md, leaves all other content and backups intact, and may leave a new instruction file empty. Disable each scope before uninstalling the plugin. Do not delete backups automatically or restore an entire old file over later user edits.
