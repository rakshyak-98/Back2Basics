[[PCI (Peripheral Component Interconnect)]] [[system bus]] [[Electronic Control Unit (ECU)]]

# Analog interface

> Connection that carries continuously varying signals (voltage, current, pressure) — contrast with digital discrete levels (0/1).

---

## Mental model

**Analog** = infinite resolution in theory; **quantized noise and drift** in practice. **Digital** = sampled, encoded bits with defined noise margin.

```txt
Real world          Analog front-end           Digital domain
──────────          ────────────────           ──────────────
sound wave    →     mic + preamp        →     ADC → PCM samples
temperature   →     thermistor divider  →     ADC → uint16
radio carrier →     mixer / IF strip    →     demod → bits
```

Engineering concerns:
- **SNR** — noise floor vs signal
- **Bandwidth** — Nyquist: sample ≥ 2× highest frequency
- **Linearity** — gain errors across range
- **Ground loops** — shared return paths inject hum

Embedded / SBC paths: GPIO is **digital**; ADC pins (e.g. `/sys/bus/iio`) read **analog** after on-chip ADC.

---

## Standard config / commands

### Linux IIO (Industrial I/O) — read ADC

```bash
# Find device
ls /sys/bus/iio/devices/
cat /sys/bus/iio/devices/iio:device0/in_voltage0_raw
cat /sys/bus/iio/devices/iio:device0/in_voltage_scale
# millivolts ≈ raw * scale
```

### ALSA capture (analog audio path)

```bash
arecord -l                    # hardware cards
arecord -D hw:0,0 -f S16_LE -r 44100 -c 2 test.wav
```

### Scope / sanity (lab)

```bash
# Not CLI — use oscilloscope for analog integrity
# Check: clipping, DC offset, ringing on lines
```

**Why differential pairs:** USB Ethernet, audio balanced XLR reject common-mode noise vs single-ended GPIO-adjacent wiring.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Noisy sensor readings | ADC reference voltage; long wire antenna | Shielding; ferrite; hardware filter; oversample + median |
| Saturated / flat signal | Input exceeds Vref | Attenuator; gain stage; different range |
| 50/60 Hz hum | Ground loop | Star ground; isolation amp; USB isolator |
| Audio crackle on SBC | CPU EMI on analog rail | Separate analog supply; ferrite on mic line |

---

## Gotchas

> [!WARNING]
> **Floating analog inputs pick up garbage** — enable pull-down/up or terminate properly.

> [!WARNING]
> **Software can't fix aliasing** — anti-alias filter before ADC is hardware's job.

> [!WARNING]
> **"Digital sensor" often has analog front-end** — I2C temperature chip still analog die inside.

---

## When NOT to use

Don't run long analog runs next to switching power supplies or motor drivers — convert to digital **close to the sensor** (local ADC, CAN, I2C) and run digital back to the host.

---

## Related

[[Data Direction Register (DDR)]] [[Electronic Control Unit (ECU)]] [[system bus]] [[PCI (Peripheral Component Interconnect)]]
