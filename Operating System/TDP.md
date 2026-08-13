[[Operating System]] [[base clock speed]] [[SMT threads]] [[cgroup (Control Group)]]

# TDP

> TDP (Thermal Design Power) is the heat a cooling solution must dissipate at sustained load — not peak power, but the thermal envelope that governs throttling and [[base clock speed]].

CPU vendors specify TDP in watts; actual power varies with workload, turbo, and [[SMT threads]] utilization. Exceed thermal limits → **throttling** → lower frequency and higher latency.

Datacenter planning pairs TDP with rack power and [[cgroup (Control Group)]]-limited workloads in shared hosts.

```bash
turbostat --Summary --quiet
cat /sys/class/thermal/thermal_zone*/temp
```

## Sources

- Intel product specification — TDP definition
- Wikipedia: [Thermal design power](https://en.wikipedia.org/wiki/Thermal_design_power)
