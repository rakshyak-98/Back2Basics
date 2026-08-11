[[base clock speed]] [[SMT threads]] [[CPU IO Bound Task]] [[Linux]]

# TDP

> Thermal Design Power — watts of heat the cooling solution must dissipate at the vendor's reference workload; not peak power, not idle power.

---

## Mental model

**TDP** is a **cooling design label**, not a hard electrical cap:

```txt
Marketing TDP 65W     →  heatsink/fan sized for sustained ~65W heat
Actual under AVX load →  may exceed TDP briefly (PL2 turbo)
Actual idle           →  far below TDP
```

Relates to **[[base clock speed]]** — all-core base assumes CPU stays within TDP at stock cooler. Laptops and datacenters **power-limit** CPUs below or above sticker TDP via BIOS/ACPI/cgroup.

**Service impact:** dense VMs on oversubscribed hosts — neighbor turbo steals power budget; sustained builds throttle when package temperature hits TJmax.

---

## Standard config / commands

### Read power / throttle signals

```bash
# Intel RAPL (if exposed)
sudo apt install linux-tools-common linux-tools-$(uname -r)
sudo turbostat --Summary --show PkgWatt,RAMWatt,Core,CPU,Busy% 1

# AMD similar via amd_energy or hwmon
cat /sys/class/hwmon/hwmon*/power*_cap
cat /sys/class/hwmon/hwmon*/temp*_input
```

### Throttle check

```bash
dmesg | grep -i 'thermal\|thrott'
journalctl -k | grep -i throttle
```

### Cloud / VM

```bash
# Often no RAPL — infer from CPU credit or perf drop
lscpu
# Compare benchmark under load vs idle
```

**Why care in K8s:** Bursty jobs on same node raise package temp → **shared frequency drop** for all pods on socket.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Performance cliff after minutes | Thermal throttle | Improve airflow; repaste; lower PL1; spread load |
| Laptop fans spin under "light" load | Background AVX (browser, ML lib) | Power profile balanced; limit threads |
| Datacenter hot aisle | Inlet temp > spec | Fix CRAC; blanking panels; workload shift |
| Spec TDP vs bill mismatch | Actual draw >> TDP label | Size PSU/cooling to **measured** peak, not sticker |

---

## Gotchas

> [!WARNING]
> **TDP numbers aren't comparable across vendors** — Intel 125W ≠ AMD 105W methodology.

> [!WARNING]
> **"Configurable TDP" (cTDP)** — same SKU, different power modes in BIOS.

> [!WARNING]
> **VMs hide physical TDP** — noisy neighbor is thermal/power contention, not your cgroup CPU limit alone.

---

## When NOT to use

Don't size datacenter power purely on summed CPU TDP labels — measure **actual rack draw** (PDU meters) including memory, NICs, and GPUs.

---

## Related

[[base clock speed]] [[SMT threads]] [[CPU IO Bound Task]] [[Linux cgroup]] [[context switching]]
