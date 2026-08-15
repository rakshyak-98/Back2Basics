[[Linux configuration]] [[Linux terminal]] [[terminal config]] [[wayland]] [[x11]]

# Font commands (fontconfig)

> fontconfig CLI tools list, match, and rebuild fonts when apps show missing glyphs or wrong faces.

## Interview Relevance
Desktop/ops niche: `fc-list` / `fc-match` / `fc-cache`, user vs system font dirs, and Flatpak sandbox font isolation.

## Sources
- [fontconfig documentation](https://www.freedesktop.org/software/fontconfig/fontconfig-user.html) — deep-dive
- [fc-cache(1)](https://man.archlinux.org/man/fc-cache.1) — overview

## Core Definition
Linux apps ask **fontconfig** (`fc-*`) for a font matching family + weight + size. Files live under `/usr/share/fonts`, `~/.local/share/fonts`, etc. After adding fonts, rebuild the cache or apps keep stale metadata.

## Key Concepts
- **fc-list:** Inventory family, style, file path.
- **fc-match:** What fontconfig would pick for a query.
- **fc-cache:** Rebuild caches after install/remove.
- **User vs system dirs:** `~/.local/share/fonts` needs no root.
- **Sandbox gap:** Snap/Flatpak may not see host fonts.

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

## Real-World Applications
Installing a Nerd Font for terminal icons, fixing missing glyphs after a fresh laptop setup, and debugging Flatpak apps that ignore host fonts.

## Pros/Cons or Trade-offs
- **Pro:** One matching layer for GTK/Qt/many apps.
- **Con:** Terminals and sandboxed apps may bypass or isolate it.
- **Trade-off:** `fc-cache -f` on NFS homes can be slow.

## Comparison
vs setting a terminal profile font: profile is app-local; fontconfig is system matching. vs Windows/macOS font stacks: different APIs entirely. Related: [[Linux terminal]], [[wayland]].

## Mistakes to Avoid
- Expecting host fonts inside Flatpak without overrides.
- Clearing `~/.cache/fontconfig` as a routine “fix” on large homes.
- Assuming `fc-match` output looks identical under X11 vs Wayland renderers.
