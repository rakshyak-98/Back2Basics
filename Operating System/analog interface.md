[[Operating System]] [[bus]] [[system bus]] [[PCI (Peripheral Component Interconnect)]] [[Electronic Control Unit (ECU)]] [[Data Direction Register (DDR)]]

# Analog interface

> An analog interface moves continuously varying physical quantities — voltage, current, pressure — across the boundary between the real world and digital logic the OS can schedule.





## Interview Relevance
Embedded interviews: ADC/DAC path, why sample rate and resolution matter, and how Linux IIO differs from bit-banged GPIO.

## Sources
- [Wikipedia — Analog-to-digital converter](https://en.wikipedia.org/wiki/Analog-to-digital_converter) — overview
- [Linux kernel docs — Industrial I/O](https://docs.kernel.org/driver-api/iio/index.html) — deep-dive
- Horowitz & Hill, *The Art of Electronics* — ADC/DAC fundamentals — deep-dive

## Key Concepts
- **Continuous → discrete:** ADC samples; DAC drives actuators.
- **Conditioning:** amplifiers/filters before conversion.
- **OS exposure:** character devices, IIO channels, or platform ioctls — not raw pin volts in user space.
- **Limits:** [[bus]] bandwidth and interrupt latency bound usable sample rates.

## Technical Details
```txt
Physical quantity → sensor → amplifier/filter → ADC → digital bus → driver → user space
User command      → DAC  → actuator → physical effect
```

On PCs, analog work often lives on codecs/SMBus sensors. On an [[Electronic Control Unit (ECU)]], analog I/O may be the primary reason the MCU exists.

[[Data Direction Register (DDR)]] GPIO is on/off. Analog deals with resolution (ADC bits), sampling rate, noise, and calibration.

## Real-World Applications
Audio codecs, temperature/pressure sensing, motor control current loops, and industrial DAQ via Linux IIO.

## Pros/Cons or Trade-offs
- **Pro:** Captures real-world continuous signals the digital core needs.
- **Con:** Noise, aliasing, calibration drift, and timing jitter.
- **Trade-off:** higher sample rate/resolution vs CPU, bus, and storage cost.

## Comparison
- vs digital GPIO ([[Data Direction Register (DDR)]]): edges vs continuous levels.
- vs [[PCI (Peripheral Component Interconnect)]] devices: many analog front-ends still attach via a digital bus afterward.

## Mistakes to Avoid
- Treating a slow analog sensor as a digital edge and losing information to aliasing.
- Sampling in a tight user-space loop and ignoring interrupt/DMA-driven capture.
- Ignoring grounding and reference voltage when “the ADC reading looks random.”
