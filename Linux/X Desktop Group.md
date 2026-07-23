[[Linux]] [[file descriptors]] [[systemctl]] [[journalctl]]

# X Desktop Group

> **XDG Base Directory Specification** — standard paths for config, data, cache, and runtime files on Linux — essential for portable CLI tools and CI.

---

## Mental model

```txt
~/.config/     XDG_CONFIG_HOME   — user settings (small, portable)
~/.local/share XDG_DATA_HOME    — app data, databases
~/.cache/      XDG_CACHE_HOME    — regenerable caches
/run/user/$UID XDG_RUNTIME_DIR   — sockets, pid files (tmpfs, user session)
```

**Before XDG:** dotfile explosion in `$HOME` (`.foo`, `.barrc`) — backup tools and corporate homedir sync suffered.

**Spec:** freedesktop.org — apps **should** read env vars; fall back to defaults above.

```txt
$HOME
├── .config/myapp/config.toml
├── .local/share/myapp/state.db
└── .cache/myapp/downloads/
```

---

## Standard config / commands

### Environment defaults

```bash
# Usually unset — defaults apply
echo "${XDG_CONFIG_HOME:-$HOME/.config}"
echo "${XDG_DATA_HOME:-$HOME/.local/share}"
echo "${XDG_CACHE_HOME:-$HOME/.cache}"
echo "${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
```

### App implementation (Go example)

```go
func configDir(app string) string {
  if d := os.Getenv("XDG_CONFIG_HOME"); d != "" {
    return filepath.Join(d, app)
  }
  home, _ := os.UserHomeDir()
  return filepath.Join(home, ".config", app)
}
// Same pattern for DATA and CACHE
```

### systemd user service

```ini
[Service]
Environment=XDG_CONFIG_HOME=%h/.config
Environment=XDG_DATA_HOME=%h/.local/share
```

### Respect in shell tools

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/mycli"
export MYCLI_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/mycli/config.yaml"
```

### Migration from legacy dotfile

```txt
1. Read new path first
2. If missing, read ~/.myapprc and offer import
3. Write only to XDG paths
4. Document in man page / --help
```

### CI / containers

```dockerfile
ENV XDG_CONFIG_HOME=/tmp/.config
ENV XDG_CACHE_HOME=/tmp/.cache
RUN mkdir -p $XDG_CONFIG_HOME $XDG_CACHE_HOME
# Writable homedir not required
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Config not found after login | `$XDG_CONFIG_HOME` typo | Unset or fix env in `.profile` |
| Disk full on cache | `~/.cache` size | `du -sh ~/.cache/*`; app cleanup; tmpfs for CI |
| Permission denied runtime | `XDG_RUNTIME_DIR` | Must be uid-owned, 0700; systemd sets on login |
| Two configs diverge | Legacy + XDG both exist | Deprecate `~/.apprc`; single source |
| Snap/Flatpak different paths | Sandbox overrides | Use `snap run --shell` / portal docs |
| NFS home slow | Cache on NFS | Point `XDG_CACHE_HOME` to local disk |

---

## Gotchas

> [!WARNING]
> **Hardcoding `~/.config`** — breaks when users relocate XDG dirs — always honor env.

> [!WARNING]
> **Secrets in config vs keyring** — tokens belong in Secret Service / keychain, not world-readable yaml.

> [!WARNING]
> **`XDG_RUNTIME_DIR` on SSH non-interactive** — may be unset; don't require for batch jobs.

> [!WARNING]
> **Roaming profiles (Windows crossover)** — WSL paths differ; document WSL `\\wsl$\` behavior separately.

---

## When NOT to use

- **System-wide daemon config** — `/etc/myapp/` + `/etc/myapp/conf.d/` (FHS), not user XDG.
- **macOS primary target** — use `~/Library/Application Support` (or cross-platform dirs crate).
- **Windows** — `%APPDATA%`, `%LOCALAPPDATA%` via known-folder API.

---

## Related

[[file descriptors]] · [[Linux]] · [[systemctl]] · [[journalctl]] · [[ssh agent]]
