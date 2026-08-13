[[System Design]] [[marshalling]] [[gRPC]] [[API design]]

# Serialization

> Serialization — turn in-memory objects into bytes for disk/network, and back; the contract between producers and consumers.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Pick a format (JSON, Protobuf, Avro, MessagePack). Define schema/compatibility rules. Version fields so old readers don’t die.

```txt
Object ──marshal──► bytes ──wire──► bytes ──unmarshal──► Object'
```

| Format | Fit |
|--------|-----|
| JSON | Human/debug; APIs |
| Protobuf/Avro | Compact; schema evolution |
| MessagePack | Binary JSON-like |

(Also called marshalling — see [[marshalling]].)

---

## Standard config / commands

```bash
# Protobuf sketch
protoc --go_out=. order.proto
```

```js
JSON.stringify(obj)
JSON.parse(buf.toString('utf8'))
```

| Knob | Why |
|------|-----|
| Field numbers / names | Compatibility |
| Optional vs required | Breaking changes |
| Content-Type | Gateways don’t guess |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbled unicode | Charset | Force UTF-8 |
| Unknown field crash | Strict decoder | Ignore unknown (proto3) |
| Float money bugs | Binary float | Integer cents / decimal string |
| Huge payloads | Over-fetch | DTO projection |
| Version skew deploy | New required field | Additive evolution only |

---

## Gotchas

> [!WARNING]
> **Type maps differ by language** — `int64` in JSON as string sometimes.

> [!WARNING]
> **Polymorphic JSON without `type`** — ambiguous decode.

> [!WARNING]
> **Encrypt then compress vs compress then encrypt** — order matters for size/security.

---

## When NOT to use

- **Same-process calls** — pass objects, don’t serialize.
- **Ad-hoc debug only** — `pprint` fine; still don’t invent formats for production.
- **Huge media** — send by reference (S3 URL), don’t embed.

---

## Related

[[marshalling]] [[gRPC]] [[API design]] [[Throughput]]
