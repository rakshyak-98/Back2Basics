**Quick check - list of NVIDIA GPUs in the system**

```bash
nvidia-smi --query-gpu=index,name,pci.bus_id,memory.total --format=csv
```
- this directly tells you the model name for every NVIDIA GPU currently installed.
- this also tells the count of the loaded detected devices

> [!INFO]
> If `nvidia-smi` isn't installed or driver isn't loaded
> ```bash
> lspci -d 10de: -v
> ```
> - filter NVIDIA vendor ID (10de) and show the device name string even without drivers running

**Cross-check against kernel-loaded driver info**

```bash
nvidia-smi -L
```
