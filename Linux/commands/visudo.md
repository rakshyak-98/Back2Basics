[[commands]] [[user management]] [[sudo]] [[linux groups]]

# visudo

> visudo edits sudoers safely — locks the file and rejects syntax errors so you don’t lock everyone out of root.

## Mental model

**Say it in one breath:** never `vim /etc/sudoers` raw — visudo validates; rules say *who* may run *what* *as whom* on *which hosts*.

```txt
who   where  =  (as_whom:as_group)  what
alice ALL=(ALL:ALL) NOPASSWD: /bin/systemctl restart myapp

%group  → rule applies to group members
/etc/sudoers.d/*  read in lexical order (later can override)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`visudo`** | Safe sudoers editor | “Syntax check before commit — prevents lockout.” |
| --- | --- | --- |
| **`%sudo`** | Group rule | “Percent means group.” |
| **`NOPASSWD:`** | No password prompt | “OK for narrow commands; dangerous with `ALL`.” |
| **`Cmnd_Alias`** | Named command sets | “Grant logs without granting shell.” |
| **`sudo -l`** | Effective privileges | “What *this* user can actually run.” |

## Standard config / commands

```bash
sudo visudo
sudo EDITOR=vi visudo
sudo visudo -f /etc/sudoers.d/50-dev-team

sudo -l
sudo -lU alice
sudo -k                    # forget cached credentials
sudo -u www-data id
```

Example drop-in:

```text
# /etc/sudoers.d/50-dev-team
User_Alias DEV_TEAM = alice, bob, charlie

Cmnd_Alias LOGS_AND_STATUS = /usr/bin/journalctl *, \
                             /usr/bin/tail -f /var/log/*

Cmnd_Alias SERVICE_CONTROL = /bin/systemctl status *, \
                             /bin/systemctl restart myapp.service

DEV_TEAM ALL=(ALL) NOPASSWD: LOGS_AND_STATUS
DEV_TEAM ALL=(ALL)         PASSWD: SERVICE_CONTROL
```

| Position | Example | Meaning |
| --- | --- | --- |
| Who | `alice` / `%devs` / `ALL` | User or group |
| Where | `ALL` | Hosts (mostly ALL on single machines) |
| Runas | `(ALL:ALL)` | Target user/group |
| What | `/usr/bin/apt` / `ALL` | Allowed commands |

## sudoers.d layout

```text
00-defaults     early Defaults
10-aliases      User_Alias / Cmnd_Alias
20-automation   CI / deploy NOPASSWD (narrow!)
50-teams        human roles
90- / zz-       emergency overrides (last wins)
```

> [!WARNING]
> Never point sudoers at files in a user’s home — they could grant themselves `ALL`.

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Locked out / parse error | Broken sudoers | Root console; fix with `visudo` / `pkexec` / live USB |
| User “in sudo group” but denied | `sudo -lU` | Group membership not refreshed — re-login; check `%sudo` line |
| Wrong file wins | Lexical order | Rename with `zz-` / `50-` prefixes |
| NOPASSWD not applied | Alias mismatch | Full path required; no unexpected args |
| `sudo -u` fails | Runas list | Allow `(www-data)` explicitly |

## Gotchas

> [!WARNING]
> **Bad sudoers can lock out all sudo** — only edit via visudo; keep a root session open while testing.

> [!WARNING]
> **`NOPASSWD: ALL` is root with extra steps** — scope commands tightly.

> [!WARNING]
> **Wildcards in command paths are tricky** — `/usr/bin/*` may be broader than you think; prefer aliases.

## When NOT to use

- **application RBAC** — application authz, not sudoers.
- **Containers as non-root by design** — drop capabilities; don’t sprinkle NOPASSWD.
- **Windows** — different privilege model.

## Related

[[user management]] [[linux groups]] [[useradd]] [[commands]]
