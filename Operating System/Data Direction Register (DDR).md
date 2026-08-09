[[Operating System]] [[bus]] [[analog interface]] [[Electronic Control Unit (ECU)]]

# Data Direction Register (DDR)

> DDR bits set each MCU GPIO pin as input or output — `1` drives the pin, `0` reads it.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Per-port register (e.g. `DDRB`); each bit owns one pin’s direction before you read `PIN*` or write `PORT*`.

```txt
DDRB bit2 = 1  →  PB2 is OUTPUT  (PORTB drives level)
DDRB bit2 = 0  →  PB2 is INPUT   (PINB samples; pull-ups optional)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **DDR** | Data Direction Register | “Configures GPIO in vs out.” |
| **PORT** | Output data / pull-up control | “Write levels when pin is output.” |
| **PIN** | Input sample register | “Read actual voltage level.” |
| **GPIO** | General-purpose I/O pin | “Bit-banged peripherals live here.” |
| **Pull-up** | Weak high when input | “Avoid floating inputs.” |
| **Alt function** | Pin mux to UART/SPI/… | “DDR alone isn’t enough if muxed away.” |

### How the story goes

1. **Mux** — assign pin to GPIO (not alternate peripheral) if required.
2. **Direction** — set DDR bit.
3. **Level / pull** — set PORT for output level or input pull-up.
4. **Use** — read PIN or toggle PORT in the app/ISR.

---

## Standard config / commands

```c
// AVR-style (ATmega328): PB2 as output high
DDRB |= (1 << DDB2);
PORTB |= (1 << PORTB2);

// PB3 as input with pull-up
DDRB &= ~(1 << DDB3);
PORTB |= (1 << PORTB3);
uint8_t v = PINB & (1 << PINB3);
```

| Knob | Why it matters |
|------|----------------|
| DDR bit | In vs out |
| PORT on input | Pull-up enable (classic AVR) |
| Pin mux / AFR | Peripheral steals the pin |
| Drive strength / slew | Signal integrity (ARM etc.) |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Pin stuck / no drive | DDR still 0 | Set direction before write |
| Random input values | Floating pin | Enable pull-up or external bias |
| Peripheral silent | Mux still GPIO or wrong AFR | Configure alternate function |
| Smoke / short | Two drivers fight | Never both sides push without open-drain plan |
| Works on reset only | Init order | Set DDR in early init, not after use |
| Wrong port letter | Board silkscreen vs MCU | Read schematic + datasheet |

---

## Gotchas

> [!WARNING]
> **DDR ≠ DDR memory** — same acronym; this note is GPIO direction, not DRAM.

> [!WARNING]
> **Read PIN, not PORT, for inputs** — PORT may show pull-up intent, not pad level (device-dependent).

> [!WARNING]
> **Reset defaults** — many MCUs start as inputs; don’t assume outputs after brown-out.

> [!WARNING]
> **5 V vs 3.3 V** — direction alone doesn’t make levels safe; use level shifters.

---

## When NOT to use

- **Bit-bang when hardware UART/SPI exists** — use the peripheral.
- **High-speed buses** — DDR GPIO won’t meet timing; use dedicated controllers.
- **Linux SBC “GPIO”** — sysfs/`libgpiod` abstracts registers; don’t poke DDR from userland casually.

---

## Related

[[bus]] [[Electronic Control Unit (ECU)]] [[analog interface]] [[opcode]] [[system bus]]
