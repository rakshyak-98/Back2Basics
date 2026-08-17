[[commands]] [[user management]] [[sudo]] [[linux groups]] [[useradd]]

# visudo

> Edits sudoers safely — file lock plus syntax check so a typo does not lock everyone out of root.

```txt
        visudo ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Expect visudo (never raw `vi /etc/sudoers`), `%group` syntax, NOPASSWD scopin…

## Sources
- [man visudo](https://man7.org/linux/man-pages/man8/visudo.8.html) — deep-dive
- [man sudoers](https://man7.org/linux/man-pages/man5/sudoers.5.html) — deep-dive

## Key Concepts
- **Syntax check before commit:** prevents parse-error lockout.
- **`%group`:** percent means group rule.
- **NOPASSWD:** OK for narrow commands; dangerous with `ALL`.
- **Cmnd_Alias:** grant logs/restarts without a full shell.
- **`sudoers.d` lexical order:** later files can override earlier ones.

## Technical Details
```txt
who   where  =  (as_whom:as_group)  what
alice ALL=(ALL:ALL) NOPASSWD: /bin/systemctl restart myapp

%group  → rule applies to group members
/etc/sudoers.d/*  read in lexical order (later can override)
```

```bash
sudo visudo
sudo EDITOR=vi visudo
sudo visudo -f /etc/sudoers.d/50-dev-team
sudo -l
sudo -lU alice
sudo -k
sudo -u www-data id
```

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
|----------|---------|---------|
| Who | `alice` / `%devs` / `ALL` | User or group |
| Where | `ALL` | Hosts |
| Runas | `(ALL:ALL)` | Target user/group |
| What | `/usr/bin/apt` / `ALL` | Allowed commands |

- Suggested drop-in layout: `00-defaults`, `10-aliases`, `20-automation`, `50-t…

| Symptom | Check | Fix |
|---------|-------|-----|
| Locked out / parse error | Broken sudoers | Root console; fix via visudo / pkexec / live USB |
| In sudo group but denied | `sudo -lU` | Re-login; check `%sudo` line |
| Wrong file wins | Lexical order | Rename with numeric/`zz-` prefixes |
| NOPASSWD not applied | Alias mismatch | Full paths; unexpected args |

## Mistakes to Avoid
- **Mistake:** Editing sudoers without visudo
- **Mistake:** `NOPASSWD: ALL` for convenience
- **Mistake:** Pointing sudoers includes at files in a user’s home (self-grant …
- **Mistake:** Keeping a root session open while testing

## Pros/Cons or Trade-offs
- **Pro:** Prevents the classic “edited sudoers, lost sudo” outage.
- **Con:** Wildcards and `NOPASSWD: ALL` recreate root with extra steps.

## Comparison
- vs editing `/etc/sudoers` directly: never — always visudo.
- vs application RBAC: sudo is host privilege, not app authorization.


### Use cases
- Least-privilege ops: allow `journalctl` and a single `systemctl restart` with…
