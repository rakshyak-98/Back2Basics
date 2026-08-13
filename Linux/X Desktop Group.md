[[display server]] [[Linux configuration]] [[wayland]]

# X Desktop Group

> The X Desktop Group (XDG) publishes freedesktop.org standards — base directory spec, `.desktop` files, icons, and portals that unify GNOME, KDE, and other desktops.

Key specs: **XDG Base Directory** (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`), **Desktop Entry** (`.desktop` launchers), **Icon Theme**, **MIME apps**, **xdg-desktop-portal** for sandboxed apps on Wayland.

## Base directories

```bash
echo $XDG_CONFIG_HOME    # default ~/.config
echo $XDG_DATA_HOME      # default ~/.local/share
echo $XDG_CACHE_HOME
```

## Desktop entry example

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
xdg-open file.pdf    # MIME default handler
update-desktop-database ~/.local/share/applications
```

## Related

[[Linux display manager]] · [[Linux configuration]] · [[wayland]]

## Sources

- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html)
