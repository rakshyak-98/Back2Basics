[[Linux configuration]] [[Linux terminal]] [[terminal configuration]]

# Font commands (fontconfig)

> fontconfig CLI — list, match, and rebuild fonts when apps show missing glyphs.

---

## Index

- [[#Quick reference]]
- [[#Standard config / commands]]
- [[#Options / flags]]
- [[#Mental model]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Examples]]
- [[#Related]]

## Quick reference

| Task | Command |
|------|---------|
| … | `…` |

## Standard config / commands

```bash
# What monospace will Firefox/terminal actually get?
fc-match monospace
fc-match "JetBrains Mono:style=Bold"

# List installed faces (grep your family)
fc-list | grep -i "jetbrains"
fc-list : family style file | column -t -s,

# After installing fonts to ~/.local/share/fonts
mkdir -p ~/.local/share/fonts
cp MyFont.ttf ~/.local/share/fonts/
fc-cache -fv ~/.local/share/fonts

# System-wide install (Debian/Ubuntu)
sudo cp MyFont.ttf /usr/local/share/fonts/
sudo fc-cache -fv
```

**Terminal-specific:** many terminals bypass fontconfig partially — set font in terminal profile *and* verify with `fc-match`. Nerd Font icons need a patched face (e.g. `MesloLGS NF`), not just "Monospace".

## Options / flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

## Mental model

Linux apps ask **fontconfig** (`fc-*`) for a font matching family + weight + size. Installed files live under `/usr/share/fonts`, `~/.local/share/fonts`, etc. After adding fonts, the cache in `~/.cache/fontconfig` (and system cache) must be rebuilt or apps keep stale metadata.

```
App → fontconfig → fc-match "Monospace" → best file on disk
Install .ttf → fc-cache -f → app restart (sometimes required)
```

| Tool | Role |
|------|------|
| `fc-list` | Inventory: family, style, file path |
| `fc-match` | What fontconfig *would* use for a query |
| `fc-cache` | Rebuild caches after install/remove |
| `fc-scan` | Low-level scan of a directory (debug) |

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **fc-list** | List fonts | “fc-list : family | sort.” |
| **fc-cache** | Rebuild cache | “After install fonts → fc-cache -fv.” |
| **~/.local/share/fonts** | User fonts | “No root needed.” |
| **fc-match** | What will render | “fc-match 'DejaVu Sans'.” |
| **Pango/Qt** | App stacks | “Apps may bypass fontconfig quirks.” |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Tofu □□□ after font install | `fc-list \| grep -i name` | Font not installed; wrong path; run `fc-cache -fv` |
| App shows different font than terminal | `fc-match "Family"` in both contexts | Snap/Flatpak sandbox has isolated font dirs |
| Bold/italic wrong | `fc-match "Family:style=Bold"` | Install separate bold file; check `@font-face` in CSS apps |
| Emoji overlap / wrong width | `fc-match emoji` | Install `fonts-noto-color-emoji`; configure fallback chain |
| Works for root, not user | Compare `fc-list` as each user | User `~/.config/fontconfig/fonts.conf` override |

## Gotchas

> [!WARNING]
> **`fc-cache -f` on NFS home** — can be slow and lock; run on login node sparingly. Prefer local font dir.

> [!WARNING]
> **Flatpak/Snap** — host fonts don't always propagate. Use `flatpak override --user --filesystem=~/.local/share/fonts` or install font inside sandbox.

- **X11 versus Wayland** — font rendering differs (Xft, Cairo, subpixel). Same `fc-match` can look different; not always a fontconfig bug.
- **Clearing cache blindly** — `rm -rf ~/.cache/fontconfig` fixes corruption but forces full rebuild on next login.

## When NOT to use

- **Choosing a font for design** — use a font book or application UI; `fc-list` is for operations/debug.
- **PDF/print embedding** — fontconfig doesn't embed; that's application-specific (LibreOffice, LaTeX).
- **Windows/macOS font sync** — different stack entirely.

## Examples

```bash
# …
```

## Related

[[Linux configuration]] [[Linux terminal]] [[terminal configuration]] [[wayland]] [[x11]]
