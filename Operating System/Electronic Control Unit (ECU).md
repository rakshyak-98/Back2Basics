[[Operating System]] [[analog interface]] [[Data Direction Register (DDR)]] [[bus]]

# Electronic Control Unit (ECU)

> An ECU is an embedded computer that reads sensors and drives actuators in real time — automotive engine control, ABS, or industrial controllers run a specialized OS (often RTOS) on bare metal or a thin POSIX layer.

Unlike a general-purpose PC booting [[Boot/UEFI]] and Linux desktop, an **ECU** typically:

- Runs **deterministic** control loops (milliseconds or microseconds).
- Uses [[analog interface]] and digital [[Data Direction Register (DDR)]] I/O directly.
- Communicates on CAN, LIN, or FlexRay rather than only [[PCI (Peripheral Component Interconnect)]].

## Software stack

```txt
Control algorithm → RTOS scheduler → drivers → MCU hardware
Optional: AUTOSAR, OBD diagnostics, secure boot
```

Resource limits mirror [[cgroup (Control Group)]] ideas but enforced statically at build time — fixed RAM, no swap ([[RAM and Swap memory]] rarely present).

## Sources

- Wikipedia: [Electronic control unit](https://en.wikipedia.org/wiki/Electronic_control_unit)
- AUTOSAR classic platform overview
- Barr Group — embedded systems architecture
