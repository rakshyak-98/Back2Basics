[[NodeJS]] [[Stream]] [[primitive non-primitive values]]

# Buffers

> Fixed-size bytes in memory outside the V8 string heap — binary I/O, crypto, and stream chunks.

---

## How it works

```txt
file/socket → Buffer chunks → process → write Buffer
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Buffer** | Byte array | “Binary-safe; strings are UTF-8 views.” |
| **alloc vs allocUnsafe** | Zeroed vs faster dirty | “Unsafe can leak old memory — zero first if needed.” |
| **highWaterMark** | Stream chunk target size | “Controls Buffer sizes from reads.” |


## Configuration and commands

```js
const a = Buffer.from('hello', 'utf8')
const b = Buffer.alloc(16) // zero-filled
console.log(a.toString('hex'))

// Prefer streaming large files — Buffers for pieces, not whole GB
import fs from 'node:fs'
fs.createReadStream('in.bin', { highWaterMark: 16 * 1024 })
  .pipe(fs.createWriteStream('out.bin'))
```

| Knob | Why it matters |
|------|----------------|
| Encoding (`utf8`, `base64`, `hex`) | Wrong encoding corrupts data |
| `Buffer.concat` | Join chunks — watch total size |
| `subarray` | View, not copy — mutations alias |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbled text | Wrong encoding | Match producer encoding |
| OOM | Concatenating all chunks | Stream / limit size |
| Security scare | `allocUnsafe` without fill | Use `alloc` or fill |
| Partial JSON parse | Split across chunks | Accumulate until complete frame |

---


## Gotchas

> [!WARNING]
> **`allocUnsafe`** — faster but may contain old heap data; never return to clients without overwriting.

> [!WARNING]
> **Mixing string and Buffer** in crypto/hash — be explicit about encoding.

---


## When not to use

- **Pure text APIs** — strings are fine until you hit binary.
- **Huge files in one Buffer** — use [[Stream]].

---


## Related

[[Stream]] [[Stream/pipe]] [[HTTP module]]

## Sources

- [Wikipedia — Buffers](https://en.wikipedia.org/wiki/Buffers)
