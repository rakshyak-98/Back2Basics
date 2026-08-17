[[NodeJS/file]] [[javascript]] [[Operating System/file descriptors]] [[python]] [[Descriptive/percentage calculation]]

# PDF parser

> Extract text, structure, and metadata from PDF byte streams — operators, fonts, and page trees — **PDF spec + production extraction pitfalls**.

```txt
        PDF parser ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** PDF parsing reviews cover structured extraction limits and why PDFs are ho…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview
- [PDF — Wikipedia](https://en.wikipedia.org/wiki/PDF) — overview

## Key Concepts
- **Note:** A PDF is not plain text. It's a **byte-oriented format**: header, body of **i…

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

- **Note:** 1. **Lexical**
2. **Structure** — resolve references, build page tree.
- **Note:** 3. **Content** — decode streams (FlateDecode, etc.), interpret operators.
- **Note:** 4. **Text extraction**

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **Text extraction ≠ visual reproduction** — PDF stores drawing instructions, not paragraphs. Tables and multi-column layouts need heuristics or ML.

- **Mistake:** **Scanned PDFs** are images — parser sees no text until OCR
- **Mistake:** **JavaScript in PDF** (Acrobat scripts)
- **Mistake:** **Incremental updates** append new xref
- **Mistake:** **Subset fonts** map limited glyph set

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbled / empty text | Font without ToUnicode map | OCR fallback (tesseract); try mutool |
| Wrong column order | Visual layout vs reading order | Use `-layout` or `pdfminer.six` with LAParams |
| Encrypted PDF | `/Encrypt` in trailer | Provide password to library |
| Parse throws on valid Adobe file | Linearized / xref stream | Upgrade parser; try qpdf `--decrypt` normalize |
| Huge memory on scan PDF | Whole file loaded as string | Stream pages one-by-one |

## Pros/Cons or Trade-offs
- Filling PDF forms at scale
- Pixel-perfect rendering — use PDFium/mupdf canvas render, not text parser.
