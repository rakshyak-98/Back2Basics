[[Linux configuration]] [[file mount]] [[user management]] [[apt config]] [[Linux Templates Directory]] [[loggging]]

# etc files

> `/etc` holds host-local configuration — the authoritative text files operators edit (or template via configuration management) to define how this machine behaves.

```txt
        etc files ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** FHS literacy: know that `/etc` is admin config (not `/usr`), name high-traffi…

## Sources
- [Filesystem Hierarchy Standard — /etc](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html#etcOpt) — overview
- `man 5 hosts`, `man 5 fstab` — deep-dive

## Key Concepts
- **Host-local authority:** This machine’s policy lives here.
- **conffiles:** Package managers merge upgrades carefully — see [[Linux Templates Directory]].
- **Validate then reload:** Prefer `sshd -t` / `nginx -t` before restart.
- **Generated files:** Some paths (often `resolv.conf`) are managed by NetworkManager or systemd-res…


- **Core:** Unlike `/usr` (vendor-shipped), **`/etc` is for local administrators**. Daemo…

## Technical Details
| File / dir | Purpose |
|------------|---------|
| `/etc/fstab` | Filesystem mounts — [[file mount]] |
| `/etc/hosts` | Static name overrides |
| `/etc/resolv.conf` | DNS resolvers (may be managed) |
| `/etc/ssh/sshd_config` | SSH server |
| `/etc/sudoers` | sudo policy — use [[visudo]] |
| `/etc/passwd`, `/etc/shadow` | Users — [[user management]] |
| `/etc/systemd/system/` | Unit overrides — [[system service unit files]] |
| `/etc/apt/` | APT config — [[apt config]] |
| `/etc/environment` | PAM-wide environment |

```bash
sudo cp -a /etc/ssh/sshd_config{,.bak.$(date +%F)}
sudo sshd -t
sudo nginx -t
```

- Do not hand-edit `/etc/ld.so.cache` — run `ldconfig`.
- Fix NetworkManager/resolved config instead of fighting a generated `resolv.co…

## Mistakes to Avoid
- **Mistake:** Editing `/etc/sudoers` with plain vim instead of `visudo` (synta…
- **Mistake:** Changing `resolv.conf` that is a symlink managed by systemd-reso…
- **Mistake:** Editing vendor files under `/usr` “because the package put an ex…

## Pros/Cons or Trade-offs
- **Pro:** Human-readable, diffable, easy to template and audit.
- **Con:** Drift accumulates without configuration management; partial edits leave services in split-brain with drop-ins.

## Comparison
- vs `/usr`: vendor defaults and binaries


### Use cases
- Before opening SSH from a change window: back up `sshd_config`, run `sshd -t`…
