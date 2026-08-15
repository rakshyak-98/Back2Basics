[[Streaming]] [[Byte stream]] [[How to attach stream to HTTP handlers]]

# pdf-stream-viewing

> Stream a PDF into the browser — render pages as bytes arrive (PDF.js + HTTP range), don’t wait for the whole file.

## Interview Relevance

Interviewers probe whether you can walk pdf-stream-viewing end-to-end — not just name it. Signal fluency with **Range request**, **206 Partial Content**, **PDF.js**, **Linearized PDF** and when you would pick a different path.

## Sources

- [Wikipedia — pdf-stream-viewing](https://en.wikipedia.org/wiki/pdf-stream-viewing) — overview

## Core Definition

This is document progressive loading, not media [[ABR]]. Same HTTP range idea as video segment fetches, different parser.

## Key Concepts

- **Range request:** Client asks for a byte slice — “We fetch only the pages needed.”
- **206 Partial Content:** Server honors the range — “No 206 ⇒ progressive view falls back to full download.”
- **PDF.js:** Mozilla’s JS PDF engine — “Renders to canvas; talks HTTP range under the hood.”
- **Linearized PDF:** “Fast web view” layout — “Hint table up front — first page shows sooner.”
- **Object stream / xref:** Where page objects live — “Broken xref ⇒ blank pages even if bytes arrived.”

**Flow:**

1. **Serve** — host PDF with range support (most static servers do).
2. **Prefer linearized** — distill/fast-web-view when generating large docs.
3. **Load** — `pdfjsLib.getDocument(url)` (or your worker setup).
4. **Render** — `getPage(n)` → viewport → canvas as the user navigates.

## Technical Details

```txt
Browser (PDF.js)
      │  Range: bytes=0-65535
      ▼
HTTP server (Accept-Ranges: bytes)
      │  206 Partial Content
      ▼
PDF.js parses xref / pages ──► canvas render
      │
      └─ more ranges as user scrolls
```

```html
<script src="https://mozilla.github.io/pdf.js/build/pdf.js"></script>
<canvas id="pdf-canvas"></canvas>
```

```js
const url = '/docs/report.pdf'

const loadingTask = pdfjsLib.getDocument(url)
loadingTask.promise.then((pdf) => {
  return pdf.getPage(1)
}).then((page) => {
  const scale = 1.5
  const viewport = page.getViewport({ scale })
  const canvas = document.getElementById('pdf-canvas')
  const ctx = canvas.getContext('2d')
  canvas.height = viewport.height
  canvas.width = viewport.width
  return page.render({ canvasContext: ctx, viewport }).promise
}).catch(console.error)
```

| Knob | Why it matters |
|------|----------------|
| `Accept-Ranges: bytes` | Enables 206; without it PDF.js downloads all |
| CDN / proxy buffering | Some proxies strip ranges — first page stalls |
| WorkerSrc for PDF.js | Keeps parse off the UI thread |
| Linearized (“fast web view”) | Faster time-to-first-page on big files |
| Auth on ranges | Signed URLs must allow multiple range GETs |

Check ranges:

```bash
curl -I https://example.com/doc.pdf | grep -i accept-ranges
curl -H 'Range: bytes=0-1023' -I https://example.com/doc.pdf  # expect 206
```

## Real-World Applications

This is document progressive loading, not media [[ABR]]. Same HTTP range idea as video segment fetches, different parser.

Used wherever pdf-stream-viewing sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Tiny PDFs** — single GET is simpler; range complexity buys nothing.
- **Con / skip when:** **Print-faithful desktop application** — native viewers / print pipelines beat canvas.
- **Con / skip when:** **You need searchable server-side text extract** — use a PDF library on the backend, not PDF.js alone.
- **Con / skip when:** **DRM’d or encrypted PDFs with proprietary plugins** — PDF.js may not unlock vendor schemes.

## Mistakes to Avoid

| Symptom | Check | Fix |
|---------|-------|-----|
| Spins until 100% then shows | No Accept-Ranges / 200 only | Enable ranges on origin or CDN |
| Blank first page, large file | Not linearized; xref at end | Re-save as Fast Web View / linearized |
| Works locally, fails behind auth | Cookie / signed URL on worker fetch | Pass `httpHeaders` / withCredentials in getDocument |
| CORS errors in console | PDF host ≠ app origin | CORS + Expose-Headers for Content-Range |
| Random page failures | Truncated object / bad upload | Re-upload; verify Content-Length; checksum |
| Mobile OOM on huge PDF | Full raster at high scale | Lower scale; render visible pages only |

- **`<iframe src="file.pdf">` is not streaming control** — browser plugin behavior varies; PDF.js gives you progressive + UX control.
- **Gzip on PDFs** — some stacks break range + Content-Encoding; prefer identity encoding for ranged PDFs.
- **“Streaming” PDF ≠ media stream** — don’t wire this into [[HLS]] handlers; it’s HTTP file progressive load ([[Byte stream]] / static).
- **Worker and file URL mismatch** — wrong `workerSrc` silently falls back to main-thread jank.
