[[Descriptive/vscode]] [[editor config]] [[Linux/CLI]] [[zed keybindings]]

# Zed config

> `~/.config/zed/settings.json` — themes, LSP, formatters, inline edit predictions, and remote editing over SSH.

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Zed reads JSON settings (user + optional project `.zed/settings.json`). Language servers attach per language block. Remote files use `zed ssh://user@host/path` with remote LSP when configured. Precedence: project overrides user for same keys.

**Completions are two different systems** — do not conflate them:

| Source | Zed name | UI | VS Code analogue |
|--------|----------|-----|------------------|
| Language server (gopls, TS, etc.) | **Code completions** | **Popup menu** | IntelliSense dropdown |
| Zeta / Copilot / Codestral | **Edit predictions** | **Inline ghost text** | Copilot inline suggest |

Zed has **no setting** to render LSP completions (e.g. `int`, `int16` in Go) as inline ghost text. That requires `textDocument/inlineCompletion` LSP support — [not implemented generically yet](https://github.com/zed-industries/zed/issues/27392). For VS Code–style ghost hints, use **edit predictions** and suppress the LSP popup from auto-opening.

```txt
Typing []in in Go
  LSP (default)     → popup menu (int, int16, int32, …)     ← your screenshot
  Edit predictions  → grey ghost text inline, Tab to accept ← VS Code Copilot feel
```

When both would show, Zed prioritizes the LSP menu in `eager` mode. **Hold `alt`** to preview the inline edit prediction and hide the menu ([Zed edit prediction UX](https://zed.dev/edit-prediction)).

## Standard config / commands

### Open remote file

```bash
zed ssh://user@192.168.1.10/etc/nginx/nginx.conf
```

### Minimal settings.json

```json
{
  "theme": "One Dark",
  "buffer_font_size": 14,
  "tab_size": 2,
  "format_on_save": "on",
  "lsp": {
    "typescript-language-server": {
      "initialization_options": {
        "preferences": { "importModuleSpecifierPreference": "non-relative" }
      }
    }
  }
}
```

### Disable ESLint LSP (keep TS server)

```json
{
  "languages": {
    "JavaScript": {
      "language_servers": ["typescript-language-server", "!eslint"]
    },
    "TypeScript": {
      "language_servers": ["typescript-language-server", "!eslint"]
    }
  }
}
```

### Project-local

```json
// .zed/settings.json in repo root
{
  "formatter": "prettier",
  "format_on_save": "on"
}
```

### Inline ghost completions (VS Code Copilot-style)

**Goal:** grey inline hint at the cursor — **not** the LSP popup menu.

**Recommended `~/.config/zed/settings.json`:**

```json
{
  // Stop LSP popup on every keystroke (manual trigger: ctrl-space)
  "show_completions_on_input": false,

  // Inline ghost text from Zeta / Copilot / Codestral
  "show_edit_predictions": true,
  "edit_predictions": {
    "provider": "zed",
    "mode": "eager"
  }
}
```

| Setting | Effect |
|---------|--------|
| `show_completions_on_input: false` | No popup while typing; `ctrl-space` opens LSP menu on demand |
| `show_edit_predictions: true` | AI predictions appear as ghost text |
| `edit_predictions.mode: "eager"` | Show ghost text automatically (default) |
| `edit_predictions.mode: "subtle"` | Ghost text only while holding `alt` — less visual noise |
| `edit_predictions.provider: "copilot"` | Use GitHub Copilot instead of Zeta |

**Accept bindings (defaults):**

| Action | Linux / Windows | macOS |
|--------|-----------------|-------|
| Accept full prediction | `tab` (if menu closed) or `alt-l` | `tab` or `alt-tab` |
| Accept next word | `alt-k` | `ctrl-cmd-right` |
| Accept next line | `alt-j` | `ctrl-cmd-down` |
| Toggle predictions off (buffer) | `ctrl-shift-e` | `ctrl-cmd-e` |
| Manual show prediction | `alt-\` | `alt-tab` |
| LSP menu on demand | `ctrl-space` | `ctrl-space` |

**When LSP menu is already open:** hold `alt` — Zed previews the inline prediction and hides the popup so you can review ghost text unobstructed.

**Per-language: popup off, predictions on (Go example):**

```json
{
  "show_completions_on_input": false,
  "languages": {
    "Go": {
      "show_completions_on_input": false,
      "completions": {
        "lsp": true,
        "lsp_insert_mode": "replace_suffix"
      }
    }
  }
}
```

**Keymap: always `tab` for ghost text, `tab tab` for LSP menu item** — add to `~/.config/zed/keymap.json`:

```json
[
  {
    "context": "Editor && edit_prediction",
    "bindings": {
      "tab": "editor::AcceptEditPrediction"
    }
  }
]
```

After this, `tab tab` still accepts the highlighted LSP completion when the menu is open.

**Limitation (important):** This gives inline ghost text for **edit predictions** (AI), not for gopls type lists (`int` vs `int16`). For LSP symbol completion you still use `ctrl-space` → popup, or pick from the menu. There is no Zed equivalent of VS Code rendering the top LSP match as inline ghost today.

→ Full keybinding reference: [[zed keybindings]]

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Popup on every key, no ghost text | `show_completions_on_input` | Set `false`; enable `show_edit_predictions` + `edit_predictions.mode: "eager"` |
| Ghost text never appears | Signed in to Zed AI / Copilot? | `edit_predictions.provider`; status bar Z/Copilot icon |
| Ghost text blocked by popup | Both LSP + predictions active | `show_completions_on_input: false` or hold `alt` to preview inline |
| `tab` inserts tab, not hint | Completion menu open | `esc` dismiss menu, or use `alt-l` / keymap above |
| Only want LSP, no AI ghost | `show_edit_predictions` | Set `false`; use `ctrl-space` for menu |
| `int`/`int16` still in popup only | LSP limitation in Zed | Expected — no inline LSP setting exists yet; use menu or edit predictions |
| Remote open fails | SSH key, host | `ssh user@host` first; fix `~/.ssh/config` |
| ESLint still runs | Language server list | Use `"!eslint"` suffix; restart Zed |
| Format on save no-op | Formatter set? | Add `"formatter": "prettier"` + project config |
| LSP not found | `which typescript-language-server` | Install globally or via mise/nvm |
| Settings ignored | Project vs user path | Check `.zed/settings.json` overrides |

## Gotchas

> [!WARNING]
> **LSP completions are always a popup in Zed** — you cannot make gopls/TS type lists render as inline ghost text (unlike VS Code inline suggest for some providers).

> [!WARNING]
> **Remote SSH needs agent forwarding or keys on remote** — LSP runs where file lives.
>
> **Duplicate formatters** — Prettier + ESLint fix both on save = slow/flappy.
>
> **Invalid JSON** — trailing commas break entire settings load silently partial.

## When NOT to use

- Don't disable all linters globally to silence one noisy rule — fix rule or use local override.
- Don't commit machine-specific absolute paths in shared `.zed/settings.json`.

## Related

[[Descriptive/vscode]] [[editor config]] [[zed keybindings]] [[npm/husk]]
