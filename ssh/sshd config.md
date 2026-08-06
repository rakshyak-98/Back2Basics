[[Linux]] [[SSH]] [[systemd]] [[Authentication command]] [[/etc files]]

# sshd config

> One-line: **server-side SSH policy** in `/etc/ssh/sshd_config` (+ drop-ins) — who can connect, how they authenticate, what they can forward, and which sockets/keys the daemon exposes. **OpenSSH sshd_config(5) + production hardening practice.**

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

`sshd` reads **one effective config** at startup (or reload) from `/etc/ssh/sshd_config`, which **includes** fragments under `/etc/ssh/sshd_config.d/*.conf`. OpenSSH ships defaults **commented**; any **uncommented** directive overrides the built-in default.

```
Client TCP :22 ──► sshd (or systemd ssh.socket) ──► sshd_config + .d/*.conf
                                                      │
                    ┌─────────────────────────────────┼─────────────────────────────┐
                    ▼                                 ▼                             ▼
              ListenAddress/Port              Auth stack (keys/PAM/password)   Forwarding/Match rules
                    │                                 │                             │
                    ▼                                 ▼                             ▼
              Host keys prove server            authorized_keys / PAM / Kerberos   shell / sftp / ForceCommand
```

| Layer | What it controls |
|-------|------------------|
| **Network** | `Port`, `ListenAddress`, `AddressFamily` — where sshd accepts connections |
| **Host identity** | `HostKey` paths — server proves itself to clients |
| **Authentication** | `PubkeyAuthentication`, `PasswordAuthentication`, `PermitRootLogin`, `AllowUsers` |
| **Session** | `X11Forwarding`, `AllowTcpForwarding`, `ClientAlive*`, `Subsystem sftp` |
| **Overrides** | `Match User/Group/Address` — per-principal policy at end of file |

**Client vs server config:** `~/.ssh/config` (see [[git ssh config]]) is the **client**; `/etc/ssh/sshd_config` is the **server**. Different files, different `man` pages (`ssh_config(5)` vs `sshd_config(5)`).

## Standard config / commands

### File layout (from default Debian/Ubuntu-style `sshd_config`)

```ini
# Main file — drop-ins are the preferred place for local overrides
Include /etc/ssh/sshd_config.d/*.conf
```

```bash
# Inspect effective runtime config (ground truth — not what's commented)
sudo sshd -T                    # all effective settings
sudo sshd -T | grep -i password # filter one knob
man 5 sshd_config
```

```bash
# Edit safely — keep a second session open on remote hosts
sudoedit /etc/ssh/sshd_config.d/99-local.conf   # preferred: small drop-in
sudo sshd -t                                     # syntax check — MUST pass
sudo systemctl reload sshd                       # or: restart ssh / ssh.socket
```

> [!WARNING]
> On systemd socket-activated installs (common default), changing **`Port`**, **`AddressFamily`**, or **`ListenAddress`** requires regenerating the socket unit:
> `sudo systemctl daemon-reload && sudo systemctl restart ssh.socket`

### Network binding

```ini
#Port 22
#AddressFamily any          # any | inet | inet6
#ListenAddress 0.0.0.0      # repeat for multiple; omit = all interfaces
#ListenAddress ::
```

| Directive | Default (commented) | Production notes |
|-----------|---------------------|------------------|
| `Port` | 22 | Non-default port is **obscurity only**; pair with firewall + keys |
| `ListenAddress` | all interfaces | Bind bastion to public NIC, admin to VPN IP |
| `AddressFamily` | `any` | IPv6-only or IPv4-only hosts |

```bash
ss -tlnp | grep sshd    # verify listening sockets match intent
```

### Host keys (server authentication)

```ini
#HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_ecdsa_key
#HostKey /etc/ssh/ssh_host_ed25519_key
```

Clients verify **these** keys (stored in `~/.ssh/known_hosts`) — distinct from **user** keys in `authorized_keys`. Defaults enable modern algorithms; removing weak keys (`ssh_host_rsa_key`) is fine once all clients support Ed25519/ECDSA.

```bash
sudo ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub   # fingerprint for docs/runbooks
ssh-keyscan -t ed25519 host.example.com                   # client-side fetch (verify OOB)
```

### Logging

```ini
#SyslogFacility AUTH
#LogLevel INFO          # DEBUG for auth troubleshooting — noisy in prod
```

