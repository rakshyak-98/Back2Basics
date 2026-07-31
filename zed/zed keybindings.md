[[zed config]] [[Descriptive/vscode]]

# Zed keybindings

## Completions & inline ghost text

| Action | Linux / Windows | macOS |
|--------|-----------------|-------|
| Accept edit prediction (ghost text) | `tab` (no menu) · `alt-l` · `alt-tab` | `tab` · `alt-tab` |
| Accept next word of prediction | `alt-k` | `ctrl-cmd-right` |
| Accept next line of prediction | `alt-j` | `ctrl-cmd-down` |
| Show / cycle edit prediction | `alt-\` · `alt-tab` / `alt-shift-tab` | `alt-tab` / `alt-shift-tab` |
| Toggle edit predictions (buffer) | `ctrl-shift-e` | `ctrl-cmd-e` |
| LSP completion menu | `ctrl-space` | `ctrl-space` |
| Accept LSP menu item | `tab tab` | `tab tab` |
| Dismiss menu / prediction | `escape` | `escape` |

When the LSP popup and a ghost prediction conflict, **hold `alt`** to preview inline and hide the menu. See [[zed config#Inline ghost completions (VS Code Copilot-style)]].

## Key bindings
```text
] c next change
[ c previous change 

g ] next problem
g [ previous problem
```

### GO to
| Command                                  | Default Shortcut |
| ---------------------------------------- | ---------------- |
| Go to definition                         | `g d`            |
| Go to declaration                        | `g D`            |
| Go to type definition                    | `g y`            |
| Go to implementation                     | `g I`            |
| Rename (change definition)               | `c d`            |
| Go to All references to the current word | `g A`            |
| Find symbol in current file              | `g s`            |
| Find symbol in entire project            | `g S`            |
| Go to next diagnostic                    | `g ]` or `] d`   |
| Go to previous diagnostic                | `g [` or `[ d`   |
| Show inline error (hover)                | `g h`            |
| Open the code actions menu               | `g .`            |