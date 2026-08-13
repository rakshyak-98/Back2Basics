<!-- note-strategy: operational -->
[[Linux]] [[lspci]] [[OOM (Linux Out Of Memory)]]

# nvidia-smi

> nvidia-smi queries the NVIDIA driver for GPU health — utilization, VRAM, processes, power/ECC.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** smi talks to the driver — if it works, the module is loaded; VRAM OOM ≠ host OOM.

```txt
nvidia-smi ──► NVIDIA kernel driver ──► GPU
                 │
                 └─ PIDs holding GPU memory
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **nvidia-smi** | Driver management CLI | “First check when GPU jobs ‘vanish’.” |
| **VRAM** | GPU framebuffer memory | “GPU OOM is not host OOM.” |
| **persistence mode** | Keep driver warm | “Cuts init latency on servers.” |
| **MIG** | Multi-instance GPU | “Slice one A100 into several.” |
| **ECC** | Error-correcting memory | “Data-center cards report ECC counts.” |

---

## Standard config / commands

```bash
nvidia-smi
nvidia-smi -L
nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv
nvidia-smi -pm 1
# drain jobs first:
sudo nvidia-smi -r
```

| Knob | Why it matters |
|------|----------------|
| `-pm 1` | Persistence for servers |
| `--query-gpu` | Scriptable CSV metrics |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NVIDIA-SMI has failed | Module/driver | `lsmod \| grep nvidia`; reinstall matching driver |
| CUDA mismatch | Driver vs toolkit | Driver must be ≥ CUDA need |
| VRAM full | Zombie PID in smi | Kill PID; `fuser -v /dev/nvidia*` |
| No devices | PCI/passthrough | `lspci \| grep -i nvidia` |

---

## Gotchas

> [!WARNING]
> **Needs the NVIDIA driver** — nouveau does not speak this interface.

> [!WARNING]
> **Reset while jobs run** corrupts workloads — drain first.

---

## When NOT to use

- **AMD/Intel GPUs** — `rocm-smi` / `intel_gpu_top`.
- **CPU-only CI** — skip or mock; don’t require smi in unit tests.

---

## Related

[[lspci]] [[OOM (Linux Out Of Memory)]] [[Linux resource management]]
