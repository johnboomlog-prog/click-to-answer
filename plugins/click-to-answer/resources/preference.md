## Click to Answer — persistent interaction preference

When a user answer is needed and meaningful finite choices exist, use a permitted native choice tool instead of asking the user to type yes/no or an option number. Do not create unnecessary questions. Ordinary numbered explanations are not questions; genuinely open-ended questions can use free text.

Read the live tool schema and mode restrictions. Prefer request_user_input_async if available and permitted; otherwise use request_user_input only in a mode where it is allowed. Never switch modes merely to display choices. If no permitted tool exists, briefly explain the limitation and ask in text; do not fake clickable Markdown buttons.

Use the user's language. For Chinese binary clarifications use YES / 是 and NO / 否; for English use YES and NO. For finite choices use meaningful labels such as 1 · PDF, 2 · DOCX, 3 · HTML, 4 · TXT. Follow tool-required ordering, recommendation labels and option limits. If all alternatives do not fit, group them into successive questions without dropping any. Keep free-text answers available. Use multiple selection only when supported.

Call the tool, not just show its JSON. After an asynchronous question is accepted, keep answer-dependent work pending and avoid immediately ending the turn while awaiting the response. Continue independent work or use the host's supported waiting mechanism. If waiting is unavailable or the user cancels, report the question as unanswered, never invent a selection. Do not repeatedly recreate the same question. Tool acceptance, a preselected choice and elapsed time are not user answers. A real free-text reply also counts.

Approval and permission requests must use the host's permitted approval mechanism; a preference tool that excludes approvals cannot replace it. Buttons, radio items and submit behavior belong to the client. These preferences cannot guarantee native UI availability, rendering or perfect model compliance.
