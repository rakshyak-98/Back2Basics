[[Operating System]] [[system bus]] [[PCI (Peripheral Component Interconnect)]] [[Data Direction Register (DDR)]] [[Electronic Control Unit (ECU)]] [[TCP]]

# Bus

> A bus is a shared communication pathway — address, data, and control — that lets the CPU, memory, and devices exchange bytes under a defined protocol.





## Interview Relevance
Hardware/systems questions: PCIe vs memory fabric vs I2C, how the OS enumerates devices, and how bus contention shows up as stalls.

## Sources
- Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* — deep-dive
- [Wikipedia — Computer bus](https://en.wikipedia.org/wiki/Computer_bus) — overview
- Linux PCI subsystem documentation / `lspci` — deep-dive

## Key Concepts
- **Shared pathway + protocol:** who may drive the lines and when.
- **Modern nesting:** CPU↔memory links, chipset [[PCI (Peripheral Component Interconnect)]], USB, I2C/SMBus.
- **Discovery:** ACPI tables, PCI config space → driver bind.
- **Local vs network:** bus is in-machine; Ethernet is off-NIC ([[TCP]] rides PCIe NICs).

## Technical Details
Early machines used parallel **system buses**. Today specialized fabrics replace one giant parallel bus.

Embedded: GPIO via [[Data Direction Register (DDR)]]; [[Electronic Control Unit (ECU)]] firmware uses CAN/LIN more than PCIe.

Symptoms of contention: DMA fighting CPU memory bandwidth, GPU copies over PCIe, chatty MMIO. Tools: `perf`, `lspci -vv`, hardware counters.

See [[system bus]] for the CPU–memory–I/O triangle.

## Real-World Applications
Attaching NICs/GPUs/NVMe on PCIe, reading motherboard sensors on SMBus, and automotive ECUs on CAN.

## Pros/Cons or Trade-offs
- **Pro:** Standard discovery and driver model.
- **Con:** Shared bandwidth; topology/NUMA complexity.
- **Trade-off:** more lanes/generations vs power and platform cost.

## Comparison
- vs [[system bus]]: system bus is the CPU–memory–I/O interconnect story; “bus” is the general term.
- vs network links: different latency, sharing, and failure domains.

## Mistakes to Avoid
- Profiling only the app while PCIe link trains degraded.
- Treating I2C sensor buses like high-bandwidth data paths.
- Ignoring IOMMU/ACS when planning device passthrough.
