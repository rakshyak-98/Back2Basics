[[Linux Key management]] [[management/Linux Key management]] [[process]] [[file mount]] [[keyrings]]

# keyctl

> keyctl manages the Linux kernel key retention service — opaque keys in session/user/process keyrings for NFS, module signing, and OS helpers.





## Interview Relevance
Distinguishes kernel keyutils from apt GPG keyrings / GNOME Keyring — and knows session vs user keyrings, `logon` unreadability.

## Sources
- [keyctl(1)](https://man7.org/linux/man-pages/man1/keyctl.1.html) — deep-dive
- [kernel keys documentation](https://www.kernel.org/doc/html/latest/security/keys/core.html) — deep-dive

## Core Definition
The kernel holds key objects in **keyrings** attached to user, session, process, or thread. User space uses `keyutils` (`keyctl`) to show, add, read (when permitted), timeout, and clear keys. Types include `user`, `logon`, `encrypted`, `asymmetric`, `dns_resolver`.

## Key Concepts
- **Key serial:** Numeric ID for a key object.
- **Session keyring (`@s`):** Per-login; default for many helpers.
- **User keyring (`@u`):** Per-UID across sessions.
- **`logon` keys:** Kernel-only secrets — `keyctl read` fails by design.
- **Not apt/GPG/GNOME:** Different “keyring” words.

## Technical Details
```bash
sudo apt install keyutils

keyctl show
keyctl list @s
keyctl describe 123456789
sudo keyctl read 123456789
keyctl clear @s
keyctl pin @s

sudo keyctl show @u
keyctl get_persistent 0 @u
```

| Type | Typical use |
|------|-------------|
| `logon` | Kernel/initramfs secrets — not userspace-readable |
| `encrypted` | Keys wrapped by master key |
| `asymmetric` | Module sig / IMA/EVM |
| `dns_resolver` | Kernel DNS cache keys |
| `user` | Generic payload; NFS idmap helpers |

| Symptom | Check | Fix |
|---------|-------|-----|
| NFS key expired | `keyctl show` / list `@s` | Remount; `nfsidmap`; `rpc.idmapd` |
| `request_key` upcall failed | `journalctl -k` | Install keyutils; fix helper |
| Module “Required key not available” | keyctl list; secure boot | Enroll signing key / MOK |
| Container empty keyrings | `keyctl show` in ns | Expected — debug inside namespace |

## Real-World Applications
Debugging NFS idmap failures, checking module signature keys, and verifying a session still holds expected kernel credentials after login.

## Pros/Cons or Trade-offs
- **Pro:** OS-integrated short-lived secrets without world-readable files.
- **Con:** Easy to clear the wrong ring; namespace-scoped; opaque errors.
- **Trade-off:** Kernel keyrings for OS contracts vs Vault/KMS for app secrets.

## Comparison
vs [[keyrings]] / apt `signed-by`: Debian package trust files. vs GPG/GNOME Keyring: userspace crypto stores. vs `ssh-add`: SSH agent protocol, not keyctl.

## Mistakes to Avoid
- `keyctl clear @s` on a live login that uses NFS/Kerberos helpers.
- Expecting `keyctl read` on `logon` keys.
- Confusing apt `/usr/share/keyrings` with kernel keyutils.
