[[Linux]] [[wayland]] [[x11]] [[compositors]]

# Linux window manager

> A window manager (WM) places and decorates windows — tiling (i3) or stacking (Openbox) — on top of a display server.

---

## Mental model

**Say it in one breath:** display server owns pixels/input; WM decides layout; desktop environments bundle WM + panels + apps.

```txt
apps ──► WM (i3/openbox/…) ──► X11
apps ──► compositor (sway/mutter) ──► Wayland
              (WM + display server merged)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **WM** | Layout policy | “i3 tiles; floating WMs stack.” |
| **compositor** | Final frame / vsync | “Tear-free needs compositing.” |
| **DE** | Full desktop suite | “GNOME/KDE include a WM/compositor.” |
| **reparenting** | X11 WM wraps windows | “Classic X model.” |
| **tiling** | Non-overlap layout | “Keyboard-driven productivity.” |

---

## Standard config / commands

```bash
# X11 session example
exec i3
# ~/.config/i3/config → $mod+Shift+r reload

echo $XDG_CURRENT_DESKTOP
echo $XDG_SESSION_TYPE   # x11 | wayland
ps -e | grep -E 'i3|sway|mutter|kwin'
```

| Knob | Why it matters |
|------|----------------|
| Config path | Per-WM (`~/.config/i3`, sway, …) |
| Mod key | Muscle memory for all binds |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen after login | WM crashed | TTY; check `~/.xsession-errors` / journal |
| Keys do nothing | Wrong mod / grabbed | Fix config; restart WM |
| Floating apps ignore rules | WM_CLASS / app_id | `xprop` / Wayland app_id rules |
| Tear / stutter | Compositor off | Enable compositing / use Wayland |

---

## Gotchas

> [!WARNING]
> **Wayland “WMs” are compositors** — i3 doesn’t run native Wayland; use Sway.

> [!WARNING]
> **DE + DIY WM** — fighting GNOME/KDE session scripts ends in pain; pick one stack.

---

## When NOT to use

- **Servers / CI** — no GUI.
- **Kiosk with a browser only** — a DE may be heavier than a minimal compositor session.

---

## Related

[[i3 Window Manager Starter Guide]] [[wayland]] [[x11]] [[compositors]] [[Linux display manager]]
