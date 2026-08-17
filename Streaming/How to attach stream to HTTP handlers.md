[[Streaming]] [[Byte stream]] [[RTMP]] [[NodeJS]] [[HLS]] [[DASH]] [[flussonic]] [[WebRTC]] [[pdf-stream-viewing]]

# How to attach stream to HTTP handlers

> Pipe Node readable streams into `res` (and `req` into files/upstreams) — backpressure-aware bytes, not buffering whole files in RAM.

```txt
        How to attach stre ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk How to attach stream to HTTP handlers…

## Sources
- [Wikipedia — How to attach stream to HTTP handlers](https://en.wikipedia.org/wiki/How_to_attach_stream_to_HTTP_handlers) — overview

## Key Concepts
- **Readable / Writable:** Source vs sink — “File is readable; `res` is writable.”
- **pipe / pipeline:** Connect with backpressure — “pipeline auto-destroys and forwards errors.”
- **Backpressure:** Slow consumer pauses producer — “pipe respects drain so we don’t OOM.”
- **Content-Disposition:** Download vs inline — “attachment forces Save As.”
- **error / finish:** Lifecycle — “Always handle stream error or the socket hangs.”

## Technical Details
```txt
Download:  fs.ReadStream ──pipe──► ServerResponse (res)
Upload:    IncomingMessage (req) ──pipe──► fs.WriteStream
Proxy:     req ──pipe──► upstreamReq ──pipe──► res
```

### Streaming file download

```js
const express = require('express')
const fs = require('fs')
const path = require('path')
const { pipeline } = require('stream')

const app = express()

app.get('/download', (req, res) => {
  const filePath = path.join(__dirname, 'large-file.txt')
  const readStream = fs.createReadStream(filePath)

  res.setHeader('Content-Disposition', 'attachment; filename="large-file.txt"')
  res.setHeader('Content-Type', 'text/plain')

  pipeline(readStream, res, (err) => {
    if (err) {
      console.error('download failed', err)
      if (!res.headersSent) res.status(500).end()
    }
  })
})

app.listen(3000)
```

| Knob | Why it matters |
|------|----------------|
| `createReadStream` | Reads in chunks — not `readFile` into a Buffer |
| `pipeline` over bare `.pipe` | Propagates errors; closes both sides |
| Headers before pipe | Too late once first chunk flushed |

### Streaming file upload

```js
app.post('/upload', (req, res) => {
  const dest = path.join(__dirname, 'uploads', `in-${Date.now()}.bin`)
  const writeStream = fs.createWriteStream(dest)

  pipeline(req, writeStream, (err) => {
    if (err) {
      console.error('upload failed', err)
      return res.status(500).json({ ok: false })
    }
    res.json({ ok: true, path: dest })
  })
})
```

- [!NOTE] Respond **after** `pipeline` callback (or `finish`)

### Proxy request and response

```js
const { request } = require('https')

app.use('/proxy', (req, res) => {
  const proxyReq = request('https://example.com' + req.url, { method: req.method, headers: req.headers })

  proxyReq.on('response', (proxyRes) => {
    res.writeHead(proxyRes.statusCode, proxyRes.headers)
    pipeline(proxyRes, res, (err) => {
      if (err) console.error('proxy response', err)
    })
  })

  pipeline(req, proxyReq, (err) => {
    if (err) {
      console.error('proxy request', err)
      if (!res.headersSent) res.status(502).end()
    }
  })
})
```

- For live video packaging/CDN delivery prefer [[HLS]] / [[DASH]] origins ([[fl…

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| OOM on large download | `fs.readFile` / buffering | Use `createReadStream` + `pipeline` |
| Client gets truncated file | No error handler; process crash mid-pipe | `pipeline` + log; don’t ignore `error` |
| Upload 200 but empty file | Responded before `finish` | Wait for pipeline callback |
| Hang after error | Half-open pipe | Destroy both sides (`pipeline` does this) |
| Proxy stalls | Missing pipe of `req` or response | Bidirectional pipeline; forward method/headers carefully |
| Wrong Content-Type | Browser sniffs / refuses | Set type explicitly before first write |

- **Mistake:** **`.pipe(res)` without error handling**
- **Mistake:** **Headers after write**
- **Mistake:** **Express JSON body parser**
- **Mistake:** **Range requests**
- **Mistake:** **Not WebRTC**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Interactive A/V between browsers**
- **Con / skip when:** **Multi-bitrate live OTT**
- **Con / skip when:** **Tiny JSON APIs**

## Comparison
- vs [[WebRTC]]: **Interactive A/V between browsers**
- vs [[HLS]]: **Multi-bitrate live OTT** — packager + CDN ([[HLS]], [[DASH]], [[flussonic]]).


### Use cases
- Used wherever How to attach stream to HTTP handlers sits in an ingest → packa…
