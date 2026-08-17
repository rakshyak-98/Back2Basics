[[Streaming]] [[Byte stream]] [[How to attach stream to HTTP handlers]]

# pdf-stream-viewing

> Stream a PDF into the browser — render pages as bytes arrive (PDF.js + HTTP range), don’t wait for the whole file.

```txt
        pdf-stream-viewing ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers probe whether you can walk pdf-stream-viewing end-to-end

## Sources
- [Wikipedia — pdf-stream-viewing](https://en.wikipedia.org/wiki/pdf-stream-viewing) — overview

## Key Concepts
- **Range request:** Client asks for a byte slice — “We fetch only the pages needed.”
- **206 Partial Content:** Server honors the range
- **PDF.js:** Mozilla’s JS PDF engine
- **Linearized PDF:** “Fast web view” layout — “Hint table up front — first page shows sooner.”
- **Object stream / xref:** Where page objects live — “Broken xref ⇒ blank pages even if bytes arrived.”

**Flow:**

- **Note:** 1. **Serve** — host PDF with range support (most static servers do).
- **Note:** 2. **Prefer linearized** — distill/fast-web-view when generating large docs.
- **Note:** 3. **Load** — `pdfjsLib.getDocument(url)` (or your worker setup).
- **Note:** 4. **Render** — `getPage(n)` → viewport → canvas as the user navigates.


- **Core:** This is document progressive loading, not media [[ABR]]

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

- Check ranges:

```bash
curl -I https://example.com/doc.pdf | grep -i accept-ranges
curl -H 'Range: bytes=0-1023' -I https://example.com/doc.pdf  # expect 206
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Spins until 100% then shows | No Accept-Ranges / 200 only | Enable ranges on origin or CDN |
| Blank first page, large file | Not linearized; xref at end | Re-save as Fast Web View / linearized |
| Works locally, fails behind auth | Cookie / signed URL on worker fetch | Pass `httpHeaders` / withCredentials in getDocument |
| CORS errors in console | PDF host ≠ app origin | CORS + Expose-Headers for Content-Range |
| Random page failures | Truncated object / bad upload | Re-upload; verify Content-Length; checksum |
| Mobile OOM on huge PDF | Full raster at high scale | Lower scale; render visible pages only |

- **Mistake:** **`<iframe src="file.pdf">` is not streaming control**
- **Mistake:** **Gzip on PDFs**
- **Mistake:** **“Streaming” PDF ≠ media stream**
- **Mistake:** **Worker and file URL mismatch**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Tiny PDFs**
- **Con / skip when:** **Print-faithful desktop application**
- **Con / skip when:** **You need searchable server-side text extract**
- **Con / skip when:** **DRM’d or encrypted PDFs with proprietary plugins**

## Real-World Applications
- **Note:** This is document progressive loading, not media [[ABR]]

- **Note:** Used wherever pdf-stream-viewing sits in an ingest → package → CDN → player p…
