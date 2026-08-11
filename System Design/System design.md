[[System Design]] [[SOLID]] [[API design]] [[Distributed computing]]

# System design

> System design — split what the system means (abstraction) from how it runs (implementation) so either can change without wrecking the other.

---

## Mental model

**Say it in one breath:** Interfaces/APIs describe *what*; adapters/DB/engines do *how*. Interviews and prod both fail when those layers glue together.

```txt
Use-case / domain  →  ports (interfaces)
                           ↑
                      adapters (HTTP, SQL, S3)
```

---

## Standard config / commands

```txt
Design checklist
[ ] Requirements: QPS, data size, consistency, latency SLO
[ ] API sketch + failure modes
[ ] Data model + ownership
[ ] Scaling path (vertical → shard → cache → async)
[ ] Observability: red metrics + traces
```

## Abstraction and implementation hierarchies

| Side | Holds |
|------|-------|
| **Abstraction** | Interfaces, use-cases, policies |
| **Implementation** | Drivers, frameworks, vendor SDKs |

Why separate: swap Postgres → Aurora, or REST → gRPC, without rewriting business rules.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Feature needs 12-file edit | Leaky abstraction | Re-draw ports |
| Can’t load-test one piece | No seams | Add interface + fake |
| Vendor lock in domain | SDK types in core | Anti-corruption layer |
| “Architecture astronaut” | Too many layers | Collapse until pain returns |
| SLO miss unknown where | No metrics per layer | Instrument adapters + use-cases |

---

## Gotchas

> [!WARNING]
> **Premature microservices** — separate *modules* before separate *deploys*.

> [!WARNING]
> **Interface per class** — noise; ports at boundaries only.

> [!WARNING]
> **Ignoring ops** — design that can’t be deployed/observed isn’t done.

---

## When NOT to use

- **Throwaway spikes** — one file is fine.
- **CRUD internal tools** — boring MVC may win.
- **Interview cargo-cult boxes** — justify every box with load/failure.

---

## Related

[[SOLID]] [[API design]] [[Distributed computing]] [[cache system]] [[Quorum]]
