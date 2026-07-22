[[NodeJS/file]] [[javascript]] [[Operating System/file descriptors]] [[python]]

# PDF parser

> Extract text, structure, and metadata from PDF byte streams — operators, fonts, and page trees — **PDF spec + production extraction pitfalls**.

## Mental model

A PDF is not plain text. It's a **byte-oriented format**: header, body of **indirect objects** (dictionaries, streams, arrays), cross-reference table, trailer. Pages reference **content streams** — lists of graphics/text **operators** (`Tj`, `Td`, `re`, …).

```
PDF file
 ├── Catalog (root)
 ├── Pages tree → Page objects
 │       └── Contents stream (drawing instructions)
 ├── Fonts (embedded or referenced)
 ├── Images (XObjects)
 └── Metadata (Info dict / XMP)
```

Parsing stages:

1. **Lexical** — find objects by `obj` / `endobj`, streams by `stream`/`endstream`.
2. **Structure** — resolve references, build page tree.
3. **Content** — decode streams (FlateDecode, etc.), interpret operators.
4. **Text extraction** — map glyph IDs through font encoding to Unicode (hardest step).

## Standard config / commands

### Node — pdf-parse (text-only, quick)

```javascript
import fs from 'fs';
import pdf from 'pdf-parse';

const buf = fs.readFileSync('invoice.pdf');
const { text, numpages, info } = await pdf(buf);
console.log(info.Title, numpages, text.slice(0, 500));
```

### Python — pypdf (structure + merge/split)

```python
from pypdf import PdfReader

reader = PdfReader("doc.pdf")
print(len(reader.pages), reader.metadata)
page = reader.pages[0]
print(page.extract_text())
```

### Poppler CLI (server-side batch)

```bash
pdftotext -layout input.pdf output.txt
pdfinfo input.pdf
pdffonts input.pdf   # missing ToUnicode CMap → garbled text
```

### Inspect raw operators (debug)

```bash
mutool draw -F txt input.pdf   # mupdf
qpdf --show-object=trailer input.pdf
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbled / empty text | Font without ToUnicode map | OCR fallback (tesseract); try mutool |
| Wrong column order | Visual layout vs reading order | Use `-layout` or `pdfminer.six` with LAParams |
| Encrypted PDF | `/Encrypt` in trailer | Provide password to library |
| Parse throws on valid Adobe file | Linearized / xref stream | Upgrade parser; try qpdf `--decrypt` normalize |
| Huge memory on scan PDF | Whole file loaded as string | Stream pages one-by-one |

## Gotchas

> [!WARNING]
> **Text extraction ≠ visual reproduction** — PDF stores drawing instructions, not paragraphs. Tables and multi-column layouts need heuristics or ML.

- **Scanned PDFs** are images — parser sees no text until OCR.
- **JavaScript in PDF** (Acrobat scripts) — most open-source parsers ignore; security risk if executing.
- **Incremental updates** append new xref — parser must read latest trailer chain.
- **Subset fonts** map limited glyph set — copy-paste can differ from display.

## When NOT to use

- Filling PDF forms at scale — use dedicated form libraries or vendor APIs (Adobe PDF Services).
- Pixel-perfect rendering — use PDFium/mupdf canvas render, not text parser.

## Related

[[NodeJS/file]] [[javascript]] [[Operating System/file descriptors]] [[Descriptive/percentage calculation]]
