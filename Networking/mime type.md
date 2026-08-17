[[Networking]] [[HTTP]] [[Registered Media Types (RMT)]]

# mime type

> MIME type labels what bytes are — browser/OS picks how to open, render, or download them.





## Interview Relevance
Interviewers ask about MIME/`Content-Type` to see if you know it is a **claim about format**, not proof of safety — wrong types cause download-vs-render bugs, XSS, and API client failures.

## Sources
- [RFC 2045 — MIME Part One](https://www.rfc-editor.org/rfc/rfc2045) — deep-dive
- [RFC 6838 — Media Type Registration](https://www.rfc-editor.org/rfc/rfc6838) — deep-dive
- [IANA Media Types Registry](https://www.iana.org/assignments/media-types/media-types.xhtml) — overview
- [MDN — MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types) — overview

## Core Definition
A media type (historically MIME type) is a `type/subtype` label, optionally with parameters such as `charset`, carried in HTTP as `Content-Type` so clients choose the right parser or handler.

## Key Concepts
- **MIME / media type:** `type/subtype` label → declares content format for the client.
- **Content-Type:** HTTP header carrying the media type → server’s claim about the body.
- **charset:** text encoding parameter → `text/html; charset=utf-8` avoids mojibake.
- **octet-stream:** opaque binary → unknown bytes; often forces download.
- **xdg-mime:** desktop default app for a type → Linux maps MIME → `.desktop` handler.

## Technical Details
```txt
Server ── Content-Type: application/json ──► Browser/app
              │
              └─ wrong type ⇒ wrong handler (download vs render vs reject)
```

| MIME | Typical use |
|------|-------------|
| `text/html` | Web pages |
| `application/json` | APIs |
| `application/octet-stream` | Generic binary / force save |
| `multipart/form-data` | File uploads |
| `image/png`, `video/mp4` | Media |

```bash
# Linux: which app opens a MIME type
xdg-mime query default text/plain
xdg-mime query default inode/directory   # file manager
xdg-mime default vim.desktop text/plain

gio mime text/plain                      # GNOME alternative

# System maps
# /etc/mime.types
# /usr/share/mime/
```

```http
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="report.pdf"
```

| Knob | Why it matters |
|------|----------------|
| `Content-Type` | Wrong type ⇒ XSS risk (HTML as text/plain vs text/html) or broken players |
| `Content-Disposition: attachment` | Force download even for viewable types |
| `application/octet-stream` | Safe default when type unknown |
| Extension vs sniffing | Prefer explicit header; don’t trust filename alone |

| Symptom | Check | Fix |
|---------|-------|-----|
| Browser downloads JSON | `Content-Type` is `octet-stream` or missing | Serve `application/json` |
| File opens in wrong app | `xdg-mime query default <type>` | `xdg-mime default app.desktop type` |
| CORS / API client rejects | Unexpected MIME | Align `Accept` / `Content-Type` with API contract |
| PDF inline vs download | Disposition + type | `inline` vs `attachment`; keep `application/pdf` |
| Upload rejected | Server MIME allowlist | Whitelist real types; don’t trust client-only |

## Real-World Applications
APIs, browsers, CDNs, and desktop file managers all branch on media types.

**Example:** An API returns JSON with `Content-Type: application/octet-stream` — the browser downloads a file instead of parsing; fix the response header to `application/json`.

## Pros/Cons or Trade-offs
- **Pro:** One shared vocabulary for format across HTTP, email, and OS handlers.
- **Con:** Type is advisory — attackers and misconfigured servers can lie; validate content when trust matters.
- **Con:** Desktop MIME databases and HTTP headers are separate systems that can disagree.

## Comparison
- vs [[Registered Media Types (RMT)]]: RMT is the IANA registry and registration trees; this note is the day-to-day `Content-Type` / handler behavior.
- vs file extension: extension is a hint on disk; HTTP clients should prefer the declared header.

## Mistakes to Avoid
- Treating extension as MIME — renaming `.txt` to `.html` does not make it HTML; servers must set `Content-Type`.
- Relying on sniffing — browsers that ignore the declared type can turn “text” into executable HTML; prefer `X-Content-Type-Options: nosniff`.
- Using MIME alone for authentication or trust — validate content; MIME is a claim.
- Serving user uploads as `text/html` — XSS; store and serve with safe types plus disposition.
