[[commands]] [[x11]] [[wayland]] [[compositors]] [[gsetting]]

# xrandr

> Configures X11 outputs — resolution, rotation, and multi-monitor layout via RandR.

```txt
        xrandr ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Desktop/Linux graphics trivia: output names, modes, and that xrandr does not …

## Sources
- [man xrandr](https://www.x.org/releases/current/doc/man/man1/xrandr.1.xhtml) — deep-dive
- [Wikipedia — xrandr](https://en.wikipedia.org/wiki/Xrandr) — overview

## Key Concepts
- **Output:** driver names like `eDP-1`, `HDMI-1`, `DP-1`.
- **Mode:** resolution + refresh (`--mode 1920x1080`).
- **Primary:** where panels/menus prefer to go.
- **Wayland:** compositor owns layout — use `wlr-randr` / GNOME settings instead.

## Technical Details
```txt
xrandr
  ├─ eDP-1 connected 1920x1080
  └─ HDMI-1 connected 2560x1440
       --mode + --right-of eDP-1
```

```bash
xrandr
xrandr --output HDMI-1 --mode 2560x1440 --right-of eDP-1
xrandr --output HDMI-1 --off
xrandr --output eDP-1 --primary
cvt 1920 1080 60
xrandr --newmode "1920x1080_60.00" ...
xrandr --addmode HDMI-1 "1920x1080_60.00"
```

| Knob | Why it matters |
|------|----------------|
| `--auto` | Enable preferred mode |
| `--same-as` | Mirror displays |

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank external | Cable / connected line | `--auto`; try other port |
| Wrong resolution | Missing mode | `cvt` + `--newmode` / fix EDID |
| Layout resets | Session start | Script / autorandr / DM hook |
| Can’t open display | `$DISPLAY` | Export `:0` / use local session |
| No effect on Wayland | Compositor owns layout | `wlr-randr` / desktop settings |

## Mistakes to Avoid
- **Mistake:** Expecting xrandr to rearrange native Wayland outputs
- **Mistake:** Using `--scale` as a HiDPI fix instead of native modes + composi…
- **Mistake:** Installing X on headless servers just to run xrandr

## Pros/Cons or Trade-offs
- **Pro:** Scriptable X11 multi-head without a GUI.
- **Con:** Useless (or Xwayland-only) on pure Wayland; `--scale` often blurs.

## Comparison
- vs [[wayland]] tools: compositor-native randr replacements.
- vs GUI display settings: same job, less automation-friendly.


### Use cases
- Docking station layouts, projector mirrors, and fixing EDID lies with `cvt` +…
