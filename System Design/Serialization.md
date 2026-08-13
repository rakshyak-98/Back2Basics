[[marshalling]] [[gRPC]] [[API design]] [[Throughput]]

# Serialization

> Serialization converts in-memory structures to bytes for storage or network transport and back — the contract between producers and consumers must survive version changes and language boundaries.

---

## Encode and decode path

```txt
Object ──serialize──► bytes ──wire / disk──► bytes ──deserialize──► object
```

Also called **marshalling** — see [[marshalling]] for language-specific notes.

| Format | Strengths | Typical use |
|--------|-----------|-------------|
| JSON | Human-readable, ubiquitous | Public HTTP APIs ([[API design]]) |
| Protocol Buffers | Compact, schema evolution | [[gRPC]], internal services |
| Apache Avro | Schema in message, compact | Kafka, data pipelines |
| MessagePack | Binary JSON-like | Caching, games |

## Schema evolution rules

```txt
Additive changes: new optional fields — old readers ignore unknown fields
Breaking changes: rename, change type, remove required field — coordinate deploy or version bump
```

Protocol Buffers field **numbers** are permanent — never reuse. Prefer optional fields over required in evolving APIs.

```bash
protoc --go_out=. order.proto
```

## Practical pitfalls

| Pitfall | Fix |
|---------|-----|
| Floating point for money | Integer minor units or decimal string |
| Character set mismatch | Explicit UTF-8 |
| Huge payloads | Transfer by reference (object storage URL), not embed |
| Polymorphic JSON without type discriminator | Ambiguous decode |
| `int64` in JSON | Some languages stringify large integers |

Compress **before** encrypting if both apply — encrypted data does not compress well.

## Symptom → direction

| Symptom | Check |
|---------|-------|
| Garbled text | Wrong charset |
| Decode crash on deploy | New required field — use additive evolution |
| Version skew | Content-Type and schema registry |

Same-process calls should pass objects — do not serialize unnecessarily.

## Sources

- [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) — JSON data interchange format.
- Google Protocol Buffers documentation — language guide and compatibility.
- Martin Kleppmann, *Designing Data-Intensive Applications* — encoding and evolution.
