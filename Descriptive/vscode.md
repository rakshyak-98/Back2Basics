[[Descriptive]] [[GIT/git command]] [[ssh/ssh allow local system with key]]

# VS Code (CLI and workspace ops)

> Editor CLI + multi-root workflow — open correct folder, reuse window, remote URIs, and command palette IDs for automation and docs.

```txt
        VS Code (CLI and w ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Editor fluency shows debugging/LSP setup

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** `code` CLI talks to a running VS Code (or Cursor-compatible) instance via IPC

```
code . ──► running instance ──► opens folder in window
         │
         └── -n forces new window; -r reuses existing
```

- **Note:** Remote: `vscode-remote://` URIs target SSH/WSL/development Containers attach …

## Technical Details
### Open workspace

```bash
# Current directory in active window
code .

# Specific path
code /home/ubuntu/GitHub/Back2Basics

# Reuse window (replace folders) — avoids window sprawl
code -r /path/to/project

# New window
code -n /path/to/project

# Add folder to workspace (multi-root)
code --add /path/to/other-repo

# Open file at line
code -g src/app.ts:42
```

### Remote / URI

```bash
# Remote SSH (when Remote-SSH extension configured)
code --folder-uri "vscode-remote://ssh-remote+myhost/home/ubuntu/project"

# WSL
code --folder-uri "vscode-remote://wsl+Ubuntu/home/ubuntu/project"
```

### Diff and wait (scripts / CI)

```bash
code --diff file1 file2
code --wait path/to/generated.md   # block until editor closed
```

### List extensions / install (bootstrap)

```bash
code --list-extensions
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
```

### User settings (JSON)

```json
{
  "window.openFoldersInNewWindow": "off",
  "files.autoSave": "onFocusChange",
  "editor.formatOnSave": true,
  "terminal.integrated.defaultProfile.linux": "zsh"
}
```

### Command ID (keybindings / tasks)

- Find command ID: **Command Palette → "Developer: Show Command Palette"** → ru…

```json
// keybindings.json
{
  "key": "ctrl+shift+t",
  "command": "workbench.action.terminal.toggleTerminal"
}
```

- Common IDs:

- `workbench.action.files.saveAll`
- `editor.action.formatDocument`
- `workbench.action.reloadWindow`
- `git.commit` (with Git extension)

### Integrated terminal

```bash
# From palette: Terminal: Create New Terminal
# Settings: terminal.integrated.cwd, shell args
```

## Mistakes to Avoid
> [!WARNING]
> **Cursor vs VS Code CLI** — may be `cursor` not `code` on some installs; same flags usually apply.

> [!WARNING]
> **`code .` from wrong cwd** — multi-root confusion; always cd to repo root or use `-g` for files.

> [!WARNING]
> ** `--wait` in scripts** — hangs if editor not GUI-available (headless CI); use non-interactive tools instead.

> [!WARNING]
> **Settings sync** — machine-specific paths in settings break remote dev; use relative or env vars.

| Symptom | Check | Fix |
|---------|-------|-----|
| `code: command not found` | CLI not on PATH | Shell Command: Install 'code' command in PATH (or Cursor equivalent) |
| Opens new window every time | `-n` or setting | Use `code -r .`; set `window.openFoldersInNewWindow`: `off` |
| Wrong folder root | Opened parent not repo | Open git root: `code $(git rev-parse --show-toplevel)` |
| Remote won't connect | SSH config / extension | Verify `Remote-SSH: Connect to Host`; check `~/.ssh/config` |
| Extension missing in remote | Local vs remote install | Install extension on SSH/WSL side |
| Format on save broken | No default formatter | Set `"editor.defaultFormatter"` per language |
| Keybinding no effect | Conflicting chord | Troubleshooting log; unbind conflict |

## Pros/Cons or Trade-offs
- **Production server editing**
- **Heavy batch refactors**
