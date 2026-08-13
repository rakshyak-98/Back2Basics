[[commands/lspci]] [[management/Linux resource management]]

# nvidia-smi

> `nvidia-smi` queries NVIDIA GPU driver state — utilization, memory, temperature, and processes using the device.

Requires proprietary or open NVIDIA kernel module loaded. Part of NVIDIA driver install on Linux.

## Quick status

```bash
nvidia-smi
watch -n1 nvidia-smi

# Query fields
nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv
```

## Processes on GPU

```bash
nvidia-smi pmon -c 1
fuser -v /dev/nvidia*
```

## Persistence / compute mode

```bash
sudo nvidia-smi -pm 1
nvidia-smi -c EXCLUSIVE_PROCESS   # caution in shared hosts
```

## Troubleshooting

| Symptom | Check |
|---------|-------|
| `NVIDIA-SMI has failed` | Driver not loaded: `lsmod | grep nvidia`; DKMS build |
| ECC errors | `nvidia-smi -q -d ECC` |
| MIG partitions | `nvidia-smi mig -lgip` (A100/H100 class) |

## Related

[[commands/lspci]] · [[process]]

## Sources

- [NVIDIA SMI documentation](https://docs.nvidia.com/deploy/nvidia-smi/)
