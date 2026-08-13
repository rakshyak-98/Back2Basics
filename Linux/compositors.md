[[display server]] [[wayland]] [[x11]] [[Linux window manager]] [[compositors]]

# compositors

> A compositor composites window buffers into the final screen image — required for transparency, animations, and many modern desktop effects.

On **Wayland**, the compositor *is* the display server: clients submit buffers; the compositor handles input routing and presentation. On **X11**, a separate **compositing manager** (often embedded in the window manager) redirects window painting through an off-screen buffer before the X server shows the frame.

## X11 vs Wayland compositing

| Model | Who composites | Examples |
|-------|----------------|----------|
| X11 + compositor | Optional compositing manager on top of X server | Picom, Mutter (GNOME), KWin effects |
| Wayland | Built into compositor | Mutter, KWin, Sway, Hyprland |

```
Wayland clients ──► compositor ──► kernel DRM/KMS ──► monitor
X11 clients ──► X server ◄── compositor (redirects) ──► monitor
```

## Picom (standalone X11 compositor)

```bash
# Install (Debian/Ubuntu)
sudo apt install picom

# Test config
picom --config ~/.config/picom/picom.conf -b

# Disable vsync for latency testing
picom --vsync=false
```

Common `picom.conf` knobs: `backend` (`glx` vs `xrender`), `vsync`, `shadow`, `fade-delta`, `inactive-opacity`.

## When compositing breaks

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Tearing without compositor | Direct X rendering | Enable compositor or use `picom` |
| Flicker / black windows | Wrong GL backend | Switch `backend` glx ↔ xrender |
| High GPU use on old hardware | Full-screen unredirect | `unredir-if-possible = false` in picom |
| Wayland app blurry on XWayland | Fractional scaling | Set integer scale or check compositor rules |

## Related

[[display server]] · [[wayland]] · [[x11]] · [[Linux window manager]] · [[i3 Window Manager Starter Guide]]

## Sources

- [Wayland compositor (Wikipedia)](https://en.wikipedia.org/wiki/Wayland_(protocol)#Compositor)
- Picom wiki: https://github.com/yshui/picom/wiki
