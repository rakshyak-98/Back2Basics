[[zed config]] [[Descriptive/vscode]]

# Zed keybindings

> JSON keymaps that bind chords to editor actions — resolve conflicts when LSP popups and inline edit predictions both want the keyboard.

```txt
        Zed keybindings ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Tooling interviews care that you can customize bindings without fighting moda…

## Sources
- [Zed — Key bindings](https://zed.dev/docs/key-bindings) — deep-dive

## Key Concepts
- **User keymap:** overrides defaults; can be context-specific (editor, workspace).
- **Conflict UX:** when LSP menu and edit prediction compete, hold `alt` to preview inline and h…
- **Actions:** bindings call named Zed actions — not raw keycodes alone.

## Technical Details
```json
[
  {
    "context": "Editor",
    "bindings": {
      "ctrl-shift-p": "command_palette::Toggle"
    }
  }
]
```

| Situation | Move |
|-----------|------|
| Want ghost text, not popup | Hold `alt` / tune prediction settings |
| Chord stolen by OS | Remap in Zed or free the OS binding |

## Mistakes to Avoid
- **Mistake:** Binding chords that the window manager already owns
- **Mistake:** Copying VS Code JSON verbatim without mapping to Zed action names
- **Mistake:** Ignoring context so a binding fires in the terminal unexpectedly

## Pros/Cons or Trade-offs
- **Pro:** Context-aware JSON keymaps are portable across machines.
- **Con:** Over-customizing slows onboarding on shared machines.

## Comparison
- vs VS Code `keybindings.json`: same idea; action names differ.
- vs [[zed config]]: settings change behavior; keybindings change how you invoke it.


### Use cases
- Map familiar VS Code muscle memory (`Ctrl/Cmd-P`, comment toggles) into Zed g…

- **Example:** LSP popup covers an accepted prediction
