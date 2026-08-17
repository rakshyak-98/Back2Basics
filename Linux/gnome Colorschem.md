[[commands/gsetting]] [[terminal config]] [[Linux configuration]] [[commands/customization]]

# gnome Colorschem

> GNOME color schemes and accent colors live in GSettings — `gsettings` / `dconf` flip dark/light preference and GTK theme for the desktop session.

```txt
        gnome Colorschem ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Light desktop-ops question: show you can change appearance non-interactively …

## Sources
- [GNOME Human Interface Guidelines — appearance](https://developer.gnome.org/hig/) — overview
- `man 1 gsettings` — deep-dive

## Key Concepts
- **GSettings vs dconf:** `gsettings` is the friendly CLI; dconf is the backing database.
- **color-scheme:** High-level dark/light preference apps should honor.
- **gtk-theme:** Concrete theme name when you pin a look.
- **Terminal profiles:** GNOME Terminal uses its own paths under `/org/gnome/terminal/`.


- **Core:** GNOME 42+ stores interface preference under `org.gnome.desktop.interface` key…

## Technical Details
```bash
gsettings get org.gnome.desktop.interface color-scheme
gsettings get org.gnome.desktop.interface gtk-theme
gsettings range org.gnome.desktop.interface color-scheme

gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'

dconf dump /org/gnome/terminal/
```

- Values (GNOME 42+): `'default'`, `'prefer-dark'`, `'prefer-light'`.

## Mistakes to Avoid
- **Mistake:** Setting `gtk-theme` alone on GNOME 42+ and wondering why libadwa…
- **Mistake:** Running `gsettings` as root expecting the logged-in user’s sessi…
- **Mistake:** Mixing filename typo “Colorschem” with docs searches for “color …

## Pros/Cons or Trade-offs
- **Pro:** Scriptable, reversible, per-user — fits configuration management of desktops.
- **Con:** Keys move across GNOME major versions; terminal theming is a different schema tree.

## Comparison
- vs [[terminal config]]: GNOME color-scheme is desktop-wide; terminal palettes…


### Use cases
- A provisioning script sets `prefer-dark` on developer workstations so GTK app…
