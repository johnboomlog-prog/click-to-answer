# Compatibility and evidence

| Layer | Status |
| --- | --- |
| Python 3.12 on Windows: preference CLI integration tests | Locally tested; run the suite for current count |
| Python 3.11/3.13 on Windows, macOS, Linux | Remote matrix runs available in [GitHub Actions](https://github.com/johnboomlog-prog/click-to-answer/actions); inspect the release commit's result |
| 0.1.0 Codex desktop Default-mode native async questions | Tool accepted; actual YES/NO and a later two-option reply received |
| Four-option native question | Desktop UI displayed all four options; fourth option clicked and TXT answer received in the 2026-09-16 live run |
| Immediate final response after async question | User reported control disappeared; waiting later received an answer; causal fix not proven |
| 0.2.0 project rules in a fresh local Codex CLI process | Read-only startup check passed on Windows, Codex 0.154.0-alpha.6.2; process reported the injected project rules without reading files or invoking tools |
| 0.2.0 desktop live interaction after setup | Ten prompted scenarios displayed choices and returned answers; two panels collapsed and were reopened. See [live UI results](choice-ui-test-2026-09-16.md). This does not establish fresh-task automatic triggering reliability |
| Codex surfaces without permitted native input tools | Text fallback, not clickable UI |
| ChatGPT general-purpose client | Not claimed supported by this first release |

## Live check

1. Enable in an explicitly chosen scope, run doctor, and open a new task in that scope.
2. Ask whether the user wants Chinese output; call the actual permitted native tool.
3. Keep the question pending, select YES or NO and submit it. Record the real answer.
4. Ask for PDF / DOCX / HTML / TXT. Keep all four alternatives; group only if required by tool limits. Submit and record the answer.
5. Ask for an ordinary numbered explanation. No new choice question should be invented.
6. Disable the same scope and open another task; verify the managed preference is absent. Native choices may still be used by Codex itself, so their mere presence does not prove disable failed.

Separate configuration, instruction loading, tool availability, tool acceptance, visual rendering and actual response. Record product version and OS; do not infer mouse use from a text response. No guarantee of universal tool availability or perfect model adherence is made.
