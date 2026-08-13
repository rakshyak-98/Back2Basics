[[Linux terminal]] [[bash script]] [[Bash syntax]] [[user management]]

# login shell

> The login shell is the first process after authentication — it loads profile scripts, sets environment, and may start SSH commands or a desktop session.

Distinguish **login shell** (`bash -l`, SSH default, tty login) from **interactive non-login** (new terminal tab runs `~/.bashrc` only on many distros).

## Startup files (Bash)

| File | Login | Interactive |
|------|-------|-------------|
| `/etc/profile` | yes | — |
| `~/.bash_profile` / `~/.profile` | yes | — |
| `~/.bashrc` | if sourced from profile | yes |
| `/etc/bash.bashrc` | — | Debian interactive |

```bash
# What am I?
shopt login_shell   # on or off
echo $0               # -bash vs bash
```

## Change default shell

```bash
chsh -s /bin/bash alice
grep alice /etc/passwd   # last field is shell
```

Valid shells listed in `/etc/shells`. Use `/usr/sbin/nologin` or `/bin/false` for non-interactive service accounts — see [[Setup Non-Login user from Running process]].

## SSH forced command

```ssh
command="/usr/bin/backup-sync" ssh-ed25519 AAAA...
```

Overrides login shell for that key — useful for automation without full shell access.

## Related

[[terminal config]] · [[bash script]] · [[user management]]

## Sources

- `man 1 bash` — INVOCATION
- [invocation section — GNU Bash manual](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html)
