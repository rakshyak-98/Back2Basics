[[sshd config]] [[TCP]] [[symmetrical encryption]] [[Asymmetrical Encryption]] [[HMAC (Hash based Message Authentication Codes)]] [[nc]] [[puTTY]] [[ufw]]

# SSH

> SSH (Secure Shell) opens an encrypted login/command channel to a remote host — authenticate with keys, then run shells, tunnels, or file copy.

## Interview Relevance
Expect host key vs user key, KEX → session cipher, and why `StrictHostKeyChecking=no` / agent forwarding are footguns — not just “ssh user@host.”

## Sources
- [OpenSSH Manual Pages](https://man.openbsd.org/ssh) — deep-dive
- [RFC 4253 — SSH Transport](https://www.rfc-editor.org/rfc/rfc4253) — overview

## Core Definition
Client connects to `sshd`, verifies the **host key**, runs key exchange for a **symmetric session**, then authenticates the **user** (usually pubkey). Channels carry shell, port forwards, or SFTP.

## Key Concepts
- **Host key:** Server identity in `known_hosts` — mismatch can mean reinstall or MITM.
- **User key:** Private key stays local; public in `authorized_keys`.
- **KEX:** Builds shared session key; bulk traffic uses AES-GCM/ChaCha, not the long-term SSH key.
- **Tunnels:** `-L` local, `-R` remote, `-D` dynamic SOCKS.
- **ssh-keyscan:** Fetches host key only — does not prove authenticity without out-of-band check.

## Technical Details

```txt
Client                         Server (sshd)
  │ TCP :22                       │
  ├─ version + host key check ────┤  (known_hosts)
  ├─ KEX → symmetric session ─────┤
  ├─ user auth (pubkey) ──────────┤
  └─ channels: shell / -L / -R ───┘
```

```bash
ssh user@host
ssh -p 2222 user@host
ssh -i ~/.ssh/id_ed25519 user@host
ssh -F ~/.ssh/config -G host
ssh-copy-id user@host
nc -zv host 22
ssh -vvv user@host

ssh-keygen -t ed25519 -C "you@work"
ssh-keygen -lf ~/.ssh/id_ed25519.pub
ssh-keygen -F github.com
ssh-keyscan -p 22 host

ssh -L 8080:localhost:80 user@host
ssh -R 8080:localhost:3000 user@host
```

Server policy: [[sshd config]] — `PasswordAuthentication`, `PermitRootLogin`, `AllowUsers`, ciphers.

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied (publickey) | `-vvv`; which key offered | Right `-i`; pubkey in `authorized_keys`; perms `600/700` |
| Host key verification failed | Rotate vs MITM | Verify fingerprint OOB; update known_hosts |
| Timeout | `nc -zv`; security groups | Open port; check bind address |
| Works in shell, fails in CI | Missing agent / key | `ssh-agent`; `IdentitiesOnly=yes` |

## Real-World Applications
Bastion/`ProxyJump` access, local port forwards to private admin UIs, and CI deploy keys with locked-down `authorized_keys` commands.

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous, auditable, supports tunnels and file copy.
- **Con:** Exposed SSH is an attack surface; key sprawl is common.
- **Trade-off:** Agent forwarding convenience vs bastion compromise risk.

## Comparison
vs HTTPS APIs: different layer — SSH is ops access, not public API auth. vs VPN: SSH tunnels are point solutions; VPN is broader network access. Related: [[nc]], [[puTTY]].

## Mistakes to Avoid
- Confusing host key trust with user authentication.
- Blind `ssh-keyscan` into CI without fingerprint pinning.
- Committing private keys or disabling host key checks “to make CI green.”
