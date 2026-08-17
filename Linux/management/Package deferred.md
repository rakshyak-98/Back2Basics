[[Package Manager]] [[apt package manager]] [[commands/APT policy]] [[apt config]]

# Package deferred

> Held or pinned packages skip unwanted upgrades — protect production pins, kernels, or a carefully tested version.





## Interview Relevance
`apt-mark hold` vs preferences pins, reading `apt-cache policy`, and auditing forgotten holds that skip security updates.

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

## Real-World Applications
Hold `kubelet`/`kubectl` across a control-plane upgrade window, then unhold after the change succeeds.

## Pros/Cons or Trade-offs
- **Pro:** Stable production versions under active change control.
- **Con:** Holds fight security baselines if left forever.

## Comparison
- vs tracking distro closely: prefer fewer holds and faster patching.
- vs container rebuilds: rebuild images instead of holding host packages when possible.

## Mistakes to Avoid
- Never auditing `apt-mark showhold`.
- Pin-Priority mistakes that leave no valid candidate.
- Assuming `dist-upgrade` always honors intent without reading the plan.
