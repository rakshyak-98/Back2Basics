[[Descriptive]] [[pdf parser]] [[embedded image]] [[pdf-stream-viewing]] [[Markdown]]

# PDF (Portable Document Format)

> PDF is a fixed-layout document format — pages, fonts, and vectors aimed at print-faithful rendering.

```txt
        PDF (Portable Docu ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** PDF questions may touch generation/rendering pipelines

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview
- [PDF — Wikipedia](https://en.wikipedia.org/wiki/PDF) — overview

## Key Concepts
```txt
objects (page, font, stream) → xref → viewer renders page N
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Page tree** | Structure of pages | “Random access to page N.” |
| **Content stream** | Draw operators | “Text as positioned glyphs.” |
| **Embedded font** | Fonts inside file | “Avoid missing glyphs.” |
| **PDF/A** | Archival subset | “Long-term preservation.” |

## Technical Details
```bash
pdftotext file.pdf -     # extract text
pdfinfo file.pdf         # metadata, page count
qpdf --check file.pdf    # structural check
```

| Knob | Why it matters |
|------|----------------|
| Font embedding | Cross-machine fidelity |
| Compression | Size vs CPU |
| Encryption | Permissions / open password |

## Mistakes to Avoid
> [!WARNING]
> **“Text” may be curves** — extractors return nothing useful.

> [!WARNING]
> **Pixel-perfect HTML≠PDF** — different layout engines.

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbled text extract | drawn as paths / bad encoding | OCR or better producer |
| Missing glyphs | fonts not embedded | Embed fonts |
| Huge file | images uncompressed | Recompress; downsample |
| Corrupt xref | bad merge | qpdf repair / regenerate |

## Pros/Cons or Trade-offs
- **Editable web content** — HTML.
- **Data interchange** — JSON/CSV.
