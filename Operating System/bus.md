[[Operating System]] [[system bus]] [[PCI (Peripheral Component Interconnect)]] [[Data Direction Register (DDR)]]

# Bus

> A bus is a shared communication pathway — address, data, and control lines — that lets the CPU, memory, and devices exchange bytes under a defined protocol.

Early machines used parallel **system buses**. Modern PCs nest specialized buses: processor ↔ memory links (QPI/UPI), chipset **PCIe** ([[PCI (Peripheral Component Interconnect)]]), USB, I2C/SMBus for sensors. Operating systems discover devices via enumeration (ACPI tables, PCI config space) and attach **drivers** that speak each protocol.

## Bus versus network

Both move packets, but a **bus** is local, low-latency, and electrically shared or switched inside one machine. Latency and ordering rules differ from Ethernet ([[TCP]] rides on NICs attached via PCIe).

## Embedded view

Microcontrollers expose GPIO with a [[Data Direction Register (DDR)]] per port — pin direction on a simple parallel bus. [[Electronic Control Unit (ECU)]] firmware bit-bangs or uses CAN/LIN buses rather than PCIe.

## Performance symptoms

Bus contention shows as **stalls**: DMA fighting CPU memory bandwidth, GPU copying over PCIe, or too many small MMIO reads. Tools: `perf`, `lspci -vv`, hardware counters — not only application profilers.

See [[system bus]] for the CPU–memory–I/O triangle.

## Sources

- Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*
- Wikipedia: [Computer bus](https://en.wikipedia.org/wiki/Computer_bus)
- Linux: `lspci`, PCI subsystem documentation
