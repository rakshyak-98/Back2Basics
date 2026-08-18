[[Descriptive]] [[html]] [[Markdown]]

# embedded image

> Embedded images ship inside the document (often base64 data URLs) — no extra HTTP fetch, bigger payload.

## Mental model

**Say it in one breath:** `data:image/…;base64,…` inlines bytes; great for tiny icons/email, costly for large photos.

```txt
bytes → base64 → data URL in HTML/CSS/Markdown
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **data URL** | Inline resource | “No separate request.” |
| --- | --- | --- |
| **base64** | Text encoding of bytes | “~33% size overhead.” |
| **CID (email)** | MIME embedded image | “Outlook-friendly.” |
| **External src** | URL fetch | “Cacheable on CDN.” |

## Standard config / commands

```html
<img alt="logo" src="data:image/png;base64,iVBORw0KGgoAAA…" />
```

| Knob | Why it matters |

| Size | Bloats HTML; blocks parse |
| --- | --- |
| Caching | Can’t cache image alone |
| CSP | may block data: URLs |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Huge HTML | inlined photos | Host on CDN; `<img src=url>` |
| CSP blocks image | policy | Allow data: or use https src |
| Email image missing | client blocks | CID attach + good MIME |
| Broken base64 | truncated | Re-encode; check padding |

## Gotchas

> [!WARNING]
> **Base64 isn’t compression** — it makes files larger.

> [!WARNING]
> **Inlining critical hero images** — can delay first paint if oversized.

## When NOT to use

- **Large photos / video posters** — normal URLs + CDN.
- **Frequently changing assets** — lose cache granularity.

## Related

[[html]] [[Markdown]] [[PDF (Portable Document Format)]]
