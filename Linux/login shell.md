[[Linux terminal]] [[Bash/bash script]] [[Bash/Bash syntax]] [[user management]] [[terminal config]] [[Setup Non-Login user from Running process]]

# login shell

> First shell after authentication — loads profile scripts, sets environment, and may start SSH commands or a desktop session.

```txt
        login shell ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic Bash trap: login vs interactive non-login startup files

## Sources
- [GNU Bash manual — Startup Files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html) — deep-dive
- `man 1 bash` (INVOCATION) — deep-dive

## Key Concepts
- **Login vs interactive:** different startup file chains.
- **`$0` / `shopt login_shell`:** how to tell what you are.
- **`/etc/shells`:** valid shells for `chsh`.
- **Forced SSH command:** `authorized_keys` `command=` overrides the login shell for that key.


- **Core:** A login shell (`bash -l`, SSH default, tty login) differs from an interactive…

## Technical Details
| File | Login | Interactive |
|------|-------|-------------|
| `/etc/profile` | yes | — |
| `~/.bash_profile` / `~/.profile` | yes | — |
| `~/.bashrc` | if sourced from profile | yes |
| `/etc/bash.bashrc` | — | Debian interactive |

```bash
shopt login_shell
echo $0
chsh -s /bin/bash alice
grep alice /etc/passwd
```

```ssh
command="/usr/bin/backup-sync" ssh-ed25519 AAAA...
```

## Mistakes to Avoid
- **Mistake:** Putting PATH only in `.bashrc` and wondering why cron/non-intera…
- **Mistake:** Using `/bin/false` without understanding login failure messages …
- **Mistake:** Assuming every new terminal is a login shell

## Pros/Cons or Trade-offs
- **Pro:** Predictable environment bootstrap for interactive humans.
- **Con:** Split startup files confuse PATH/alias debugging across SSH vs GUI terminals.

## Comparison
- vs non-login interactive: tabs/GUI terminals often skip profile.
- vs forced-command keys: automation without a full shell ([[Setup Non-Login user from Running proc…


### Use cases
- Fixing “PATH works over SSH but not in a new terminal tab” by sourcing `.bash…
