[[Linux terminal]] [[Bash/bash script]] [[Bash/Bash syntax]] [[user management]] [[terminal config]] [[Setup Non-Login user from Running process]]

# login shell

> First shell after authentication — loads profile scripts, sets environment, and may start SSH commands or a desktop session.





## Interview Relevance
Classic Bash trap: login vs interactive non-login startup files — why SSH gets `.profile` but a new terminal tab often only gets `.bashrc`.

## Sources
- [GNU Bash manual — Startup Files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html) — deep-dive
- `man 1 bash` (INVOCATION) — deep-dive

## Core Definition
A login shell (`bash -l`, SSH default, tty login) differs from an interactive non-login shell (many terminal tabs run `~/.bashrc` only). Service accounts often use `/usr/sbin/nologin` or `/bin/false`.

## Key Concepts
- **Login vs interactive:** different startup file chains.
- **`$0` / `shopt login_shell`:** how to tell what you are.
- **`/etc/shells`:** valid shells for `chsh`.
- **Forced SSH command:** `authorized_keys` `command=` overrides the login shell for that key.

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

## Real-World Applications
Fixing “PATH works over SSH but not in a new terminal tab” by sourcing `.bashrc` from `.profile`, and locking service accounts to nologin.

## Pros/Cons or Trade-offs
- **Pro:** Predictable environment bootstrap for interactive humans.
- **Con:** Split startup files confuse PATH/alias debugging across SSH vs GUI terminals.

## Comparison
- vs non-login interactive: tabs/GUI terminals often skip profile.
- vs forced-command keys: automation without a full shell ([[Setup Non-Login user from Running process]]).

## Mistakes to Avoid
- Putting PATH only in `.bashrc` and wondering why cron/non-interactive jobs miss it.
- Using `/bin/false` without understanding login failure messages vs nologin.
- Assuming every new terminal is a login shell.
