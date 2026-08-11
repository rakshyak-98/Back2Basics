[[Operating System]] [[Heap memory]] [[buffer]]

# Browser memory

> Browser RAM holds FileReader buffers, blobs, and WASM heaps — close the tab and it is gone.

---

## Mental model

**Say it in one breath:** The browser process allocates JS heap + ArrayBuffers; disk is only touched if you write to IndexedDB / Cache / download.

```txt
<input type=file>  →  File / Blob (still disk-backed handle)
FileReader / arrayBuffer()  →  copy into JS heap (RAM)
URL.createObjectURL  →  blob URL (refcounted; revoke!)
close tab / OOM  →  gone (unless you persisted)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **JS heap** | GC’d object memory | “Objects live until unreachable; then GC.” |
| **ArrayBuffer / TypedArray** | Raw bytes in RAM | “Binary payloads sit off the string heap.” |
| **Blob / File** | Opaque binary + metadata | “File is a Blob with a name; may stream from disk.” |
| **Object URL** | `blob:` pointer | “Must revoke or you leak until navigation.” |
| **IndexedDB** | Durable browser DB | “Survives refresh; not ‘pure RAM’.” |
| **sql.js / WASM heap** | SQLite in WASM memory | “Fast and private until you export/persist.” |

### How the story goes

1. **Load** — user picks a file; browser may mmap/stream, not fully copy yet.
2. **Materialize** — `arrayBuffer()` / `FileReader` copies into process RAM.
3. **Use** — preview, hash, upload, or put into WASM/sql.js.
4. **Release** — drop refs, `URL.revokeObjectURL`, let GC run; or persist intentionally.

---

## Standard config / commands

```js
// Keep in RAM only (no write to disk APIs)
const buf = await file.arrayBuffer()
const url = URL.createObjectURL(file)
// … preview …
URL.revokeObjectURL(url)

// In-memory SQLite (sql.js) — lost on refresh unless you export
const db = new SQL.Database()
db.run("CREATE TABLE t(x); INSERT INTO t VALUES(1);")
```

| Knob | Why it matters |
|------|----------------|
| Chrome Task Manager | See which tab eats RAM |
| `performance.memory` (Chrome) | Rough JS heap size |
| DevTools → Memory | Snapshots / detached DOM leaks |
| Cap upload size client-side | Avoid multi‑GB ArrayBuffers |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Tab crash / “Aw, Snap” | Huge ArrayBuffer / many object URLs | Stream upload; revoke URLs; chunk process |
| Memory climbs on each upload | Forgotten blob URLs / closures | Revoke; null buffers after send |
| Data “vanishes” on refresh | Never wrote IndexedDB/Cache | Persist explicitly or warn user |
| sql.js OOM | WASM heap too small | Grow/export; don’t load whole DB twice |
| Slow UI after big file | Main-thread decode | Worker + transferable ArrayBuffer |
| Privacy surprise | File still on disk at path | Browser didn’t copy to “temp disk”; don’t confuse with OS temp |

---

## Gotchas

> [!WARNING]
> **File ≠ already in RAM** — until you read it, the handle may stream from the user’s disk path.

> [!WARNING]
> **IndexedDB is disk** — not “browser memory only”; treat it like durable storage for GDPR/wipe.

> [!WARNING]
> **Object URLs leak** — create without revoke pins Blob memory across navigations in the SPA.

> [!WARNING]
> **Mobile browsers kill tabs** — large in-RAM DBs die under memory pressure; checkpoint if needed.

---

## When NOT to use

- **Must survive refresh / crash** — use IndexedDB, OPFS, or server storage.
- **Multi‑GB media editing** — stream / WebCodecs; don’t `arrayBuffer()` the whole file.
- **Secrets that must never touch disk** — still risk swap + extensions; prefer short-lived server vaults.

---

## Related

[[Heap memory]] [[buffer]] [[RAM and Swap memory]] [[fsync]]
