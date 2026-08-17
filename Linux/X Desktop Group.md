[[display server]] [[Linux configuration]] [[wayland]] [[Linux display manager]] [[gsetting]]

# X Desktop Group

> The X Desktop Group (XDG) publishes freedesktop.org standards — base directories, `.desktop` files, icons, and portals that unify GNOME, KDE, and other desktops.





## Interview Relevance
Useful for “where does config live?” — `XDG_CONFIG_HOME`, desktop entries, and portals for sandboxed apps on Wayland.

## Sources
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) — deep-dive
- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html) — deep-dive

## Core Definition
XDG (via freedesktop.org) defines shared desktop conventions: **Base Directory** (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`), **Desktop Entry** (`.desktop` launchers), **Icon Theme**, **MIME apps**, and **xdg-desktop-portal** for sandboxed apps on Wayland.

## Key Concepts
- **Base dirs:** Prefer `~/.config`, `~/.local/share`, `~/.cache` over dumping in `$HOME`.
- **.desktop files:** Launch metadata — Name, Exec, Icon, Categories, MIME types.
- **Portals:** Mediated access to files, screenshots, devices for Flatpak/sandboxes.
- **MIME defaults:** `xdg-open` / `xdg-mime` choose handlers.

## Technical Details
```bash
echo $XDG_CONFIG_HOME    # default ~/.config
echo $XDG_DATA_HOME      # default ~/.local/share
echo $XDG_CACHE_HOME
```

```ini
# ~/.local/share/applications/myapp.desktop
[Desktop Entry]
Type=Application
Name=My App
Exec=/usr/local/bin/myapp
Icon=myapp
Categories=Utility;
```

```bash
xdg-open file.pdf
update-desktop-database ~/.local/share/applications
```

## Real-World Applications
Shipping a custom launcher for an internal tool, fixing “Open with…” defaults, and explaining why Flatpak apps ask portals instead of reading arbitrary paths.

## Pros/Cons or Trade-offs
- **Pro:** Cross-DE consistency; cleaner home directories.
- **Con:** Not every app honors XDG; some still write `~/.<app>`.
- **Trade-off:** Portals improve security at the cost of extra prompts and integration bugs.

## Comparison
vs dumping config in `$HOME`: XDG is the modern convention. vs GNOME-only gsettings: XDG is cross-desktop; [[gsetting]] is GNOME/dconf-specific. Related: [[wayland]], [[Linux display manager]].

## Mistakes to Avoid
- Hard-coding `~/.config` without respecting `$XDG_CONFIG_HOME`.
- Forgetting `update-desktop-database` after adding `.desktop` files.
- Expecting portals to work identically across every compositor.
