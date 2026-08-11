[[Linux]] [[terminal emulator]] [[Bash syntax]]

# terminal config

> Terminal config is how the emulator and shell look/behave — fonts, colors, scrollback, keybindings, and shell rc files.

---

## Mental model

**Say it in one breath:** emulator owns UI chrome; shell owns prompt/aliases; keep them in dotfiles you can reinstall.

```txt
~/.config/<emulator>/  → font, theme, keys
~/.bashrc / ~/.zshrc   → prompt, aliases, PATH
terminfo / $TERM       → capability negotiation
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **dotfiles** | Tracked config | “Symlink from a git repo.” |
| **profile vs rc** | Login vs interactive | “Know which file your DE sources.” |
| **color scheme** | Palette | “Emulator theme ≠ LS_COLORS alone.” |
| **keybinding** | Chord → action | “Conflict with tmux/WM mods.” |
| **scrollback** | Buffer size | “Big buffers cost RAM.” |

---

## Standard config / commands

```bash
# examples
ls ~/.config/kitty ~/.config/alacritty ~/.config/ghostty 2>/dev/null
echo $SHELL
# reload shell config
source ~/.bashrc
# terminfo check
infocmp "$TERM" >/dev/null && echo ok
```

| Knob | Why it matters |
|------|----------------|
| Font size / DPI | HiDPI readability |
| Cursor / bell | Noise vs focus |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Config ignored | Wrong path / format | Validate YAML/TOML; correct XDG path |
| Theme ugly in SSH | Remote `$TERM` | Install terminfo or simplify TERM |
| Keys clash with WM | Mod overlap | Remap emulator or WM |
| Slow startup | Heavy rc | Profile `zsh -x` / bash timing |

---

## Gotchas

> [!WARNING]
> **Editing production servers’ prompts** with fancy git scripts can slow every command — keep server rc lean.

> [!WARNING]
> **Copying macOS `$TERM` to Linux** without terminfo breaks ncurses.

---

## When NOT to use

- **Ephemeral containers** — bake need-to-haves; skip personal themes.
- **Non-interactive automation** — no prompt config required.

---

## Related

[[terminal emulator]] [[Linux terminal]] [[Bash history]] [[editor config]]
