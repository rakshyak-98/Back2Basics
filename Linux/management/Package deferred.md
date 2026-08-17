[[Package Manager]] [[apt package manager]] [[commands/APT policy]] [[apt config]]

# Package deferred

> Held or pinned packages skip unwanted upgrades — protect production pins, kernels, or a carefully tested version.

```txt
        Package deferred ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** `apt-mark hold` vs preferences pins, reading `apt-cache policy`, and auditing…

## Sources
- [apt_preferences(5)](https://manpages.debian.org/bookworm/apt/apt_preferences.5.en.html) — deep-dive
- [man apt-mark](https://manpages.debian.org/bookworm/apt/apt-mark.8.en.html) — overview

## Key Concepts
- **hold:** blunt do-not-upgrade mark.
- **pin:** precise candidate selection via `Pin-Priority`.
- **candidate:** version apt would install now.
- **Invisible debt:** forgotten holds skip security fixes.

## Technical Details
```txt
apt upgrade ──skips──► held packages
apt preferences ──► candidate version selection
```

```bash
apt-mark hold kubelet kubectl
apt-mark showhold
apt-mark unhold kubelet
apt-cache policy kubelet
```

```
# /etc/apt/preferences.d/kube
Package: kubelet
Pin: version 1.29.*
Pin-Priority: 1001
```

| Knob | Why it matters |
|------|----------------|
| Pin-Priority ≥1000 | Force pin even if newer exists |
| hold vs pin | hold is blunt; pin is precise |

| Symptom | Check | Fix |
|---------|-------|-----|
| Package “kept back” | hold/pin | `showhold`; read preferences.d |
| Security update skipped | Forgotten hold | Unhold; schedule upgrade |
| Manual dpkg overwrote | Direct install | Re-apply pin; document |
| Unattended-upgrades ignores intent | Config | Align origins/holds |

## Mistakes to Avoid
- **Mistake:** Never auditing `apt-mark showhold`
- **Mistake:** Pin-Priority mistakes that leave no valid candidate
- **Mistake:** Assuming `dist-upgrade` always honors intent without reading the…

## Pros/Cons or Trade-offs
- **Pro:** Stable production versions under active change control.
- **Con:** Holds fight security baselines if left forever.

## Comparison
- vs tracking distro closely: prefer fewer holds and faster patching.
- vs container rebuilds: rebuild images instead of holding host packages when possible.


### Use cases
- Hold `kubelet`/`kubectl` across a control-plane upgrade window, then unhold a…
