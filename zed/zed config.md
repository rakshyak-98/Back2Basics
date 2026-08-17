[[Descriptive/vscode]] [[zed keybindings]] [[zed debugger]] [[LSP]]

# Zed config

> JSON settings for the Zed editor — user defaults plus optional project `.zed/settings.json`; language servers and edit predictions are separate systems.





## Interview Relevance
Interviewers (tooling/DX) care that you do not confuse LSP popup completions with inline “ghost” predictions, and that project settings override user settings.

## Sources
- [Zed — Configuring Zed](https://zed.dev/docs/configuring-zed) — deep-dive
- [Zed — Language servers](https://zed.dev/docs/language-model-tool) — overview

## Key Concepts
- **Precedence:** project `.zed/settings.json` overrides user settings for the same keys.
- **Code completions (LSP):** popup menu from gopls/tsserver/etc.
- **Edit predictions:** inline ghost text (Zeta/Copilot-style) — different protocol/UX.
- **Remote edit:** `zed ssh://user@host/path` with remote LSP when configured.

## Technical Details
| Source | UI | VS Code analogue |
|--------|----|------------------|
| Language server | Popup menu | IntelliSense |
| Edit predictions | Inline ghost text | Copilot inline |

```bash
zed ssh://user@192.168.1.10/etc/nginx/nginx.conf
```

Zed does not generically render normal LSP completions as ghost text; that needs inline-completion support. When both would show, hold `alt` to preview the inline prediction and hide the menu.

## Real-World Applications
Team-shared `.zed/settings.json` pins formatters and enable/disable predictions per repository.

**Example:** Go `int` completions appear only in the popup — expected for LSP; enable edit predictions if you want Copilot-like ghosts.

## Pros/Cons or Trade-offs
- **Pro:** Fast native editor with first-class LSP + optional AI predictions.
- **Con:** Mental model differs from VS Code if you expect all hints as ghost text.

## Comparison
- vs [[Descriptive/vscode]]: similar settings layers; different prediction/completion UX details.
- vs [[zed keybindings]]: config defines behavior; keybindings bind chords to actions.

## Mistakes to Avoid
- Hunting for a setting to turn LSP items into ghost text — use edit predictions instead.
- Committing machine-local paths in project settings.
- Assuming remote SSH opens without considering remote LSP install.
