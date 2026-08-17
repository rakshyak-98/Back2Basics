[[nvim setup]] [[Linux/CLI]] [[Descriptive/LSP]]

# Neovim commands

> Everyday operator vocabulary — modes, motions, and ex commands that make Neovim faster than arrow-key editing.

```txt
        Neovim commands ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Rarely a deep interview topic, but pairing/onsite screens reward fluent navig…

## Sources
- [Neovim help — quickref](https://neovim.io/doc/user/quickref.html) — deep-dive
- [Vim — Modes](https://vimhelp.org/) — overview

## Key Concepts
- **Modes:** normal, insert, visual, command-line.
- **Motions + operators:** `d`, `c`, `y` combined with motions.
- **Leader maps:** custom shortcuts from config.
- **`:commands`:** ex mode for write/quit/search/replace.

## Technical Details
```text
i/a     insert
Esc     normal
:w :q   write/quit
/pattern  search
:%s/old/new/g  replace
Ctrl-o / Ctrl-i  jump list
```

| Task | Keys |
|------|------|
| Delete line | `dd` |
| Yank word | `yiw` |
| Go to definition | LSP mapping (config-dependent) |

- `prepend` in path settings adds directories to the front of `runtimepath`/`pa…

## Mistakes to Avoid
- **Mistake:** Staying in insert mode for navigation
- **Mistake:** Blindly pasting from web without checking registers
- **Mistake:** Heavy mouse reliance that fights the modal model

## Pros/Cons or Trade-offs
- **Pro:** Fast once internalized; available almost everywhere.
- **Con:** Learning curve; modal editing surprises newcomers.

## Comparison
- vs VS Code/Zed: modal editing vs modeless; LSP exists in both worlds.
- vs [[nvim setup]]: commands are usage; setup is configuration.


### Use cases
- Edit remote configs over SSH with muscle memory that works on any host with n…

- **Example:** Fix a typo across a file with `:%s/foo/bar/g` instead of manual …
