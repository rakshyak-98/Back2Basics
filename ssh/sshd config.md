[[ssh allow local system with key]] [[SSH authentication]] [[ssh agent]] [[git ssh configuration]]

# sshd config

> `sshd_config` is the server SSH policy file — who can log in, how they authenticate, and which session features are allowed.

```txt
        sshd config ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers expect `sshd -T` / `sshd -t`, drop-in files, `Match` block order…

## Sources
- [OpenSSH — sshd_config](https://man.openbsd.org/sshd_config) — deep-dive
- [CIS — OpenSSH Benchmark](https://www.cisecurity.org/benchmark/openssh) — overview

## Key Concepts
- **Server vs client config:** `sshd_config` ≠ `~/.ssh/config`.
- **Layers:** network (`Port`/`ListenAddress`), auth, session features, then `Match` overri…
- **Effective config:** `sshd -T` shows what actually applies after drop-ins.
- **Reload carefully:** validate with `sshd -t`; keep a second session open.

## Technical Details
```txt
Client :22 → sshd → config + Match blocks → keys/PAM → session
```

| Layer | Knobs |
|-------|-------|
| Network | `Port`, `ListenAddress` |
| Auth | `PubkeyAuthentication`, `PasswordAuthentication`, `PermitRootLogin` |
| Session | Forwarding, `ClientAlive*`, `Subsystem sftp` |
| Overrides | `Match User/Group/Address` at end |

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

- Port/Listen changes on socket-activated installs need `daemon-reload` + resta…

| Symptom | Check | Fix |
|---------|-------|-----|
| Locked out after edit | Second session still open? | Fix from console; revert drop-in |
| Key rejected | `StrictModes`, key in `authorized_keys` | `chmod 700 ~/.ssh`; `600` keys file |
| Password still works | Effective `sshd -T` | Drop-in order; reload |
| Slow login | DNS / GSSAPI | `UseDNS no`; disable unused GSSAPI |
| Wrong port | `ss -tlnp \| grep ssh` | Match socket unit + config |

## Mistakes to Avoid
- **Mistake:** Changing auth on the only live session
- **Mistake:** Putting directives after a `Match` block without realizing they …
- **Mistake:** Root login with password
- **Mistake:** Password authentication on internet hosts when keys work

## Pros/Cons or Trade-offs
- **Pro:** Central policy with drop-ins and `Match` for per-network rules.
- **Con:** One typo locks out remote admins — console access required.
- **Con:** PAM + keyboard-interactive can bypass naive “password off” assumptions — verify with `sshd -T`.

## Comparison
- vs client `~/.ssh/config`: client chooses identity/jump; server enforces policy.
- vs cloud security groups: SGs filter packets


### Use cases
- Hardening internet-facing bastions, restricting deploy users, and fixing slow…

- **Example:** Drop `PasswordAuthentication no` into `sshd_config.d`, run `sshd…
