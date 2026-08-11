[[commands]] [[apt package manager]] [[apt configuration]]

# APT policy

> `apt policy` shows which versions exist, where they come from, and which pin priority wins — so you know *what apt will install next*.

---

## Mental model

**Say it in one breath:** higher pin priority wins; installed packages sit at 100; repos usually 500; pins in `preferences` can force or hold versions.

```txt
apt policy pkg
  Installed: …
  Candidate: …     ← what the next upgrade/install would pick
  Version table:
     1.2.3 500     ← priority + origin
 *** 1.1.0 100     ← *** marks currently installed
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Candidate** | Version apt would choose | “Policy’s Candidate is the resolver’s answer.” |
| **Priority 100** | Installed / dpkg status | “Installed isn’t automatically preferred over a 500 repo.” |
| **500** | Normal repo pin | “Default archive priority.” |
| **≥1000** | Force even downgrades | “Dangerous pin — can yank you backward.” |
| **Pinning** | preferences.d rules | “How we stay on nginx from the PPA.” |

### Priority cheat sheet

| Priority | Typical meaning |
|----------|-----------------|
| **100** | Installed (status file) |
| **500** | Default from repositories / PPAs |
| **990** | `APT::Default-Release` target |
| **1–99** | Soft-pin / never auto-upgrade onto |
| **>1000** | Force install even if downgrade |

---

## Standard config / commands

```bash
apt policy
apt policy nginx

# Example reading
# nginx:
#   Installed: 1.18.0-0ubuntu1
#   Candidate: 1.21.0-1+ubuntu20.04
#   Version table:
#      1.21.0-1+ubuntu20.04 500
#         500 http://ppa.../nginx/stable/...
#  *** 1.18.0-0ubuntu1 100
#         100 /var/lib/dpkg/status
```

Pin files: `/etc/apt/preferences`, `/etc/apt/preferences.d/` — see [[apt configuration]].

```bash
apt-cache policy nginx    # older synonym-ish via apt-cache
apt list -a nginx         # all known versions
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong version keeps winning | `apt policy pkg` | Adjust pin / disable conflicting repo |
| Upgrade never picks installed security fix | Candidate origin | Enable `-security` pocket; refresh `apt update` |
| Hold ignored? | `apt-mark showhold` | Hold ≠ pin; use both deliberately |
| Mystery 990 | Default-Release set | Check apt.conf.d |
| “But apt-cache show says…” | Different code paths | Trust **policy Candidate** for install decisions |

---

## Gotchas

> [!WARNING]
> **Installed at 100 loses to repo at 500** — that is why upgrades replace the local version.

> [!WARNING]
> **Pins >1000 can downgrade** — use only with a written rollback plan.

> [!WARNING]
> **Multiple origins same version** — priority *and* order matter; policy shows the truth.

---

## When NOT to use

- **Searching package names** — `apt search` / `apt-cache search`.
- **Reading changelogs** — `apt changelog`.
- **dnf/yum systems** — different stack.

---

## Related

[[apt package manager]] [[apt configuration]] [[gpg]] [[commands]]
