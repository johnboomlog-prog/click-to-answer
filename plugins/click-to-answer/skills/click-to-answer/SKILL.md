---
name: click-to-answer
description: Use when the user wants to enable, disable, inspect or test persistent clickable-answer preferences in Codex, or explicitly asks to use Click to Answer for yes/no and finite-choice questions. Includes project or global setup and native-choice smoke tests.
---

# Click to Answer

This skill is a setup and test entry point. Daily behavior comes from opt-in persistent instructions; installation alone does not enable them.

## Configure

Read [the command reference](references/setup.md). Use the packaged Python CLI; do not hand-edit global instructions or create duplicate copies of the skill. No third-party packages or network access are required.

- Explicit project/global enable or disable: perform the command within that scope. Follow host permissions; don't ask again when scope and authorization are clear.
- Persistent enable without a scope: ask project versus global through a permitted native preference tool. This chooses scope, not permission to bypass approval. If that tool forbids asking for approval, use the host's approved mechanism.
- Status or diagnosis: use read-only status/doctor. Report the target file, configured state and material warnings. Configured does not mean loaded or UI verified.
- Demo/current-conversation preference only: do not modify files.

After configuration, explain that subsequent new tasks load the rule. Preserve unrelated instructions. Report malformed marker, encoding or symlink errors instead of overwriting. Project disable does not disable a global preference. Disable enabled scopes before uninstalling; plugin removal does not remove persisted instructions.

## Real native-choice test

Read [the shared interaction policy](../../resources/preference.md) and apply it in this conversation. Inspect live schemas and mode restrictions. Ask one harmless YES/NO preference, then a four-option preference when full verification is requested. Wait for each actual reply before advancing. If capacity is three, group the alternatives without dropping any. Do not change modes to access a tool.

After async acceptance, keep the interaction pending and use a supported interruptible wait; do not immediately send a final response that can dismiss pending UI. Never invent a reply or treat timeout as consent. If the host cannot keep it pending, report an unanswered test. User cancellation ends the test.

Report separately: instruction configured, skill discovered, tool called, tool accepted, real reply received. Claim rendering or mouse interaction only when directly observed or explicitly confirmed by the user. JSON examples, static screenshots and accepted=true alone are not successful clicks.
