[[Linux]] [[sshd config]] [[TCP]] [[symmetrical encryption]] [[Asymmetrical Encryption]] [[HMAC (Hash based Message Authentication Codes)]]

# SSH

> SSH (Secure Shell) opens an encrypted login/command channel to a remote host — authenticate with keys, then run shells, tunnels, or file copy.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** TCP connect → agree session crypto → prove who you are (key or password) → you get a shell or a tunnel.

```txt
Client                         Server (sshd)
  │ TCP :22                       │
  ├─ version + host key check ────┤  (known_hosts)
  ├─ KEX → symmetric session ─────┤  ([[symmetrical encryption]])
  ├─ user auth (pubkey) ──────────┤  ([[Asymmetrical Encryption]])
  └─ channels: shell / -L / -R ───┘
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Host key** | Server’s identity key | “Client verifies fingerprint vs known_hosts.” |
| **User key** | Your login credential | “Private stays local; public in `authorized_keys`.” |
| **KEX** | Key exchange | “Builds a shared session key; then symmetric crypto.” |
| **Session cipher** | Bulk encryption | “AES-GCM/chacha — not your long-term SSH key.” |
| **MAC / AEAD** | Integrity | “Detects tampering on the wire.” |
| **Tunnel `-L/-R/-D`** | Port forwarding | “SSH as a poor man’s VPN for one port.” |

### How the story goes (4 steps)

1. **Connect** — TCP to `sshd` (often :22).
2. **Trust host** — compare host key; abort on mismatch (possible MITM).
3. **Secure channel** — KEX → symmetric session; MACs/AEAD on packets.
4. **Authenticate user** — pubkey challenge (or other methods) → open channels.

`ssh-keyscan` only fetches the host key — it does **not** authenticate you and it does **not** prove the host is genuine without an out-of-band fingerprint check.

---

## Standard config / commands

```bash
ssh user@host
ssh -p 2222 user@host
ssh -i ~/.ssh/id_ed25519 user@host
ssh -F ~/.ssh/config -G host     # print effective config
ssh-copy-id user@host

# Connectivity
nc -zv host 22
ssh -vvv user@host               # auth/debug

# Keys
ssh-keygen -t ed25519 -C "you@work"
ssh-keygen -lf ~/.ssh/id_ed25519.pub
ssh-keygen -F github.com         # find known_hosts line

# Host key fetch (verify fingerprint separately!)
ssh-keyscan -p 22 host

# Local / remote forward
ssh -L 8080:localhost:80 user@host
ssh -R 8080:localhost:3000 user@host
```

Server policy: [[sshd config]] (`/etc/ssh/sshd_config`) — `PasswordAuthentication`, `PermitRootLogin`, `AllowUsers`, ciphers.

| Knob | Why it matters |
|------|----------------|
| `IdentityFile` / `-i` | Wrong key → auth failure loop |
| `HostKeyAlgorithms` | Legacy servers need explicit algos |
| `StrictHostKeyChecking` | `no` is a MITM footgun |
| `ProxyJump` / bastion | Corporate entry pattern |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied (publickey) | `-vvv`; which key offered | Right `-i`; pubkey in `authorized_keys`; perms `600/700` |
| Host key verification failed | Someone rotated keys **or** MITM | Verify fingerprint OOB; then update known_hosts |
| Timeout | `nc -zv`; security groups | Open :22/custom; check bind address |
| Works in shell, fails in CI | Missing agent / key | `ssh-agent`; non-interactive `IdentitiesOnly=yes` |
| Tunnel open, app fails | Bound to localhost only | `-L` bind address; remote firewall |

---

## Gotchas

> [!WARNING]
> **Host key ≠ user key.** Trusting the server is separate from logging in as you.

> [!WARNING]
> **`ssh-keyscan` is not verification.** Always compare fingerprints with a trusted source (e.g. GitHub’s published fingerprints).

> [!WARNING]
> **Private key in the repo / AMI** — rotate immediately; use short-lived certs or cloud IAM where possible.

> [!WARNING]
> **Agent forwarding (`-A`)** — convenient and dangerous on untrusted bastions.

---

## When NOT to use

- **Public machine-to-machine APIs** — HTTPS + app auth; don’t expose SSH broadly.
- **Bulk file sync as primary transport** — consider object storage; `scp`/`rsync`-over-SSH for ops, not CDN.
- **Interactive root over password on the open internet** — keys + allowlists + bastion.

---

## Related

[[sshd config]] [[TCP]] [[symmetrical encryption]] [[Asymmetrical Encryption]] [[HMAC (Hash based Message Authentication Codes)]] [[nc]] [[puTTY]] [[ufw]]