```bash
sudo journalctl -u ssh -f              # systemd
sudo tail -f /var/log/auth.log         # Debian/Ubuntu classic
```

### Authentication block (highest-impact section)

```ini
#LoginGraceTime 2m           # time to complete authentication
#PermitRootLogin prohibit-password   # default: root with keys only, not password
#StrictModes yes              # reject loose ~/.ssh permissions
#MaxAuthTries 6
#MaxSessions 10

#PubkeyAuthentication yes
#AuthorizedKeysFile .ssh/authorized_keys .ssh/authorized_keys2
#PasswordAuthentication yes
#PermitEmptyPasswords no
KbdInteractiveAuthentication no
UsePAM yes
```

| Directive | Shipped default | Hardened typical | Meaning |
|-----------|-----------------|------------------|---------|
| `PubkeyAuthentication` | yes | yes | [[ssh allow local system with key\|Key-based login]] |
| `PasswordAuthentication` | yes | **no** (after keys work) | Cleartext password over encrypted channel |
| `KbdInteractiveAuthentication` | **no** (explicit) | no | Challenge-response / keyboard-interactive |
| `UsePAM` | **yes** (explicit) | yes | PAM account/session checks; enables password path when allowed |
| `PermitRootLogin` | `prohibit-password` | `no` | Root SSH policy |
| `PermitEmptyPasswords` | no | no | Accounts with empty password |
| `MaxAuthTries` | 6 | 3 | Failed attempts per connection |
| `StrictModes` | yes | yes | Home/`~/.ssh` ownership checks |

**PAM interaction (non-obvious):** `UsePAM yes` runs PAM **account** and **session** stacks. Password auth can arrive via `PasswordAuthentication` or `KbdInteractiveAuthentication` depending on PAM modules. A restrictive `PermitRootLogin` can still be **bypassed** by PAM keyboard-interactive if misconfigured — test with `sshd -T` and a throwaway user before disabling passwords globally.

```ini
# Production drop-in example — /etc/ssh/sshd_config.d/99-hardening.conf
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers deploy admin
```

### Host-based and legacy auth (usually stay off)

```ini
#HostbasedAuthentication no
#IgnoreRhosts yes
#IgnoreUserKnownHosts no
```

Host-based auth trusts host keys + `.rhosts` — rare today; leave disabled unless you operate a legacy cluster.

### Kerberos / GSSAPI (enterprise AD)

```ini
#KerberosAuthentication no
#GSSAPIAuthentication no
```

Enable only when integrated with AD/Heimdal; otherwise noise and attack surface.

### Forwarding and session features

```ini
#AllowAgentForwarding yes
#AllowTcpForwarding yes      # -L / -R / -D tunnels
#GatewayPorts no              # remote binds 0.0.0.0 vs localhost only
X11Forwarding yes             # explicit enable in sample config
#PermitTTY yes
PrintMotd no                  # explicit disable — use pam_motd instead on modern distros
#TCPKeepAlive yes
#ClientAliveInterval 0
#ClientAliveCountMax 3
#PermitUserEnvironment no
#Compression delayed
```

| Directive | Sample value | Ops note |
|-----------|--------------|----------|
| `X11Forwarding` | yes | Disable on servers with no GUI need |
| `AllowTcpForwarding` | yes (default) | Set `no` on jump-sensitive hosts; use `Match` for exceptions |
| `GatewayPorts` | no | `yes` exposes remote forward to world — dangerous |
| `PrintMotd` | no | MOTD often from PAM; avoids duplicate banners |
| `ClientAliveInterval` | 0 (off) | Set 60–300s behind NAT/firewalls to drop dead sessions |
| `PermitUserEnvironment` | no | Client `SendEnv` mostly blocked unless enabled |

### Environment and SFTP

```ini
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
```

- `AcceptEnv LANG LC_*` — allows clients to pass locale variables (safe subset).
- `Subsystem sftp` — `sftp` and `scp` (modern scp) use this; chroot patterns use `internal-sftp` + `ChrootDirectory` in `Match` blocks.

### Connection limits and DNS

```ini
#UseDNS no                   # reverse DNS on connect — can slow/fail auth
#MaxStartups 10:30:100       # unauthenticated connection throttle
#Banner none
```

Set `UseDNS no` when slow logins correlate with broken PTR records.

