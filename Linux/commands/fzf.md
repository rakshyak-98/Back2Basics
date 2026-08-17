[[Linux terminal]] [[Find command]] [[bash script]] [[grep]] [[NodeJS CLI]]

# fzf

> fzf is an interactive fuzzy filter — pipe candidate lines in, type to narrow, pick one out for the next command.

```txt
        fzf ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows shell productivity tooling: Ctrl+R history, piping `ps`/`git`/`find` in…

## Sources
- [junegunn/fzf](https://github.com/junegunn/fzf) — deep-dive
- [fzf(1)](https://manpages.debian.org/fzf) — overview

## Key Concepts
- **Pipe in, pick out:** `cmd | fzf` → selected line.
- **Shell integration:** Ctrl+R history, Ctrl+T paths, Alt+C directories.
- **Preview:** `--preview` side pane before open/kill.
- **Multi-select:** `-m` with Tab.
- **Exit codes:** Cancel/no match must be handled in scripts.


- **Core:** `fzf` reads stdin (or shell hooks), scores lines against a typed fuzzy patter…

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

- Install hooks from distro examples (e.g.
- `/usr/share/doc/fzf/examples/key-bindings.bash`).

| Symptom | Check | Fix |
|---------|-------|-----|
| command not found | Not installed | `apt`/`brew install fzf` |
| Ctrl+R still bash default | Hooks not sourced | Source key-bindings in `.bashrc` |
| Empty list | Upstream pipe empty | Test pipe alone |
| Slow on huge trees | `find /` | Scope; use `fd`; set `FZF_DEFAULT_COMMAND` |
| xargs wrong | Spaces / blank | Quote `"$(fzf)"`; `xargs -r -I{}` |

## Mistakes to Avoid
- **Mistake:** `fzf | xargs rm` without confirmation/`-r`
- **Mistake:** Unquoted `"$(fzf)"` with paths containing spaces
- **Mistake:** Using fzf in non-interactive CI scripts

## Pros/Cons or Trade-offs
- **Pro:** Huge speed-up for interactive ops.
- **Con:** Needs a TTY; dangerous when piped into `rm`/`kill` without preview.
- **Trade-off:** Interactive browsing vs explicit args in automation.

## Comparison
- vs plain Ctrl+R: fzf ranks fuzzy matches across full history. vs [[Find comma…


### Use cases
- Fuzzy checkout of git branches, picking a journal unit to follow, and killing…
