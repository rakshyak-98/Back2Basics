[[Linux]] [[SSH]] [[systemd]] [[Authentication command]] [[/etc files]]

# sshd config

> `sshd_config` — server SSH policy: who can log in and how they authenticate.

---

## How it works

```txt
Client :22 → sshd → config + Match blocks → keys/PAM → session
```

| Layer | Knobs |
|-------|-------|
| Network | `Port`, `ListenAddress` |
| Auth | `PubkeyAuthentication`, `PasswordAuthentication`, `PermitRootLogin` |
| Session | Forwarding, `ClientAlive*`, `Subsystem sftp` |
| Overrides | `Match User/Group/Address` at end |

Client `~/.ssh/config` ≠ server `sshd_config`.

---


## Configuration and commands

```bash
sudo sshd -T | less                 # effective config
sudo sshd -t                        # syntax check
sudoedit /etc/ssh/sshd_config.d/99-local.conf
sudo systemctl reload sshd
```

```ini
# /etc/ssh/sshd_config.d/99-hardening.conf
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers deploy admin
```

| Knob | Why it matters |
|------|----------------|
| `UsePAM yes` | Account/session + password path |
| `StrictModes yes` | Reject loose `~/.ssh` perms |
| `UseDNS no` | Avoid slow/broken PTR delays |
| `ClientAliveInterval` | Drop dead NAT sessions |

Port/Listen changes on socket-activated installs need `daemon-reload` + restart `ssh.socket`.

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Locked out after edit | Second session still open? | Fix from console; revert drop-in |
| Key rejected | `StrictModes`, key in `authorized_keys` | `chmod 700 ~/.ssh`; `600` keys file |
| Password still works | Effective `sshd -T` | Drop-in order; reload |
| Slow login | DNS / GSSAPI | `UseDNS no`; disable unused GSSAPI |
| Wrong port | `ss -tlnp \| grep ssh` | Match socket unit + config |

---


## Gotchas

> [!WARNING]
> **Keep a second session open** when changing auth — one typo locks you out.

> [!WARNING]
> **PAM + keyboard-interactive** can bypass naive “password off” assumptions — verify with `sshd -T`.

> [!WARNING]
> **`Match` blocks must be last** — directives after `Match` are scoped.

---


## When not to use

- **Password authentication on internet hosts** — keys (+ optional bastion).
- **Root login with password** — never.
- **GatewayPorts yes** unless you know the exposure.

---


## Related

[[ssh allow local system with key]] [[SSH authentication]] [[ssh agent]] [[git ssh configuration]]

## Sources

- [Wikipedia — sshd config](https://en.wikipedia.org/wiki/sshd_config)
