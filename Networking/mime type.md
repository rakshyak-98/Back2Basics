[[Networking]] [[HTTP]]

# mime type

> MIME type labels what bytes are — browser/OS picks how to open, render, or download them.

---

## How it works

```txt
Server ── Content-Type: application/json ──► Browser/app
              │
              └─ wrong type ⇒ wrong handler (download vs render vs reject)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **MIME / media type** | `type/subtype` label | “Declares content format for the client.” |
| **Content-Type** | HTTP header carrying MIME | “Server’s claim about the body.” |
| **charset** | Text encoding param | “`text/html; charset=utf-8` avoids mojibake.” |
| **octet-stream** | Opaque binary | “Unknown bytes — often forces download.” |
| **xdg-mime** | Desktop default app for a type | “Linux maps MIME → `.desktop` handler.” |

### Common types

| MIME | Typical use |
|------|-------------|
| `text/html` | Web pages |
| `application/json` | APIs |
| `application/octet-stream` | Generic binary / force save |
| `multipart/form-data` | File uploads |
| `image/png`, `video/mp4` | Media |

---


## Configuration and commands

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
| `Content-Type` | Wrong type ⇒ XSS risk (serving HTML as text/plain vs text/html) or broken players |
| `Content-Disposition: attachment` | Force download even for viewable types |
| `application/octet-stream` | Safe default when type unknown |
| Extension vs sniffing | Prefer explicit header; don’t trust filename alone |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Browser downloads JSON | `Content-Type` is `octet-stream` or missing | Serve `application/json` |
| File opens in wrong app | `xdg-mime query default <type>` | `xdg-mime default app.desktop type` |
| CORS / API client rejects | Unexpected MIME | Align `Accept` / `Content-Type` with API contract |
| PDF inline vs download | Disposition + type | `inline` vs `attachment`; keep `application/pdf` |
| Upload rejected | Server MIME allowlist | Whitelist real types; don’t trust client-only |

---


## Gotchas

> [!WARNING]
> **Extension ≠ MIME** — rename `.txt` to `.html` does not make it HTML; servers must set `Content-Type`.

> [!WARNING]
> **Sniffing is dangerous** — browsers that ignore declared type can turn “text” into executable HTML. Prefer `X-Content-Type-Options: nosniff`.

> [!WARNING]
> **Desktop MIME ≠ HTTP MIME** — `/usr/share/mime` for local apps; HTTP still needs correct response headers.

---


## When not to use

- **authentication / trust decisions based only on MIME** — validate content; MIME is a claim.
- **Serving user uploads as `text/html`** — XSS; store and serve with safe types + disposition.
- **Inventing custom types without a registry need** — prefer standard types + versioning in the API schema.

---


## Related

[[Networking]] [[HTTP]] [[https]]

## Sources

- [Wikipedia — mime type](https://en.wikipedia.org/wiki/mime_type)
