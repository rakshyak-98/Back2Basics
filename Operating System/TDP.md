[[Operating System]] [[base clock speed]] [[SMT threads]] [[cgroup (Control Group)]]

# TDP

> TDP (Thermal Design Power) is the heat a cooling solution must handle at sustained load — the thermal envelope that drives throttling and sustainable [[base clock speed]], not a peak-watt number.

## Interview Relevance

Hardware capacity planning: TDP vs turbo, why sustained load throttles, and how rack power budgets constrain density.

## Sources

- Intel product specification — TDP definition — overview
- [Wikipedia — Thermal design power](https://en.wikipedia.org/wiki/Thermal_design_power) — overview

## Key Concepts

- **Thermal envelope (watts):** cooling design target for sustained operation.
- **Not peak power:** short turbo can exceed TDP briefly.
- **Throttling:** exceed limits → lower frequency → higher latency.
- **Workload sensitivity:** [[SMT threads]] utilization and vector units change real power.

## Technical Details

```bash
turbostat --Summary --quiet
cat /sys/class/thermal/thermal_zone*/temp
```

Datacenter planning pairs TDP with rack power and [[cgroup (Control Group)]]-limited workloads on shared hosts.

## Real-World Applications

Choosing SKUs for dense Kubernetes nodes, laptop battery/thermal design, and explaining why “same CPU” is slower in a hot rack.

## Pros/Cons or Trade-offs

- **Higher TDP SKUs:** more sustained performance; more cooling and power cost.
- **Lower TDP:** denser racks; earlier throttle under load.
- **Trade-off:** turbo marketing numbers vs sustained throughput.

## Comparison

- vs [[base clock speed]]: base/turbo are frequency claims; TDP constrains how long you stay there.
- vs software CPU limits (cgroups): cgroups cap share/quota; TDP is physical heat.

## Mistakes to Avoid

- Designing capacity from turbo frequency without sustained thermal tests.
- Ignoring ambient and chassis airflow when comparing bench vs production.
- Equating nameplate TDP across vendors without reading their definition footnotes.
