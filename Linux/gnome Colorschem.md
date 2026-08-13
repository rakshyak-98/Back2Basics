[[commands/gsetting]] [[terminal config]] [[Linux configuration]]

# gnome Colorschem

> GNOME color schemes and accent colors are stored in GSettings — `gsettings` and `dconf` change GTK theme and dark/light preference for the desktop session.

## Read settings

```bash
gsettings get org.gnome.desktop.interface color-scheme
gsettings get org.gnome.desktop.interface gtk-theme
gsettings range org.gnome.desktop.interface color-scheme
```

Values (GNOME 42+): `'default'`, `'prefer-dark'`, `'prefer-light'`.

## Set dark mode

```bash
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
```

## Terminal profile

GNOME Terminal profiles are separate schemas — use GUI or `dconf dump /org/gnome/terminal/`.

## Related

[[commands/gsetting]] · [[commands/customization]] · [[terminal config]]

## Sources

- [GNOME Human Interface Guidelines — appearance](https://developer.gnome.org/hig/)
- `man 1 gsettings`
