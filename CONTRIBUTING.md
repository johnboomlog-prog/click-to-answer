# Contributing

Keep the tool small: native choices, safe preference management and honest compatibility reporting. Python 3.11+ standard library only.

Run `python -m unittest discover -s tests -v` before a pull request. Test file mutations in temporary directories, never against a contributor's real global instructions. Do not upload AGENTS files, backups, tokens or raw private conversation logs.

For a compatibility report include OS, Codex surface/version, mode, whether native tools were available, whether the control stayed visible, and whether an actual answer was returned. Redact personal content. A tool returning accepted=true is not proof of rendering or a mouse click.

For changes to managed blocks, verify enable twice, disable, preservation of unrelated edits, BOM/line endings, override precedence and refusal of malformed data. Preserve backwards-compatible begin/end markers so old preferences can be removed.

For release work follow docs/publishing.md. Do not publish invented screenshots or claim unrun CI jobs passed.
