[[Commands]] [[apt package manager]] [[apt config]] [[source list file]] [[gpg]]

# APT policy

> apt policy shows which versions exist, where they come from, and which pin priority wins — so you know what apt will install next.





## Interview Relevance
Debian/Ubuntu packaging: Candidate vs Installed, priority 100 vs 500, and how preferences.d pins steer upgrades.

## Sources
- [apt_preferences(5)](https://manpages.debian.org/apt_preferences.5) — deep-dive
- [apt(8)](https://manpages.debian.org/apt.8) — overview

## Core Definition
`apt policy pkg` prints Installed, **Candidate** (what the next install/upgrade would pick), and a version table with **pin priorities** and origins. Trust **Candidate** for install decisions — not a random `apt-cache show` line.

## Key Concepts
- **Candidate:** Resolver’s chosen version.
- **Priority 100:** Installed / dpkg status — loses to normal repo 500 on upgrade.
- **500:** Default archive/PPA priority.
- **≥1000:** Can force downgrades — dangerous.
- **Pinning:** `/etc/apt/preferences.d/` rules to prefer an origin.

## Technical Details
```txt
apt policy pkg
  Installed: …
  Candidate: …     ← next upgrade/install
  Version table:
     1.2.3 500
 *** 1.1.0 100     ← *** = currently installed
```

| Priority | Typical meaning |
|----------|-----------------|
| 100 | Installed (status file) |
| 500 | Default from repositories |
| 990 | `APT::Default-Release` target |
| 1–99 | Soft-pin / never auto-upgrade onto |
| >1000 | Force even downgrade |

```bash
apt policy
apt policy nginx
apt-cache policy nginx
apt list -a nginx
```

Pin files: `/etc/apt/preferences`, `/etc/apt/preferences.d/` — see [[apt config]].

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong version keeps winning | `apt policy pkg` | Adjust pin / disable conflicting repo |
| Security fix not candidate | Candidate origin | Enable `-security`; `apt update` |
| Hold ignored? | `apt-mark showhold` | Hold ≠ pin; use both deliberately |
| Mystery 990 | Default-Release | Check apt.conf.d |

## Real-World Applications
Explaining why a PPA nginx upgrades over Ubuntu’s, pinning a vendor package, and debugging “apt wants to downgrade.”

## Pros/Cons or Trade-offs
- **Pro:** Transparent resolver view across multiple origins.
- **Con:** Pins >1000 and conflicting origins are easy to misuse.
- **Trade-off:** Stay on distro packages vs third-party freshness.

## Comparison
vs [[source list file]]: sources define *where*; policy decides *which version*. vs `apt-mark hold`: hold blocks upgrades; pins steer choice. vs dnf/yum: different stack.

## Mistakes to Avoid
- Assuming Installed (100) always beats repo (500).
- Using priority >1000 without a downgrade plan.
- Trusting `apt-cache show` over policy Candidate for “what will install.”
