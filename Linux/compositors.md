[[Linux]] [[wayland]] [[x11]] [[Linux window manager]]

# compositors

> A compositor builds the final screen image — vsync, transparency, screenshots — either as an X helper or as the Wayland display server itself.

---

## Mental model

**Say it in one breath:** on X, compositors (Picom/Compton) sit atop the WM; on Wayland, the compositor *is* the display server.

```txt
X11:    apps → WM → (picom) → Xorg → DRM
Wayland: apps → sway/mutter/kwin → DRM
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **compositing** | Off-screen assemble + flip | “Stops tearing; costs GPU.” |
| **Picom** | Popular X compositor | “Add effects without changing WM.” |
| **Mutter/KWin/Sway** | Wayland compositors | “Own input + output.” |
| **VSync** | Sync to refresh | “Prevents screen tear.” |
| **direct scanout** | Bypass compose when possible | “Saves power/latency for fullscreen.” |

---

## Standard config / commands

```bash
# X11 helper
picom --vsync --backend glx &
# Wayland: choose session (Sway/GNOME/KDE) — no separate picom

journalctl --user -u plasma-kwin_wayland -b   # example
echo $XDG_SESSION_TYPE
```

| Knob | Why it matters |
|------|----------------|
| Backend (glx/xrender) | Performance vs compatibility |
| Unredirect fullscreen | Latency for games |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Tearing on X | Compositor running? | Start picom with vsync |
| Laggy UI | Heavy effects | Disable blur/shadows |
| Screenshare black | Portal/compositor | Install xdg-desktop-portal + backend |
| Games stutter | Compose forced | Enable unredirect / fullscreen direct |

---

## Gotchas

> [!WARNING]
> **Two compositors at once on X** — DE already compositing + picom = flicker/fights.

> [!WARNING]
> **NVIDIA + X compositing** historically flaky — prefer vendor-tested setups or Wayland.

---

## When NOT to use

- **Latency-critical X games** sometimes disable compositing intentionally.
- **SSH/no display** — irrelevant.

---

## Related

[[wayland]] [[x11]] [[Linux window manager]] [[display server]]
