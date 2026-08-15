[[Operating System]] [[analog interface]] [[Data Direction Register (DDR)]] [[bus]] [[Boot/UEFI]] [[PCI (Peripheral Component Interconnect)]] [[cgroup (Control Group)]] [[RAM and Swap memory]]

# Electronic Control Unit (ECU)

> An ECU is an embedded computer that reads sensors and drives actuators in real time — cars, ABS, and industrial controllers often run an RTOS on bare metal or a thin POSIX layer.

## Interview Relevance

Useful for embedded / systems roles: contrast deterministic control loops with general-purpose Linux desktops, and name how I/O and scheduling differ.

## Sources

- [Wikipedia — Electronic control unit](https://en.wikipedia.org/wiki/Electronic_control_unit) — overview
- AUTOSAR classic platform overview — overview
- Barr Group — embedded systems architecture — deep-dive

## Key Concepts

- **Hard timing:** control loops in milliseconds or microseconds.
- **Direct I/O:** [[analog interface]] and digital [[Data Direction Register (DDR)]] pins.
- **Vehicle buses:** CAN, LIN, FlexRay — not only [[PCI (Peripheral Component Interconnect)]].
- **Static resources:** fixed RAM, usually no swap — limits decided at build time.

## Technical Details

Unlike a PC booting [[Boot/UEFI]] and a desktop OS, a typical ECU:

```txt
Control algorithm → RTOS scheduler → drivers → MCU hardware
Optional: AUTOSAR, OBD diagnostics, secure boot
```

Resource isolation ideas resemble [[cgroup (Control Group)]] but are usually compile-time budgets, not dynamic cgroups. [[RAM and Swap memory]] swap is rarely present.

## Real-World Applications

Engine management, brake controllers, and battery-management systems. Industrial PLCs follow the same pattern: sensor → control law → actuator with watchdog resets.

## Pros/Cons or Trade-offs

- **Pro:** Deterministic latency; small trusted computing base.
- **Con:** Hard to update; limited observability vs Linux.
- **Trade-off:** AUTOSAR/middleware portability vs bare-metal simplicity.

## Comparison

- vs general-purpose OS: ECUs optimize worst-case latency; desktops optimize throughput and compatibility.
- vs [[Boot/UEFI]] PCs: firmware + OS stack is far heavier than MCU reset vectors.

## Mistakes to Avoid

- Assuming Linux desktop scheduling guarantees for closed-loop control without PREEMPT_RT / careful design.
- Ignoring watchdog and brown-out behavior in failure analysis.
- Treating CAN like Ethernet TCP — different reliability and timing models.
