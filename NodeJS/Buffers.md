[[NodeJS]] [[Stream]] [[primitive non-primitive values]] [[Stream/pipe]] [[HTTP module]]

# Buffers

> Fixed-size bytes in memory outside the V8 string heap — binary I/O, crypto, and stream chunks.

```txt
        Buffers ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **Buffers** to check whether you can explain the mechanism i…

## Sources
- [Node.js — Buffer](https://nodejs.org/api/buffer.html) — deep-dive
- [Wikipedia — Buffers](https://en.wikipedia.org/wiki/Buffers) — overview

## Key Concepts
- **Buffer:** Byte array — Binary-safe; strings are UTF-8 views.
- **alloc vs allocUnsafe:** Zeroed vs faster dirty — Unsafe can leak old memory — zero first if needed.
- **highWaterMark:** Stream chunk target size — Controls Buffer sizes from reads.

## Technical Details
```txt
file/socket → Buffer chunks → process → write Buffer
```

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

## Mistakes to Avoid
- **Mistake:** **`allocUnsafe`**
- **Mistake:** **Garbled text:** check Wrong encoding
- **Mistake:** **OOM:** check Concatenating all chunks; fix: Stream / limit size
- **Mistake:** **Security scare:** check `allocUnsafe` without fill
- **Mistake:** **Partial JSON parse:** check Split across chunks

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Fixed-size bytes in memory outside the V8 string heap — binary I/O, crypto, and …).
- **Con / when not:** **Pure text APIs**
- **Con / when not:** **Huge files in one Buffer** — use [[Stream]].

## Comparison
- vs [[Stream]]: Streams process data over time with backpressure; Buffers are …


### Use cases
- In production APIs and tooling, **Buffers** shows up whenever teams ship Node…
