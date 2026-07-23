[[Linux configuration]] [[vscode]] [[Scripting]]

# EditorConfig (editor config)

> One-line: **`.editorconfig` — one repo-root file so every editor agrees on indent, charset, and EOL** — stops the PR wars between "tabs vs spaces" and fixes mixed line-ending CI failures.

## Mental model

[EditorConfig](https://editorconfig.org) is a **declarative INI-style file** committed at repo root. Plugins in VS Code, IntelliJ, Vim, etc. read it on save/open. It overrides personal editor defaults **within that project** — not global IDE settings. Prettier/ESLint can still conflict if not aligned.

```
.editorconfig (root)
  ├── [*] defaults
  ├── [*.{js,ts}] JS rules
  └── [Makefile] tabs exception
Developer opens file → plugin applies nearest matching section
```

| Key | Typical value | Why |
|-----|---------------|-----|
| `root = true` | stop searching parent dirs | Monorepo boundary |
| `indent_style` | space / tab | Team consistency |
| `indent_size` | 2 / 4 | Match language norm |
| `end_of_line` | lf | Linux CI; avoid CRLF diffs |
| `charset` | utf-8 | No Latin-1 surprises |
| `trim_trailing_whitespace` | true | Clean diffs |
| `insert_final_newline` | true | POSIX text file; git diff noise |

## Standard config / commands

**Production-safe baseline for polyglot repo:**

```ini
# .editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.{md,markdown}]
trim_trailing_whitespace = false   # markdown line breaks use trailing spaces

[*.{py,rs,go}]
indent_size = 4

[Makefile]
indent_style = tab

[{*.yaml,*.yml,.github/**}]
indent_size = 2
```

**Verify plugin (VS Code / Cursor):**

- Install "EditorConfig for VS Code" (often built-in or default).
- Status bar shows indent when file matches section.

**Check file obeys (CI optional):**

```bash
# editorconfig-checker (eclint) in CI
npm install -g editorconfig-checker
editorconfig-checker

# Or eclint
gem install eclint   # legacy
eclint check *
```

**Align Prettier (avoid fighting):**

```json
// .prettierrc — match .editorconfig
{
  "endOfLine": "lf",
  "tabWidth": 2,
  "useTabs": false
}
```

**Git attributes complement (binary/EOL):**

```
# .gitattributes
* text=auto eol=lf
*.png binary
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Settings ignored | Plugin installed? | Enable EditorConfig extension; reload |
| Wrong indent in subfolder | Nested `.editorconfig` | Child `root = true` stops inherit — rare |
| CI fails EOL | `file` or `git diff --check` | Set `end_of_line = lf`; `.gitattributes` |
| Makefile broken | spaces in recipes | `[Makefile] indent_style = tab` |
| Markdown lists break | trim_trailing_whitespace | Disable for `*.md` section |
| Prettier reverts format | Conflicting rules | Sync `.prettierrc` with editorconfig |

## Gotchas

> [!WARNING]
> **EditorConfig ≠ formatter** — doesn't fix AST; only basic whitespace/charset. Run Prettier/black/gofmt separately.

> [!WARNING]
> **No plugin in editor** — file is inert. Onboarding doc must list required extensions.

- **`max_line_length`** — supported but not enforced unless editor wraps; use linter for hard limits.
- **Vim** — `editorconfig-vim` plugin; native support limited without it.
- **Generated code** — exclude with `[{dist/**,*.min.js}]` skip sections if tool supports; or don't format generated paths in CI.

## When NOT to use

- **Org-wide IDE policy only** — use enterprise settings + still add `.editorconfig` for open-source contributors.
- **Languages with strong official style enforced by formatter alone** — still keep `charset`/`eol`; optional indent keys if gofmt/rustfmt owns indent.

## Related

[[Linux configuration]] [[vscode]] [[Scripting]] [[git command]]
