[[Security]]

# Base64

> Turn binary into ASCII text for protocols and configs that dislike raw bytes — encoding, not encryption.





## Interview Relevance
Quick filter: Base64 is encoding, not encryption — interviewers watch for that misconception and padding/URL-safe variants.

## Sources
- [RFC 4648 — The Base16, Base32, and Base64 Data Encodings](https://www.rfc-editor.org/rfc/rfc4648) — deep-dive
- [Wikipedia — Base64](https://en.wikipedia.org/wiki/Base64) — overview

## Core Definition
Base64 encodes binary as ASCII text using a 64-character alphabet so binary can travel in text protocols and configs.

## Key Concepts
turn binary data (like images, files, PDFs) into plain text so it can be safely sent over the internet or stored in places that only allow text.
> [!INFO]
> You cannot paste raw photo bytes (binary data) into an email or JSON. So Base64 converts that photo into a long string of letters, numbers, and symbols
> Base64 strings are ~33% larger than the original file.
**Image in HTML**
```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ..." />
```
### How It Works (Simple Math)
- Normal text uses **8 bits per character** (1 byte)
- Base64 uses **64 safe characters**: A–Z, a–z, 0–9, +, / (and = for padding)
It takes **3 bytes** of binary data (24 bits) → splits into **4 characters** (6 bits each)

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Base64** | This note’s core idea | “I explain Base64 in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

## Technical Details
```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Apply/deploy fail | plan / events | Fix IAM or syntax |
| TLS/DNS wrong | dig / openssl | Fix records and certs |
| Secret leak risk | repo scan | Rotate; use secret store |

## Real-World Applications
PEM certificates, JWT parts, and `data:` URLs all carry binary as Base64 text — never treat that as confidentiality.

## Pros/Cons or Trade-offs
- **Pro:** Safe binary-in-text transport for PEMs, JWTs, and protocols.
- **Con:** Skip when a simpler existing approach already fits.

## Mistakes to Avoid
- Prefer words you can say aloud in an interview.
