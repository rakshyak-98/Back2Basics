[[Vim CLI]] [[vim config]] [[Linux/CLI]]

# ed

> Line-oriented Unix text editor — edit files by address and command when you have a shell but no full-screen UI.

```txt
        ed ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers rarely quiz `ed` itself

## Sources
- [GNU ed manual](https://www.gnu.org/software/ed/manual/ed_manual.html) — deep-dive
- [Wikipedia — ed (text editor)](https://en.wikipedia.org/wiki/Ed_(text_editor)) — overview
- [POSIX ed](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/ed.html) — deep-dive

## Key Concepts
- **Address then command:** `1,$p` prints all lines
- **Current line (`.`):** most commands act on `.` unless you give a range → track where you are with `…
- **Input mode vs command mode:** `a` / `i` / `c` enter text until `.` → easy to strand yourself if you forget …
- **Vim lineage:** Vim’s `:` commands and `:g//` global are Ex/`ed` heritage → knowing ranges tr…


- **Core:** `ed` addresses lines (by number, `$`, `.`, or regex), then runs a single-lett…

## Technical Details
| Command | Meaning |
|---------|---------|
| `e file` | Edit (open) file |
| `w` / `w file` | Write / write as |
| `q` / `q!` | Quit / quit discarding |
| `1` / `$` / `.` | First / last / current line |
| `n` | Print with line numbers |
| `a` / `i` / `c` | Append after / insert before / change |
| `.` (alone) | Leave input mode |
| `p` | Print addressed lines |
| `d` | Delete |
| `s/old/new/` | Substitute on current line |
| `g/re/cmd` | Global: run `cmd` on matches |

```bash
ed myfile.txt
# 1,$p          print all
# /pattern/     go to match
# s/foo/bar/g   substitute on current line
# w
# q
```

## Mistakes to Avoid
- **Mistake:** Forgetting `.` to leave insert/append
- **Mistake:** Using `q` without `w` after edits — changes are lost
- **Mistake:** Confusing `ed` with `ex`/`vi`

## Pros/Cons or Trade-offs
- **Pro:** Tiny binary, scriptable, always available on Unix-like systems.
- **Con:** No visual context — high cognitive load; prefer [[Vim CLI]] or `sed` for day-to-day work.

## Comparison
- vs Vim Ex mode (`:`): same address/command model, but Vim keeps a buffer UI and undo.
- vs `sed`: `sed` is stream-oriented and non-interactive; `ed` is interactive and file-backed.


### Use cases
- Rescue disks, serial consoles, and minimal containers where Vim/Emacs are mis…

- **Example:** SSH into a tiny Alpine box, `ed /etc/hosts`, append a line with …
