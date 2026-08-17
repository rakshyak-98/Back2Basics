[[display server]] [[Linux configuration]] [[wayland]] [[Linux display manager]] [[gsetting]]

# X Desktop Group

> The X Desktop Group (XDG) publishes freedesktop.org standards — base directories, `.desktop` files, icons, and portals that unify GNOME, KDE, and other desktops.

```txt
        X Desktop Group ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Useful for “where does config live?”

## Sources
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) — deep-dive
- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html) — deep-dive

## Key Concepts
- **Base dirs:** Prefer `~/.config`, `~/.local/share`, `~/.cache` over dumping in `$HOME`.
- **.desktop files:** Launch metadata — Name, Exec, Icon, Categories, MIME types.
- **Portals:** Mediated access to files, screenshots, devices for Flatpak/sandboxes.
- **MIME defaults:** `xdg-open` / `xdg-mime` choose handlers.


- **Core:** XDG (via freedesktop.org) defines shared desktop conventions: **Base Director…

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

## Mistakes to Avoid
- **Mistake:** Hard-coding `~/.config` without respecting `$XDG_CONFIG_HOME`
- **Mistake:** Forgetting `update-desktop-database` after adding `.desktop` fil…
- **Mistake:** Expecting portals to work identically across every compositor

## Pros/Cons or Trade-offs
- **Pro:** Cross-DE consistency; cleaner home directories.
- **Con:** Not every app honors XDG; some still write `~/.<app>`.
- **Trade-off:** Portals improve security at the cost of extra prompts and integration bugs.

## Comparison
- vs dumping config in `$HOME`: XDG is the modern convention. vs GNOME-only gse…


### Use cases
- Shipping a custom launcher for an internal tool, fixing “Open with…” defaults…
