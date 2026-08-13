[[commands]] [[gnome Colorschem]] [[X Desktop Group]]

# gsetting

> `gsettings` reads/writes GNOME/dconf keys — the schema’d way to change desktop settings from the shell.

---

## How it works

```txt
gsettings ──► dconf DB (~/.config/dconf/user)
                 ▲
            GSettings schemas (/usr/share/glib-2.0/schemas)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **schema** | Namespace of keys | “List with `gsettings list-schemas`.” |
| **key** | One setting | “`get` before `set`.” |
| **dconf** | Binary settings DB | “gsettings is the safe API over dconf.” |
| **range / describe** | Allowed values | “`gsettings range SCHEMA KEY`.” |
| **reset** | Back to default | “`gsettings reset` undoes experiments.” |

---


## Configuration and commands

```bash
gsettings list-schemas | head
gsettings list-keys org.gnome.desktop.interface
gsettings get org.gnome.desktop.interface color-scheme
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings range org.gnome.desktop.interface color-scheme
gsettings reset org.gnome.desktop.interface color-scheme
# dump/load (dconf)
dconf dump /org/gnome/ > gnome.dconf
dconf load /org/gnome/ < gnome.dconf
```

| Knob | Why it matters |
|------|----------------|
| Correct schema path | Typos silently no-op or error |
| Session bus | Needs user D-Bus (logged-in GUI) |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| No such schema | Package missing | Install GNOME schema package |
| Set does nothing | Wrong session / Wayland | Run as desktop user; check schema |
| Reverts on login | Managed by fleet policy | dconf locks / enterprise profiles |
| Can’t run over SSH | No session bus | `export DBUS_SESSION_BUS_ADDRESS=…` or local terminal |

---


## Gotchas

> [!WARNING]
> **Editing dconf binary by hand** — prefer `gsettings`/`dconf dump|load`.

> [!WARNING]
> **Root gsettings ≠ user desktop** — keys are per-user.

---


## When not to use

- **Non-GNOME desktops** — KDE uses different configuration stores.
- **Server automation** — no GUI schemas; use files/systemd instead.

---


## Related

[[gnome Colorschem]] [[X Desktop Group]] [[D-Bus]] [[editor configuration]]

## Sources

- [Wikipedia — gsetting](https://en.wikipedia.org/wiki/gsetting)
