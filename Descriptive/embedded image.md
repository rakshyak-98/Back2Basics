[[Descriptive]] [[html]] [[Markdown]] [[PDF (Portable Document Format)]]

# embedded image

> Embedded images ship inside the document (often base64 data URLs) — no extra HTTP fetch, bigger payload.

```txt
        embedded image ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Embedded image questions cover base64 vs URL assets

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
bytes → base64 → data URL in HTML/CSS/Markdown
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **data URL** | Inline resource | “No separate request.” |
| **base64** | Text encoding of bytes | “~33% size overhead.” |
| **CID (email)** | MIME embedded image | “Outlook-friendly.” |
| **External src** | URL fetch | “Cacheable on CDN.” |

## Technical Details
```html
<img alt="logo" src="data:image/png;base64,iVBORw0KGgoAAA…" />
```

| Knob | Why it matters |
|------|----------------|
| Size | Bloats HTML; blocks parse |
| Caching | Can’t cache image alone |
| CSP | may block data: URLs |

## Mistakes to Avoid
> [!WARNING]
> **Base64 isn’t compression** — it makes files larger.

> [!WARNING]
> **Inlining critical hero images** — can delay first paint if oversized.

| Symptom | Check | Fix |
|---------|-------|-----|
| Huge HTML | inlined photos | Host on CDN; `<img src=url>` |
| CSP blocks image | policy | Allow data: or use https src |
| Email image missing | client blocks | CID attach + good MIME |
| Broken base64 | truncated | Re-encode; check padding |

## Pros/Cons or Trade-offs
- **Large photos / video posters** — normal URLs + CDN.
- **Frequently changing assets** — lose cache granularity.
