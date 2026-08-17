[[zed config]] [[Descriptive/vscode]]

# Zed keybindings

> JSON keymaps that bind chords to editor actions — resolve conflicts when LSP popups and inline edit predictions both want the keyboard.





## Interview Relevance
Tooling interviews care that you can customize bindings without fighting modal conflicts — especially Alt-to-preview when completions and ghost text collide.

## Sources
- [Zed — Key bindings](https://zed.dev/docs/key-bindings) — deep-dive

## Key Concepts
- **User keymap:** overrides defaults; can be context-specific (editor, workspace).
- **Conflict UX:** when LSP menu and edit prediction compete, hold `alt` to preview inline and hide the menu (see [[zed config]]).
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

## Real-World Applications
Map familiar VS Code muscle memory (`Ctrl/Cmd-P`, comment toggles) into Zed gradually while learning native defaults.

**Example:** LSP popup covers an accepted prediction — Alt preview clarifies which system is active.

## Pros/Cons or Trade-offs
- **Pro:** Context-aware JSON keymaps are portable across machines.
- **Con:** Over-customizing slows onboarding on shared machines.

## Comparison
- vs VS Code `keybindings.json`: same idea; action names differ.
- vs [[zed config]]: settings change behavior; keybindings change how you invoke it.

## Mistakes to Avoid
- Binding chords that the window manager already owns.
- Copying VS Code JSON verbatim without mapping to Zed action names.
- Ignoring context so a binding fires in the terminal unexpectedly.
