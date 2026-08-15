[[Linux terminal]] [[Find command]] [[bash script]] [[grep]] [[CLI]]

# fzf

> fzf is an interactive fuzzy filter — pipe candidate lines in, type to narrow, pick one out for the next command.

## Interview Relevance
Shows shell productivity tooling: Ctrl+R history, piping `ps`/`git`/`find` into fzf, and why non-interactive CI cannot use it.

## Sources
- [junegunn/fzf](https://github.com/junegunn/fzf) — deep-dive
- [fzf(1)](https://manpages.debian.org/fzf) — overview

## Core Definition
`fzf` reads stdin (or shell hooks), scores lines against a typed fuzzy pattern, and shows a TUI. It is a **filter**, not a search engine — you supply candidates, then use the selection via `$()` or key bindings.

## Key Concepts
- **Pipe in, pick out:** `cmd | fzf` → selected line.
- **Shell integration:** Ctrl+R history, Ctrl+T paths, Alt+C directories.
- **Preview:** `--preview` side pane before open/kill.
- **Multi-select:** `-m` with Tab.
- **Exit codes:** Cancel/no match must be handled in scripts.

## Technical Details

```bash
ls | fzf
find . -type f | fzf
vim "$(find . -type f | fzf)"
ps aux | fzf | awk '{print $2}' | xargs kill
git branch | fzf | xargs git checkout

fzf --preview 'cat {}' --preview-window=right:50%
fzf -m
fd . | fzf

export FZF_DEFAULT_COMMAND='fd --type f'
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'

cd "$(find . -type d | fzf)"
grep '^Host ' ~/.ssh/config | awk '{print $2}' | fzf | xargs -I{} ssh {}
```

Install hooks from distro examples (e.g. `/usr/share/doc/fzf/examples/key-bindings.bash`).

| Symptom | Check | Fix |
|---------|-------|-----|
| command not found | Not installed | `apt`/`brew install fzf` |
| Ctrl+R still bash default | Hooks not sourced | Source key-bindings in `.bashrc` |
| Empty list | Upstream pipe empty | Test pipe alone |
| Slow on huge trees | `find /` | Scope; use `fd`; set `FZF_DEFAULT_COMMAND` |
| xargs wrong | Spaces / blank | Quote `"$(fzf)"`; `xargs -r -I{}` |

## Real-World Applications
Fuzzy checkout of git branches, picking a journal unit to follow, and killing the right process without memorizing PIDs.

## Pros/Cons or Trade-offs
- **Pro:** Huge speed-up for interactive ops.
- **Con:** Needs a TTY; dangerous when piped into `rm`/`kill` without preview.
- **Trade-off:** Interactive browsing vs explicit args in automation.

## Comparison
vs plain Ctrl+R: fzf ranks fuzzy matches across full history. vs [[Find command]]/[[grep]]: those generate candidates; fzf selects among them.

## Mistakes to Avoid
- `fzf | xargs rm` without confirmation/`-r`.
- Unquoted `"$(fzf)"` with paths containing spaces.
- Using fzf in non-interactive CI scripts.
