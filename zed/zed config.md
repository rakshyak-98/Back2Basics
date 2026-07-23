[[Descriptive/vscode]] [[editor config]] [[Linux/CLI]]

# Zed config

> `~/.config/zed/settings.json` — themes, LSP, formatters, and remote editing over SSH.

## Mental model

Zed reads JSON settings (user + optional project `.zed/settings.json`). Language servers attach per language block. Remote files use `zed ssh://user@host/path` with remote LSP when configured. Precedence: project overrides user for same keys.

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Remote open fails | SSH key, host | `ssh user@host` first; fix `~/.ssh/config` |
| ESLint still runs | Language server list | Use `"!eslint"` suffix; restart Zed |
| Format on save no-op | Formatter set? | Add `"formatter": "prettier"` + project config |
| LSP not found | `which typescript-language-server` | Install globally or via mise/nvm |
| Settings ignored | Project vs user path | Check `.zed/settings.json` overrides |

## Gotchas

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

[[Descriptive/vscode]] [[editor config]] [[npm/husk]]
