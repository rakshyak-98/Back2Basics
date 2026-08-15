[[Concurrent modification]] [[Networking]] [[mime type]]

# ETAG or IF MATCH

> ETag + If-Match stop lost updates — write only if the resource is still the version you read.

## Interview Relevance

Interviewers use ETag/`If-Match` to test optimistic concurrency on HTTP: version tokens, `412 Precondition Failed`, and strong vs weak validators — not just “caching headers.”

## Sources

- [RFC 9110 — HTTP Semantics (Conditional Requests / ETag)](https://www.rfc-editor.org/rfc/rfc9110#name-conditional-requests) — deep-dive
- [MDN — ETag](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag) — overview
- [MDN — If-Match](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Match) — overview
- [MDN — Conditional requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Conditional_requests) — overview

## Core Definition

An ETag is an opaque version of a representation; `If-Match` makes a write conditional so the server applies the change only when the current ETag still matches (optimistic lock on the HTTP wire).

## Key Concepts

- **ETag:** opaque version of the representation → hash, counter, or revision; client treats it as opaque.
- **If-Match:** “apply only if current ETag is this” → optimistic concurrency for PUT/PATCH/DELETE.
- **412 Precondition Failed:** mismatch → someone else wrote first; merge and retry.
- **If-None-Match:** cache validation / create-if-absent → `*` can mean create-only; with ETag = conditional GET.
- **Strong vs weak (`W/`):** strong comparison required for `If-Match` → weak tags are fine for caches, unsafe as the only write guard.

## Technical Details

```txt
GET  → 200 + ETag: "v3"
PUT + If-Match: "v3"
        │
        ├─ still "v3" → apply, new ETag "v4"
        └─ now "v4"   → 412 Precondition Failed
```

Server checklist:

1. Store a version (integer, hash, or row version) with the resource.
2. On GET/PUT response, emit `ETag`.
3. On mutating request, compare `If-Match` **inside the same database transaction** as the write.
4. Bump version atomically on success.

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

| Symptom | Check | Fix |
|---------|-------|-----|
| Constant `412` | Client stale / shared ETag | Refetch; don’t reuse ETag across tabs blindly |
| Lost updates still happen | Server ignores `If-Match` | Enforce in transaction; reject missing header |
| `200` but client confused | ETag not updated after write | Always return new ETag on success |
| CDN serves old body | Weak validators / long cache | Short TTL or purge on write |
| Quotes stripped | Middleware mangles header | Keep quoted form `"…"` end-to-end |

## Real-World Applications

Shared document APIs, inventory updates, and config resources use ETag/`If-Match` so concurrent editors don’t silently overwrite each other.

**Example:** Two admins edit the same channel bitrate; the second PUT without a matching ETag gets `412`, refetches, merges, and retries.

## Pros/Cons or Trade-offs

- **Pro:** No long-held row lock while the user edits — conflict detected at write time.
- **Con:** Clients must handle `412` (refetch/merge) — not last-write-wins by default.
- **Con:** Weak ETags simplify caching but are the wrong sole guard for byte-exact updates.

## Comparison

- vs last-write-wins: unconditional PUT overwrites silently; `If-Match` rejects stale writers.
- vs [[Concurrent modification]] / pessimistic locks: locks block during edit; ETag detects conflict at commit.
- vs `If-None-Match`: used for cache revalidation and create-only, not “update if still this version.”

## Mistakes to Avoid

- Missing `If-Match` = last-write-wins — if you require optimistic concurrency, reject unconditional PUT with `428`/`400`.
- Stuck ETag when the body changes — hides conflicts; ETag must change when content changes.
- Using only weak ETags (`W/"…"`) as the write guard — fine for caches; dangerous for OCC.
- Comparing outside the write transaction — TOCTOU races reintroduce lost updates.
