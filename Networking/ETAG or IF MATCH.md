<!-- note-strategy: operational -->
[[Concurrent modification]] [[Networking]]

# ETAG or IF MATCH

> ETag + If-Match stop lost updates — write only if the resource is still the version you read.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Server hands you a version token (ETag); you send it back on write; mismatch → `412`, refetch, retry.

```txt
GET  → 200 + ETag: "v3"
PUT + If-Match: "v3"
        │
        ├─ still "v3" → apply, new ETag "v4"
        └─ now "v4"   → 412 Precondition Failed
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ETag** | Opaque version of the representation | “Hash, counter, or revision — client treats it as opaque.” |
| **If-Match** | “Apply only if current ETag is this” | “Optimistic lock on the HTTP wire.” |
| **412** | Precondition failed | “Someone else wrote first — merge and retry.” |
| **If-None-Match** | Cache / create-if-absent | “`*` can mean create-only; with ETag = conditional GET.” |
| **Optimistic concurrency** | Detect conflict at write time | “No row lock held while the user edits.” |

### Server checklist

1. Store a version (integer, hash, or row version) with the resource.
2. On GET/PUT response, emit `ETag`.
3. On mutating request, compare `If-Match` **inside the same DB transaction** as the write.
4. Bump version atomically on success.

---

## Standard config / commands

```http
GET /channels/42 HTTP/1.1

HTTP/1.1 200 OK
ETag: "a1b2c3d4"
{"id":42,"name":"channel1","bitrate":"6000k"}
```

```http
PUT /channels/42 HTTP/1.1
If-Match: "a1b2c3d4"
{"id":42,"name":"channel1","bitrate":"8000k"}

HTTP/1.1 200 OK
ETag: "e5f6a7b8"
```

```js
// Client: always send the ETag you last saw
await fetch(`/channels/${id}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'If-Match': etag, // from prior GET
  },
  body: JSON.stringify(body),
})
// 412 → GET again, merge, retry
```

| Knob | Why it matters |
|------|----------------|
| Strong vs weak ETag (`W/`) | Weak may not be safe for byte-exact PUT |
| Compare-and-swap in DB | Check version in `UPDATE … WHERE version=?` |
| Proxy caches | `Cache-Control` + ETag for GET; don’t cache unsafe PUT |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Constant `412` | Client stale / shared ETag | Refetch; don’t reuse ETag across tabs blindly |
| Lost updates still happen | Server ignores `If-Match` | Enforce in transaction; reject missing header |
| `200` but client confused | ETag not updated after write | Always return new ETag on success |
| CDN serves old body | Weak validators / long cache | Short TTL or purge on write |
| Quotes stripped | Middleware mangles header | Keep quoted form `"…"` end-to-end |

---

## Gotchas

> [!WARNING]
> **Missing If-Match = last-write-wins** — if you require OCC, reject unconditional PUT with `428`/`400`.

> [!WARNING]
> **ETag must change when body changes** — a stuck ETag hides conflicts.

> [!WARNING]
> **Weak ETags (`W/"…"`)** — fine for caches; dangerous as the only write guard.

---

## When NOT to use

- **Single-writer append-only logs** — versioning may be overkill; use offsets.
- **WebSocket fan-out state** — prefer CRDT/OT or server authority, not HTTP ETags alone.
- **Binary upload resume** — use upload protocols / checksums designed for chunks.

---

## Related

[[Concurrent modification]] [[Networking]] [[mime type]]
