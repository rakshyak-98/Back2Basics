[[Linux management]] [[Linux Key management]] [[process]]

# keyctl

> keyctl — linux key retention service holds opaque blobs (keys) in keyrings attached to user, session, process, or thread. User-space sees them via keyutils (keyctl, keyctl(1)).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Linux **key retention service** holds opaque blobs (keys) in **keyrings** attached to user, session, process, or thread. User-space sees them via `keyutils` (`keyctl`, `keyctl(1)`).

```
request_key / add_key / keyctl
         │
         ▼
  ┌──────────────┐     ┌─────────────────┐
  │ session      │────►│ user / process  │──► key serial → description, type, expiry
  │ keyring      │     │ keyrings        │
  └──────────────┘     └─────────────────┘
         │
    nfs.idmap, dns_resolver, asymmetric, logon, encrypted, …
```

| Concept | Meaning |
|---------|---------|
| **Key serial** | Numeric ID for a key object |
| **Keyring** | Container of keys (like a directory) |
| **Key type** | `user`, `logon`, `encrypted`, `asymmetric`, `dns_resolver`, … |
| **Session keyring** | Per-login session; default for `request_key` helpers |

**Do not confuse with:** apt `/usr/share/keyrings/*.gpg` (Debian repository trust) or GNOME Keyring / GnuPG — see [[Linux Key management]] for **OpenSSL/GPG file keys**. `keyctl` is **kernel keyutils**.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **keyring** | In-kernel key store | “Keys can live in kernel, not files.” |
| **keyctl** | Userspace control | “keyctl show / add / pipe.” |
| **session keyring** | Per-login keys | “Gone at logout unless linked.” |
| **user keyring** | Per-UID | “Shared across sessions of user.” |
| **timeout** | Key expiry | “Short-lived creds via keyctl timeout.” |

## Standard config / commands

```bash
# Package (most distros)
sudo apt install keyutils   # Debian/Ubuntu
sudo dnf install keyutils   # RHEL/Fedora

# Show keyrings for current session
keyctl show
# @s  session keyring
#  -3  user keyring
#  -1  thread/process keyring (context-dependent)

# Session for a specific UID (root)
sudo keyctl show @u

# List keys in session ring
keyctl list @s

# Describe one key by serial (from list output)
keyctl describe 123456789

# Read payload (types that permit it — often restricted)
sudo keyctl read 123456789

# Clear session keyring (destructive — know what uses it)
keyctl clear @s

# Pin / unpin (prevent expiry under memory pressure)
keyctl pin @s
```

**Common key types operators see:**

| Type | Typical use |
|------|-------------|
| `logon` | Kernel / initramfs secrets — **not readable from user space** |
| `encrypted` | Keys wrapped by master key in kernel |
| `asymmetric` | Module signature verification, IMA/EVM |
| `dns_resolver` | Kernel DNS cache keys |
| `user` | Generic payload; NFS idmap helpers |

**Persistent keyrings (survive process exit):**

```bash
# Root persistent keyring for UID 0
keyctl get_persistent 0 @u
keyctl show $(keyctl get_persistent 0 @u)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NFS `key expired` / mount auth fails | `keyctl show`; `keyctl list @s` | Re-run `nfsidmap`; remount; check `rpc.idmapd` |
| `request_key: upcall failed` in dmesg | `journalctl -k`; helper `/sbin/request-key` | Install `keyutils`; fix helper timeout |
| Module load `Required key not available` | `keyctl list @s`; MOK/secure boot | Enroll signing key; `mokutil` / distro doc |
| Keys accumulate / memory | `keyctl show` serial count | Expire stale keys; restart session; `keyctl clear` in dev only |
| Container lacks session keyring | `keyctl show` inside namespace | Expected — host keys not visible; debug per-namespace |

```bash
# Kernel messages for key subsystem
dmesg | grep -i key
journalctl -k | grep -i 'request_key\|keyctl'
```

## Gotchas

> [!WARNING]
> **`keyctl clear @s` on a live login** can break NFS, Kerberos tickets cached in kernel, or custom `request_key` workflows until re-authenticated.

- **`logon` keys are intentionally unreadable** — `keyctl read` fails by design.
- **Namespaces:** PID/mount/user namespaces each affect which keyring `@s` refers to — debug from **inside** the failing context.
- **Not SSH agent** — `ssh-add` uses agent protocol; different from kernel keyrings.

## When NOT to use

- **Managing TLS cert files or GPG keys** — use [[Linux Key management]], `gpg`, `openssl`.
- **Storing application secrets in production** — use vault/KMS; kernel keyrings are for OS/integration contracts (NFS, IMA, module sig).
- **Daily password/keyring unlock prompts on GNOME** — that’s **GNOME Keyring** / PAM, not `keyctl` CLI.

## Related

[[Linux Key management]] [[Linux management]] [[process]] [[file mount]]
