<!-- note-strategy: operational -->
[[commands]] [[x11]] [[wayland]]

# xrandr

> xrandr configures X11 outputs — resolution, rotation, and multi-monitor layout via RandR.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** list connected outputs, set mode, place monitors with `--left-of` / `--above`.

```txt
xrandr
  ├─ eDP-1 connected 1920x1080
  └─ HDMI-1 connected 2560x1440
       --mode + --right-of eDP-1
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **output** | eDP/HDMI/DP name | “Names come from the driver.” |
| **mode** | Resolution + refresh | “`--mode 1920x1080`.” |
| **primary** | Main monitor | “Where panels/menus prefer to go.” |
| **panning / scale** | HiDPI tricks | “Scale can blur; prefer native mode.” |
| **Wayland** | Different tools | “xrandr won’t drive pure Wayland.” |

---

## Standard config / commands

```bash
xrandr
xrandr --output HDMI-1 --mode 2560x1440 --right-of eDP-1
xrandr --output HDMI-1 --off
xrandr --output eDP-1 --primary
# add mode (when EDID lies)
cvt 1920 1080 60
xrandr --newmode "1920x1080_60.00" ...
xrandr --addmode HDMI-1 "1920x1080_60.00"
```

| Knob | Why it matters |
|------|----------------|
| `--auto` | Enable preferred mode |
| `--same-as` | Mirror displays |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank external | Cable/`xrandr` connected | `--auto`; try other port |
| Wrong resolution | Missing mode | `cvt` + `--newmode` / fix EDID |
| Layout resets | Session start | Save script; DM/autorandr |
| “Can’t open display” | `$DISPLAY` | Export `:0` / use local session |
| No effect on Wayland | Compositor owns layout | Use `wlr-randr` / GNOME settings |

---

## Gotchas

> [!WARNING]
> **Wayland sessions** — xrandr may show Xwayland only; it won’t rearrange native Wayland outputs.

> [!WARNING]
> **`--scale`** as HiDPI fix often blurs; prefer native modes + fractional scaling in the compositor.

---

## When NOT to use

- **Pure Wayland desktops** — compositor tools instead.
- **Headless servers** — no display; don’t install X just for xrandr.

---

## Related

[[x11]] [[wayland]] [[compositors]] [[gsetting]]
