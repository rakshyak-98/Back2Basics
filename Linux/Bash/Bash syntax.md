[[Bash]] [[bash script]] [[bash flags]] [[Bash history]] [[Bash functions]] [[Scripting]]

# Bash syntax

> Bash syntax is how the shell parses words, expansions, and control operators — so pipelines and scripts do what you meant.

```txt
        Bash syntax ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Quoting, `[[ ]]`, parameter expansion, `&&`/`||`, and process substitution

## Sources
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) — deep-dive
- [Bash FAQ — quoting](https://mywiki.wooledge.org/Quotes) — deep-dive

## Key Concepts
- **Quoting:** `'literal'` vs `"expand but no split"` vs bare (split+glob).
- **`[[ ]]` vs `[ ]`:** Prefer `[[` in bash for safer tests.
- **Parameter expansion:** `${var:-default}`, `${var:0:3}`, suffix strip.
- **Process substitution:** `<(cmd)` as a pseudo-file.
- **End of options:** `--` before filenames starting with `-`.


- **Core:** The shell tokenizes a line, performs expansions (`$VAR`, `$(…)`, globs), appl…

## Technical Details
```bash
mkdir -p new_dir && cd new_dir
cmd1 || echo "failed"
(cd /tmp && ls)                 # cwd restored after

touch -- -file.txt
rm -- -file.txt

diff <(ls dir1) <(ls dir2)

echo "${my_var:-default}"
echo "${my_var:0:3}"

!!
!-2

set -euo pipefail
```

| Pitfall | What happens | Fix |
|---------|--------------|-----|
| `$var` unquoted | Split/glob | `"$var"` |
| `[ $a = $b ]` | Breaks on spaces | `[[ "$a" == "$b" ]]` |
| `cd dir && rm -rf *` | Wrong dir risk | Check; use absolute paths |
| Globs with no match | Literal `*` (nullglob off) | `shopt -s nullglob` or test |

## Mistakes to Avoid
- **Mistake:** Unquoted variables around `rm`, paths, and tests
- **Mistake:** Mixing up `=` inside `[` with `==` habits from other languages w…
- **Mistake:** Relying on history expansion (`!!`) inside scripts

## Pros/Cons or Trade-offs
- **Pro:** Extremely expressive for glue code.
- **Con:** Subtle expansion rules; easy to footgun.
- **Trade-off:** Clever one-liners vs readable quoted scripts.

## Comparison
- vs POSIX `sh`: bash has `[[`, arrays, process substitution


### Use cases
- Safe deploy scripts with quoted paths, comparing two directory listings via p…
