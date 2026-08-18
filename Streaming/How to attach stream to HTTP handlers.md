[[Streaming]] [[Byte stream]] [[RTMP]] [[NodeJS]]

# How to attach stream to HTTP handlers

> Pipe Node readable streams into `res` (and `req` into files/upstreams) — backpressure-aware bytes, not buffering whole files in RAM.

## Mental model

**Say it in one breath:** In Node HTTP/Express, a stream is a chunked pipe. `.pipe(res)` (or `pipeline`) pushes file/proxy bytes to the client as they arrive so memory stays flat.

```txt
Download:  fs.ReadStream ──pipe──► ServerResponse (res)
Upload:    IncomingMessage (req) ──pipe──► fs.WriteStream
Proxy:     req ──pipe──► upstreamReq ──pipe──► res
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Readable / Writable** | Source vs sink | “File is readable; `res` is writable.” |
| --- | --- | --- |
| **pipe / pipeline** | Connect with backpressure | “pipeline auto-destroys and forwards errors.” |
| **Backpressure** | Slow consumer pauses producer | “pipe respects drain so we don’t OOM.” |
| **Content-Disposition** | Download vs inline | “attachment forces Save As.” |
| **error / finish** | Lifecycle | “Always handle stream error or the socket hangs.” |

This is **HTTP byte streaming**, not WebRTC media. For P2P A/V see [[WebRTC]] / [[ICE (Interactive Connectivity Establishment)]].

## Standard config / commands

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

| `createReadStream` | Reads in chunks — not `readFile` into a Buffer |
| --- | --- |
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

> [!NOTE]
> Respond **after** `pipeline` callback (or `finish`) — otherwise the client may get 200 before the file is fully on disk.

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

For live video packaging/CDN delivery prefer [[HLS]] / [[DASH]] origins ([[flussonic]]), not ad-hoc Express pipes of elementary streams.

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| OOM on large download | `fs.readFile` / buffering | Use `createReadStream` + `pipeline` |
| Client gets truncated file | No error handler; process crash mid-pipe | `pipeline` + log; don’t ignore `error` |
| Upload 200 but empty file | Responded before `finish` | Wait for pipeline callback |
| Hang after error | Half-open pipe | Destroy both sides (`pipeline` does this) |
| Proxy stalls | Missing pipe of `req` or response | Bidirectional pipeline; forward method/headers carefully |
| Wrong Content-Type | Browser sniffs / refuses | Set type explicitly before first write |

## Gotchas

> [!WARNING]
> **`.pipe(res)` without error handling** — uncaught `EPIPE` / read errors can crash or leak sockets. Prefer `stream.pipeline`.

> [!WARNING]
> **Headers after write** — first chunk commits headers; set `Content-Disposition` / length estimates first.

> [!WARNING]
> **Express JSON body parser** — `express.json()` consumes `req`; disable for raw upload routes or you can’t pipe the body.

> [!WARNING]
> **Range requests** — video players need `Accept-Ranges` / 206 for seeking; naive full-file pipe breaks scrubbing.

> [!WARNING]
> **Not WebRTC** — piping HTTP is unrelated to SDP/ICE; don’t debug with `chrome://webrtc-internals`.

## When NOT to use

- **Interactive A/V between browsers** — [[WebRTC]] + [[WebRTC Signaling channels]], not `res.pipe`.
- **Multi-bitrate live OTT** — packager + CDN ([[HLS]], [[DASH]], [[flussonic]]).
- **Tiny JSON APIs** — `res.json()` is fine; streams add complexity for kilobyte payloads.

## Related

[[Byte stream]] [[RTMP]] [[HLS]] [[DASH]] [[flussonic]] [[WebRTC]] [[pdf-stream-viewing]]
