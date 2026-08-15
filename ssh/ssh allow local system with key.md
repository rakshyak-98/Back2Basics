[[sshd config]] [[SSH authentication]] [[ssh agent]] [[ssh login]] [[loopback]]

# ssh allow local system with key

> Install an ed25519 public key into a local user’s `authorized_keys`, lock down permissions, then confirm login — including on loopback — before turning off passwords.

## Interview Relevance

Interviewers look for permission pitfalls (`StrictModes`), `AllowUsers` lockouts, and `authorized_keys` options like `from=` / `command=`.

## Sources

- [OpenSSH — sshd](https://man.openbsd.org/sshd.8) — deep-dive
- [OpenSSH — AUTHORIZED_KEYS file format](https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT) — deep-dive

## Key Concepts

- **Trust model:** possession of private key + listing in `authorized_keys`.
- **StrictModes:** `~/.ssh` 700, `authorized_keys` 600, home not group/world-writable — otherwise sshd ignores keys silently.
- **AllowUsers / Match:** can reject valid keys before auth messaging completes.
- **Key options:** `from=`, `command=`, `restrict` limit blast radius per key.

## Technical Details

```
client (private key) ──► SSH handshake ──► sshd ──► ~/.ssh/authorized_keys match?
                                              │
                                              ├── pubkey auth OK → shell / forced command
                                              └── AllowUsers / Match rules
```

### Client: generate key

```bash
ssh-keygen -t ed25519 -C "user@host-$(date +%Y)" -f ~/.ssh/id_ed25519
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Server: install key for local user

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
install -m 600 /tmp/id_ed25519.pub ~/.ssh/authorized_keys
# or
echo "ssh-ed25519 AAAA... comment" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

One line per key; first matching key wins.

```bash
ssh -i ~/.ssh/id_ed25519 -v ubuntu@127.0.0.1    # local loopback test
ssh -i ~/.ssh/id_ed25519 ubuntu@server.example.com
```

### authorized_keys options

```bash
from="10.0.0.0/8,192.168.1.5" ssh-ed25519 AAAA... deploy-laptop
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

### sshd_config knobs

```ini
PubkeyAuthentication yes
PasswordAuthentication no          # after keys verified
PermitRootLogin prohibit-password
AllowUsers ubuntu deploy backup
AuthorizedKeysFile .ssh/authorized_keys

Match Address 10.0.0.0/8
    PasswordAuthentication no
```

```bash
sudo sshd -t && sudo systemctl reload sshd   # never restart blindly on remote box
sudo tail -f /var/log/auth.log
sudo sshd -T | grep -E 'pubkey|password|allowusers|permitroot'
```

If `AllowUsers` is set, only listed users may SSH. Loopback tests validate sshd + keys without network/firewall variables.

| Symptom | Check | Fix |
|---------|-------|-----|
| `Permission denied (publickey)` | `ssh -vvv`; server auth log | Key not in authorized_keys; wrong user; wrong key file |
| Still asks password | `PasswordAuthentication yes` fallback | Install key; set PasswordAuthentication no after |
| `Authentication refused: bad ownership` | `namei -l ~/.ssh` | chmod 700 ~/.ssh; 600 authorized_keys; fix home perms |
| Key works for A not B | AllowUsers | Add user or remove restriction |
| `from=` restriction fail | Client IP changed | Update CIDR; check NAT egress IP |
| `command=` exits immediately | Script path/shebang | ForceCommand logs in `/var/log/auth.log` |
| Connection timeout (not denied) | firewall, `ListenAddress`, SG | `ss -tlnp \| grep 22` |
| Root can't login | `PermitRootLogin no` | Use sudo user |

## Real-World Applications

Cloud image bootstrap (`ubuntu`/`ec2-user` keys), deploy users with forced commands, and lab loopback validation before remote cutover.

**Example:** Add a deploy key with `command=` and `no-port-forwarding`, confirm via `127.0.0.1`, then set `PasswordAuthentication no`.

## Pros/Cons or Trade-offs

- **Pro:** Strong, auditable per-user access without shared passwords.
- **Con:** Easy to lock yourself out with `AllowUsers` / sshd edits — keep console + second session.
- **Con:** `command=` does not automatically cover scp/sftp subsystems — design restrictions explicitly.

## Comparison

- vs password login: keys after verified setup; never disable passwords first.
- vs shared team private key: per-user keys + bastion/SSO at org scale.
- Full directive reference: [[sshd config]].

## Mistakes to Avoid

- Editing `sshd_config` on the only session without `sshd -t` and a second session.
- World-readable `authorized_keys` or home — sshd ignores keys silently.
- Pasting a key with a mid-line break; `ssh-copy-id` without verifying permissions.
- SELinux wrong context on RHEL — `restorecon -Rv ~/.ssh`.
- `PasswordAuthentication no` before confirming the key works.
