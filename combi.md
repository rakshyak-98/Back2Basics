[[Linux/commands/fzf]] [[Linux/CLI]]

# combi (rofi mode)

> Rofi **combi** mode merges window switcher, app launcher, and run dialog into one fuzzy search — muscle memory launcher on Linux desktops.

## Mental model

Rofi is a dmenu replacement. **combi** aggregates multiple internal modes (`window`, `drun`, `run`) into a single filtered list. User types; rofi ranks matches across modes. Configured via CLI flags or `~/.config/rofi/config.rasi`.

## Standard config / commands

```bash
rofi -show combi -combi-modes "window,drun,run"
rofi -show combi -combi-modes "window,drun,run" -terminal alacritty
```

| Mode | Shows |
|------|-------|
| `window` | Open windows (Alt-Tab alternative) |
| `drun` | `.desktop` applications |
| `run` | Arbitrary shell commands |

### Keybind (i3/sway example)

```
bindsym $mod+d exec rofi -show combi -combi-modes "window,drun,run"
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty drun list | `.desktop` paths | Install `rofi` + `desktop-file-utils`; check `XDG_DATA_DIRS` |
| Wrong terminal flag | `-terminal` | Set your terminal emulator name |
| Theme broken | `config.rasi` | Validate rasi syntax |
| Slow start | Many windows | Reduce modes; disable icons |

## Related

[[Linux/commands/fzf]] [[Linux/CLI]] [[Linux/windowing system]]
