[[Linux]] [[Commands]]

# ssh allow local system with key

> Key-based SSH login for local or remote users — `authorized_keys`, strict permissions, optional `from=`/`command=` restrictions, `sshd_config` allowlists.

## Mental model

```
Client (private key) ──► SSH handshake ──► sshd ──► ~/.ssh/authorized_keys match?
                                              │
                                              ├── pubkey auth OK → shell / forced command
                                              └── AllowUsers / Match rules
```

**Pubkey auth** trusts **possession of private key** + **server's authorized_keys list**. Password auth is separate — disable in prod after keys work.

```
~/.ssh/authorized_keys   permissions 600
~/.ssh/                  permissions 700
/home/user               not group/world writable (sshd checks)
```

## Standard config / commands

### Client: generate key

```bash
ssh-keygen -t ed25519 -C "user@host-$(date +%Y)" -f ~/.ssh/id_ed25519
# Passphrase recommended — use ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Server: install key for local user

```bash
# As target user (e.g. ubuntu)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
install -m 600 /tmp/id_ed25519.pub ~/.ssh/authorized_keys
# or
echo "ssh-ed25519 AAAA... comment" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**One line per key.** Order doesn't matter; first matching key wins.

### Test login

```bash
ssh -i ~/.ssh/id_ed25519 -v ubuntu@127.0.0.1    # local loopback test
ssh -i ~/.ssh/id_ed25519 ubuntu@server.example.com
```

### authorized_keys options (restrict before trust expands)

```bash
# ~/.ssh/authorized_keys
from="10.0.0.0/8,192.168.1.5" ssh-ed25519 AAAA... deploy-laptop
from="backup.example.com" ssh-ed25519 AAAA... backup-only
command="/usr/local/bin/backup.sh",no-port-forwarding,no-X11-forwarding ssh-ed25519 AAAA... backup
restrict,port-forwarding ssh-ed25519 AAAA... tunnel-user
```

| Option | Effect |
|--------|--------|
| `from="CIDR"` | Accept key only from source IPs/hostnames |
| `command="…"` | Force command; no shell (git deploy, rsync) |
| `no-port-forwarding` | Block `-L/-R/-D` |
| `restrict` | Implies several no-* restrictions (OpenSSH 7.4+) |
| `environment="VAR=val"` | Set env (often disabled in sshd_config) |

### sshd_config — allow specific users

```ini
# /etc/ssh/sshd_config — validate with sudo sshd -t after edit
PubkeyAuthentication yes
PasswordAuthentication no          # after keys verified
PermitRootLogin prohibit-password  # or no — key-only if ever root
AllowUsers ubuntu deploy backup    # space-separated; usernames OR user@host
# AllowGroups ssh-users

AuthorizedKeysFile .ssh/authorized_keys
# System-wide alternative (rare): /etc/ssh/authorized_keys/%u

Match Address 10.0.0.0/8
    PasswordAuthentication no
```

```bash
sudo sshd -t && sudo systemctl reload sshd   # never restart blindly on remote box
```

### AllowUsers vs AllowGroups

- **AllowUsers** — if set, *only* listed users may SSH (others rejected before auth completes messaging).
- Omit AllowUsers = any local user with valid auth method allowed (subject to PermitRootLogin etc.).

### Local system login (`127.0.0.1`)

Same steps — sshd listens on all interfaces by default:

```ini
# Restrict listen if only remote needed
# ListenAddress 0.0.0.0
# ListenAddress ::
```

Loopback test validates sshd + keys without network/firewall variables.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Permission denied (publickey)` | `ssh -vvv` client; server auth log | Key not in authorized_keys; wrong user; wrong key file |
| Still asks password | `PasswordAuthentication yes` fallback | Install key; set PasswordAuthentication no after |
| `Authentication refused: bad ownership` | `namei -l ~/.ssh` | chmod 700 ~/.ssh; 600 authorized_keys; fix home perms |
| Key works for A not B | AllowUsers | Add user to AllowUsers or remove restriction |
| `from=` restriction fail | Client IP changed | Update CIDR; check NAT egress IP |
| `command=` exits immediately | Script path/shebang | ForceCommand logs in `/var/log/auth.log` |
| Connection timeout (not denied) | firewall, `ListenAddress`, SG | `ss -tlnp \| grep 22`; ufw/iptables |
| Root can't login | `PermitRootLogin no` | Use sudo user; or prohibit-password + root key (discouraged) |

### Server-side debug

```bash
sudo tail -f /var/log/auth.log          # Debian/Ubuntu
sudo journalctl -u ssh -f
sudo sshd -T | grep -E 'pubkey|password|allowusers|permitroot'
```

Common log lines:

- `Authentication refused: bad ownership or modes for directory /home/user`
- `User user from 1.2.3.4 not allowed because not listed in AllowUsers`
- `Failed publickey for user from …`

## Gotchas

> [!WARNING]
> **Lock yourself out** — editing `sshd_config` / `AllowUsers` on only session. Keep console access; test `sshd -t`; use `reload` not restart; keep second session open.

> [!WARNING]
> **World-readable authorized_keys or home** — sshd ignores keys silently (secure default).

- **Cloud images** — default user (`ubuntu`, `ec2-user`) with cloud-init injected key; manual keys additive.
- **Duplicate keys / paste corruption** — line break mid-key breaks auth; one line per key.
- **`ssh-copy-id`** — convenient but verify permissions after; overwrites doesn't merge carefully.
- **SELinux** — `restorecon -Rv ~/.ssh` if context wrong on RHEL.
- **ForceCommand + SFTP** — use `internal-sftp` subsystem pattern for chrooted SFTP, not random shell script.

## When NOT to use

- **Shared private key across team** — per-user keys + audit; use SSO bastion for org scale.
- **command= bypass with scp** — scp/sftp use different subsystem; design restrictions explicitly.
- **PasswordAuthentication no before confirming key** — classic outage pattern.

## Related

[[Linux]] [[Commands]] [[loopback]] [[Networking]]
