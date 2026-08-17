[[marshalling]] [[gRPC]] [[API design]] [[Throughput]]

# Serialization

> Serialization converts in-memory structures to bytes for storage or network transport and back — the contract between producers and consumers must survive version changes and language boundaries.

```txt
        Serialization ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Schema evolution, versioning, and CPU/size trade-offs across JSON/Protobuf/Av…

## Sources
- [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) — JSON data interchange format — deep-dive
- Google Protocol Buffers documentation — language guide and compatibility — overview
- Martin Kleppmann, *Designing Data-Intensive Applications* — encoding and evolution — deep-dive

## Key Concepts
- **Object ↔ bytes:** for disk, queue, or wire.
- **Schema evolution:** add optional fields; avoid silent breaks.
- **Format choice:** JSON ergonomics vs Protobuf/Avro size/CPU.
- **Versioning:** embed type/version; reject unknowns safely.


### Schema evolution rules

```txt
- **Note:** Additive changes: new optional fields — old readers ignore unknown fields
- **Note:** Breaking changes: rename, change type, remove required field
```

- **Note:** Protocol Buffers field **numbers** are permanent

```bash
protoc --go_out=. order.proto
```

## Technical Details
### Encode and decode path

```txt
Object ──serialize──► bytes ──wire / disk──► bytes ──deserialize──► object
```

- Also called **marshalling** — see [[marshalling]] for language-specific notes.

| Format | Strengths | Typical use |
|--------|-----------|-------------|
| JSON | Human-readable, ubiquitous | Public HTTP APIs ([[API design]]) |
| Protocol Buffers | Compact, schema evolution | [[gRPC]], internal services |
| Apache Avro | Schema in message, compact | Kafka, data pipelines |
| MessagePack | Binary JSON-like | Caching, games |

### Practical pitfalls

| Pitfall | Fix |
|---------|-----|
| Floating point for money | Integer minor units or decimal string |
| Character set mismatch | Explicit UTF-8 |
| Huge payloads | Transfer by reference (object storage URL), not embed |
| Polymorphic JSON without type discriminator | Ambiguous decode |
| `int64` in JSON | Some languages stringify large integers |

- Compress **before** encrypting if both apply

## Mistakes to Avoid
### Symptom → direction

| Symptom | Check |
|---------|-------|
| Garbled text | Wrong charset |
| Decode crash on deploy | New required field — use additive evolution |
| Version skew | Content-Type and schema registry |

Same-process calls should pass objects — do not serialize unnecessarily.


- **Mistake:** Treating Serialization as a silver bullet without measuring the …
- **Mistake:** Ignoring failure modes and operability until production
- **Mistake:** Skipping idempotency, timeouts, or rollback where the pattern re…

## Pros/Cons or Trade-offs
- **Pro:** Portable state across languages and time.
- **Con:** Version drift and expensive (de)serialization CPU.
- **Trade-off:** human-readable JSON vs compact binary.

## Comparison
- vs [[marshalling]]: overlapping; marshalling often implies RPC object graphs.
- vs [[event-driven]]: events need stable serialized contracts.


### Use cases
- RPC payloads, event buses, and durable message formats.
