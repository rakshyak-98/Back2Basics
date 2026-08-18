[[Linux]] [[gsetting]] [[X Desktop Group]]

# gnome Colorschem

> GNOME color scheme is the light/dark preference — `org.gnome.desktop.interface color-scheme` plus GTK/app theme keys.

## Mental model

**Say it in one breath:** set `color-scheme` to `prefer-dark`/`prefer-light`/`default`; apps that honor Settings portal follow.

```txt
gsettings set … color-scheme 'prefer-dark'
        │
        └─ GTK/libadwaita / portals → app chrome
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **color-scheme** | prefer-dark/light | “The modern GNOME switch.” |
| --- | --- | --- |
| **gtk-theme** | Legacy theme name | “Still matters for older apps.” |
| **libadwaita** | Modern GNOME toolkit | “Follows color-scheme.” |
| **portal** | Sandboxed settings API | “Flatpak apps ask the portal.” |
| **accent-color** | Highlight hue | “Separate from light/dark.” |

## Standard config / commands

```bash
gsettings get org.gnome.desktop.interface color-scheme
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings set org.gnome.desktop.interface color-scheme 'prefer-light'
gsettings range org.gnome.desktop.interface color-scheme
gsettings get org.gnome.desktop.interface gtk-theme
```

| Knob | Why it matters |

| `prefer-dark` | Apps should switch without theme pack hacks |
| --- | --- |
| gtk-theme | Older apps ignore color-scheme |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| App stays light | Toolkit age / flatpak | Update app; check portal perms |
| Reverts on login | Managed dconf | Fleet profile overrides |
| Only some apps change | Mixed GTK/Qt | Set Qt theme separately |
| gsettings no schema | Headless | Needs GNOME schemas package |

## Gotchas

> [!WARNING]
> **`gtk-theme='Adwaita-dark'`** is legacy; prefer `color-scheme` on modern GNOME.

> [!WARNING]
> **Terminal themes** are separate from GNOME color-scheme.

## When NOT to use

- **Non-GNOME desktops** — use that DE’s theme system.
- **Servers** — no-op.

## Related

[[gsetting]] [[X Desktop Group]] [[terminal configuration]]
