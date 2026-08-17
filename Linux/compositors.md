[[display server]] [[wayland]] [[x11]] [[Linux window manager]] [[i3 Window Manager Starter Guide]]

# compositors

> A compositor composites window buffers into the final screen image — required for transparency, animations, and many modern desktop effects.

```txt
        compositors ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Separates people who treat “Wayland compositor” as a buzzword from those who …

## Sources
- [Wayland protocol — compositor role](https://wayland.freedesktop.org/) — overview
- [Picom wiki](https://github.com/yshui/picom/wiki) — deep-dive
- [Wayland (Wikipedia) — Compositor](https://en.wikipedia.org/wiki/Wayland_(protocol)#Compositor) — overview

## Key Concepts
- **Buffer → screen:** Windows are surfaces
- **Wayland unity:** Display server + compositor + often WM in one process (Mutter, Sway, KWin).
- **X11 optional compositor:** Picom or DE-integrated effects on top of `Xorg`.
- **vsync / tearing:** Compositor timing vs bare X rendering trade latency for smoothness.
- **XWayland:** X clients on Wayland still go through the compositor’s X compatibility path.


- **Core:** Clients submit pixel buffers

## Technical Details
| Model | Who composites | Examples |
|-------|----------------|----------|
| X11 + compositor | Optional compositing manager on top of X server | Picom, Mutter (GNOME), KWin effects |
| Wayland | Built into compositor | Mutter, KWin, Sway, Hyprland |

```
Wayland clients ──► compositor ──► kernel DRM/KMS ──► monitor
X11 clients ──► X server ◄── compositor (redirects) ──► monitor
```

```bash
sudo apt install picom
picom --config ~/.config/picom/picom.conf -b
picom --vsync=false
```

- Common `picom.conf` knobs: `backend` (`glx` vs `xrender`), `vsync`, `shadow`,…

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Tearing without compositor | Direct X rendering | Enable compositor or use `picom` |
| Flicker / black windows | Wrong GL backend | Switch `backend` glx ↔ xrender |
| High GPU use on old hardware | Full-screen unredirect | `unredir-if-possible = false` in picom |
| Wayland app blurry on XWayland | Fractional scaling | Integer scale or compositor rules |

## Mistakes to Avoid
- **Mistake:** Running Picom on a pure Wayland session where the compositor alr…
- **Mistake:** Blaming the GPU driver for tearing when no compositor is running…
- **Mistake:** Leaving fractional scaling on without checking XWayland blur

## Pros/Cons or Trade-offs
- **Pro:** Effects, tear-free presentation, consistent scaling policy.
- **Con:** Extra GPU work; misconfigured backends cause flicker or high idle usage on old hardware.

## Comparison
- vs [[display server]]: compositor may *be* the display server (Wayland) or si…


### Use cases
- An i3 user enables Picom for transparency and tear-free video; a GNOME Waylan…
