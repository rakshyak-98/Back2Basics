[[vim commands]] [[vim config]] [[Linux/CLI]]

# ed

> Line-oriented Unix text editor — edit files by address and command when you have a shell but no full-screen UI.





## Interview Relevance
Interviewers rarely quiz `ed` itself; they use it as a signal that you know Vim’s Ex mode (`:`) descends from `ed`, and that remote/rescue shells may only ship a line editor.

## Sources
- [GNU ed manual](https://www.gnu.org/software/ed/manual/ed_manual.html) — deep-dive
- [Wikipedia — ed (text editor)](https://en.wikipedia.org/wiki/Ed_(text_editor)) — overview
- [POSIX ed](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/ed.html) — deep-dive

## Core Definition
`ed` addresses lines (by number, `$`, `.`, or regex), then runs a single-letter command. Input for insert/append ends with a lone `.` on its own line — the same convention Vim Ex mode still uses.

## Key Concepts
- **Address then command:** `1,$p` prints all lines; `g/TODO/d` deletes matching lines → batch edits without a cursor UI.
- **Current line (`.`):** most commands act on `.` unless you give a range → track where you are with `n` or `.=`.
- **Input mode vs command mode:** `a` / `i` / `c` enter text until `.` → easy to strand yourself if you forget the terminator.
- **Vim lineage:** Vim’s `:` commands and `:g//` global are Ex/`ed` heritage → knowing ranges transfers to [[vim commands]].

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

## Real-World Applications
Rescue disks, serial consoles, and minimal containers where Vim/Emacs are missing — fix `/etc/fstab` or a broken unit with addresses and `w`.

**Example:** SSH into a tiny Alpine box, `ed /etc/hosts`, append a line with `a`, end with `.`, then `w` and `q`.

## Pros/Cons or Trade-offs
- **Pro:** Tiny binary, scriptable, always available on Unix-like systems.
- **Con:** No visual context — high cognitive load; prefer [[vim commands]] or `sed` for day-to-day work.

## Comparison
- vs Vim Ex mode (`:`): same address/command model, but Vim keeps a buffer UI and undo.
- vs `sed`: `sed` is stream-oriented and non-interactive; `ed` is interactive and file-backed.

## Mistakes to Avoid
- Forgetting `.` to leave insert/append — then every typed line becomes text.
- Using `q` without `w` after edits — changes are lost.
- Confusing `ed` with `ex`/`vi` — related family, different entry points.
