[[Operating System]] [[bus]] [[Electronic Control Unit (ECU)]] [[analog interface]]

# Data Direction Register (DDR)

> On simple microcontrollers, a Data Direction Register sets each GPIO pin as input or output — the firmware-level switch that decides who drives the wire.

**GPIO** (General Purpose I/O) ports group pins. Writing a bit to the **DDR** (direction register) marks the corresponding data register bit as driven by the chip (**output**) or sampled from the pad (**input**). The name “DDR” here is **not** DRAM “Double Data Rate” memory.

```txt
DDR bit = 1 → output (MCU drives pin high/low)
DDR bit = 0 → input  (MCU reads external level)
```

## Operating system angle

Linux on embedded SoCs exposes GPIO through **libgpiod**, sysfs (legacy), or device tree pinctrl. User space rarely maps raw DDR addresses; the kernel’s GPIO subsystem abstracts port and pin numbers.

Contrast [[analog interface]] pins (ADC channels) and [[bus]] peripherals where direction is fixed by protocol (PCIe, I2C).

## Sources

- AVR / ARM Cortex-M vendor reference manuals — GPIO chapters
- Linux kernel documentation: [GPIO Subsystem](https://docs.kernel.org/driver-api/gpio/index.html)
- Wikipedia: [General-purpose input/output](https://en.wikipedia.org/wiki/General-purpose_input/output)
