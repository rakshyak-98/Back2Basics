- Switch between Emac-style and Vmi-style keybinding in the terminal.
- By default Bash uses Emacs-style keys.
- (Optional) Make it permanent by adding to `~/.bashrc` or `~/.bash_profile`.

```bash
set -o vi;
set -o emacs;
```

- Toggle between emac and vim

```bash
# Press Ctrl+Z to toggle between vi and emacs mode
bind '"\C-z": vi-editing-mode'    # in emacs mode → switch to vi
bind -m vi-insert '"\C-z": emacs-editing-mode'  # in vi insert mode → switch to emacs
```
