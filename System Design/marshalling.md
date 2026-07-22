[[Serialization]] [[Distributed computing]] [[API design]] [[gRPC]]

# Marshalling

> Convert in-memory structures ↔ wire/storage bytes across process boundaries — **schema + version discipline** prevent silent corruption.

---

## Mental model

**Marshalling** (synonymous with **serialization** in most teams) transforms **runtime objects** into **bytes** for network, disk, or IPC, and **unmarshals** back on the receiver. Boundaries: **different languages**, **different processes**, **different versions** — all need an **explicit format contract**.

```txt
Process A: object ──marshal──► bytes ──TCP/HTTP──► bytes ──unmarshal──► Process B: object
                         │
                  JSON / Protobuf / Avro / MessagePack
```

| Format | Schema | Human-readable | Typical use |
|--------|--------|----------------|-------------|
| **JSON** | Informal / OpenAPI | Yes | Public REST [[API design]] |
| **Protobuf** | `.proto` strict | No | gRPC internal |
| **Avro** | ID registry | No | Kafka events |
| **MessagePack** | Informal | No | Compact JSON-like |

**Endianness, field order, nullable fields, enum evolution** — bugs appear **only cross-process** ([[race condition]] with bytes).

---

## Standard config / commands

### JSON marshalling (API default)

```python
import json
from dataclasses import asdict

payload = json.dumps(asdict(user), separators=(",", ":"))
user = json.loads(payload)
```

```txt
Rules: UTF-8, ISO8601 dates, explicit null vs omit policy
Never marshal arbitrary objects — define DTO/schema
```

### Protobuf (versioned contract)

```protobuf
message User {
  string id = 1;
  string email = 2;
  optional string phone = 3;  // added in v2 — old clients ignore
}
```

```txt
Field numbers permanent; never reuse
Backward compatible: add optional fields only
Breaking: rename field number, change type
```

### gRPC unary call (marshal hidden)

```go
resp, err := client.GetUser(ctx, &pb.GetUserRequest{Id: "u1"})
// protobuf handles marshal/unmarshal
```

### IPC / shared nothing

```txt
Unix socket: length-prefix + JSON/protobuf frame
Avoid: pickle, Java native serialization across trust boundaries
```

### Validation at boundary

```txt
Unmarshal → validate (types, ranges) → domain logic
Never trust unmarshaled input without validation
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbled strings | UTF-8 vs Latin-1 | Enforce UTF-8; Content-Type charset |
| Works Java, fails Go | JSON field casing | Tag conventions; shared OpenAPI |
| Old client crash on deploy | New required field | Optional fields + defaults |
| Float rounding | JSON number precision | Use string decimal or int cents |
| Huge payloads | Marshal entire graph | DTO projection; pagination |
| Kafka poison message | Bad Avro schema ID | Schema registry; DLQ |
| Endian binary bug | Raw struct pack | Use protobuf, not manual pack |

---

## Gotchas

> [!WARNING]
> **Marshal same object graph twice** — circular references blow JSON serializers.

> [!WARNING]
> **Datetime timezone naive** — always UTC ISO8601 on wire.

> [!WARNING]
> **Implicit float for money** — use integer minor units.

> [!WARNING]
> **Security: unmarshaling bombs** — cap payload size; depth limits on JSON parse.

> [!WARNING]
> **[[DRY]] generated DTOs** — hand-editing generated marshal code gets overwritten.

---

## When NOT to use

- **Same process, same language** — pass object references; no marshal.
- **Shared memory ring buffer** — fixed binary layout OK with strict schema doc.
- **JSON for high-frequency numeric telemetry** — protobuf/MessagePack bandwidth.

---

## Related

[[Serialization]] [[Distributed computing]] [[API design]] [[event-driven]] [[race condition]] [[gRPC]]
