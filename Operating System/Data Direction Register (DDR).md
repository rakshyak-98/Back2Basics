[[Operating System]] [[bus]] [[Electronic Control Unit (ECU)]] [[analog interface]]

# Data Direction Register (DDR)

> On simple microcontrollers, a Data Direction Register sets each GPIO pin as input or output — the firmware switch that decides who drives the wire.

```txt
        Data Direction Reg ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Embedded / firmware reviews use DDR to check you know GPIO direction, and …

## Sources
- AVR / ARM Cortex-M vendor reference manuals — GPIO chapters — deep-dive
- [Linux kernel docs — GPIO Subsystem](https://docs.kernel.org/driver-api/gpio/index.html) — deep-dive
- [Wikipedia — General-purpose input/output](https://en.wikipedia.org/wiki/General-purpose_input/output) — overview

## Key Concepts
- **GPIO port:** group of pins with a data register and a direction register.
- **DDR bit:** `1` = output (MCU drives); `0` = input (MCU samples the pad).
- **Name collision:** not Double Data Rate memory.
- **OS abstraction:** Linux rarely maps raw DDR; use libgpiod / pinctrl / device tree.

## Technical Details
```txt
DDR bit = 1 → output (MCU drives pin high/low)
DDR bit = 0 → input  (MCU reads external level)
```

- Linux on embedded SoCs exposes GPIO through **libgpiod**, legacy sysfs, or de…
- User space works with chip/line numbers, not raw DDR MMIO, except in bare-met…

## Mistakes to Avoid
- **Mistake:** Confusing GPIO DDR with DDR SDRAM
- **Mistake:** Driving a pin as output while another device also drives the sam…
- **Mistake:** Bit-banging timing-critical buses from Linux user space when a h…

## Pros/Cons or Trade-offs
- **Pro:** Direct, cycle-cheap pin control on MCUs.
- **Con:** Wrong direction can short pads against external drivers.
- **Trade-off:** kernel GPIO abstraction is safer/portable but hides timing-critical bit-banging.

## Comparison
- vs [[analog interface]]: ADC channels measure voltage; DDR is digital direction.
- vs [[bus]] peripherals (I2C, PCIe): direction is fixed by protocol, not a per-pin DDR.


### Use cases
- ECU firmware sets DDR before toggling injectors or reading switches
