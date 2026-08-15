[[Linux/commands/fzf]] [[Linux/CLI]] [[Linux/Linux window manager]] [[Linux]]

# combi

> Rofi **combi** mode — one fuzzy launcher that merges window switcher, app menu, and run dialog.

## Interview Relevance
Rare as a formal interview topic; useful systems/desktop literacy when discussing Linux tooling, UX for power users, and composing small Unix tools ([[Linux/commands/fzf]] kinship).

## Sources
- [Rofi documentation](https://github.com/davatorium/rofi) — deep-dive
- [man rofi](https://man.archlinux.org/man/rofi.1) — overview

## Core Definition
Rofi is a dmenu-style application launcher/switcher. **combi** aggregates multiple modes (commonly `window`, `drun`, `run`) into a single ranked list so one keybind covers “switch or launch.”

## Key Concepts
- **Modes:** `window` (open windows), `drun` (`.desktop` apps), `run` (PATH binaries).
- **Fuzzy filter:** Type to rank across combined results.
- **Config:** CLI flags or `~/.config/rofi/config.rasi`.
- **Compositor/WM fit:** Common with i3/sway/other tiling WMs ([[Linux/Linux window manager]]).

## Technical Details
```bash
rofi -show combi -combi-modes "window,drun,run"
# or set in config.rasi:
# modi: "combi"
# combi-modes: "window,drun,run"
```

Bind to a hotkey in the window manager. Theme via `configuration { … }` / `@theme` in the rasi file.

## Real-World Applications
Muscle-memory desktop: Alt+Space opens combi → type `term` or window title → Enter. Same idea as Spotlight/PowerToys, but scriptable on Linux.

## Pros/Cons or Trade-offs
- **Pro:** One habit for switch + launch; keyboard-driven speed.
- **Con:** Mode noise if too many sources enabled; desktop-specific (not a server tool).

## Comparison
vs [[Linux/commands/fzf]]: fzf is a generic fuzzy filter for pipes; rofi combi is a GUI/launcher front-end for desktop actions. vs separate `rofi -show window` binds: combi reduces keybind sprawl.

## Mistakes to Avoid
- Expecting combi on headless servers — it is a desktop launcher.
- Enabling every mode until results are unusable.
- Forgetting `.desktop` files when `drun` finds nothing.
