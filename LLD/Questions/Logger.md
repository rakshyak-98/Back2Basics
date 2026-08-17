[[Design pattern/Singleton]] [[Design pattern/Observer]] [[LLD/Questions/Connection Pool]]

# Logger (LLD)

> Shared logging module that writes structured records to sinks (file, stdout) with levels, correlation ids, and safe concurrency.

```txt
        Logger (LLD) ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers expect levels, single-writer vs locked multi-writer, rotation, a…

## Sources
- [Unicode TR35 / structured logging practice](https://www.rfc-editor.org/rfc/rfc5424) — overview (syslog model)
- [OpenTelemetry — Logs](https://opentelemetry.io/docs/concepts/signals/logs/) — overview

## Key Concepts
- **Levels:** DEBUG/INFO/WARN/ERROR filtering.
- **Sinks:** stdout for containers; files with rotation for VMs.
- **Correlation:** request/trace id fields on every line.
- **Concurrency:** mutex or queue so lines do not interleave mid-record.
- **Sampling / rate limits:** protect disk during error storms.

## Technical Details
```txt
app → logger.api → format (JSON) → sink(s)
                     ↘ async queue (optional)
```

- API sketch: `info(msg, fields)`, `error(err, fields)`, `withContext(fields)`.

| Failure | Design response |
|---------|-----------------|
| Disk full | Fallback stderr; circuit-break file sink |
| Lock contention | Async logger with bounded queue |
| Sensitive data | Redaction filters |

## Mistakes to Avoid
- **Mistake:** Logging secrets (tokens, passwords, card data)
- **Mistake:** Synchronous disk write on the request path without bounds
- **Mistake:** Unlimited in-memory queue “for performance.”

## Pros/Cons or Trade-offs
- **Pro:** Central policy for level and redaction.
- **Con:** Async logging can drop or delay logs on crash — document durability guarantees.

## Comparison
- vs `print` scattered everywhere: no level control or structure.
- vs full observability stacks: logger is the producer; collectors are the pipeline.


### Use cases
- Microservice logs JSON to stdout

- **Example:** Two threads `print` partial lines
