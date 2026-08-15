[[Serialization]] [[Distributed computing]] [[API design]] [[gRPC]] [[race condition]]

# marshalling

> Marshalling converts runtime objects to bytes for network, disk, or inter-process communication and unmarshals them on the receiver — the explicit contract where languages, versions, and endianness meet.

## Interview Relevance

Object↔bytes for RPC/storage; schema/versioning; difference from loose ‘serialization’ talk.

## Sources

- Google Protocol Buffers Language Guide — overview
- [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) — JSON — deep-dive
- OWASP Deserialization Cheat Sheet — untrusted input risks — overview

## Key Concepts

- **Runtime object → bytes** for network or disk (and back).
- **RPC emphasis:** stubs marshal arguments/results across processes.
- **Schema/version:** incompatible marshalers break silently.
- **Security:** never deserialize untrusted blobs without limits.


## Technical Details

### Boundary crossing

```txt
Process A: object ──marshal──► bytes ──TCP/HTTP──► bytes ──unmarshal──► Process B: object
                         │
                  JSON / Protocol Buffers / Avro / MessagePack
```

Synonymous with **serialization** in most teams — see [[Serialization]] for format comparison.

| Format | Schema | Human-readable | Typical use |
|--------|--------|----------------|-------------|
| JSON | Informal / OpenAPI | Yes | Public REST [[API design]] |
| Protocol Buffers | `.proto` strict | No | [[gRPC]] internal services |
| Avro | Schema registry | No | Kafka events ([[event-driven]]) |
| MessagePack | Informal | No | Compact JSON-like payloads |

Bugs appear **only cross-process**: field order, nullable fields, enum evolution, 32-bit versus 64-bit integers in JSON.

## JSON marshalling

```python
import json
from dataclasses import asdict

payload = json.dumps(asdict(user), separators=(",", ":"))
user = json.loads(payload)
```

Rules: UTF-8, ISO 8601 dates, explicit null versus omit policy. Never marshal arbitrary objects — define data transfer objects.

## Protocol Buffers evolution

```protobuf
message User {
  string id = 1;
  string email = 2;
  optional string phone = 3;  // v2 — old clients ignore
}
```

Field **numbers** are permanent; never reuse. Backward compatible changes add optional fields; breaking changes need coordination.

## Real-World Applications

gRPC/Thrift stubs, Java RMI-era lessons, and cross-language IPC.


## Pros/Cons or Trade-offs

- **Pro:** Hides byte layout behind typed APIs.
- **Con:** Version skew and gadget attacks on rich deserializers.
- **Trade-off:** convenience vs explicit DTOs you control.


## Comparison

- vs [[Serialization]]: overlapping; marshalling often implies RPC object graphs.
- vs [[remote data]]: remote calls depend on a marshal format.


## Mistakes to Avoid

| Symptom | Direction |
|---------|-----------|
| Garbled text | Wrong charset — force UTF-8 |
| Intermittent decode errors | Version skew — schema registry |
| Money rounding errors | Float on wire — integer minor units |
| Security issues | Deserializing untrusted types — allow-list classes |

*What breaks first under load?* Large JSON payloads — prefer binary formats or reference by identifier for bulk media.
