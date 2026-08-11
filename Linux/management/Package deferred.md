[[management]] [[Package Manager]] [[apt package manager]]

# Package deferred

> Deferred/held packages skip upgrades until you say so — protect prod pins, kernel, or a carefully tested version.

---

## Mental model

**Say it in one breath:** `apt-mark hold` blocks APT upgrades; preferences pins prefer a version; neither stops manual `dpkg -i`.

```txt
apt upgrade ──skips──► held packages
apt preferences ──► candidate version selection
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **hold** | Mark do-not-upgrade | “`apt-mark hold docker-ce`.” |
| **pin** | Priority in preferences | “Numeric priority picks candidate.” |
| **candidate** | Version apt would install | “`apt-cache policy`.” |
| **unhold** | Allow upgrades again | “After change window.” |
| **dist-upgrade** | May still fight holds | “Read the plan before yes.” |

---

## Standard config / commands

```bash
apt-mark hold kubelet kubectl
apt-mark showhold
apt-mark unhold kubelet
# /etc/apt/preferences.d/kube
# Package: kubelet
# Pin: version 1.29.*
# Pin-Priority: 1001
apt-cache policy kubelet
```

| Knob | Why it matters |
|------|----------------|
| Pin-Priority ≥1000 | Force pin even if newer exists |
| hold vs pin | hold is blunt; pin is precise |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Package “kept back” | hold/pin | `showhold`; read preferences.d |
| Security update skipped | Forgotten hold | Unhold; schedule upgrade |
| Manual dpkg overwrote | Direct install | Re-apply pin; document |
| Unattended-upgrades ignores intent | Config | Align origins/holds |

---

## Gotchas

> [!WARNING]
> **Holds are invisible debt** — audit `showhold` in reviews.

> [!WARNING]
> **Pin-Priority mistakes** can make apt prefer an empty candidate set.

---

## When NOT to use

- **Tracking distro closely** — holds fight security baselines.
- **Containers** — rebuild images instead of holding host packages.

---

## Related

[[Package Manager]] [[apt package manager]] [[apt configuration]] [[APT policy]]
