[[Operating System]] [[bus]] [[system bus]] [[PCI (Peripheral Component Interconnect)]] [[Electronic Control Unit (ECU)]]

# Analog interface

> An analog interface moves continuously varying physical quantities — voltage, current, pressure — across the boundary between the real world and digital logic the operating system can schedule.

Digital computers store discrete bits. Sensors and actuators in the physical world are analog. An **analog interface** (often an ADC or DAC plus conditioning circuitry) samples or drives those signals so firmware and drivers can treat them as numbers.

## Signal path

```txt
Physical quantity → sensor → amplifier/filter → ADC → digital bus → driver → user space
User command      → DAC  → actuator → physical effect
```

On a general-purpose PC, analog work often lives on dedicated chips (audio codec, temperature sensor on the SMBus). On embedded targets such as an [[Electronic Control Unit (ECU)]], analog I/O may be the primary reason the microcontroller exists.

## Operating system view

The kernel exposes analog-backed devices as **character devices**, **Industrial I/O (IIO)** channels, or platform-specific ioctls. User space reads structured samples (`read()`, `read()` on `/dev/iio:device0`) rather than raw pin voltages. Timing and sample rate are constrained by the [[bus]] bandwidth and interrupt latency — not by how fast a loop can spin in Python.

## Contrast with digital I/O

[[Data Direction Register (DDR)]] style GPIO is on/off. Analog interfaces deal with resolution (bits of ADC), sampling rate, noise, and calibration. Choosing the wrong interface type — treating a slow analog sensor as a digital edge — loses information or adds aliasing.

## Sources

- Wikipedia: [Analog-to-digital converter](https://en.wikipedia.org/wiki/Analog-to-digital_converter)
- Linux kernel documentation: [Industrial I/O](https://docs.kernel.org/driver-api/iio/index.html)
- Horowitz & Hill, *The Art of Electronics* — ADC/DAC fundamentals
