[[Operating System]] [[MBR]] [[Persistent Block Storage]] [[cgroup (Control Group)]]

# Logical partitions

> Split one physical machine into isolated OS instances (LPARs) — each gets its own CPU, RAM, and disks from the hypervisor.

---

## Mental model

**Say it in one breath:** Firmware/hypervisor carves hardware into partitions; each boots its own OS and fails mostly independently.

```txt
Physical server
├─ LPAR A  (AIX / Linux)  CPU caps + dedicated RAM
├─ LPAR B
└─ VIOS / hypervisor layer  (I/O virtualization)
```

> Disk “logical partition” (extended/logical *drive* in MBR) is a different meaning — see [[MBR]].

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **LPAR** | Logical partition of a server | “Mainframe/POWER-style hard isolation.” |
| **Hypervisor** | Layer that owns hardware | “Assigns cores, memory, adapters.” |
| **Dedicated vs shared** | Exclusive vs capped pools | “Shared CPU needs entitlement math.” |
| **Dynamic LPAR** | Hot-add resources | “Move RAM/CPU without full outage when supported.” |
| **VIOS** | I/O server partition | “Clients see virtual disks/NICs.” |
| **Disk logical partition** | MBR extended/logical | “Different term — filesystem layout, not LPAR.” |

### How the story goes

1. **Define** — profile: CPU entitlement, RAM, boot disk, network.
2. **Activate** — hypervisor starts the partition.
3. **Boot** — guest OS sees “its” hardware.
4. **Operate** — resize (if supported), migrate, snapshot policy.

---

## Standard config / commands

```bash
# Inside a Linux guest (any virt) — see what you were given
lscpu
free -h
lsblk
# IBM POWER example tooling lives on HMC/PowerVC — not local bash
```

| Knob | Why it matters |
|------|----------------|
| CPU entitlement / capped | Noisy neighbor vs SLA |
| Memory balloon / reserved | Overcommit risk |
| Virtual I/O vs dedicated HBA | Latency / failure domains |
| Boot mode UEFI/BIOS | Image compatibility |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Guest starved | Entitlement / capped shared pool | Raise entitlement; dedicated cores |
| Disk missing after move | VIOS mapping / WWID | Remap LUN; update initramfs |
| “OOM” with free host RAM | Partition memory cap | Add RAM to LPAR; fix guests |
| Network down one LPAR | Virtual switch / VLAN | Fix VIOS SEA / port group |
| Live resize fails | OS/hotplug support | Reboot window; enable balloon drivers |
| Confused with MBR logical | Partition type vs LPAR | Use right note: [[MBR]] |

---

## Gotchas

> [!WARNING]
> **Word collision** — “logical partition” means LPAR *or* MBR logical drive; clarify audience.

> [!WARNING]
> **Shared CPU looks idle** — steal time / entitlement throttling hides under “%idle”.

> [!WARNING]
> **I/O still shared** — VIOS failure can take many LPARs down together.

> [!WARNING]
> **Licensing** — some software keys to physical cores or LPAR IDs.

---

## When NOT to use

- **Simple Linux containers** — [[cgroup (Control Group)]] / pods are enough for app isolation.
- **One app, one cheap VM** — public cloud VM without LPAR ceremony.
- **Need process-level only** — namespaces, not firmware partitions.

---

## Related

[[MBR]] [[Persistent Block Storage]] [[cgroup (Control Group)]] [[UTS namespace]] [[IPC namespace]] [[Take snapshot]]
