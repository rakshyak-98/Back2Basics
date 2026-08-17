[[commands/lspci]] [[management/Linux resource management]] [[process]]

# nvidia-smi

> Queries NVIDIA GPU driver state — utilization, memory, temperature, and which processes hold the device.





## Interview Relevance
ML/infra interviews: prove you can read GPU memory pressure, find stuck CUDA processes, and diagnose “NVIDIA-SMI has failed” as a driver/module problem.

## Sources
- [NVIDIA SMI documentation](https://docs.nvidia.com/deploy/nvidia-smi/) — deep-dive

## Core Definition
`nvidia-smi` talks to the loaded NVIDIA kernel module. It is part of the NVIDIA driver install on Linux — no module means the CLI fails.

## Key Concepts
- **Utilization vs memory:** a job can be memory-bound with low SM busy %.
- **Process list:** who holds `/dev/nvidia*`.
- **Persistence mode:** keeps driver initialized between jobs.
- **Compute / MIG modes:** exclusivity and partitioning on multi-tenant GPUs.

## Technical Details
```bash
nvidia-smi
watch -n1 nvidia-smi
nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv
nvidia-smi pmon -c 1
fuser -v /dev/nvidia*
sudo nvidia-smi -pm 1
nvidia-smi -c EXCLUSIVE_PROCESS
nvidia-smi -q -d ECC
nvidia-smi mig -lgip
```

| Symptom | Check |
|---------|-------|
| `NVIDIA-SMI has failed` | `lsmod \| grep nvidia`; DKMS build |
| ECC errors | `nvidia-smi -q -d ECC` |
| MIG partitions | `nvidia-smi mig -lgip` (A100/H100 class) |

## Real-World Applications
Find a leaked training process holding VRAM after a crashed notebook, or confirm a new driver loaded after reboot before launching jobs.

## Pros/Cons or Trade-offs
- **Pro:** Single pane for GPU health and process attribution.
- **Con:** NVIDIA-specific; AMD/Intel need different tools (`rocm-smi`, `intel_gpu_top`).

## Comparison
- vs [[commands/lspci]]: hardware presence vs driver runtime metrics.
- vs [[process]]/`top`: CPU view misses GPU memory holders.

## Mistakes to Avoid
- Setting exclusive compute mode on a shared interactive host without warning.
- Debugging CUDA OOMs with only CPU `top`.
- Ignoring driver/DKMS failure when the CLI says it “has failed.”
