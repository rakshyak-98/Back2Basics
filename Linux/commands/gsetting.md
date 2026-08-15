[[Commands]] [[gnome Colorschem]] [[X Desktop Group]] [[D-Bus]] [[customization]]

# gsetting

> gsettings reads and writes GNOME/dconf keys — the schema’d way to change desktop settings from the shell.

## Interview Relevance
Desktop Linux: schema/key model, dconf vs gsettings, and why SSH without a session bus cannot change the logged-in user’s desktop.

## Sources
- [GSettings overview — GNOME](https://developer.gnome.org/documentation/tutorials/gsettings.html) — deep-dive
- [gsettings(1)](https://man.archlinux.org/man/gsettings.1) — overview

## Core Definition
`gsettings` is the typed API over the per-user **dconf** database. Schemas under `/usr/share/glib-2.0/schemas` define keys and allowed values; `get`/`set`/`reset` change them for the current user session.

## Key Concepts
- **schema / key:** Namespace and one setting inside it.
- **dconf:** Binary settings DB (`~/.config/dconf/user`).
- **range / describe:** Allowed values before you set.
- **Session bus:** Needs the desktop user’s D-Bus.
- **Per-user:** Root gsettings ≠ the GUI user’s settings.

## Technical Details

```txt
gsettings ──► dconf DB (~/.config/dconf/user)
                 ▲
            GSettings schemas (/usr/share/glib-2.0/schemas)
```

```bash
gsettings list-schemas | head
gsettings list-keys org.gnome.desktop.interface
gsettings get org.gnome.desktop.interface color-scheme
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings range org.gnome.desktop.interface color-scheme
gsettings reset org.gnome.desktop.interface color-scheme

dconf dump /org/gnome/ > gnome.dconf
dconf load /org/gnome/ < gnome.dconf
```

| Symptom | Check | Fix |
|---------|-------|-----|
| No such schema | Package missing | Install GNOME schema package |
| Set does nothing | Wrong session / Wayland | Run as desktop user; check schema |
| Reverts on login | Fleet policy | dconf locks / enterprise profiles |
| Can’t run over SSH | No session bus | Export `DBUS_SESSION_BUS_ADDRESS` or use local terminal |

## Real-World Applications
Toggling dark mode from a script, dumping GNOME settings into dotfiles, and resetting a broken extension schema key.

## Pros/Cons or Trade-offs
- **Pro:** Safer than hand-editing dconf binary; schema-validated.
- **Con:** GNOME-centric; useless on headless servers.
- **Trade-off:** Per-user tweaks vs locked corporate dconf baselines.

## Comparison
vs [[customization]] (extensions CLI): extensions vs settings keys. vs KDE: different stores. vs [[X Desktop Group]] base dirs: XDG paths vs dconf values.

## Mistakes to Avoid
- Editing the dconf binary by hand.
- Changing settings as root and expecting the desktop user to see them.
- Automating gsettings from cron without a session bus.