### Per-user overrides (`Match`)

```ini
#Match User anoncvs
#    X11Forwarding no
#    AllowTcpForwarding no
#    PermitTTY no
#    ForceCommand cvs server
```

`Match` stanzas apply **last wins** for matching connections — use for:
- SFTP-only accounts (`ForceCommand internal-sftp`, `ChrootDirectory`)
- Stricter auth from Internet (`Match Address` + `PasswordAuthentication no`)
- Service accounts with no forwarding

```ini
Match Group sftp-only
    ChrootDirectory /srv/sftp/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
```

### Validate → apply workflow

```bash
# 1. Syntax
sudo sshd -t

# 2. Diff effective config before/after (save output first on prod)
sudo sshd -T | sort > /tmp/sshd-before.txt
# ... edit ...
sudo sshd -t && sudo systemctl reload sshd
sudo sshd -T | sort > /tmp/sshd-after.txt
diff -u /tmp/sshd-before.txt /tmp/sshd-after.txt

# 3. Test new session without closing existing one
ssh -o PreferredAuthentications=publickey user@host 'echo ok'
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Config change ignored | Drop-in override; wrong file | `sudo sshd -T \| grep <option>`; check `sshd_config.d/` |
| `sshd: no hostkeys available` | Missing/regenerated keys | `sudo ssh-keygen -A`; verify `HostKey` paths |
| Slow SSH login | Reverse DNS | `UseDNS no`; fix PTR or ignore |
| Password still works after `no` | PAM / KbdInteractive path | `sshd -T`; set `KbdInteractiveAuthentication no`; check `/etc/pam.d/sshd` |
| `Connection refused` after port change | systemd socket not updated | `daemon-reload`; `restart ssh.socket`; check `ss -tlnp` |
| `Permission denied (publickey)` | Auth directives, keys | See [[ssh allow local system with key]]; `journalctl -u ssh` |
| SFTP works, shell doesn't | `ForceCommand` / `Match` | Review `Match User` blocks; `sshd -T -C user=x,host=y,addr=z` |
| Locked out | Bad `AllowUsers` / syntax | Serial console; recovery ISO; revert drop-in |
| X11 apps fail | Forwarding disabled | `X11Forwarding yes`; client `-X`/`-Y`; `xauth` on server |

```bash
# Simulate effective config for a specific connection context
sudo sshd -T -C user=deploy,host=myhost,addr=10.0.0.5
```

## Gotchas

> [!WARNING]
> **`sshd -t` does not catch logic errors** — `AllowUsers typo` passes syntax but rejects everyone. Always open a **second session** before reload on remote hosts.

> [!WARNING]
> **`UsePAM yes` + `PasswordAuthentication no`** — account lockout and session limits still run through PAM; password may be disabled but PAM failures (expired account, nologin shell) still block login.

> [!WARNING]
> **Socket activation vs standalone** — service may be `ssh.socket` + `ssh.service`; editing config without reloading the right unit leaves old listeners.

- **Commented ≠ disabled** — `#PasswordAuthentication yes` means default **yes**; you must set `PasswordAuthentication no` explicitly to harden.
- **`authorized_keys2`** — legacy filename; default still lists it but OpenSSH deprecates it.
- **`PrintMotd no`** — does not remove all banners; PAM (`pam_motd`) or `Banner` may still print.
- **Package upgrades** — `openssh-server` conffile prompts can merge or keep old files; diff after `apt upgrade`.
- **`MaxStartups` hit** — symptoms look like intermittent timeouts under brute force or CI fan-out; tune or firewall.
- **`Match` order matters** — first matching `Match` block in file wins for its directives; put specific rules after general ones.

## When NOT to use

- **Don't edit `sshd_config` for client key selection** — use `~/.ssh/config` and `IdentityFile` ([[git ssh config]]).
- **Don't rely on non-default `Port` alone** — it's not access control; use firewall, keys, bastion.
- **Don't enable `PermitRootLogin` or passwords** to "fix it quick" — use console, fix keys/`AllowUsers`, then restore policy.
- **Don't `Match` your way around bad IAM** — per-user `ForceCommand` is for narrow service accounts, not org-wide auth design.

## Related

[[SSH]] [[/etc files]] [[ssh allow local system with key]] [[SSH authentication]] [[systemd]] [[Authentication command]] [[ufw]] [[journalctl]] [[x11]]
