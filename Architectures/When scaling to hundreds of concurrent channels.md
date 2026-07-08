| **Resource Type** | **Bottleneck Point**        | **Scaling Consideration**                                                                                                                                                          |
| ----------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CPU/Kernel**    | Interrupt Handling          | High packet rates for 300 channels can trigger excessive CPU interrupts. Use **RSS (Receive Side Scaling)** and **IRQ Affinity** to pin network traffic to specific CPU cores.     |
| **GPU/ASIC**      | Hardware Encoder Throughput | Each of the 300 channels requires a slice of the NVENC engine. If the aggregate bitrate or resolution exceeds the hardware clock speed, the encoder will stall.                    |
| **Memory**        | Kernel Socket Buffers       | Each open connection requires space in the OS network stack. With 300+ streams, tune `/proc/sys/net/core/rmem_max` and `wmem_max` to prevent buffer overflows during micro-bursts. |
|                   |                             |                                                                                                                                                                                    |

### Measurements
- Socket monitoring use `ss -ntu` to count active established connections.
- Hardware monitoring use `nvidia-smi dmon -s u` to monitor Encoder Utilization `enc` and decoder utilization `dec`.

> [!NOTE]
> Even if the GPU utilization `gpu` is low, the `enc` column will show the actual pressure on the video engine

- Context management -> If you are using FFmpeg, every `ffpmpeg -i ...` command initiates a new process, which consumes memory and overhead. To hit 300 channels efficiently, you must move to a multi-threading or single process model using the NVIDIA Video SDK directly, or an optimized pipeline like GStreamer with `nvv4l264enc`