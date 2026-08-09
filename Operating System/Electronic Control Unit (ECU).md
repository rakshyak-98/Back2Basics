[[Operating System]] [[Data Direction Register (DDR)]] [[bus]] [[analog interface]]

# Electronic Control Unit (ECU)

> An ECU is a small computer in a vehicle/machine that runs one job — engine, brakes, transmission — over real-time buses.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Sensors in → MCU firmware decides → actuators out; peers talk CAN/LIN/FlexRay/Automotive Ethernet.

```txt
Sensors ──► ECU (MCU + firmware) ──► Actuators
               │
               └── vehicle bus ──► other ECUs (TCU, ABS, …)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ECU** | Electronic Control Unit | “Domain controller for one vehicle function.” |
| **TCU** | Transmission Control Unit | “ECU that shifts gears.” |
| **CAN** | Controller Area Network | “Multi-master bus for ECU traffic.” |
| **DTCs** | Diagnostic trouble codes | “What OBD-II reports when something fails.” |
| **Flash** | Reflash firmware | “Dealer/CI updates the ECU image.” |
| **ASIL** | Safety integrity level | “How hard failure modes are mitigated.” |

### How the story goes

1. **Sense** — ADC/GPIO/bus inputs.
2. **Control** — periodic tasks / ISRs with deadlines.
3. **Actuate** — drive outputs safely (watchdogs).
4. **Diagnose** — log DTCs; talk UDS/OBD off-board.

---

## Standard config / commands

```bash
# Host-side diagnostics (examples; toolchain varies)
# candump can0
# iso14229 / UDS client against ECU
# Vendor flashing utilities — never "dd" a random image in the field
```

| Knob | Why it matters |
|------|----------------|
| Bus termination | CAN signal integrity |
| Cycle time / deadlines | Missed frames → limp mode |
| Calibration maps | Performance vs emissions |
| Secure boot / signing | Prevent unauthorized firmware |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Limp mode | DTCs / freeze frame | Sensor, wiring, reflash if corrupt |
| Bus-off CAN | Errors / termination | Fix wiring; 120Ω ends; noise |
| No comms after update | Wrong image / brick | Recovery bootloader / bench flash |
| Intermittent actuator | Ground / supply sag | Power integrity; connectors |
| One ECU floods bus | Babbling idiot | Gateway filter; isolate node |
| TCU harsh shifts | Calibration / temp | Adaptations; fluid; software map |

---

## Gotchas

> [!WARNING]
> **ECU ≠ general server** — no MMU comfort; bugs are physical safety issues.

> [!WARNING]
> **Flashing risk** — power loss mid-write can brick; use qualified procedures.

> [!WARNING]
> **Security** — unsigned diagnostic access is a fleet risk; gate UDS.

> [!WARNING]
> **“TCU” vs “ECU”** — TCU is a kind of ECU, not a rival acronym.

---

## When NOT to use

- **Phone apps / cloud backends** — different reliability model.
- **Soft PLC on a laptop** — not a substitute for certified vehicle ECUs.
- **GPIO toys without safety case** — hobby MCU ≠ automotive ECU process.

---

## Related

[[Data Direction Register (DDR)]] [[bus]] [[analog interface]] [[opcode]] [[system bus]] 
