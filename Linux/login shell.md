<!-- note-strategy: operational -->
[[Linux]] [[Linux terminal]] [[Bash/Bash syntax]] [[Setup Non-Login user from Running process]]

# Login shell

> A login shell is the first shell after you sign in — it loads profile files to build your environment.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Login shells read “profile” files once at session start; interactive non-login shells read “rc” files (e.g. `.bashrc`) for each new terminal window.

```txt
SSH / console login          GUI terminal tab
        │                            │
   login shell                  interactive shell
        │                            │
  /etc/profile                   ~/.bashrc
  ~/.bash_profile (or            (often sourced from
   ~/.profile)                    .bash_profile too)
        │
   PATH, umask, locale, …
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Login shell** | Shell started as a login session | “SSH and `bash -l` are login shells.” |
| **Interactive** | Attached to a terminal, prompts you | “Can run job control and readlines.” |
| **Non-interactive** | Script / `bash -c` — no prompt | “Scripts skip `.bashrc` unless you force it.” |
| **Profile files** | `/etc/profile`, `~/.profile`, `~/.bash_profile` | “Login path sets PATH once.” |
| **rc files** | `~/.bashrc`, `/etc/bash.bashrc` | “Per-terminal aliases and functions.” |
| **`-l` / `--login`** | Force login behavior | “Reproduce ‘works in SSH, fails in cron’.” |

### Bash startup (practical)

| How you started | Typical files read |
|-----------------|--------------------|
| SSH / `login` / `bash -l` | `/etc/profile` → `~/.bash_profile` or `~/.bash_login` or `~/.profile` |
| New gnome-terminal tab | Often interactive **non-login** → `~/.bashrc` |
| `bash script.sh` / cron | Non-interactive — minimal env; **not** your aliases |
| `su - user` | Login shell for `user` |
| `su user` | Non-login — keeps caller env quirks |

> [!INFO]
> Many distros make `~/.bash_profile` source `~/.bashrc` so login and terminal tabs feel the same. If that line is missing, PATH differs between SSH and local terminals.

---

## Standard config / commands

```bash
# Am I a login shell?
shopt -q login_shell && echo login || echo not-login

# Force login semantics to inspect env
bash --login -c 'echo "$PATH"; type ll 2>/dev/null; env | sort'

# See what systemd/user sessions inject
systemctl --user show-environment 2>/dev/null

# Common profile layout (Bash)
# /etc/profile
# ~/.bash_profile  →  often: [ -f ~/.bashrc ] && . ~/.bashrc
# ~/.bashrc
# ~/.profile       # used by sh / some display managers
```

| Knob | Why it matters |
|------|----------------|
| `~/.bash_profile` vs `~/.bashrc` | Login-only vs every interactive shell |
| `/etc/profile.d/*.sh` | Distro drops PATH snippets here |
| `$SHELL` in `/etc/passwd` | Login binary for the account |
| `bash --noprofile --norc` | Clean shell for debugging env pollution |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Command works in SSH, fails in IDE terminal | Login vs non-login files | Source `.bashrc` from `.bash_profile` or put PATH in both |
| Cron / CI missing PATH | Non-interactive env | Use absolute paths or set PATH in crontab/unit |
| `source ~/.bashrc` errors in scripts | Guard: `$-` / `PS1` checks | Keep interactive-only code behind `[[ $- == *i* ]]` |
| Broken after `chsh` | `/etc/shells` + passwd shell | Valid shell path; re-login |
| Duplicate PATH entries grow | Profile sourced twice | Idempotent PATH prepend; avoid nesting loops |
| GUI app lacks CLI PATH | Started from `.desktop`, not login shell | Put env in systemd user environment or pam_env |

---

## Gotchas

> [!WARNING]
> **Terminal tabs are often not login shells** — putting PATH only in `.bash_profile` hides tools from local terminals.

> [!WARNING]
> **Scripts are not interactive** — aliases and `shopt` from `.bashrc` do not apply unless the script sources them.

> [!WARNING]
> **`su` vs `su -`** — without `-`, you do not get a clean login environment; debugging “permission” issues often starts here.

> [!WARNING]
> **zsh/fish differ** — login files are `.zprofile` / `.zlogin` / fish conf.d; don’t assume Bash names.

---

## When NOT to use

- **Don’t force every script to be a login shell** — slower, order-dependent, and surprises CI.
- **Don’t stuff secrets only in interactive rc files** — use a secrets manager or restricted environment for services ([[system service unit files]]).
- **Don’t equate “login shell” with “root”** — any user can have a login shell; privilege is separate.

---

## Related

[[process]] [[Linux terminal]] [[terminal emulator]] [[Bash/Bash syntax]] [[Bash/bash script]] [[Setup Non-Login user from Running process]] [[etc files]] [[SSH]]
