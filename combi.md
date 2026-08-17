[[Linux/commands/fzf]] [[Linux/CLI]] [[Linux/Linux window manager]] [[Linux]]

# combi

> Rofi **combi** mode — one fuzzy launcher that merges window switcher, app menu, and run dialog.

```txt
        combi ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Rare as a formal review topic

## Sources
- [Rofi documentation](https://github.com/davatorium/rofi) — deep-dive
- [man rofi](https://man.archlinux.org/man/rofi.1) — overview

## Key Concepts
- **Modes:** `window` (open windows), `drun` (`.desktop` apps), `run` (PATH binaries).
- **Fuzzy filter:** Type to rank across combined results.
- **Config:** CLI flags or `~/.config/rofi/config.rasi`.
- **Compositor/WM fit:** Common with i3/sway/other tiling WMs ([[Linux/Linux window manager]]).


- **Core:** Rofi is a dmenu-style application launcher/switcher

## Technical Details
```bash
rofi -show combi -combi-modes "window,drun,run"
# or set in config.rasi:
# modi: "combi"
# combi-modes: "window,drun,run"
```

- Bind to a hotkey in the window manager.
- Theme via `configuration { … }` / `@theme` in the rasi file.

## Mistakes to Avoid
- **Mistake:** Expecting combi on headless servers — it is a desktop launcher
- **Mistake:** Enabling every mode until results are unusable
- **Mistake:** Forgetting `.desktop` files when `drun` finds nothing

## Pros/Cons or Trade-offs
- **Pro:** One habit for switch + launch; keyboard-driven speed.
- **Con:** Mode noise if too many sources enabled; desktop-specific (not a server tool).

## Comparison
- vs [[Linux/commands/fzf]]: fzf is a generic fuzzy filter for pipes


### Use cases
- Muscle-memory desktop: Alt+Space opens combi → type `term` or window title → …
