[[Linux configuration]] [[Linux terminal]] [[terminal config]] [[wayland]] [[x11]]

# Font commands (fontconfig)

> fontconfig CLI tools list, match, and rebuild fonts when apps show missing glyphs or wrong faces.

```txt
        Font commands (fon ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Desktop/ops niche: `fc-list` / `fc-match` / `fc-cache`, user vs system font d…

## Sources
- [fontconfig documentation](https://www.freedesktop.org/software/fontconfig/fontconfig-user.html) — deep-dive
- [fc-cache(1)](https://man.archlinux.org/man/fc-cache.1) — overview

## Key Concepts
- **fc-list:** Inventory family, style, file path.
- **fc-match:** What fontconfig would pick for a query.
- **fc-cache:** Rebuild caches after install/remove.
- **User vs system dirs:** `~/.local/share/fonts` needs no root.
- **Sandbox gap:** Snap/Flatpak may not see host fonts.


- **Core:** Linux apps ask **fontconfig** (`fc-*`) for a font matching family + weight + …

## Technical Details
```txt
App → fontconfig → fc-match "Monospace" → best file on disk
Install .ttf → fc-cache -f → app restart (sometimes)
```

```bash
fc-match monospace
fc-match "JetBrains Mono:style=Bold"

fc-list | grep -i "jetbrains"
fc-list : family style file | column -t -s,

mkdir -p ~/.local/share/fonts
cp MyFont.ttf ~/.local/share/fonts/
fc-cache -fv ~/.local/share/fonts

sudo cp MyFont.ttf /usr/local/share/fonts/
sudo fc-cache -fv
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Tofu □□□ after install | `fc-list \| grep -i name` | Wrong path; `fc-cache -fv` |
| App ≠ terminal font | `fc-match` in both contexts | Sandbox font dirs; terminal profile |
| Bold/italic wrong | `fc-match "Family:style=Bold"` | Install bold face file |
| Emoji wrong | `fc-match emoji` | Install Noto Color Emoji; fix fallbacks |

## Mistakes to Avoid
- **Mistake:** Expecting host fonts inside Flatpak without overrides
- **Mistake:** Clearing `~/.cache/fontconfig` as a routine “fix” on large homes
- **Mistake:** Assuming `fc-match` output looks identical under X11 vs Wayland …

## Pros/Cons or Trade-offs
- **Pro:** One matching layer for GTK/Qt/many apps.
- **Con:** Terminals and sandboxed apps may bypass or isolate it.
- **Trade-off:** `fc-cache -f` on NFS homes can be slow.

## Comparison
- vs setting a terminal profile font: profile is app-local


### Use cases
- Installing a Nerd Font for terminal icons, fixing missing glyphs after a fres…
