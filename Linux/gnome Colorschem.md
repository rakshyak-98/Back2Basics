[[commands/gsetting]] [[terminal config]] [[Linux configuration]] [[commands/customization]]

# gnome Colorschem

> GNOME color schemes and accent colors live in GSettings — `gsettings` / `dconf` flip dark/light preference and GTK theme for the desktop session.

## Interview Relevance
Light desktop-ops question: show you can change appearance non-interactively (`gsettings`) for golden images or remote sessions without clicking through Settings UI.

## Sources
- [GNOME Human Interface Guidelines — appearance](https://developer.gnome.org/hig/) — overview
- `man 1 gsettings` — deep-dive

## Core Definition
GNOME 42+ stores interface preference under `org.gnome.desktop.interface` keys such as `color-scheme` (`default` / `prefer-dark` / `prefer-light`) and `gtk-theme`. Terminal colors are separate schemas.

## Key Concepts
- **GSettings vs dconf:** `gsettings` is the friendly CLI; dconf is the backing database.
- **color-scheme:** High-level dark/light preference apps should honor.
- **gtk-theme:** Concrete theme name when you pin a look.
- **Terminal profiles:** GNOME Terminal uses its own paths under `/org/gnome/terminal/`.

## Technical Details

```bash
gsettings get org.gnome.desktop.interface color-scheme
gsettings get org.gnome.desktop.interface gtk-theme
gsettings range org.gnome.desktop.interface color-scheme

gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'

dconf dump /org/gnome/terminal/
```

Values (GNOME 42+): `'default'`, `'prefer-dark'`, `'prefer-light'`.

## Real-World Applications
A provisioning script sets `prefer-dark` on developer workstations so GTK apps and the shell match without each user hunting through Settings.

## Pros/Cons or Trade-offs
- **Pro:** Scriptable, reversible, per-user — fits configuration management of desktops.
- **Con:** Keys move across GNOME major versions; terminal theming is a different schema tree.

## Comparison
vs [[terminal config]]: GNOME color-scheme is desktop-wide; terminal palettes are emulator-specific. vs qt5ct/KDE: different settings buses — do not expect `gsettings` to theme Qt apps the same way.

## Mistakes to Avoid
- Setting `gtk-theme` alone on GNOME 42+ and wondering why libadwaita apps ignore it — prefer `color-scheme`.
- Running `gsettings` as root expecting the logged-in user’s session to change (needs the session D-Bus / correct user).
- Mixing filename typo “Colorschem” with docs searches for “color scheme” — search both.
